"""
    A timesheet is represented by a 2D list, with 2 1D list for the headers
"""

import string
import csv

class Timesheet(object):
    def __init__(self, L, dayHeader, timeHeader):
        self.L = L
        self.dayHeader = dayHeader
        self.timeHeader = timeHeader
        self.timeIncrement = self.calcTimeIncr(timeHeader)

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
        
    def calcTimeIncr(self, timeHeader):
        if len(timeHeader) > 1: return subTime(timeHeader[1], timeHeader[0])
        else: return False #there is no timeIncrement

class Time(object):
    def __init__(self, hours, mins, period):
        self.hours = hours
        self.mins = mins
        self.period = period.upper()
        
    def __repr__(self):
        return "%02d:%02d %s" % (self.hours, self.mins, self.period)
        
    def __sub__(self, other):
        hours1 = self.hours + 12 if (self.period == "PM") else self.hours
        hours1 = 0 if (self.period == "AM" and self.hours == 12) else hours1
        
        hours2 = other.hours + 12 if (other.period == "PM") else other.hours
        hours2 = 0 if (other.period == "AM" and other.hours == 12) else hours2
        
        
        
class Conflict(object):
    def __init__(self, timesheet, startTime, endTime)
    
def timesheet_from_csv():
    timesheet_file = open(TIMESHEET_FROM_CSV_FILE), 'rU')
    timeHeader, L = [], [[]]
    for i, line in enumerate(timesheet_file):
        columns = line.strip().split(',')
        if i == 0: #header line
            columns.pop(0) #remove the blank day header
            dayHeader = columns
            continue
        
        timeHeader.append(columns[0])
        columns.pop(0) #remove the time header
        L[i-1] = columns
