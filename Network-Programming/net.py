#!/usr/bin/python3

from scapy.all import *
from prettytable import PrettyTable
from mac_vendor_lookup import MacLookup
from argparse import ArgumentParser
from sys import exit, stderr, argv

class NetworkScanner:
    def __init__(self, hosts):
        # Loop through each host or network range
        for host in hosts:
            self.host = host
            self.alive = {}                # Dictionary to store alive hosts
            self.create_packet()           # Build ARP packet
            self.send_packet()             # Send and receive responses
            self.get_alive()               # Parse responses
            self.print_alive()             # Print results in table

    def create_packet(self):
        # Create Ethernet and ARP layers for broadcast
        layer1 = Ether(dst="ff:ff:ff:ff:ff:ff")
        layer2 = ARP(pdst=self.host)       # ARP packet targeting provided host/subnet
        self.packet = layer1 / layer2      # Combine layers into a single packet

    def send_packet(self):
        # Send the packet and wait for responses (timeout after 1 sec)
        answered, unanswered = srp(self.packet, timeout=1, verbose=False)
        if answered:
            self.answered = answered       # Store only answered responses
        else:
            print("No host is up!")
            sys.exit(1)

    def get_alive(self):
        # Extract IP and MAC from responses
        for sent, received in self.answered:
            self.alive[received.psrc] = received.hwsrc

    def print_alive(self):
        # Print results in a formatted table
        table = PrettyTable(["IP", "MAC", "VENDOR"])
        for ip, mac in self.alive.items():
            try:
                vendor = MacLookup().lookup(mac)  # Lookup vendor by MAC
                table.add_row([ip, mac, vendor])
            except:
                table.add_row([ip, mac, "Unknown"])
        print(table)

def get_args():
    parser = ArgumentParser(description="Network Scanner")
    parser.add_argument("--h", dest="hosts", nargs="+", help="Hosts to scan")  # Corrected 'add_arguement' to 'add_argument'
    args = parser.parse_args()

    # If no arguments provided, print help and exit
    if len(argv) == 1:
        parser.print_help(stderr)
        exit(1)
    return args.hosts

# Get targets from command-line and start scanning
hosts = get_args()
NetworkScanner(hosts)
