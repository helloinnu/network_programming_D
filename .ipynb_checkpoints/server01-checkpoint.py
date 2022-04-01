#import socket library

import socket

#declare variable

IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP,PORT)

#create socket with ip v4 and TCP
tcp_server_sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"[STARTING] starting server on IP {IP}:{PORT}")

#bind the socket ip and port
tcp_server_sock.bind(ADDR)

server.listen()
print("[LISTENING] listening connection from client...")

while True :
    client_socket,  address = server.accept()
    print(f"connection from {address} is connected")
    client_socket.send(bytes("Wellcome Client Socket", "utf-8"))