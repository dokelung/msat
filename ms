#!/usr/bin/env python3

import os
import sys
import time
import types
import json
from msat import mc, solver, settings, profiling
from msat.reporter import *


def cmd_cmd():
    """
    USAGE: list all avalible commands and their short usage
    SYNOPSIS:
        cmd
    """
    cmds = [item for item in globals() if item[0:4]=='cmd_']
    cmds.sort()
    print('CMD:')
    for cmd in cmds:
        docstr = globals()[cmd].__doc__
        docstr = docstr.strip().split('\n')[0]
        docstr = docstr.split(':')[1].strip()
        print('    {cmd:<12} : {docstr}'.format(cmd=cmd.split('_')[1], docstr=docstr))

def cmd_configure():
    """
    USAGE: setting enviroments
    SYNOPSIS:
        configure 
    """
    with open('local_settings.py', 'w') as writer:
        for setting in dir(settings):
            if not setting[0]=='_':
                value = eval('settings.'+setting)
                if isinstance(value, str):
                    value = "'" + value + "'"
                print(setting, '=', value, file=writer)

def cmd_help(command):
    """
    USAGE: show the full infomation of a command
    SYNOPSIS:
        help <command>
    """
    print(globals()['cmd_'+command].__doc__)

def cmd_setdiff():
    """
    USAGE: diff the default settings and the local settings
    SYNOPSIS:
        setdiff
    """
    with open('local_settings.py', 'r') as reader:
        for line in reader:
            setting = line.strip()
            var, value = setting.split('=')
            var = var.strip()
            value = value.strip()
            value = value.split('#')[0].strip()
            if var in dir(settings):
                old_value = eval('settings.'+var)
                exec('settings.'+setting)
                new_value = eval('settings.'+var)
                if not old_value==new_value:
                    print('M', var, '=', new_value)
            else:
                print('Error: unavalible settings -> ' + setting)

def cmd_solve(options):
    """
    USAGE: solve a mc problem
    SYNOPSIS:
        solve [-i] <mc file> [-o <result file>]
    OPTIONS:
        -i : intelligent setting
        -o : result file name
    """
    with open('local_settings.py', 'r') as reader:
        for line in reader:
            setting = line.strip()
            var, value = setting.split('=')
            var = var.strip()
            value = value.strip()
            value = value.split('#')[0].strip()
            if var in dir(settings):
                exec('settings.'+setting)
            else:
                print('Error: unavalible settings -> ' + setting)

    mc_file = argv[2]
    
    if 'o' in options:
        result_file = argv[3]
    else:
        result_file = mc_file + '.result'

    elements = []
    targets = []
    relation = None 
    mc_settings = []

    # Read mc file
    
    with open(mc_file, 'r') as reader:
        try:
            for line in reader:
                line = line.strip()
                if not line or line[0]=='#':
                    continue
                if line[0] == 'e':
                    elements.extend([int(e) for e in line.split()[1:]])
                elif line[0] == 't':
                    targets.extend([int(t) for t in line.split()[1:]])
                elif line[0] == 'r':
                    relation = line.split()[1]
                elif line[0] == 's':
                    setting = line[1:].strip()
                    var, value = setting.split('=')
                    var = var.strip()
                    value = value.strip()
                    value = value.split('#')[0].strip()
                    if var in dir(settings):
                        exec('settings.'+setting)
                        mc_settings.append(' S '+var+' = '+value)
                    else:
                        print('Error: unavalible settings -> ' + setting)
        except:
            print('Error: Mc file format')

    # Intelligent setting

    if 'i' in options:

        if sum(elements)==sum(targets) and relation in ['=', '>=']:
            settings.ALL_USE_RULE = True
            mc_settings.append(' I ALL_USE_RULE = True')
            
        if relation in ['>', '>=']:
            settings.ELEMENTS_ORDER = 'increase'
            settings.CHOOSE_FROM_MAX_OR_MIN = 'max'
            mc_settings.append(' I ELEMENTS_ORDER = increase')
            mc_settings.append(' I CHOOSE_FROM_MAX_OR_MIN = max')
        elif relation=='=':
            settings.ELEMENTS_ORDER = 'increase'
            settings.CHOOSE_FROM_MAX_OR_MIN = 'min'
            mc_settings.append(' I ELEMENTS_ORDER = increase')
            mc_settings.append(' I CHOOSE_FROM_MAX_OR_MIN = min')
    
    # Run
    
    print(getLine(True))
    print(getTitle('MSAT - Multiset Constraint Solver for Multi-SAT'))
    print(getLine(True))
    print(getItem('MC file', mc_file.rpartition('/')[2]))
    print(getItem('Elements (Num:{num})'.format(num=len(elements)),elements))
    print(getItem('Targets  (Num:{num})'.format(num=len(targets)),targets))
    print(getItem('Relation', relation))
    print(getLine())
    
    if mc_settings:
        print(getTitle('Mc Settings Specified in Mc File and Intelligent Setting'))
        print(getLine())
        while True:
            s1 = mc_settings.pop() if len(mc_settings)>0 else ''
            s2 = mc_settings.pop() if len(mc_settings)>0 else ''
            if not s2:
                if not s1:
                    break
                else:
                    print(getMsgInTwoCol(s1, ''))
                    break
            print(getMsgInTwoCol(s1, s2))
        print(getLine())
    
    if relation == '=':
        mcp = mc.McEq()
    elif relation == '>':
        mcp = mc.McGt()
    elif relation == '>=':
        mcp = mc.McGe()
    elif relation == '<':
        mcp = mc.McLt()
    elif relation == '<=':
        mcp = mc.McLe()
    
    mcp.setElements(elements)
    mcp.setTargets(targets)
    print(getTitle('MC Table & MC Dictionary'))
    print(getLine())
    tb_size_str = '{0}*{1} = {2}'.format(len(mcp.getIRange()), len(mcp.getJRange()), mcp.getTableSize())
    print(getItem('Table Size', tb_size_str))
    print(getItem('Elements Order', settings.ELEMENTS_ORDER))
    print(getItem('J-range Min', settings.JRANGE_MIN))
    t1 = time.time()
    mcp.buildTable()
    mcp.buildDic()
    t2 = time.time()
    print(getItem('Build Time', '{0:.5f}'.format(t2-t1)))
    print(getLine())
    
    print(getTitle('Multiset Constraint Solving'))
    print(getLine())
    t3 = time.time()
    mc_solver = solver.Solver(mcp)
    mc_solver.solve()
    t4 = time.time()
    solution_space = (len(targets)+1)**len(elements)
    print(getItem('Satisfiability', mc_solver.getSatisfiability()))
    print(getItem('Solving Time', '{0:.5f}'.format(t4-t3)))
    profiling.profiling_summary()
    print(getLine(True))

    # output results

    result_lst = [{'target':target.getValue(), 'elements':target.getPickedElements()} for target in mc_solver.targets]

    if settings.OUTPUT_SUBSET and mc_solver.getSatisfiability():
        with open(result_file, 'w') as writer:
            print(json.dumps(result_lst, indent=2, separators=(',', ':')), file=writer)

argv = sys.argv[:]

if __name__ == '__main__':

    options = []
    for arg in argv:
        if '-' in arg:
            options.append(arg)
            argv.remove(arg)

    options = [option.strip('-') for option in options]

    try:
        cmd = argv[1]
        if cmd == 'cmd':
            cmd_cmd()
        elif cmd == 'configure':
            cmd_configure()
        elif cmd == 'help':
            try:
                obj = argv[2]
                cmd_help(obj)
            except:
                print('Please use "help [command]" to get the usage of command')
        elif cmd == 'setdiff':
            cmd_setdiff()
        elif cmd == 'solve':
            cmd_solve(options)
        else:
            print('Error: unavalible command : '+cmd)
            print('Please use "cmd" to list all avalible commands')
    except:
        print('msat:')
        print('    python3 ms <CMD> [OBJECTS & OPTIONS]')
        print('            ms <CMD> [OBJECTS & OPTIONS]')
        print('          ./ms <CMD> [OBJECTS & OPTIONS]')
        print('    If this is your first use, please run configure!')
        cmd_cmd()
