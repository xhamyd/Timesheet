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
        
    def disp(self):
        winWidth, winHeight = 300, 200
        cellWidth, cellHeight = 50, 25
        topMargin = 35
        
        root = Tk()
        canvas = Canvas(root, winWidth, winHeight)
        canvas.pack()

        canvas.create_rectangle(0, 0, winWidth, topMargin, text=self.name)
        for row in xrange(len(self.timeHeader)):
            for col in xrange(len(self.dayHeader)):
                if row == 0: 
                    cellFill = ""
                    cellText = self.dayHeader[col]
                elif col == 0: 
                    cellFill = ""
                    cellText = self.timeHeader[row]
                else: 
                    cellText = self.L[row][col]
                    cellFill = "" if len(cellText) == 0 else "green"
                canvas.create_rectangle(row * cellHeight + topMargin, col * cellWidth,
                                        (row + 1) * cellHeight + topMargin, (col + 1) * cellWidth,
                                        text=cellText, fill=cellFill)
            
        root.mainloop()
