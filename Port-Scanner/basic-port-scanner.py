#!/usr/bin/python3

import sys
import socket

# Check if at least 1 argument (IP address) is provided
if len(sys.argv) == 1:
    print(f"{sys.argv[0]} IP START(optional) END(optional)", file=sys.stderr)
    exit(1)

# Get the target IP from the command line argument
ip = sys.argv[1]

# Set default port scanning range
start = 1
end = 65525

# If custom start port is provided, override default
if len(sys.argv) >= 3:
    start = int(sys.argv[2])
    # If custom end port is provided, override default
    if len(sys.argv) >= 4:
        end = int(sys.argv[3])

# Function to check if a port is open
def check_port_status(port: int) -> bool: # -> is used to see what return value is in our case it is boolean
    try:
        # Create a TCP socket
        s = socket.socket()
        # Set timeout to 1 second for faster scanning
        s.settimeout(1)
        # Try to connect to the port
        s.connect((ip, port))
        s.close()  
        return True
    except (ConnectionRefusedError, socket.timeout):
        return False

# Iterate through the port range
for port in range(start, end):
    # Check if current port is open
    response = check_port_status(port)
    if response:
        print(f"Open Port Found [{port}]")

