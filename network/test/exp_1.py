#!/usr/bin/python

'Setting position of the nodes'
import os
import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference

def topology(args):

    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference, noise_th=-91, fading_cof=3)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g',
                             failMode="standalone", mac='00:00:00:00:00:01',
                             position='50,50,0')
    #net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8',
    #               position='40,40,0')
    #net.addStation('name_robo2', mac='00:00:00:00:00:03', ip='10.0.0.3/8',
    #               position='400,500,0')
    h1 = net.addHost('h1', ip='10.0.0.2/8')
    #c1 = net.addController('c1')

    #info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, h1)

    if '-p' not in args:
        net.plotGraph(max_x=100, max_y=100)

    info("*** Starting network\n")
    net.build()
    #c1.start()
    ap1.start([])

    info("*** Running CLI\n")
    CLI(net)
    os.system('sudo service network-manager start')
    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    os.system('sudo systemctl stop network-manager')
    setLogLevel('debug')
    topology(sys.argv)
