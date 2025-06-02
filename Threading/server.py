#!/usr/bin/python3

import socket
import threading

def send_msg():
    while True:
        msg = input().encode()
        client.send(msg)

def recv_msg():
    while True:
        recieved = client.recv(1024)
        print(recieved.decode())


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 8888))
print("Listening....")
s.listen(1)
client,addr = s.accept()
print("Connected...")

t1 = threading.Thread(target=send_msg)
t1.start()
recv_msg() # To make it busy

