#Created by Justin Alderson
#A class to represent a motion 

class Movement(object):

    def __init__ (self, count, date_time):
        self.count = count
        self.date_time = date_time

    def getCount(self):
        return self.count

    def getDateTime(self):
        return self.date_time
