import time

class TimeQueue():

    def __init__(self):
        self.timeDict = {}
        self.queue = []

    def add(self, item, expecttime = 0):
        '''expecttime is a timestamp, indicate the time when you want to active flow item'''

        # Condition 1: Default add item to queue end.
        if not expecttime:
            return self.queue.append(item) #no attribute

        # Condition 2: Expect runnning time latter than now.
        currTime = time.time()
        if expecttime <= currTime:
            self.queue.insert(0, item)
            return 

        # Condition 3: Add expecttime to time map.
        self.timeDict[expecttime] = item

    # Get left time to next item. Min: 0
    def lefttime(self):
        if self.queue:
            return 0

        if self.timeDict:
            lt = time.time() - min(self.timeDict.keys())
        else:
            lt = 0

        return lt>0 and lt or 0

    def pop(self):
        if self.timeDict and min(self.timeDict.keys())<=time.time():
            return self.timeDict.pop(min(self.timeDict.keys()))

        if self.queue:
            return self.queue.pop(0)

        return None


    def getQueue(self):
        return self.queue