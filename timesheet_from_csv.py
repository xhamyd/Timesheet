"""
    A timesheet is represented by a 2D list, with 2 1D list for the headers
"""

import string
import csv
from Classes import *
from Tkinter import *

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
