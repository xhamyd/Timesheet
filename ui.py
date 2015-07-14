import timesheet_from_csv as TFC

def incorrectTypes(T, day, startTime, endTime):
    return (type(T) != Timesheet or
            type(day) != string or
            type(startTime) != Time or
            type(endTime) != Time)

def calcNumSlots(T, startTime, endTime):
    duration = endTime - startTime
    return duration / T.timeIncrement
    
def add(T, day, startTime, endTime): #add a time when busy (conflict)
    if incorrectTypes(T, day, startTime, endTime):
        #bad types, do not execute function
        
    numSlots = calcNumSlots(T.startTime, startTime, endTime)
    for i in xrange(numSlots):
        T.markBusy(day
    
