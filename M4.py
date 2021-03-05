import numpy as np
import matplotlib.pyplot as plt
from random import shuffle, randint
from time import sleep
from collections import deque
from helper import G,M, W, METRICS_SOCKETS
from utils import autolabel

import socket 
import pickle


# bind each promotion (promo_[0,A,B]) to each bar
# bind each count to the appropriate bar height

BAR_WIDTH = 0.7
BARS_COLOR = ["#64B5F6", "#ef9a9a", "#00796B"]

# we use the term window for grouped bar to contextualize
# this "window" is different from the one provided by pyplot

# number of windows
N_GROUPED_BARS = 4



def animate():

    aid_list = []
    bad_list = []
    good_list = []
    neutral_list = []
    humour_list_names = ["bad_list", "good_list", "neutral_list"]
    count_list = []

    # BEGIN SOCKET_INIT
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    # fully qualified domain name 
    fqdn = socket.getfqdn()
    ip_address = socket.gethostbyname(hostname)
    port = METRICS_SOCKETS["metric4"]["port"]
    print(f"server working on {hostname} {fqdn} with {ip_address}")
    server_sckt = (ip_address, port)
    print(f"starting up on {server_sckt[0]} port {server_sckt[1]}")
    sckt.bind(server_sckt)
    sckt.listen(1)
    
    print("waiting for a connection")
    # END SOCKET_INIT
    
    # we initialize the dataset that we gonna plot

    try:
        # show who connected to us
        connection, client_address = sckt.accept()
        print("connection from", client_address)

        while True:
            # listening to incomming data through socket connection
            # and integrate them to the graph in realtime
            data = connection.recv(1024)

            if data:
                # output received data
                unserialised_data = pickle.loads(data)
                # print("received:", unserialised_data)
                humour_list_as_string = unserialised_data[1].lower() + "_list"
                try:
                    i = aid_list.index(unserialised_data[2])
                    humour_list = eval(humour_list_as_string)
                    humour_list[i] = unserialised_data[3]
                except Exception as exception:
                    aid_list.append(unserialised_data[2])
                    j = humour_list_names.index(humour_list_as_string)
                    eval(humour_list_names[j]).append(unserialised_data[3])
                    tmp_list = humour_list_names[:j]
                    tmp_list.extend(humour_list_names[j+1:])
                    for __, hl in enumerate(tmp_list):
                        eval(hl).append(0)
                finally:
                    assert len(aid_list) == len(bad_list) 
                    assert len(aid_list) == len(good_list) 
                    assert len(aid_list) == len(neutral_list)
                    count_list = [sum(count) for count in zip(good_list, bad_list, neutral_list)]
                    print("aid_list:", M, aid_list, W)
                    print("bad_list:", M, bad_list, W)
                    print("good_list:", M, good_list, W)
                    print("neutral_list:", M, neutral_list, W)
                    
                    totals = [i+j+k for i,j,k in zip(bad_list, good_list, neutral_list)]
                    good_bar = [i / j * 100 for i,j in zip(good_list, totals)]
                    bad_bar = [i / j * 100 for i,j in zip(bad_list, totals)]
                    neutral_bar = [i / j * 100 for i,j in zip(neutral_list, totals)]
                    count_bar = [0.5 for i in range(len(aid_list))]
                    

                    good_rect = plt.bar(aid_list, good_bar, color=BARS_COLOR[2], edgecolor='white', width=BAR_WIDTH, label="Good comment %")
                    bad_rect = plt.bar(aid_list, bad_bar, bottom=good_bar, color=BARS_COLOR[1], edgecolor='white', width=BAR_WIDTH, label="Bad comment %")
                    neutral_rect = plt.bar(aid_list, neutral_bar, bottom=[i+j for i,j in zip(good_bar, bad_bar)], color=BARS_COLOR[0], edgecolor='white', width=BAR_WIDTH, label="Neutral comment %")
                    count_rect = plt.bar(aid_list, count_bar, bottom=[i+j+k for i,j,k in zip(good_bar, bad_bar, neutral_bar)], color='black', edgecolor='white', width=BAR_WIDTH)

                    autolabel(plt, count_rect, count_list)
                    plt.xticks(aid_list)
                    plt.yticks(range(0,101,10))
                    plt.xlabel("Identifiants de articles")
                    plt.ylabel("Pourcentage humour")
                    plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3)
                    fig.canvas.draw()
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
fig = plt.figure(figsize=(20,20)) #figsize=(20,20)
win = fig.canvas.manager.window
win.after(10000, animate)
plt.show()

