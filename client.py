#!/usr/bin/python3
# coding: utf-8


import os
import socket
import sys
import time

import zmq
import pickle

# include <czmq.h>
PING_PORT_NUMBER = 10002
PING_MSG_SIZE = 1024


def main():
    info = socket.getaddrinfo('fe80::58f1:ff:fe00:7%nstack', 10002, socket.AF_UNSPEC, socket.SOCK_DGRAM, 0,
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
    for j in range(mss[2]):
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

    print("tests all finished.")


if __name__ == '__main__':
    main()


