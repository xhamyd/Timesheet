"""
    A timesheet is represented by a 2D list, with 2 1D list for the headers
"""

import csv

class Timesheet(object):
    def __init__(self, L, dayHeader, timeHeader):
        self.L = L
        self.dayHeader = dayHeader
        self.timeHeader = timeHeader

    def getIndices(self, day, time):
        return (self.dayHeader.index(day), self.timeHeader.index(time))
        
    def checkAvail(self, day, time):
        (dayIndex, timeIndex) = getIndices(self, day, time)
        return self.L[dayIndex][timeIndex] == "x"

    def markBusy(self, day, time):
        (dayIndex, timeIndex) = getIndices(self, day, time)
        return self.L[dayIndex][timeIndex] = "x"

    def markFree(self, day, time):
        (dayIndex, timeIndex) = getIndices(self, day, time)
        return self.L[dayIndex][timeIndex] = ""
