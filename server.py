#!/usr/bin/python3
# coding: utf-8

"""
For testing the debit of CPL. The part of time is referred to

http://www.culte.org/listes/linux-31/2007-10/msg00008.html

"""

import socket
import time
import pickle
from multiprocessing import Process

N_PAQUET = 100
PAQUET = b"t"
T_PAQUET = 10
DESTINATION = [(('192.168.42.1', 10002),5556)]
KO = 1024
PING_MSG_SIZE = 2


def get_debit(port_PC, destination):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    soc.bind(('', port_PC))

    mss = PAQUET * T_PAQUET
    soc.sendto(pickle.dumps([N_PAQUET, T_PAQUET]), destination)
    y = time.time()
    for j in range(N_PAQUET):
        soc.sendto(mss, destination)
        soc.recvfrom(PING_MSG_SIZE)
    t = time.time()-y
    v = N_PAQUET * T_PAQUET / t

    print("Nombre de paquet", N_PAQUET, ", taille de paquet", T_PAQUET, "octets, destination", destination)
    print("                                                   ------>", v, "O/s")


def main():
    processes = None
    for dest in DESTINATION:
        test = Process(target=get_debit, args=(dest[1], dest[0]))
        #test.daemon = True
        test.start()

if __name__ == '__main__':
    main()

