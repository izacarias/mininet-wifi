#!/usr/bin/env python

'Example for WiFi Direct'

import sys
from time import sleep

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, WifiDirectLink
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


def topology(args):
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference,
                       configWiFiDirect=True)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', ip='10.0.0.1/8', position='10,10,0')
    sta2 = net.addStation('sta2', ip='10.0.0.2/8', position='20,20,0')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    if '-p' not in args:
        net.plotGraph(max_x=200, max_y=200)

    info("*** Starting WiFi Direct\n")
    net.addLink(sta1, intf='sta1-wlan0', cls=WifiDirectLink)
    net.addLink(sta2, intf='sta2-wlan0', cls=WifiDirectLink)

    info("*** Starting network\n")
    net.build()

    sta1.cmd('wpa_cli -ista1-wlan0 p2p_find')
    sta2.cmd('wpa_cli -ista2-wlan0 p2p_find')
    sta2.cmd('wpa_cli -ista2-wlan0 p2p_peers')
    sleep(3)
    sta1.cmd('wpa_cli -ista1-wlan0 p2p_peers')
    sleep(3)
    pin = sta1.cmd('wpa_cli -ista1-wlan0 p2p_connect %s pin auth'
                   % sta2.wintfs[0].mac)
    sleep(3)
    sta2.cmd('wpa_cli -ista2-wlan0 p2p_connect %s %s'
             % (sta1.wintfs[0].mac, pin))

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
