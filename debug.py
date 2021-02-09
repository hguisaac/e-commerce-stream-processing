import numpy as np
import matplotlib.pyplot as plt
import re
from random import shuffle, randint
from time import sleep
from collections import namedtuple
from helper import W,R,P,G
Point = namedtuple("Point", "win_start, win_end, promo, count")

list_points = [
    Point(win_start='2021-02-07T17:25:00.000+01:00', win_end='2021-02-07T17:27:00.000+01:00', promo='promo_A', count=7), 
    Point(win_start='2021-02-07T17:25:00.000+01:00', win_end='2021-02-07T17:27:00.000+01:00', promo='promo_0', count=12), 
    Point(win_start='2021-02-07T17:25:00.000+01:00', win_end='2021-02-07T17:27:00.000+01:00', promo='promo_0', count=15), 
    Point(win_start='2021-02-07T17:25:00.000+01:00', win_end='2021-02-07T17:27:00.000+01:00', promo='promo_C', count=12),
    Point(win_start='2021-02-07T17:25:00.000+01:00', win_end='2021-02-07T17:27:00.000+01:00', promo='promo_A', count=13),
    Point(win_start='2021-02-07T17:27:00.000+01:00', win_end='2021-02-07T17:29:00.000+01:00', promo='promo_C', count=16),
    Point(win_start='2021-02-07T17:27:00.000+01:00', win_end='2021-02-07T17:29:00.000+01:00', promo='promo_0', count=10),
    Point(win_start='2021-02-07T17:27:00.000+01:00', win_end='2021-02-07T17:29:00.000+01:00', promo='promo_C', count=11)
]

bar_width = 0.25

# bar := promotion
# bar_height := promotion_count
list_promos = ["promo_A", "promo_C", "promo_0"]
drawing_list = [ ["dd:dd:dd-dd:dd:dd", promo, 0] for promo in list_promos]


# print(drawing_list)

def from_namedtuples_update_drawing_list():
    global drawing_list
    
    for point in list_points:
        # win_start and win_end have the following format 
        # %Y%Y%Y%Y-%M%M-%D%DT%H%h%h:%m%m:%s%s
        # we then wrote the regex regarding that format

        start_match = re.search("\d\d:\d\d:\d\d", point.win_start)
        end_match = re.search("\d\d:\d\d:\d\d", point.win_end)
        if start_match == None:
            start_match = re.search("\d\d:\d\d:\d\d", point.win_start)
        if end_match == None:
            end_match = re.search("\d\d:\d\d:\d\d", point.win_start)

        assert(start_match != None)
        assert(end_match != None)

        # Take only the times and leave the date (month, year, day)
        time_win = (
            point.win_start[start_match.start():start_match.end()]
            +
            "-"
            +
            point.win_end[end_match.start():end_match.end()]
        )

        some_count_has_been_updated = False
        for line in drawing_list:
            if line[0] == time_win and line[1] == point.promo:
                line[2] = point.count
                some_count_has_been_updated = True
                # as were are using update mode in spark we can not 
                # have the same line many times, so we break
                break
        if some_count_has_been_updated == False:
            drawing_list.append([time_win, point.promo, point.count])


from_namedtuples_update_drawing_list()

print(drawing_list)

