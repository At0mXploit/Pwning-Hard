#!/usr/bin/python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1 ) # Allow the socket to reuse the address (prevents "address already in use" error when restarting) and 1 just means enable, 0 means disable
s.bind(("127.0.0.1", 8888)) 
print("Listening...")
s.listen(1)

client,addr = s.accept()
print("Connected")

while True:
    cmd = input("$ ")
    client.send(cmd.encode()) # Converts string to byte
    
    if cmd == "exit":
        break

    output = (client.recv(1024).decode())
    print(output)

client.close()
s.close()
