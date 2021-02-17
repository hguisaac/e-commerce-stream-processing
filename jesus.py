import numpy as np
import matplotlib.pyplot as plt
from random import shuffle, randint
from time import sleep
import pickle
import socket



bar_width = 0.25

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

# Set position of bar on X axis
bar1_x_pos = np.arange(5)
bar2_x_pos = [x + bar_width for x in bar1_x_pos]
bar3_x_pos = [x + bar_width for x in bar2_x_pos]

isset_legend = False

def get_plotted():
    global isset_legend
    global bars1, bars2, bars3
    x_tick_labels = ['14:11-14:11', 'B', 'C', 'D', 'E']

    # BEGIN SOCKET_INIT
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    # fully qualified domain name 
    fqdn = socket.getfqdn()
    ip_address = socket.gethostbyname(hostname)
    port = 33332
    print(f"server working on {hostname} {fqdn} with {ip_address}")
    server_sckt = (ip_address, port)
    print(f"starting up on {server_sckt[0]} port {server_sckt[1]}")
    sckt.bind(server_sckt)
    sckt.listen(1)
    
    print("waiting for a connection")
    # END SOCKET_INIT

    try:
        pass
    exe
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

