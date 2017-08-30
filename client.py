#!/usr/bin/python3
# coding: utf-8


import os
import socket
import sys
import time

import zmq

#include <czmq.h>
PING_PORT_NUMBER = 10002
PING_MSG_SIZE    = 10
PING_INTERVAL    = 1  # Once per second

def main():
    print(socket.getaddrinfo('fe80::58f1:ff:fe00:7%nstack', 10002, socket.AF_UNSPEC, socket.SOCK_DGRAM, 0, socket.AI_PASSIVE))
    # Create UDP socket
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Ask operating system to let us do broadcasts from socket
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)

    # Bind UDP socket to local port so we can receive pings
    sock.bind(('fe80::58f1:ff:fe00:7%nstack', 10002,0,5))

    # main ping loop
    # We use zmq_poll to wait for activity on the UDP socket, since
    # this function works on non-0MQ file handles. We send a beacon
    # once a second, and we collect and report beacons that come in
    # from other nodes:

    poller = zmq.Poller()
    poller.register(sock, zmq.POLLIN)

    # Send first ping right away
    ping_at = time.time()

    while True:
        timeout = ping_at - time.time()
        if timeout < 0:
            timeout = 0
        try:
            events = dict(poller.poll(1000* timeout))
        except KeyboardInterrupt:
            print("interrupted")
            break

        # Someone answered our ping
        if sock.fileno() in events:
            msg, addrinfo = sock.recvfrom(PING_MSG_SIZE)
            print("Found peer %s:%d" % addrinfo)


if __name__ == '__main__':
    main()
