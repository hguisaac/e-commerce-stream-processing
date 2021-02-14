import socket
import pickle
from time import sleep

# create a client socket
sckt = None
def create_client_sckt(sckt_socket=("127.0.1.1",33333)):
    # global sckt
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.connect(sckt_socket)
    return sckt

# sckt = create_client_sckt()
# data = "hello server!"
# sckt.send(data.encode())

def send_data(data:list):
    global sckt
    if sckt == None:
        sckt = create_client_sckt()
    serialized_data = pickle.dumps(data)
    sckt.send(serialized_data)
while True:
    l = [i for i in range(50)]
    send_data(l)
#     data = pickle.dumps(l)
#     sckt.send(data)
    sleep(2)

# receive data from server
# data_from_server = sckt.recv(1024000);
# print(data_from_server.decode());

