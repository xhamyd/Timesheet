"""
    A timesheet is represented by a 2D list, with 2 1D list for the headers
"""

import string
import csv
from Tkinter import *

def string_to_time(timeString):
    timeString_list = timeString.split()
    hoursmins_list = timeString_list[0].split(":")
    hours, mins = int(hoursmins_list[0]), int(hoursmins_list[1])
    period = timeString_list[1].upper()
    return Time(hours, mins, period)

def calcEndpointTimes(timeHeader):
    return string_to_time(timeHeader[0]), string_to_time(timeHeader[-1])

def minTime(time1, time2):
    return time1 if time1 < time2 else time2
    
def maxTime(time1, time2):
    return time1 if time1 > time2 else time2


class Timesheet(object):
    def __init__(self, name, L, dayHeader, timeHeader):
        self.name = name
        self.L = L
        self.dayHeader = dayHeader
        self.timeHeader = timeHeader
        self.timeIncrement = self.calcTimeIncr(timeHeader)
        self.startingTime, self.endingTime = calcEndpointTimes(timeHeader)

    def getIndices(self, day, time):
        if (day in dayHeader and time in timeHeader):
            return (self.dayHeader.index(day), self.timeHeader.index(time))
        else:
            print "The requested day or time does not exist in the headers"
            return False
            
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
        if len(timeHeader) > 1: 
            return string_to_time(timeHeader[1]) - string_to_time(timeHeader[0])
        else: 
            return False #there is no timeIncrement
            
    def calcEndpointTimes(self):
        return string_to_time(self.timeHeader[0]), string_to_time(self.timeHeader[-1])
        
    def disp(self, freeTimesOnly=False):
        winWidth, winHeight = 300, 200
        cellWidth, cellHeight = 50, 25
        topMargin = 35
        
        root = Tk()
        canvas = Canvas(root, winWidth, winHeight)
        canvas.pack()

        canvas.create_rectangle(0, 0, winWidth, topMargin, text=self.name)
        for row in xrange(len(self.timeHeader)):
            for col in xrange(len(self.dayHeader)):
                if row == 0: cellText = self.dayHeader[col]
                elif col == 0: cellText = self.timeHeader[row]
                else: cellText = self.L[row][col]
                canvas.create_rectangle(row * cellHeight + topMargin, col * cellWidth,
                                        (row + 1) * cellHeight + topMargin, (col + 1) * cellWidth,
                                        text=cellText)
            
        root.mainloop()

class Time(object):
    def __init__(self, hours, mins, period):
        self.hours = hours
        self.mins = mins
        self.period = period.upper()
        
    def __repr__(self):
        return "%02d:%02d %s" % (self.hours, self.mins, self.period)
        
    def __sub__(self, other):
        hours1, mins1 = self.convert_to_24hr()
        hours2, mins2 = other.convert_to_24hr()
        
        if mins1 < mins2:
            hours1 = hours1 - 1 if (hours1 != 0) else hours + 24 - 1
            mins1 += 60
        
        hoursX, minsX = hours1 - hours2, mins1 - mins2
        if hoursX > 12:
            hoursX -= 12
            periodX = "PM"
        elif hoursX == 0:
            hoursX += 12
            periodX = "AM"
        else:
            periodX = "AM"
        return Time(hoursX, minsX, periodX)
        
    def __lt__(self, other):
        hours1, mins1 = self.convert_to_24hr()
        hours2, mins2 = other.convert_to_24hr()
        
        if hours1 < hours2: 
            return self
        elif hours2 < hours1: 
            return other
        else: #hours1 == hours2
            return self if mins1 < mins2 else other 

    def __gt__(self, other):
        hours1, mins1 = self.convert_to_24hr()
        hours2, mins2 = other.convert_to_24hr()
        
        if hours1 > hours2: 
            return self
        elif hours2 > hours1: 
            return other
        else: #hours1 == hours2
            return self if mins1 > mins2 else other 

    def convert_to_24hr(self): 
        hours = self.hours + 12 if (self.period == "PM") else self.hours
        hours = 0 if (self.period == "AM" and self.hours == 12) else hours
        mins = self.mins
        
        return hours, mins

def timesheet_from_csv():
    timesheet_file = open(TIMESHEET_FROM_CSV_FILE), 'rU')
    timeHeader, L = [""], [[]]
    for i, line in enumerate(timesheet_file):
        columns = line.strip().split(',')
        if i == 0: 
            dayHeader = columns
            continue
        
        timeHead = columns.pop(0) #remove the time header
        timeHeader.append(timeHead)
        L[i - 1] = columns
    
    return Timesheet(TIMESHEET_FROM_CSV_FILE.strip(".csv"), L, dayHeader, timeHeader)
