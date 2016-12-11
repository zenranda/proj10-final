##Supplemental Python functions to simulate certain date functionality from get_freebusy.py without having to go through the entire massive function
##Largely for testing

import arrow

def date_overlap(array):   #tests whether a recieved block of dates overlaps at all. input = [[start, end], [start, end] . . . ]. Sorted
    overlap = arrow.get(array[0][1])
    for item in array:
        if item == array[0]:
            pass
        elif overlap > arrow.get(item[0]):
            return True
        overlap = arrow.get(item[1])
        
    return False
    
    
def date_underlap(array, start):   #tests whether any of a block of dates start before our daterange beings
    for item in array:
        for i in range(0, len(array)-1):
            if arrow.get(array[i][0]) > arrow.get(start):
                return True
        
    return False
    
    