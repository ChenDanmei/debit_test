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


def plot_debit(x,y,name,title,xname):
    fig,ax = plt.subplots()
    ax.plot(x,y)
    fig.savefig(name)
    plt.title(title)
    plt.xlabel(xname, fontproperties='SimHei')
    plt.ylabel(u'debit (O/s)', fontproperties='SimHei')


def get_debit(port_pc, destination, limit, n_paquet, t_paquet, mode, name):
    loop = int((limit[2]-limit[0])/limit[1])
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    soc.bind(('', port_pc))

    if mode == 'n':
        n = limit[0]
        v=[]
        x=[]
        soc.sendto(pickle.dumps([n,t_paquet,loop,limit[1]]), destination)
        soc.recvfrom(PING_MSG_SIZE)

        for j in range(loop):
            print("Test starts: destination {d}, n_paquet {n}, t_paquet {t}.".format(d=destination,n=n,t=t_paquet))
            mss = PAQUET * t_paquet
            y = time.time()
            for i in range(n):
                try:
                    soc.sendto(mss, destination)
                    soc.recvfrom(PING_MSG_SIZE)
                except KeyboardInterrupt:
                    print("interrupted!!!")
                    return
            t = time.time()-y
            v.append(n * t_paquet / t)
            x.append(n)
            n=n+limit[1]

            print("Nombre de paquet", n_paquet, ", taille de paquet", t_paquet, "octets, destination", destination)
            print("                                                   ------>", v[j], "O/s")

        plot_debit(x,v,name,'debit with different n_paquet', u'n_paquet')

# Default arguments
MAIN_DEFAULTS = {
                 'object': [(('192.168.42.1', 10002),5556)],
                 'mode': 'h',
                 'limit': [100,100,1100],
                 'n_paquet': 100,
                 't_paquet': 10,
                 'name': 'debit.PNG'
                 }

HELP_MSG = {
    'object': 'A list of udp port of Raspberry Pi and bind port of server itself. It decides we will test how '
              'many Raspberry Pi.The default object is {!r}.'.format(MAIN_DEFAULTS['object']),
    'mode': """Test mode. If 'h', nothing tests. If 'n', it will test debit with different number of package; If 't',
     it will test debit with different size of package; if 'r', it will test debit with different number of Raspberry. 
     The default mode  is {!r}.""".format(MAIN_DEFAULTS['mode']),
    'limit': """A list includes valuer minimum, interval and valuer maximum of test variable. It's useful for 
    mode 'n' or 't'.The default limit is is {!r}.""".format(MAIN_DEFAULTS['limit']),
    'n_paquet': 'Number of package. The default n_paquet valuer is {!r}.'.format(MAIN_DEFAULTS['n_paquet']),
    't_paquet': 'Size of package. The default t_paquet valuer is {!r}.'.format(MAIN_DEFAULTS['t_paquet']),
    'name': 'Name of the image of test result. The default name is {!r}.'.format(MAIN_DEFAULTS['name']),
}
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], max_content_width=120)


@click.command(help='This function is meant to test debit in different conditions.',
               context_settings=CONTEXT_SETTINGS)
@click.option('--object', default=MAIN_DEFAULTS['object'], help=HELP_MSG['object'])
@click.option('--mode', '-m', default=MAIN_DEFAULTS['mode'], type=click.Choice(['n', 't', 'r', 'h']),
              help=HELP_MSG['mode'])
@click.option('--limit', default=MAIN_DEFAULTS['limit'], help=HELP_MSG['limit'])
@click.option('--n-paquet', default=MAIN_DEFAULTS['n_paquet'], help=HELP_MSG['n_paquet'])
@click.option('--t-paquet', default=MAIN_DEFAULTS['t_paquet'], help=HELP_MSG['t_paquet'])
@click.option('--name', default=MAIN_DEFAULTS['name'], help=HELP_MSG['name'])
def main(object,mode,limit,n_paquet,t_paquet,name):
    if mode != 'h':
        # if len(object)!= 1:
        #    raise ValueError("We will suggest you test only one Raspberry in this mode!")
        if len(limit) != 3:
            raise ValueError("Limit valuer is confusing. See \n", HELP_MSG['limit'])

        for dest in object:
            if len(dest) != 2:
                raise ValueError("Must give the two ports, See \n", HELP_MSG['object'])
            test = Process(target=get_debit, args=(dest[1], dest[0], limit, n_paquet, t_paquet, mode, name))
            # test.daemon = True
            test.start()

if __name__ == '__main__':
    main()

