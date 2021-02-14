
import socket 
import pickle

sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
# fully qualified hostname 
fqdn_hostname = socket.getfqdn()
ip_address = socket.gethostbyname(hostname)
port = 33332
print("server working on %s (%s) with %s" % (hostname, fqdn_hostname, ip_address))
server_sckt = (ip_address, port)
print ('starting up on %s port %s' % server_sckt)
sckt.bind(server_sckt)
sckt.listen(1)

promotions_count_list = []

# while True:
print('waiting for a connection')
connection, client_address = sckt.accept()
try:
    # show who connected to us
    print('connection from', client_address)
    # receive the data in small chunks and print it
    while True:
        data = connection.recv(1024)
        if data:
            # output received data
            print("Data: %s" % pickle.loads(data))
            promotions_count_list.extend(data)
            # je dois écrire une fonction   
        else:
            # no more data -- quit the loop
            print ("no more data.")
            break
finally:
    # Clean up the connection
    connection.close()
    