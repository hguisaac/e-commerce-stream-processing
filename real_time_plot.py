

#--------------------------------------------------

# libraries
import numpy as np
import matplotlib.pyplot as plt
from random import shuffle, randint
from time import sleep
# set width of bar
barWidth = 0.25
 
# set height of bar

bars1 = [12, 30, 1, 8, 22]
bars2 = [28, 6, 16, 5, 10]
bars3 = [29, 3, 24, 25, 17]

# Set position of bar on X axis
r1 = np.arange(5)
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

isset_legend = False

def get_plotted():
    global isset_legend
    global bars1, bars2, bars3
    x_list = ['14:11-14:11', 'B', 'C', 'D', 'E']
    while True:
        # Make the plot
        
        padding_list1 = [ randint(0,5) for __ in range(5)]
        padding_list2 = [ randint(0,5) for __ in range(5)]
        padding_list3 = [ randint(0,5) for __ in range(5)]
        plt.bar(r1, padding_list1, color='#7f6d5f', width=barWidth, edgecolor='white', label='var1')
        plt.bar(r2, padding_list2, color='#557f2d', width=barWidth, edgecolor='white', label='var2')
        plt.bar(r3, padding_list3, color='#2d7f5e', width=barWidth, edgecolor='white', label='var3')
        print(x_list, padding_list1, padding_list2, padding_list3)
        # Add xticks on the middle of the group bars
        plt.xlabel('group', fontweight='bold')
        
        if isset_legend == False:
            plt.legend()
            isset_legend = True

        plt.xticks([r + barWidth for r in range(len(bars1))], x_list)
        shuffle(x_list)
        # print(x_list)
        fig.canvas.draw()
        sleep(2)
        plt.cla()
    
    # Create legend & Show graphic

fig = plt.figure()
win = fig.canvas.manager.window
win.after(100, get_plotted)
plt.show()