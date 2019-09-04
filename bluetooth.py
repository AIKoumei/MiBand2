#!/usr/bin/env python
# coding=utf-8

from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr, dev.getValueText(9))
        elif isNewData:
            print("Received new data from", dev.addr)

def scan(timeout = 5):
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(timeout)

    result = []
    for dev in devices:
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        for (adtype, desc, value) in dev.getScanData():
            print("%s, %s = %s" % (adtype, desc, value))
        result.append({"name" : dev.getValueText(9), "mac": dev.addr})
            
    return result
