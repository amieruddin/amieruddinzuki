import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_name = '192.168.250.20'
server_address = (server_name, 9100)
print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)



print(sys.stderr, 'waiting for a connection')
try:
    connection, client_address = sock.accept()
    print('connection establish')
except:
    print('connection not establish')


try:
    while True:
        data = connection.recv(1024)

        if data:
            print(data)
except:
    pass
finally:
    sock.close()
    print('PCL disconnected')



    