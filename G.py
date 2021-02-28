import numpy as np
import matplotlib.pyplot as plt
from random import shuffle, randint
from time import sleep
from collections import deque
import socket 
import pickle


# bind each promotion (promo_[0,A,B]) to each bar
# bind each count to the appropriate bar height

BAR_WIDTH = 0.25
BARS_COLOR = ["#64B5F6", "#ef9a9a", "#00796B"]

# we use the term window for grouped bar to contextualize
# this "window" is different from the one provided by pyplot

# number of windows
N_GROUPED_BARS = 4

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

# set position of bar on x-axis
xbar1 = np.arange(N_GROUPED_BARS)
xbar2 = [x + BAR_WIDTH for x in xbar1]
xbar3 = [x + BAR_WIDTH for x in xbar2]

def animate():

    isset_legend = False
    isset_bars_label = False
    isset_data = False
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
    
    # we initialize the dataset that we gonna plot

    promotions_count_list = deque(
        [
            [
                ["hh:mm:ss-ħħ:µµ:ßß", "promo_0", 0],
                ["hh:mm:ss-ħħ:µµ:ßß", "promo_A", 0],
                ["hh:mm:ss-ħħ:µµ:ßß", "promo_B", 0]
            ]
        ]*N_GROUPED_BARS,
        maxlen=N_GROUPED_BARS
    ) 

    try:
        # show who connected to us
        connection, client_address = sckt.accept()
        print("connection from", client_address)

        while True:
            # listening to incomming data through socket connection
            # and integrate them to the graph in realtime
            data = connection.recv(1024)

            if data:
                bar1_heights = [promotions_count_list[nth_win][0][-1] for nth_win in range(N_GROUPED_BARS)]
                bar2_heights = [promotions_count_list[nth_win][1][-1] for nth_win in range(N_GROUPED_BARS)]
                bar3_heights = [promotions_count_list[nth_win][2][-1] for nth_win in range(N_GROUPED_BARS)]

                win_labels = [promotions_count_list[nth_win][0][0] for nth_win in range(N_GROUPED_BARS)]

                if isset_bars_label == False:
                    bar_labels = [promotions_count_list[nth_win][0][0] for nth_win in range(N_GROUPED_BARS)]
                
                # output received data
                unserialised_data = pickle.loads(data)
                print("data:", unserialised_data)
                promotions_count_list.append(unserialised_data)            

                rects1 = plt.bar(xbar1, bar1_heights, color=BARS_COLOR[0], width=BAR_WIDTH, edgecolor='white', label='Promo_0')
                rects2 = plt.bar(xbar2, bar2_heights, color=BARS_COLOR[1], width=BAR_WIDTH, edgecolor='white', label='Promo_A')
                rects3 = plt.bar(xbar3, bar3_heights, color=BARS_COLOR[2], width=BAR_WIDTH, edgecolor='white', label='Promo_B')
                
                if isset_data == False:
                    isset_data = True
                else:
                    autolabel(rects1)
                    autolabel(rects2)
                    autolabel(rects3)


                plt.xlabel("Fenêtres de Traitements", fontweight="bold")
                plt.ylabel("Nombres d'Achats", fontweight="bold")

                # if isset_legend == False:
                plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3)
                # isset_legend = True

                plt.xticks([r + BAR_WIDTH for r in range(N_GROUPED_BARS)], win_labels)

                fig.canvas.draw()
                sleep(1)
                plt.cla()
            else:
                # no more data -- quit the loop
                print ("no more data.")
                # break
    finally:
        # clean up the connection
        # connection.close()
        pass
    

# make the plot
fig = plt.figure(figsize=(20,20))
win = fig.canvas.manager.window
win.after(100, animate)
plt.show()

