#!/usr/bin/python3
# coding: utf-8

"""
For testing the debit of CPL. The part of time is referred to

http://www.culte.org/listes/linux-31/2007-10/msg00008.html

"""

import socket
import time
import pickle

N_PAQUET = 500
PAQUET = b"t"
T_PAQUET = 10
DESTINATION = ('192.168.42.1', 10002)
KO = 1024
PING_MSG_SIZE = 2



class handle():
    def __init__(self):
        y = (1970, 1, 1, 1, 0, 0, 0, 0, 0)
        self.y = time.mktime(y)

    def restart(self):
        self.y = time.time()

    def get_value(self):
        x = time.time()

        resultat = x - self.y
        return resultat

    def get_debit(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        soc.bind(('', 5556))

        mss = PAQUET*T_PAQUET
        soc.sendto(pickle.dumps([N_PAQUET, T_PAQUET]), DESTINATION)
        self.restart()
        for j in range(N_PAQUET):
            soc.sendto(mss, DESTINATION)
            soc.recvfrom(PING_MSG_SIZE)
        t = self.get_value()
        v=N_PAQUET*T_PAQUET/t

        print("Nombre de paquet",N_PAQUET, ", taille de paquet", T_PAQUET, "octets, destination", DESTINATION)
        print("                                                   ------>", v, "O/s")

if __name__ == '__main__':
    server = handle()
    server.get_debit()
