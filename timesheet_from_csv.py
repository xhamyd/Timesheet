"""
    A timesheet is represented by a 2D list, with 2 1D list for the headers
"""

import string
import csv

def string_to_time(timeString):
    timeString_list = timeString.split()
    hoursmins_list = timeString_list[0].split(":")
    hours, mins = int(hoursmins_list[0]), int(hoursmins_list[1])
    period = timeString_list[1].upper()
    return Time(hours, mins, period)
    
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
        if len(timeHeader) > 1: 
            return string_to_time(timeHeader[1]) - string_to_time(timeHeader[0])
        else: 
            return False #there is no timeIncrement
            
    def disp(self):
        #use some Tkinter shii

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
        mins1 = self.mins
        
        hours2 = other.hours + 12 if (other.period == "PM") else other.hours
        hours2 = 0 if (other.period == "AM" and other.hours == 12) else hours2
        mins2 = other.mins
        
        if self.mins < other.mins:
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
    
    return Timesheet(L, dayHeader, timeHeader)
