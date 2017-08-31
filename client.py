#!/usr/bin/python3
# coding: utf-8


import os
import socket
import sys
import time

import zmq
import pickle
import click

# include <czmq.h>

PING_MSG_SIZE = 1024


def test_debit(address,port):
    info = socket.getaddrinfo(address, port, socket.AF_UNSPEC, socket.SOCK_DGRAM, 0,
                              socket.AI_PASSIVE)
    print(info)
    # Create UDP socket
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Ask operating system to let us do broadcasts from socket
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)

    # Bind UDP socket to local port so we can receive pings
    sock.bind(info[0][4])

    t, addrinfo = sock.recvfrom(PING_MSG_SIZE)
    sock.sendto(b"OK", addrinfo)
    mss = pickle.loads(t)
    num = mss[0]
    size = mss[1]
    if mss[4] == 1:
        for j in range(1,mss[2]+1):
            print("test {} starts.".format(j))
            for i in range(num):
                try:
                    msg, addrinfo = sock.recvfrom(mss[1])
                    sock.sendto(b"OK", addrinfo)
                except KeyboardInterrupt:
                    print("interrupted")
                    return
            num = num + mss[3]
            print("test {} finished.".format(j))
    elif mss[4] == 2:
        for j in range(1,mss[2]+1):
            print("test {} starts.".format(j))
            for i in range(num):
                try:
                    msg, addrinfo = sock.recvfrom(size)
                    sock.sendto(b"OK", addrinfo)
                except KeyboardInterrupt:
                    print("interrupted")
                    return
            size = size + mss[3]
            print("test {} finished.".format(j))

    print("tests all finished.")

@click.command()
@click.option('--address', default='fe80::58f1:ff:fe00:7%nstack')
@click.option('--port', default=10002, type=int)
def main(address,port):
    test_debit(address,port)

if __name__ == '__main__':
    main()


