import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
from time import sleep

def animated_barplot():
    # http://www.scipy.org/Cookbook/Matplotlib/Animations
    mu, sigma = 100, 15
    N = 4
    x = mu + sigma*np.random.randn(N)
    print(x)
    rects = plt.bar(range(N), x,  align = 'center')
    for i in range(50):
        x = mu + sigma*np.random.randn(N)
        for rect, h in zip(rects, x):
            rect.set_height(h)
        fig.canvas.draw()
        # sleep(1)

fig = plt.figure()
win = fig.canvas.manager.window
win.after(100, animated_barplot)
plt.show()
