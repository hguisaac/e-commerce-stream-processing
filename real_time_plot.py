import matplotlib.pyplot as plt
from random import randint
from matplotlib import animation
from time import sleep



def list_data():
    pass 

x = [1, 2, 3, 4, 5, 6]
y = [1, 2, 3, 4, 5, 6]

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
    global x, y
    animate.count += 1
    print(animate.count)
    while True:
        x.append(x[-1]+1)
        y.append(x[-1]+1)
        plt.xticks(x)
        rect = plt.bar(x,y, width = 0.5, color = 'blue', label="nothing")
        autolabel(rect)
        plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3)
        fig.canvas.draw()
        sleep(1)
        plt.cla()

animate.count = 0

fig = plt.figure()
win = fig.canvas.manager.window
win.after(100, animate)
plt.show()

	