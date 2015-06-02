import msat.settings as settings
import msat.reporter as reporter

def debug_title(title, debug=settings.DEBUG_TITLE):
	if debug:
		front_blank_num = (30-len(title))//2
		print('='*30)
		print(' '*front_blank_num, end='')
		print(title)
		print('='*30)

def debug_msg(msg, debug=settings.DEBUG_MSG):
    if debug:
        print(msg)

def debug_interupt(debug=settings.DEBUG_INTERUPT):
	if debug:
		input('press enter to continue ...')

def debug_show_search_status(solver, debug=settings.DEBUG_SHOW_SEARCH_STATUS):
	if debug:
		mc_rpt = reporter.McReporter(solver.mc)
		color_position = [(solver.level, target.getCurrentValue()) for target in solver.targets]
		mc_rpt.reportTableWithColor(color_position)
