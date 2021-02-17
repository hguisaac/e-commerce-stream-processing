import socket
import pickle
from time import sleep
from random import choice
# create a client socket
sckt = None
def create_client_sckt(sckt_socket=("127.0.1.1",33332)):
    # global sckt
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.connect(sckt_socket)
    return sckt

# sckt = create_client_sckt()
# data = "hello server!"
# sckt.send(data.encode())

win1 = [["10:23:30-10:25:30", "promo_0", 11],["10:23:30-10:25:30", "promo_A", 7],["10:23:30-10:25:30", "promo_B", 10]]
win2 = [["10:25:30-10:27:30", "promo_0", 11],["10:25:30-10:27:30", "promo_A", 7],["10:25:30-10:27:30", "promo_B", 10]]
win3 = [["10:27:30-10:29:30", "promo_0", 11],["10:27:30-10:29:30", "promo_A", 7],["10:27:30-10:29:30", "promo_B", 10]]



def send_data(data:list):
    global sckt
    if sckt == None:
        sckt = create_client_sckt()
    serialized_data = pickle.dumps(data)
    sckt.send(serialized_data)
while True:
    l = choice([win1, win2, win3])
    send_data(l)
#     data = pickle.dumps(l)
#     sckt.send(data)
    sleep(4)

# receive data from server
# data_from_server = sckt.recv(1024000);
# print(data_from_server.decode());

