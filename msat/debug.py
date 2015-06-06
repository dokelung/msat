import msat.settings as settings
import msat.reporter as reporter

def debug_title(title):
    if settings.DEBUG_TITLE:
        front_blank_num = (30-len(title))//2
        print('='*30)
        print(' '*front_blank_num, end='')
        print(title)
        print('='*30)

def debug_msg(msg):
    if settings.DEBUG_MSG:
        print(msg)

def debug_interupt():
    if settings.DEBUG_INTERUPT:
        input('press enter to continue ...')

def debug_show_search_status(solver):
    if settings.DEBUG_SHOW_SEARCH_STATUS:
        mc_rpt = reporter.McReporter(solver.mc)
        color_position = [(solver.level, target.getCurrentValue()) for target in solver.targets]
        mc_rpt.reportTableWithColor(color_position)
