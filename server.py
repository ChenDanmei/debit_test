#!/usr/bin/python3
# coding: utf-8

"""
For testing the debit of CPL. The part of time is referred to

http://www.culte.org/listes/linux-31/2007-10/msg00008.html

"""

import socket
import time

N_PAQUET = 2560000
PAQUET = b"t"
T_PAQUET = 10
DESTINATION = ('192.168.42.1', 10002)
KO = 1024


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
        v=[]

        mss = PAQUET*T_PAQUET
        self.restart()
        for j in range(N_PAQUET):
            soc.sendto(mss, DESTINATION)
        t = self.get_value()
        v=N_PAQUET*T_PAQUET/(t*KO)

        print("Nombre de paquet",N_PAQUET, ", taille de paquet", T_PAQUET, "octets, destination", DESTINATION)
        print("                                                   ------>", v, "kO/s")

if __name__ == '__main__':
    server = handle()
    server.get_debit()
