import re
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import animation
# uncomment if using in jupyter notebook
# %matplotlib nbagg 

def read_log(path, index, separator=chr(9)):
    data = []
    my_file = open(path,"r+")
    rows = my_file.readlines()
    for row in rows:
        line = re.sub(r'\r\n|\r|\n','',row, flags=re.M)
        if line != '':
            data.append(line.split(separator)[index])
    my_file.close()
    return Counter(data)

fig = plt.figure()
ax = fig.add_subplot()
counter_data = read_log(r'tmp.csv',2)
plt.title('This is a title')
bar = ax.bar(range(len(counter_data)), list(counter_data.values()), align='center')
plt.xticks(range(len(counter_data)), list(counter_data.keys()))
plt.tight_layout()
plt.ylim((0, 30))

def animate(val, counter_data):
    data = list(counter_data.values())
    for i in range(len(data)):
        bar[i].set_height(data[i]+val)

animation.FuncAnimation(fig, func=animate, frames=20, fargs=[counter_data], save_count=10)