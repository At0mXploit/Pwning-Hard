#!/usr/bin/python3

from argparse import ArgumentParser,FileType
from threading import Thread
from requests import get,exceptions
from time import time

subdomains = []

def prepare_args():
    """Prepare Arguments

        return:
        args(argparse)
    """
    parser = ArgumentParser(description="Python Subdomain Finder",usage="%(prog)s google.com",epilog="Example - %(prog)s -w /usr/share/wordlists/wordlist.txt -t 500 -V google.com")
    parser.add_argument(metavar="Domain",dest="domain",help="Domain Name")
    parser.add_argument("-w","--wordlist",dest="wordlist",metavar="",type=FileType("r"),help="wordlist of subdomains",default="wordlist.txt")
    parser.add_argument("-t","--threads",dest="threads",metavar="",type=int,help="threads to use",default=500)
    parser.add_argument("-V","--verbose",action="store_true",help="verbose output")
    parser.add_argument("-v","--version",action="version",help="print version",version="%(prog)s 1.0")
    args = parser.parse_args()
    return args

def prepare_words():
    """generator function for words
    """
    words = arguments.wordlist.read().split()
    for words in words:
        yield words 

def check_subdomain():
    """check subdomain for 200
    """
    while True:
        try:
            word = next(words)
            url = f"https://{word}.{arguments.domain}"
            request = get(url,timeout=5)
            if request.status_code == 200:
                subdomains.append(url)
                if arguments.verbose:
                        print(url)
        except(exceptions.ConnectionError,exceptions.ReadTimeout):
            continue
        except StopIteration:
            break

def prepare_threads():
    """create,start,join threads
    """
    thread_list = []
    for _ in range(arguments.threads):
        thread_list.append(Thread(target=check_subdomain))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == "__main__":
    arguments =  prepare_args()
    words = prepare_words()
    start_time = time()
    prepare_threads()
    end_time = time()
    print("\nSubdomains Found:\n" + "\n".join(subdomains))
    print(f"Time Taken - {round(end_time-start_time,2)}")
