from msat.debug import *
from msat.profiling import *
import msat.settings as settings
import msat.progress as progress

class Target:

    def __init__(self, value):
        self.value = value
        self.current_value = value
        self.picked_elements = []

    def getValue(self):
        return self.value

    def getCurrentValue(self):
        return self.value - sum(self.picked_elements)

    def getPickedElements(self):
        return self.picked_elements

    def pickElement(self, element):
        self.picked_elements.append(element)

    def popElement(self):
        self.picked_elements.pop()

class Layer:

    def __init__(self, level, mc):
        self.level = level
        self.element = mc.elements[level-1]

        self.picked_target = None
        self.candidates = []
        self.forbiden_combinations = set()

        self.mc = mc

    def clear(self):
        self.picked_target = None
        self.candidates = []

    def getLayerElement(self):
        return self.element

    def getPickedTarget(self):
        return self.picked_target

    def setCandidates(self, targets, should_use=settings.ALL_USE_RULE):
        if not settings.CHOOSE_NOUSE_FIRST:
            if not should_use:
                self.candidates.append('no')

        values = set()
        for target in targets:
            if eval(str(target.getCurrentValue())+self.mc.getAllTrueRegion()):
                continue
            if not target.getCurrentValue() in values:
                values.add(target.getCurrentValue())
                self.candidates.append(target)

        if settings.CHOOSE_NOUSE_FIRST:
            self.candidates.append('no')

    def pickNextTarget(self):
        try:
            self.picked_target = self.candidates.pop()
            return True
        except:
            self.picked_target = 'no candidates'
            return False

    def pickNextValidTarget(self):
        while True:
            if self.pickNextTarget():
                if not self.picked_target=='no':
                    if self.mc.getUpperValue(self.level, self.picked_target.getCurrentValue()):
                        return True
                else:
                    return True
            else:
                return False

    def recordForbidenCombination(self, targets):
        self.forbiden_combinations.add(tuple(sorted([target.getCurrentValue() for target in targets])))

    def isForbidenCombination(self, targets):
        return tuple(sorted([target.getCurrentValue() for target in targets])) in self.forbiden_combinations

class Solver:

    def __init__(self, mc):
        self.mc = mc

        self.level = len(self.mc.elements)
        self.targets = [Target(target) for target in self.mc.targets]

        self.layers = [ None ]
        for i, element in enumerate(self.mc.elements):
            self.layers.append(Layer(i+1, mc))

        self.satisfiability = None

        self.state = 'checkfalse'

    def isSearchSucceed(self):
        if all([eval(str(target.getCurrentValue())+self.mc.getAllTrueRegion()) for target in self.targets]):
            return True
        else:
            return False

    def getFalseTargets(self, steps=1):
        assert self.level - steps >= 0
        false_targets = []
        for target in self.targets:
            if not self.mc.getValue(self.level-steps, target.getCurrentValue()):
                false_targets.append(target)
        return false_targets

    def checkSum(self):
        value = sum([target.getCurrentValue() for target in self.targets])
        return self.mc.getValue(self.level, value)
        
        # return self.mc.getValue(self.level, sum([target.getCurrentValue() for target in self.targets]))

    def checkSumComb(self, num):
        target_values = [target.getCurrentValue() for target in self.targets]
        while True:
            comb = []
            try:
                for y in range(num):
                    comb.append(target_values.pop())
            except:
                return True
            if not self.mc.getValue(self.level, sum(comb)):
                return False

    def checkDistances(self):
        for distance in range(len(self.targets)+1)[1:]:
            if self.level - distance < 0:
                break
            if len(self.getFalseTargets(steps=distance)) > distance:
                return False
        return True

    def checkForEarlyBacktrack(self):

        if settings.CHECK_SUM and not self.checkSum():
            profiling_count('check_sum_fail_num')
            return False

        if settings.CHECK_SUM_COMB and not self.checkSumComb(settings.CHECK_SUM_COMB_NUM):
            profiling_count('check_sum_comb_fail_num')
            return False

        if settings.CHECK_DISTANCES and not self.checkDistances():
            profiling_count('check_distance_fail_num')
            return False

        if settings.CHECK_FORBIDEN and self.layers[self.level].isForbidenCombination(self.targets):
            profiling_count('forbiden_combination_num')
            return False

        return True

    def solve(self):

        debug_title('Search process')
        
        
        self.total_count = (len(self.mc.targets)+1) ** len(self.mc.elements)
        if settings.PROGRESS:
            self.pb_solving = progress.ProgressBar('Search Sol Space', self.total_count)
        
        while True:

            ts = [ target.getCurrentValue() for target in self.targets ]
            msg = 'do \033[94m{action:<10}\033[0m in level \033[94m{level:>3}\033[0m with targets {ts}'.format(action=self.state, level=self.level, ts=ts)
            debug_msg(msg)

            debug_show_search_status(self)

            if self.satisfiability!=None:

                if settings.PROGRESS:
                    self.pb_solving.finishProgress()

                return self.satisfiability

            debug_interupt()

            self.solveInOneStep()

    def solveInOneStep(self):
        if self.state == 'checkfalse':
            self.checkFalse()
        elif self.state == 'choose':
            self.choose()
        elif self.state == 'propagate':
            self.propagate()
        elif self.state == 'backtrack':
            profiling_count('backtrack_num')
            self.backtrack()

    def checkFalse(self):

        if settings.EARLY_CHECK_SATISFIABILITY and not settings.ALL_USE_RULE:
            if self.isSearchSucceed():
                self.satisfiability = True

        if settings.CHECK_FOR_EARLY_BACKTRACK and not self.checkForEarlyBacktrack():
            self.state = 'backtrack'
            return

        false_targets = self.getFalseTargets()
        if len(false_targets) > 1:
            self.state = 'backtrack'

            self.layers[self.level].recordForbidenCombination(self.targets)
        
        elif len(false_targets) == 1:
            self.layers[self.level].setCandidates(false_targets, should_use=True)
            self.state = 'choose'
        else:
            self.layers[self.level].setCandidates(self.targets)
            self.state = 'choose'

    def choose(self):
        
        if settings.PROGRESS:
            remain_count = 0
            for level in range(self.level, len(self.layers)):
                remain_count += len(self.layers[level].candidates)*(len(self.targets)+1)**(level-1)
            self.pb_solving.updateProgress(self.total_count-remain_count)

        if self.layers[self.level].pickNextValidTarget():
            self.state = 'propagate'
        else:
            self.layers[self.level].recordForbidenCombination(self.targets)
            self.state = 'backtrack'

    def propagate(self):
        if not self.layers[self.level].getPickedTarget() == 'no':
            self.layers[self.level].getPickedTarget().pickElement(self.layers[self.level].getLayerElement())
        
        self.level -= 1

        if settings.CHOOSE_FROM_MAX_OR_MIN == 'max':
            self.targets.sort(key=lambda target:target.getCurrentValue())
        elif settings.CHOOSE_FROM_MAX_OR_MIN == 'min':
            self.targets.sort(key=lambda target:target.getCurrentValue())
            self.targets.reverse()

        self.state = 'checkfalse'

        if self.level == 0:
            self.satisfiability = True
            
    def backtrack(self):

        if self.level == len(self.mc.elements):
            self.satisfiability = False
            return

        self.layers[self.level].clear()
        self.level += 1

        if not self.layers[self.level].getPickedTarget() == 'no':
            self.layers[self.level].getPickedTarget().popElement()

        self.state = 'choose'

    def getSatisfiability(self):
        return self.satisfiability
    
    def getLayer(self, level):
        return self.layers[level]
