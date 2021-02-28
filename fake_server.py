import socket 
import pickle
from helper import G,M, W
import matplotlib.pyplot as plt


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


sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
# fully qualified hostname 
fqdn = socket.getfqdn()
ip_address = socket.gethostbyname(hostname)
port = 33334
print(f"server working on {hostname} {fqdn} with {ip_address}")
server_sckt = (ip_address, port)
print(f"starting up on {server_sckt[0]} port {server_sckt[1]}")
sckt.bind(server_sckt)
sckt.listen(1)

promotions_count_list = []
aid_list = []
bad_list = []
good_list = []
neutral_list = []
barWidth = 0.5
humour_list_names = ["bad_list", "good_list", "neutral_list"]

while True:
    print("waiting for a connection")
    # the following line is blocking instruction
    connection, client_address = sckt.accept()
    try:
        # show who connected to us
        print("connection from", client_address)
        
        # receive the data in small chunks and print it
        while True:
            data = connection.recv(1024)
            if data:
                # output received data
                unserialised_data = pickle.loads(data)
                print("data:", M, unserialised_data, W)
                promotions_count_list.extend(unserialised_data)
                # from here
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
                    print("aid_list:", M, aid_list, W)
                    print("bad_list:", M, bad_list, W)
                    print("good_list:", M, good_list, W)
                    print("neutral_list:", M, neutral_list, W)
                    # print(aid_list, bad_list, good_list, neutral_list)
                    totals = [i+j+k for i,j,k in zip(bad_list, good_list, neutral_list)]
                    good_bar = [i / j * 100 for i,j in zip(good_list, totals)]
                    bad_bar = [i / j * 100 for i,j in zip(bad_list, totals)]
                    neutral_bar = [i / j * 100 for i,j in zip(neutral_list, totals)]
                    
                    good_rect = plt.bar(aid_list, good_bar, color='#b5ffb9', edgecolor='white', width=barWidth, label="group C")
                    bad_rect = plt.bar(aid_list, bad_bar, bottom=good_bar, color='#f9bc86', edgecolor='white', width=barWidth, label="group C")
                    neutral_rect = plt.bar(aid_list, neutral_bar, bottom=[i+j for i,j in zip(good_bar, bad_bar)], color='#a3acff', edgecolor='white', width=barWidth, label="group C")

                    autolabel(good_rect)
                    autolabel(bad_rect)
                    autolabel(neutral_rect)

                    plt.xticks(aid_list)
                    plt.xlabel("group")
                    plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
                    plt.cla()
                    plt.show()
            else:
                # no more data -- quit the loop
                print("no more data.")
                break
    finally:
        # clean up the connection
        connection.close()
