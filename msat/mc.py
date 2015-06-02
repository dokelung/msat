import copy
import msat.progress as progress
import msat.settings as settings

class Mc:

    def setElements(self, elements):
        self.elements = copy.copy(elements)
        if settings.ELEMENTS_ORDER == 'increase':
            self.elements.sort()
        elif settings.ELEMENTS_ORDER == 'decrease':
            self.elements.sort()
            self.elements.reverse()
        self.pos_sum = sum([item if item >= 0 else 0 for item in self.elements])
        self.neg_sum = sum([item if item  < 0 else 0 for item in self.elements])
    
    def setTargets(self, targets):
        self.targets = copy.copy(targets)
        if settings.TARGETS_ORDER == 'increase':
            self.targets.sort()
        elif settings.TARGETS_ORDER == 'decrease':
            self.targets.sort()
            self.targets.reverse()

    def getPositiveSumOfElements(self):
        return self.pos_sum

    def getNegativeSumOfElements(self):
        return self.neg_sum

    def getLeftBorderTarget(self):
        pass

    def getRightBorderTarget(self):
        pass

    def getValueByBorderTarget(self, j):
        pass

    def getValueByFactOfEmptyMultiset(self, j):
        pass

    def getAllTrueRegion(self):
        pass

    def getJRange(self):
        try:
            return self.jrange
        except:
            if settings.JRANGE_MIN:
                left_border = max(min(self.targets)-self.getPositiveSumOfElements(), self.getLeftBorderTarget())
                right_border = min(max(self.targets)-self.getNegativeSumOfElements(), self.getRightBorderTarget())
            else:
                left_border = self.getNegativeSumOfElements()
                right_border = self.getPositiveSumOfElements()
            self.jrange = range(left_border, right_border+1)
            return self.jrange

    def getIRange(self):
        try:
            return self.irange
        except:
            self.irange = range(len(self.elements)+1)
            return self.irange

    def getTableSize(self):
        return len(self.getIRange()) * len(self.getJRange())

    def getValue(self, i, j):
        return self.getValueByDic(i, j)

    def getValueByDic(self, i, j):
        try:
            return i >= self.dic[j]
        except:
            return self.computeValue(i, j)

    def getValueByTable(self, i, j):
        try:
            return self.table[i][j]
        except:
            return self.computeValue(i, j)

    def getValueWithoutTable(self, i, j):
        return i >= self.dic[j] 

    def getUpperValue(self, i, j):
        return self.getValueByDic(i-1, j-self.elements[i-1])

    def getUpperTarget(self, i, j):
        return j-self.elements[i-1]

    def computeValue(self, i, j):
        
        try:
            if not self.table[i][j]==None:
                return self.table[i][j]
        except:
            pass

        if i==0:
            value = self.getValueByFactOfEmptyMultiset(j)
        elif j not in range(self.getLeftBorderTarget(), self.getRightBorderTarget()+1):
            value = self.getValueByBorderTarget(j)
        else:
            value = self.computeValue(i-1, j) or self.computeValue(i-1, j-self.elements[i-1])

        if i in self.getIRange() and j in self.getJRange():
            self.table[i][j] = value

        return value

    def buildTable(self):
        self.table = []

        if settings.PROGRESS:
            pb_build_table = progress.ProgressBar('Build MC Table', 2*self.getTableSize())

        for i in self.getIRange():
            self.table.append({})
            for k, j in enumerate(self.getJRange()):
                self.table[i][j] = None

                if settings.PROGRESS:
                    current_count = (i+1)*len(self.getJRange()) + (k+1)
                    pb_build_table.updateProgress(current_count)

        for i in self.getIRange():
            for k, j in enumerate(self.getJRange()):
                if self.table[i][j]==None:
                    self.computeValue(i, j)

                if settings.PROGRESS:
                    current_count = (i+1)*len(self.getJRange()) + (k+1) + self.getTableSize()
                    pb_build_table.updateProgress(current_count)

    def buildDic(self):
        self.dic = {}

        if settings.PROGRESS:
            pb_build_dic = progress.ProgressBar('Build MC Dic', 3*len(self.getJRange()))

        for k, j in enumerate(self.getJRange()):
            self.dic[j] = -1
            
            if settings.PROGRESS:
                pb_build_dic.updateProgress(k)

        for k, j in enumerate(self.getJRange()):
            for i in self.getIRange():
                if not self.table[i][j]:
                    self.dic[j] = i
                else:
                    break
            
            if settings.PROGRESS:
                pb_build_dic.updateProgress(k+1+len(self.getJRange()))

        for k, j in enumerate(self.getJRange()):
            self.dic[j] += 1
            
            if settings.PROGRESS:
                pb_build_dic.updateProgress(k+1+2*len(self.getJRange()))

class McEq(Mc):

    def getLeftBorderTarget(self):
        return self.getNegativeSumOfElements()

    def getRightBorderTarget(self):
        return self.getPositiveSumOfElements()

    def getValueByBorderTarget(self, j):
        if  j < self.getLeftBorderTarget() or j > self.getRightBorderTarget():
            return False

    def getValueByFactOfEmptyMultiset(self, j):
        return False if not j==0 else True

    def getAllTrueRegion(self):
        return '==0'

class McGt(Mc):

    def getLeftBorderTarget(self):
        return 0

    def getRightBorderTarget(self):
        return self.getPositiveSumOfElements()-1

    def getValueByBorderTarget(self, j):
        if j < self.getLeftBorderTarget():
            return True
        elif j > self.getRightBorderTarget():
            return False

    def getValueByFactOfEmptyMultiset(self, j):
        return True if j<0 else False

    def getAllTrueRegion(self):
        return '<0'

class McGe(Mc):

    def getLeftBorderTarget(self):
        return 1

    def getRightBorderTarget(self):
        return self.getPositiveSumOfElements()

    def getValueByBorderTarget(self, j):
        if j < self.getLeftBorderTarget():
            return True
        elif j > self.getRightBorderTarget():
            return False

    def getValueByFactOfEmptyMultiset(self, j):
        return True if j<=0 else False

    def getAllTrueRegion(self):
        return '<1'

class McLt(Mc):

    def getLeftBorderTarget(self):
        return self.getNegativeSumOfElements()+1

    def getRightBorderTarget(self):
        return 0

    def getValueByBorderTarget(self, j):
        if j < self.getLeftBorderTarget():
            return False
        elif j > self.getRightBorderTarget():
            return True

    def getValueByFactOfEmptyMultiset(self, j):
        return False if j<=0 else True

    def getAllTrueRegion(self):
        return '>0'

class McLe(Mc):

    def getLeftBorderTarget(self):
        return self.getNegativeSumOfElements()

    def getRightBorderTarget(self):
        return -1

    def getValueByBorderTarget(self, j):
        if j < self.getLeftBorderTarget():
            return False
        elif j > self.getRightBorderTarget():
            return True

    def getValueByFactOfEmptyMultiset(self, j):
        return False if j<0 else True

    def getAllTrueRegion(self):
        return '>-1'
