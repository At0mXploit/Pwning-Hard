#!/usr/bin/python3

from argparse import ArgumentParser
import socket
from threading import Thread
from threading import Lock
from time import time

ports_lock = Lock()
open_ports = []


def prepare_args():
    """prepare arguments - Btw this is called docstring.

         return:
            args(argparse.Namespace)
    """
    parser = ArgumentParser(description="Python Port Scanner", usage="%(prog)s 192.168.1.2", epilog="Example - %(prog)s -s 20 -e 40000 -t 500 -V 192.168.1.2")
    parser.add_argument(metavar="IPv4",dest="ip",help="host to scan") # Positional Argument
    parser.add_argument("-s","--start",dest="start",metavar="\b",type=int,help="starting port",default=1)
    parser.add_argument("-e","--end",dest="end",metavar="\b",type=int,help="ending port",default=65535)  
    parser.add_argument("-t","--thread",dest="threads",metavar="\b",type=int,help="threads to use",default=500)
    parser.add_argument("-V","--verbose",dest="verbose",action="store_true",help="verbose output") # action puts default value to false
    parser.add_argument("-v","--version",action="version",version="%(prog)s 1.0",help="displays version")
    args = parser.parse_args()
    return args

def prepare_ports(start:int,end:int):
    """Generator - In Python, generators are a way to create iterators in a simple and efficient manner. They allow you to yield values one at a time as they're needed, rather than computing and storing them all at once like lists do.
     
    This is generator function for ports
        
        arguments:
            start(int) - starting port
            end(int) - ending port
    """
    for port in range(start,end+1):
        yield port  # yield gives one port at a time without running the whole loop at once, yield doesn't need return. Basically its storing our ports one at time like array.

def scan_port():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            with ports_lock:
                port = next(ports)  # safely get next port with lock
            s.connect((arguments.ip, port))
            open_ports.append(port)
            if arguments.verbose:
                print(f"\r{open_ports}", end="")
            s.close()  # close socket
        except (ConnectionRefusedError, socket.timeout):
            continue
        except StopIteration:
            break

def prepare_threads(threads:int):
    """create,starts,join,run threads

        arguments:
            threads(int) - Number of threads to use
    
    """

    thread_list = []
    for _ in range(threads+1): # Using _ instead of i in loop because its just fancy for me duck you if you are seeing this btw,
        thread_list.append(Thread(target=scan_port))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == "__main__": # Runs this block only if the script is executed directly, not when imported as a module

    arguments = prepare_args()
    ports = prepare_ports(arguments.start,arguments.end)
    start_time = time()
    prepare_threads(arguments.threads)
    end_time = time()
    if arguments.verbose:
        print()
    print(f"Open Ports Found - {open_ports}")
    print(f"Time Taken - {round(end_time-start_time,2)}")
