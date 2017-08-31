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
import click
import matplotlib.pyplot as plt

PAQUET = b"t"
PING_MSG_SIZE = 2


def plot_debit(x,y,name):
    fig,ax = plt.subplots()
    ax.plot(x,y)
    fig.savefig(name)


def get_debit(port_pc, destination, range, n_paquet, t_paquet, mode):
    loop = int((range[2]-range[0])/range[1])
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    soc.bind(('', port_pc))

    if mode == 'n':
        n_paquet = range[0]
        v=[]
        x=[]
        soc.sendto(pickle.dumps([n_paquet, t_paquet,loop]), destination)
        soc.recvfrom(PING_MSG_SIZE)

        while n_paquet < range[2]:
            print("Test starts: destination {d}, n_paquet {n}, t_paquet{t}.".format(d=destination,n=n_paquet,t=t_paquet))
            mss = PAQUET * t_paquet
            y = time.time()
            for j in range(n_paquet):
                try:
                    soc.sendto(mss, destination)
                    soc.recvfrom(PING_MSG_SIZE)
                except KeyboardInterrupt:
                    print("interrupted!!!")
                    return
            t = time.time()-y
            v.append(n_paquet * t_paquet / t)
            x.append(n_paquet)
            n_paquet=n_paquet+range[1]

            print("Nombre de paquet", n_paquet, ", taille de paquet", t_paquet, "octets, destination", destination)
            print("                                                   ------>", v, "O/s")

        plot_debit(x,v,'debit_n_paquet.PNG')

# Default arguments
MAIN_DEFAULTS = {
                 'object': [(('192.168.42.1', 10002),5556)],
                 'mode': 'h',
                 'range': [100,100,1000],
                 'n_paquet': 100,
                 't_paquet': 10
                 }

HELP_MSG = {
    'object': 'A list of udp port of Raspberry Pi and bind port of server itself. It decides we will test how '
              'many Raspberry Pi.The default object is {!r}.'.format(MAIN_DEFAULTS['object']),
    'mode': """Test mode. If 'h', nothing tests. If 'n', it will test debit with different number of package; If 't',
     it will test debit with different size of package; if 'r', it will test debit with different number of Raspberry. 
     The default mode  is {!r}.""".format(MAIN_DEFAULTS['mode']),
    'range': """A list includes valuer minimum, interval and valuer maximum of test variable. It's useful for 
    mode 'n' or 't'.The default range is is {!r}.""".format(MAIN_DEFAULTS['range']),
    'n_paquet': 'Number of package. The default n_paquet valuer is {!r}.'.format(MAIN_DEFAULTS['n_paquet']),
    't_paquet': 'Size of package. The default t_paquet valuer is {!r}.'.format(MAIN_DEFAULTS['t_paquet'])
}
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], max_content_width=120)


@click.command(help='This function is meant to test debit in different conditions.',
               context_settings=CONTEXT_SETTINGS)
@click.option('--object', default=MAIN_DEFAULTS['object'], help=HELP_MSG['object'])
@click.option('--mode', '-m', default=MAIN_DEFAULTS['mode'], type=click.Choice(['n', 't', 'r', 'h']),
              help=HELP_MSG['mode'])
@click.option('--range', default=MAIN_DEFAULTS['range'], help=HELP_MSG['range'])
@click.option('--n-paquet', default=MAIN_DEFAULTS['n_paquet'], help=HELP_MSG['n_paquet'])
@click.option('--t-paquet', default=MAIN_DEFAULTS['t_paquet'], help=HELP_MSG['t_paquet'])
def main(object,mode,range,n_paquet,t_paquet):
    if mode != 'h':
        # if len(object)!= 1:
        #    raise ValueError("We will suggest you test only one Raspberry in this mode!")
        if len(range) != 3:
            raise ValueError("Range valuer is confusing. See \n", HELP_MSG['range'])

        for dest in object:
            if len(dest) != 2:
                raise ValueError("Must give the two ports, See \n", HELP_MSG['object'])
            test = Process(target=get_debit, args=(dest[1], dest[0], range, n_paquet, t_paquet, mode))
            # test.daemon = True
            test.start()

if __name__ == '__main__':
    main()

