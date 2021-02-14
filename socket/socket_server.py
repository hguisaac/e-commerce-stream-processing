
import socket 
import pickle

sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
# fully qualified hostname 
fqdn = socket.getfqdn()
ip_address = socket.gethostbyname(hostname)
port = 33333
print(f"server working on {hostname} {fqdn} with {ip_address}")
server_sckt = (ip_address, port)
print(f"starting up on {server_sckt[0]} port {server_sckt[1]}")
sckt.bind(server_sckt)
sckt.listen(1)

promotions_count_list = []

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
                print("data:", unserialised_data)
                promotions_count_list.extend(unserialised_data)
                # je dois écrire une fonction   
            else:
                # no more data -- quit the loop
                print ("no more data.")
                break
    finally:
        # clean up the connection
        connection.close()

    