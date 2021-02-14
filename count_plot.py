import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
from time import sleep


def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            # 
            plt.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


def animated_barplot():
    # http://www.scipy.org/Cookbook/Matplotlib/Animations
    mu, sigma = 100, 15
    N = 4
    x = mu + sigma*np.random.randn(N)
    print(x)
    
    for i in range(50):
        rects = plt.bar(range(N), x,  align = 'center')
        x = mu + sigma*np.random.randn(N)
        for rect, h in zip(rects, x):
            rect.set_height(h)
        autolabel(rects)
        fig.canvas.draw()
        sleep(1)
        plt.cla()

fig = plt.figure()
win = fig.canvas.manager.window
win.after(100, animated_barplot)
plt.show()
