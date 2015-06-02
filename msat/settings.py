# solver display
SOLVER_WIDTH = 100 # should be even
SOLVER_ITEM_WIDTH = 20 

# mc
ELEMENTS_ORDER = 'increase' # increase/decrease/no
TARGETS_ORDER = 'increase'  # increase/decrease/no
JRANGE_MIN = False

# search
CHOOSE_NOUSE_FIRST = False
CHOOSE_FROM_MAX_OR_MIN = 'max' # max/min/no

# other constraint
ALL_USE_RULE = False

# judge satifiability
EARLY_CHECK_SATISFIABILITY = False

# early backtrack check
CHECK_FOR_EARLY_BACKTRACK = True
CHECK_SUM = True
CHECK_SUM_COMB = True
CHECK_SUM_COMB_NUM = 6
CHECK_DISTANCES = True
CHECK_FORBIDEN = True

# progress
PROGRESS = False

# profiling
PROFILING_VARS = (
    'backtrack_num',
    'check_sum_fail_num',
    'check_sum_comb_fail_num',
    'check_distance_fail_num',
    'forbiden_combination_num'
)

PROFILING_COUNT = True
PROFILING_SUMMARY = True

# debug 
DEBUG_TITLE = False
DEBUG_MSG = False
DEBUG_INTERUPT = False
DEBUG_SHOW_SEARCH_STATUS = False
