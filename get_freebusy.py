import arrow
from operator import itemgetter


def get_freebusy(ranges, start, end):
#Given a date/time range and a list of lists containing start/end times for busy blocks,
# finds the free time, the busy time, truncates them if applicable (ie: if they go over/under the maximum/minimum range)
# then puts them in a sorted list, finalized and ready to be read by the user.
#
# Some of these loops are a little convoluted, there's probably a better way to do this.
    if ranges == []:        #if the free/busy blocks are empty, return empty list (prevents indexing crashes)
        free = []
        busy = []
        res = []
        res.append(free)
        res.append(busy)
        return res
        
    daylist = []
    dayof = []
    currday = arrow.get(start).to('local')
    while currday <= end.to('local'):                       #Adds each free/busy block into a list based on day
        for item in ranges:
            if arrow.get(item[0]).day == currday.day:
                dayof.append(item)
            if item == ranges[-1]:
                daylist.append(sorted(dayof, key=itemgetter(0)))
                dayof = []
                currday = currday.replace(days=+1)


    for item in daylist:                                        #overlap logic; searches through the list of items and changes start/end time
        x = 0
        i = 1
        set = 0
        while i <= len(item)/2:
            if arrow.get(item[x][1]) > arrow.get(item[i][0]):   #if the end time of one is after the start time of the other
                if arrow.get(item[i][1]) < arrow.get(item[x][1]):   #if the end time of one is before the end time of the other (ie: full overlap)
                    set = 1
                if arrow.get(item[i][1]) > arrow.get(item[x][1]):    #if the end time of the other is after the end time of the first
                    item[x][1] = item[i][1]                        #set the end time of the first to the end time of the second (in essence, merge the two
                    set = 1
                if set == 1:
                    del item[i]
                    x = -2
                    i = -1
                    set = 0

            x += 2
            i += 2

    startdelta = start                                                                      #if the dates start/end before/after our range starts or ends
    enddelta = startdelta.replace(hour=arrow.get(end).hour, minute = arrow.get(end).minute)
    for item in daylist:
        deldex = []
        for elem in item:
            if arrow.get(elem[0]) < startdelta.to('local'): #if the start time is before our start time, make its start time equal to it
                elem[0] = startdelta.isoformat()
            if arrow.get(elem[1]) > enddelta.to('local'):   #if the end time is after our end time, make its end time equal to it
                elem[1] = enddelta.isoformat()
            if arrow.get(elem[0]) > arrow.get(elem[1]):          #if the event starts after it ends, then just remove it
                deldex.append(elem)
                        

        startdelta = startdelta.replace(days=+1)
        enddelta = enddelta.replace(days=+1)
        for obj in deldex:
            item.remove(obj)

    free = []
    busy = []
    i = 0
    starter = start
    ender = starter.replace(hour=arrow.get(end).hour, minute=arrow.get(end).minute)
    for item in daylist:                                        #actually filling out the free/busy ranges
        for elem in item:
            busy.append("At " + str(arrow.get(elem[0]).date()) + " from " + str(arrow.get(elem[0]).time()) + " to " + str(arrow.get(elem[1]).time()))
            if elem == item[0]:                                 #if it's the first item
                if str(starter) != str(elem[0]):
                    free.append("At " + str(arrow.get(starter).date()) + " from " + str(arrow.get(starter).time()) + " to " + str(arrow.get(elem[0]).time()))
            else:
                free.append("At " + str(arrow.get(last).date()) + " from " + str(arrow.get(last).time()) + " to " +  str(arrow.get(elem[0]).time()))
                i += 1
            if elem == item[-1]:                                #if it's the last item
                if str(elem[1]) != str(ender):
                    free.append("At " + str(arrow.get(elem[1]).date()) + " from " + str(arrow.get(elem[1]).time()) + " to " + str(arrow.get(ender).time()))
            
            last = elem[1]                                      #the ending value is saved so we can refer to it on the final item
        starter = starter.replace(days=+1)
        ender = ender.replace(days=+1)
            
        

    res = []
    res.append(free)
    res.append(busy)
    
    return res
