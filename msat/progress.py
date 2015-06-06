import sys
import time
import msat.settings as settings

class ProgressBar:

    def __init__(self, title, total):
        self.title =title
        self.total = total
        self.finish = False
        self.updateProgress(0)

    def updateProgress(self, current_count):
        if self.finish:
            return
        progress = current_count / self.total
        progress_str = ('\r| P {title:<' + 
                        str(settings.SOLVER_ITEM_WIDTH) +
                        '}: [{bar:<' + str(settings.SOLVER_WIDTH-17-settings.SOLVER_ITEM_WIDTH) +
                        '}] {progress:<6.2f}%|')

        sys.stdout.write(progress_str.format(
            title=self.title,
            bar='='*int(progress*(settings.SOLVER_WIDTH-18-settings.SOLVER_ITEM_WIDTH))+'>',
            progress=progress*100)
        )
        
        sys.stdout.flush()
        if progress == 1:
            sys.stdout.write('\n')
            self.finish = True

    def finishProgress(self):
        sys.stdout.write('\n')
        self.finish = True
