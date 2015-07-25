from timesheet_from_csv import *
import math

def incorrectTypes(T, day, startTime, endTime):
    return (type(T) != Timesheet or
            type(day) != string or
            type(startTime) != Time or
            type(endTime) != Time)

def missingFromHeaders(T, day, startTime, endTime):
    return (day not in T.dayHeader or
            startTime > T.endingTime or
            endTime < T.startingTime) 
    
def REQUIRES_CHECK(T, day, startTime, endTime):
    return (not incorrectTypes(T, day, startTime, endTime) and
            not missingFromHeaders(T, day, startTime, endTime))
            
def calcNumSlots(T, startTime, endTime):
    sT = maxTime(startTime, T.startingTime)
    eT = minTime(endTime, T.endingTime)
    duration = eT - sT
    return int(math.ceil(duration / T.timeIncrement)), sT, eT
    
def add(T, day, startTime, endTime): #add a time when busy (conflict)
    if not REQUIRES_CHECK(T, day, startTime, endTime):
        #bad types, do not execute function
        print "Could not add timeslot as requested, please check the types of the files passed in"
        
    numSlots, sT, eT = calcNumSlots(T, startTime, endTime)
    for i in xrange(numSlots): 
        T.markBusy(day, startTime + i * T.timeIncrement)
    
    print "Added conflict for %s from %r to %r" % (day, sT, eT)
    
def freeTimes(T):
    
    
