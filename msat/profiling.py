import msat.settings as settings
from msat.reporter import *
import copy

profiling_dic = {
    'backtrack_num': 0,
    'check_sum_fail_num' : 0,
    'check_sum_comb_fail_num' : 0,
    'check_distance_fail_num' : 0,
    'forbiden_combination_num' : 0
}

def profiling_count(var_name, profiling=settings.PROFILING_COUNT):
    if profiling:
        profiling_dic[var_name] += 1

def profiling_summary(profiling=settings.PROFILING_SUMMARY):
    print(getLine())
    print(getTitle('Profiling Summary'))
    print(getLine())
    if profiling:
        for var in settings.PROFILING_VARS:
            print(getItem(var, profiling_dic[var]))
