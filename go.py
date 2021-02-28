# libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
 

def autolabel(rects):
    # attach a text label above each bar in rects, displaying its height
    for rect in rects:
        height = rect.get_height()
        plt.annotate(
            '{}'.format(height),
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha='center', va='bottom'
        )

def animate():

    # Data
    r = [0,1,2,3,4]
    green_data = [20, 1.5, 7, 10, 5]
    orange_data = [5, 15, 5, 10, 15]
    blue_data = [2, 15, 18, 5, 10]

    # From raw value to percentage
    totals = [i+j+k for i,j,k in zip(green_data, orange_data, blue_data)]
    greenBars = [i / j * 100 for i,j in zip(green_data, totals)]
    orangeBars = [i / j * 100 for i,j in zip(orange_data, totals)]
    blueBars = [i / j * 100 for i,j in zip(blue_data, totals)]
    
    # plot
    barWidth = 0.85
    names = ('A','B','C','D','E')
    # Create green Bars
    green_rect = plt.bar(r, greenBars, color='#b5ffb9', edgecolor='white', width=barWidth, label="group C")
    # Create orange Bars
    orange_rect = plt.bar(r, orangeBars, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth, label="group C")
    # Create blue Bars
    blue_rect = plt.bar(r, blueBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color='#a3acff', edgecolor='white', width=barWidth, label="group C")

    autolabel(green_rect)
    autolabel(orange_rect)
    autolabel(blue_rect)

    # Custom x axis
    plt.xticks(r, names)
    plt.xlabel("group")
    
    # Add a legend
    plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)

animate() 
    # Show graphic
plt.show()