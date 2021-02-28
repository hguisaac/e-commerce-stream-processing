#importing libraries
import matplotlib.pyplot as plt
import matplotlib.animation as animation


fig = plt.figure()
#creating a subplot 
ax1 = fig.add_subplot(1,1,1)


def animate(i):
    data = open('stock.txt','r').read()
    lines = data.split('\n')
    xs = []
    ys = []
    print(toto)
   
    for line in lines:
        x, y = line.split(',') # Delimiter is comma    
        xs.append(float(x))
        ys.append(float(y))
   
    
    ax1.clear()
    ax1.plot(xs, ys)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Live graph with matplotlib')	
	
    
ani = animation.FuncAnimation(fig, animate, interval=1000) 
plt.show()













# from matplotlib.animation import FuncAnimation
# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np


# labels = [
#     ['Group1', 'Group2', 'Group3', 'Group4', 'Group5'],
#     ['GroupA', 'GroupB', 'GroupC', 'GroupD', 'GroupE']
# ]
# men_means = [20, 34, 30, 35, 27]
# women_means = [25, 32, 34, 20, 25]
# childreen_means = [11, 25, 25, 32, 34]

# fig, ax = plt.subplots()

# def autolabel(rects):
#         """Attach a text label above each bar in *rects*, displaying its height."""
#         for rect in rects:
#             height = rect.get_height()
#             ax.annotate('{}'.format(height),
#                         xy=(rect.get_x() + rect.get_width() / 2, height),
#                         xytext=(0, 3),  # 3 points vertical offset
#                         textcoords="offset points",
#                         ha='center', va='bottom')

# def graph():

#     x = np.arange(len(labels[0]))  # the label locations
#     width = 0.25  # the width of the bars

#     rects1 = ax.bar(x + 0.00 , men_means, width, label='Men')
#     rects2 = ax.bar(x + 0.25, women_means, width, label='Women')
#     rects3 = ax.bar(x + 0.50, childreen_means, width, label='Childreen')

#     # Add some text for labels, title and custom x-axis tick labels, etc.
#     ax.set_ylabel('Scores')
#     ax.set_title('Scores by group and gender')
#     ax.set_xticks(x+width)
#     ax.set_xticklabels(labels[0])
#     ax.legend()

#     autolabel(rects1)
#     autolabel(rects2)
#     autolabel(rects3)

#     fig.tight_layout()
#     return 

# # ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
# #                     init_func=init, blit=True)


# graph()

# plt.show()
