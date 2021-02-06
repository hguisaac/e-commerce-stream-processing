from matplotlib.animation import FuncAnimation
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


labels = [
    ['Group1', 'Group2', 'Group3', 'Group4', 'Group5'],
    ['GroupA', 'GroupB', 'GroupC', 'GroupD', 'GroupE']
]
men_means = [20, 34, 30, 35, 27]
women_means = [25, 32, 34, 20, 25]
childreen_means = [11, 25, 25, 32, 34]


def autolabel(rects, ax):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

fig, ax = plt.subplots()
def graph(i):

    x = np.arange(len(labels[0]))  # the label locations
    width = 0.25  # the width of the bars

    rects1 = ax.bar(x + 0.00 , men_means, width, label='Men')
    rects2 = ax.bar(x + 0.25, women_means, width, label='Women')
    rects3 = ax.bar(x + 0.50, childreen_means, width, label='Childreen')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(x+width)
    ax.set_xticklabels(labels[0])
    ax.legend()

    # autolabel(rects1, ax)
    # autolabel(rects2, ax)
    # autolabel(rects3, ax)

    fig.tight_layout()
    return 

# ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
#                     init_func=init, blit=True)


ani = FuncAnimation(
    fig, graph, interval=3000, blit=True)


plt.show()
