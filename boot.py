#! /usr/bin/python3
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
   
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('realme narzo 20A', '579f15d38462')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())



import esp
esp.osdebug(None)

import gc
gc.collect()

do_connect()
