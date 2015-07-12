def incorrectTypes(T, day, startTime, endTime):
    return (type(T) != Timesheet or
            type(day) != string or
            type(startTime) != Time or
            type(endTime) != Time)

def add(T, day, startTime, endTime):
    if incorrectTypes(T, day, startTime, endTime):
        #bad types, do not execute function
        
    
