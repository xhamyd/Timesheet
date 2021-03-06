from Tkinter import *

def string_to_time(timeString):
    timeString_list = timeString.split()
    hoursmins_list = timeString_list[0].split(":")
    hours, mins = int(hoursmins_list[0]), int(hoursmins_list[1])
    period = timeString_list[1].upper()
    return Time(hours, mins, period)

def get_maxCellWidth(d_t_l, option):
    maxCellWidth = 0
    if option == "day":
        for day in d_t_l:
            if maxCellWidth < len(day): 
                maxCellWidth = len(day)
    elif option == "time":
        for time in d_t_l:
            if maxCellWidth < len(time): 
                maxCellWidth = len(time)
    elif option == "L":
        for row in d_t_l:
            for item in row:
                if maxCellWidth < len(item):
                    maxCellWidth = len(item)
    else:
        print option
        error("This option should not be a possibility")
    return maxCellWidth

def points_to_pixels(pt): # techically (pt*4/3) but was making things too big on the page
    return round(pt * 3 / 3) 


class Timesheet(object):
    def __init__(self, name, L, dayHeader, timeHeader):
        self.name = name
        self.L = L
        self.dayHeader = dayHeader
        self.timeHeader = timeHeader
        self.timeIncrement = self.calcTimeIncr() # minute difference
        self.startingTime, self.endingTime = self.calcEndpointTimes()

    def __str__(self):
        return "Timesheet (%s)" % self.name

    def getIndices(self, day, time):
        if (day in self.dayHeader and time in self.timeHeader):
            return (self.dayHeader.index(day), self.timeHeader.index(time))
        else:
            print "The requested day or time does not exist in the headers"
            return False
            
    def checkAvail(self, day, time):
        (dayIndex, timeIndex) = self.getIndices(day, time)
        return self.L[timeIndex][dayIndex] == ''

    def markBusy(self, day, time):
        (dayIndex, timeIndex) = self.getIndices(day, time)
        self.L[timeIndex][dayIndex] = "x"

    def markFree(self, day, time):
        (dayIndex, timeIndex) = self.getIndices(day, time)
        self.L[timeIndex][dayIndex] = ""
        
    def calcTimeIncr(self):
        if len(self.timeHeader) > 1: 
            second_time, first_time = string_to_time(self.timeHeader[1]), string_to_time(self.timeHeader[0])
            return second_time.diff(first_time)
        else: 
            return False #there is no timeIncrement
            
    def calcEndpointTimes(self):
        return string_to_time(self.timeHeader[0]), string_to_time(self.timeHeader[-1])
        
    def disp(self):
        # x is width, y is height
        maxCellWidth_day = get_maxCellWidth(self.dayHeader, "day")
        maxCellWidth_time = get_maxCellWidth(self.timeHeader, "time")
        maxCellWidth_L = get_maxCellWidth(self.L, "L")
        maxCellWidth_dL = max(maxCellWidth_day, maxCellWidth_L)

        font_size = 8
        cellWidth_dL = points_to_pixels(maxCellWidth_dL * font_size)
        cellWidth_time = points_to_pixels(maxCellWidth_time * font_size)
        cellHeight = 2 * font_size
        topMargin = 3 * font_size
        borderMargin = 20
        winWidth = cellWidth_time + cellWidth_dL * len(self.dayHeader) + 2 * borderMargin
        winHeight = cellHeight * len(self.timeHeader) + topMargin + 1.5 * borderMargin
        root = Tk()
        root.wm_title("Timesheet")
        canvas = Canvas(root, width=winWidth, height=winHeight)
        canvas.pack(expand=YES)

        # create title header
        canvas.create_text(winWidth/2 + cellWidth_time/2, topMargin/2, text=self.name)

        tH, dH, L = [""], [""], [[]]
        for t in self.timeHeader: tH.append(t)
        for d in self.dayHeader: dH.append(d)
        for row in self.L: 
            Lrow = [""]
            for item in row: Lrow.append(item)
            L.append(Lrow)

        maxCellLength = 0
        for row in xrange(len(tH)):
            for col in xrange(len(dH)):
                if (row == 0) and (col == 0):
                    continue
                elif row == 0: # day header
                    cellFill = ""
                    cellText = dH[col]
                    x0 = cellWidth_time + (col - 1) * cellWidth_dL + borderMargin
                    y0 = topMargin
                    x1 = x0 + cellWidth_dL
                    y1 = y0 + cellHeight
                elif col == 0: # time header
                    cellFill = ""
                    cellText = tH[row]
                    x0 = borderMargin
                    y0 = row * cellHeight + topMargin
                    x1 = x0 + cellWidth_time
                    y1 = y0 + cellHeight
                else: # inside L
                    cellFill = "red" if (len(L[row][col]) > 0) else "green"
                    cellText = L[row][col]
                    x0 = cellWidth_time + (col - 1) * cellWidth_dL + borderMargin
                    y0 = cellHeight * row + topMargin
                    x1 = x0 + cellWidth_dL
                    y1 = y0 + cellHeight
                canvas.create_rectangle(x0, y0, x1, y1, fill=cellFill)
                canvas.create_text((x0 + x1)/2, (y0 + y1)/2, text=cellText) 
            
        root.mainloop()

    def write(self, printout_path):
        free_mark = "o"
        busy_mark = "."

        f = open(printout_path + "/%s.txt" % self.name, "w+")
        for i_time in xrange(len(self.timeHeader) + 1):
            for i_day in xrange(len(self.dayHeader) + 1):
                if (i_time == 0) and (i_day == 0):
                    print >> f, "        ", " \t",
                elif (i_day == 0):
                    time = self.timeHeader[i_time - 1]
                    if len(time) == len("h:mm XM"):
                        print >> f, "", self.timeHeader[i_time - 1], " \t",
                    else:
                        print >> f, self.timeHeader[i_time - 1], " \t",
                elif (i_time == 0):
                    print >> f, self.dayHeader[i_day - 1][0], " \t",
                else:
                    item = self.L[i_time - 1][i_day - 1]
                    if len(item) == 0:
                        print >> f, free_mark, " \t",
                    else:
                        print >> f, busy_mark, " \t",
            print >> f
        f.close()
        print "File written at %s" % printout_path
            

class Time(object):
    def __init__(self, hours, mins, period):
        self.hours = hours
        self.mins = mins
        self.period = period.upper()
        
    def __str__(self):
        return "%d:%02d %s" % (self.hours, self.mins, self.period)

    def __add__(self, other):
        if type(other) is Time:
            hours1, mins1 = self.convert_to_24hr()
            hours2, mins2 = other.convert_to_24hr()
            hoursX, minsX = hours1 + hours2, mins1 + mins2

        elif type(other) is int:
            hours1, mins1 = self.convert_to_24hr()
            mins2 = other
            hoursX, minsX = hours1, mins1 + mins2

        else:
            print "Time cannot be added to %s objects" % str(type(other))

        while minsX >= 60: # minutes can only be from :00 to :59
            hoursX += 1
            minsX -= 60
        hoursX = hoursX % 24 # hours (in 24hr format) can only be from 0: to 23:
            
        if hoursX > 12:
            hoursX -= 12
            periodX = "PM"
        elif hoursX == 12:
            periodX = "PM"
        elif hoursX == 0:
            hoursX = 12
            periodX = "AM"
        else:
            periodX = "AM"

        return Time(hoursX, minsX, periodX)

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
        elif hoursX == 12:
            periodX = "PM"
        elif hoursX == 0:
            hoursX = 12
            periodX = "AM"
        else:
            periodX = "AM"
        return Time(hoursX, minsX, periodX)
        
    def diff(self, other):
        hours1, mins1 = self.convert_to_24hr()
        hours2, mins2 = other.convert_to_24hr()

        true_mins1 = hours1 * 60 + mins1
        true_mins2 = hours2 * 60 + mins2

        return abs(true_mins1 - true_mins2) # integer

    def __lt__(self, other):
        hours1, mins1 = self.convert_to_24hr()
        hours2, mins2 = other.convert_to_24hr()
        
        if hours1 < hours2: 
            return True
        elif hours2 < hours1: 
            return False
        else: #hours1 == hours2
            return True if mins1 < mins2 else False 

    def __le__(self, other):
        hours1, mins1 = self.convert_to_24hr()
        hours2, mins2 = other.convert_to_24hr()
        
        if hours1 <= hours2: 
            return True
        elif hours2 <= hours1: 
            return False
        else: #hours1 == hours2
            return True if mins1 <= mins2 else False 

    def __gt__(self, other):
        hours1, mins1 = self.convert_to_24hr()
        hours2, mins2 = other.convert_to_24hr()
        
        if hours1 > hours2: 
            return True
        elif hours2 > hours1: 
            return False
        else: #hours1 == hours2
            return True if mins1 > mins2 else False 

    def __ge__(self, other):
        hours1, mins1 = self.convert_to_24hr()
        hours2, mins2 = other.convert_to_24hr()
        
        if hours1 >= hours2: 
            return True
        elif hours2 >= hours1: 
            return False
        else: #hours1 == hours2
            return True if mins1 >= mins2 else False 

    def __eq__(self, other):
        hours1, mins1 = self.convert_to_24hr()
        hours2, mins2 = self.convert_to_24hr()

        return (hours1 == hours2) and (mins1 == mins2)

    def __ne__(self, other):
        hours1, mins1 = self.convert_to_24hr()
        hours2, mins2 = self.convert_to_24hr()

        return (hours1 != hours2) or (mins1 != mins2)

    def convert_to_24hr(self):
        if self.period == "AM":
            if self.hours == 12: hours = 0
            else: hours = self.hours
        elif self.period == "PM":
            if self.hours == 12: hours = 12
            else: hours = self.hours + 12
        else:
            print "Period is not correctly defined: use only 'AM' or 'PM'"
            return
        mins = self.mins
        
        return hours, mins
