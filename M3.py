import numpy as np
import matplotlib.pyplot as plt
import socket 
import pickle
from random import shuffle, randint
from time import sleep
from collections import deque
from helper import AID_LIMIT, METRICS_SOCKETS


BAR_WIDTH = 0.8
BARS_COLOR = ["#64B5F6", "#ef9a9a", "#00796B"]


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

    isset_legend = False
    isset_bars_label = False
    # BEGIN SOCKET_INIT
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    # fully qualified domain name 
    fqdn = socket.getfqdn()
    ip_address = socket.gethostbyname(hostname)
    port = METRICS_SOCKETS["metric3"]["port"]
    print(f"server working on {hostname} {fqdn} with {ip_address}")
    sckt_addr = (ip_address, port)
    print(f"starting up on {sckt_addr[0]} port {sckt_addr[1]}")
    sckt.bind(sckt_addr)
    # one connection
    sckt.listen(1)
    
    print("waiting for a connection")
    # END SOCKET_INIT
    
    # we initialize the dataset that we gonna plot

    bookmark_list = []  
    aid_list = []

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
                aid = int(unserialised_data[1])

                try:
                    tmp_index = aid_list.index(aid)
                    bookmark_list[tmp_index] = unserialised_data[2]
                except Exception as exception:
                    aid_list.append(aid)
                    bookmark_list.append(unserialised_data[2])
                finally:
                    assert len(bookmark_list) == len(aid_list)
                    print(aid_list, bookmark_list)
                    plt.xlabel("Identifiant des articles")
                    plt.ylabel("Sauvegarde count")
                    plt.xticks(aid_list)
                    rect = plt.bar(aid_list, bookmark_list, width=0.8, color="#00796B", label="Sauvegarde count bar")
                    autolabel(rect)
                    plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3)
                    fig.canvas.draw()
                    sleep(10)
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
fig = plt.figure()
win = fig.canvas.manager.window
win.after(100, animate)
plt.show()

