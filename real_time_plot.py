import numpy as np
import matplotlib.pyplot as plt
from random import shuffle
from threading import Thread
from random import shuffle, randint
from time import sleep
import asyncio
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

async def update_bars():
    global bars1, bars2, bars3
    print("just get into update_bars")
    shuffle(bars1)
    shuffle(bars2)
    shuffle(bars3)
    return bars1, bars2, bars3
    
    
    

# thread_update = Thread(
#     target=update_bars
# )

# thread_update.start()
# thread_update.join()


async def get_plotted():
    global isset_legend
    # global 
    x_list = ['14:11-14:11', 'B', 'C', 'D', 'E']
    
    # Make the plot
    bars1, bars2, bars3 = await update_bars()
    print(bars1, bars2, bars3)

    plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='var1')
    plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='var2')
    plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='var3')
    # print(x_list, bars1, bars2, bars3)
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

if __name__ == "__main__":
    fig = plt.figure()
    win = fig.canvas.manager.window
    win.after(100, get_plotted)
    plt.show()

    r = get_plotted()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(r)



