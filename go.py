import numpy as np
import matplotlib.pyplot as plt
from random import shuffle, randint
from time import sleep
from collections import namedtuple

Point = namedtuple("Point", "win_start, win_end, promo, count")

list_points = [
    Point(win_start='2021-02-07T17:25:00.000+01:00', win_end='2021-02-07T17:27:00.000+01:00', promo='promo_A', count=7), 
    Point(win_start='2021-02-07T17:25:00.000+01:00', win_end='2021-02-07T17:27:00.000+01:00', promo='promo_0', count=12), 
    Point(win_start='2021-02-07T17:25:00.000+01:00', win_end='2021-02-07T17:27:00.000+01:00', promo='promo_0', count=15), 
    Point(win_start='2021-02-07T17:25:00.000+01:00', win_end='2021-02-07T17:27:00.000+01:00', promo='promo_C', count=12)
]

bar_width = 0.25

# bar := promotion
# bar_height := promotion_count

def namedtuple_to_namedlist():
    NamedList = namedtuple("NamedList", "window", )
    pass

# set height of bar
# bars1 = [12, 30, 1, 8, 22]
# bars2 = [28, 6, 16, 5, 10]
# bars3 = [29, 3, 24, 25, 17]

# Set position of bar on X axis
bar1_x_pos = np.arange(5)
bar2_x_pos = [x + bar_width for x in bar1_x_pos]
bar3_x_pos = [x + bar_width for x in bar2_x_pos]

isset_legend = False

def get_plotted():
    global isset_legend
    global bars1, bars2, bars3
    x_tick_labels = ['14:11-14:11', 'B', 'C', 'D', 'E']
    while True:
        # Make the plot
        bar1_heights = [ randint(0,5) for __ in range(5)]
        bar2_heights = [ randint(0,5) for __ in range(5)]
        bar3_heights = [ randint(0,5) for __ in range(5)]
        plt.bar(bar1_x_pos, bar1_heights, color='#7f6d5f', width=bar_width, edgecolor='white', label='var1')
        plt.bar(bar2_x_pos, bar2_heights, color='#557f2d', width=bar_width, edgecolor='white', label='var2')
        plt.bar(bar3_x_pos, bar3_heights, color='#2d7f5e', width=bar_width, edgecolor='white', label='var3')
        print(x_tick_labels, bar1_heights, bar2_heights, bar3_heights)
        # Add xticks on the middle of the group bars
        plt.xlabel('group', fontweight='bold')
        
        if isset_legend == False:
            plt.legend()
            isset_legend = True

        plt.xticks([r + bar_width for r in range(5)], x_tick_labels)
        # plt.xticks([r + bar_width for r in range(len(bars1))], x_tick_labels)
        shuffle(x_tick_labels)
        # print(x_tick_labels)
        fig.canvas.draw()
        sleep(2)
        plt.cla()
    
    # Create legend & Show graphic

fig = plt.figure()
win = fig.canvas.manager.window
win.after(100, get_plotted)
plt.show()

