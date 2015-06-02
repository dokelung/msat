import msat.settings as settings

def getLine(bold=False):
    if bold:
        return '='*settings.SOLVER_WIDTH
    else:
        return '-'*settings.SOLVER_WIDTH

def getMsg(msg, place=''):
    return ('|{msg:'+place+str(settings.SOLVER_WIDTH-2)+'}|').format(msg=msg)

def getMsgInTwoCol(msg1, msg2, place=''):
    m1 = ('|{msg:'+place+str(int(settings.SOLVER_WIDTH/2)-2)+'}|').format(msg=msg1)
    m2 = ('|{msg:'+place+str(int(settings.SOLVER_WIDTH/2)-2)+'}|').format(msg=msg2)
    return m1 + m2
    
def getTitle(title):
    return ('|{title:^'+str(settings.SOLVER_WIDTH-2)+'}|').format(title=title)

def getSubTitle(title):
    line = getMsg(' ' + '-'*(len(title)+2))
    title = getMsg(' |{title}|'.format(title=title))
    return line + '\n' + title + '\n' + line

def getItem(item, value):
    item_str = (' % {item:<'+str(settings.SOLVER_ITEM_WIDTH)+'}').format(item=item)
    value_str = '{value}'.format(value=value)
    if len(value_str) > settings.SOLVER_WIDTH-10-settings.SOLVER_ITEM_WIDTH:
        value_str = value_str[:settings.SOLVER_WIDTH-18-settings.SOLVER_ITEM_WIDTH] + ' ... more'
    msg = item_str + ': ' + value_str
    return getMsg(msg)

def getProcess(process_name):
    process_str = ' ===== ' + process_name + ' ====='
    return getMsg(process_str)

class McReporter:

    def __init__(self, mc):
        self.mc = mc

    def reportTable(self):
        print('================')
        print('    Mc Table    ')
        print('================')
        print('-'* (3*len(self.mc.getJRange())+8) )
        print('{0:>3}     '.format('*'), end='')
        for j in self.mc.getJRange():
            print('{0:>3}'.format(j), end='')
        print()
        print('-'* (3*len(self.mc.getJRange())+8) )
        for i in self.mc.getIRange():
            if not i==0:
                print('{0:>3}({1:>3})'.format(i, self.mc.elements[i-1]), end='')
            else:
                print('{0:>3}     '.format(i), end='')
            for j in self.mc.getJRange():
                if self.mc.table[i][j] == None:
                    print('{0:>3}'.format('x'), end='')
                elif self.mc.table[i][j]:
                    print('{0:>3}'.format('T'), end='')
                else:
                    print('{0:>3}'.format('F'), end='')
            print()
        print('-'* (3*len(self.mc.getJRange())+8) )

    def reportTableWithColor(self, color_position):
        print('-'* (3*len(self.mc.getJRange())+8) )
        print('{0:>3}     '.format('*'), end='')
        for j in self.mc.getJRange():
            print('{0:>3}'.format(j), end='')
        print()
        print('-'* (3*len(self.mc.getJRange())+8) )
        for i in self.mc.getIRange():
            if not i==0:
                print('{0:>3}({1:>3})'.format(i, self.mc.elements[i-1]), end='')
            else:
                print('{0:>3}     '.format(i), end='')
            for j in self.mc.getJRange():
                if self.mc.table[i][j] == None:
                    if (i,j) in color_position:
                        print('\033[94m{0:>2}\033[0m'.format(color_position.count((i,j))), end='')
                        print('\033[94m{0}\033[0m'.format('x'), end='')
                    else:
                        print('{0:>3}'.format('x'), end='')
                elif self.mc.table[i][j]:
                    if (i,j) in color_position:
                        print('\033[94m{0:>2}\033[0m'.format(color_position.count((i,j))), end='')
                        print('\033[94m{0}\033[0m'.format('T'), end='')
                    else:
                        print('{0:>3}'.format('T'), end='')
                else:
                    if (i,j) in color_position:
                        print('\033[94m{0:>2}\033[0m'.format(color_position.count((i,j))), end='')
                        print('\033[94m{0}\033[0m'.format('F'), end='')
                    else:
                        print('{0:>3}'.format('F'), end='')
            print()
        print('-'* (3*len(self.mc.getJRange())+8) )

    def reportDic(self):
        print('{0:>8}'.format('McDic'), end='')
        for j in self.mc.getJRange():
            print('{0:>3}'.format(self.mc.dic[j]), end='')
        print()

class SolverReporter:

    def __init__(self, solver):
        self.solver = solver

    def reportSatisfiability(self):
        print('================')
        print(' Satisfiability ')
        print('================')
        print(self.solver.satisfiability)

    def reportResults(self):
        print('================')
        print('    Results     ')
        print('================')
        for target in self.solver.targets:
            print('target:{t:>5} --> subset:{subset}'.format(t=target.getValue(), subset=target.getPickedElements()))
