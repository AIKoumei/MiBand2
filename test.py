#!/usr/bin/python3
# coding=utf-8

# 功能
# 1、连接后除非主动销毁否则保持连接
# 2、10秒检测连接心跳，否则尝试每10秒尝试重连
# 3、提供获取功能列表方法
# 4、提供发送单独功能 msg 方法
# 5、提供匹配、退出连接方法
# 6、提供扫描蓝牙设备方法


# import sys
# import time
# import argparse
# from datetime import datetime
# from base import MiBand2
# from constants import ALERT_TYPES


# parser = argparse.ArgumentParser()
# parser.add_argument('-s', '--standard',  action='store_true',help='Shows device information')
# parser.add_argument('-r', '--recorded',  action='store_true',help='Shows previews recorded data')
# parser.add_argument('-l', '--live',  action='store_true',help='Measures live heart rate')
# parser.add_argument('-i', '--init',  action='store_true',help='Initializes the device')
# parser.add_argument('-m', '--mac', required=True, help='Mac address of the device')
# parser.add_argument('-t', '--set_current_time', action='store_true',help='Set time')
# args = parser.parse_args()


# MAC = args.mac # sys.argv[1]

# band = MiBand2(MAC, debug=True)
# band.setSecurityLevel(level="medium")


# band.send_alert(ALERT_TYPES.NONE)
# time.sleep(3)
# band.send_alert(ALERT_TYPES.MESSAGE)

# band.disconnect()


# # 测试，异步IO
# import functools
# import asyncio
# import sys

# async def timeout(loop):
#     print('请在 3 秒内输入，否则结束程序。')
#     await asyncio.sleep(3)
#     loop.stop()

# def echo(loop):
#     print("您输入了: " + sys.stdin.readline(), end='')
#     loop.stop()

# loop = asyncio.get_event_loop()
# asyncio.ensure_future(timeout(loop))
# loop.add_reader(sys.stdin, functools.partial(echo, loop=loop))
# loop.run_forever()


import bluetooth
import time
from lib.miband2 import * 
from lib.miband2.base import MiBand2
from lib.miband2.constants import ALERT_TYPES
import struct

def main():
    result = bluetooth.scan()
    print("[info] find devices:", result)

    miband2_device = None
    for device in result:
        if device["name"] == "MI Band 2":
            miband2_device = device
            break
    
    print("[info] find MI Band 2:", miband2_device)

    if miband2_device == None:
        print("[info] no miband2 device found. exit.")
        pass 

    # connect to miband2
    band = MiBand2(miband2_device["mac"], debug=True)
    band.setSecurityLevel(level="medium")

    if not band.authenticate():
        print("[info] band authenticate now")
        if band.initialize():
            print("[info] init OK")
        else:
            print("[info] init failed. exit.")
            pass 
    else:
        print("[info] band had authenticated")

    print("[info] test connection")
    time.sleep(3)
    band.send_alert(ALERT_TYPES.NONE)

    time.sleep(3)
    print ('[info] Soft revision:',band.get_revision())
    print ('[info] Hardware revision:',band.get_hrdw_revision())
    print ('[info] Serial:',band.get_serial())
    print ('[info] Battery:', band.get_battery_info())
    print ('[info] Time:', band.get_current_time())
    print ('[info] Steps:', band.get_steps())
    print ('[info] Heart rate oneshot:', band.get_heart_rate_one_time())

        
    band.disconnect()

    
def getMiBand2():
    result = bluetooth.scan()
    print("[info] find devices:", result)

    miband2_device = None
    for device in result:
        if device["name"] == "MI Band 2":
            miband2_device = device
            break
    
    print("[info] find MI Band 2:", miband2_device)

    if miband2_device == None:
        print("[info] no miband2 device found. exit.")
        pass 

    # connect to miband2
    band = MiBand2(miband2_device["mac"], debug=True)
    band.setSecurityLevel(level="medium")

    if not band.authenticate():
        print("[info] band authenticate now")
        if band.initialize():
            print("[info] init OK")
        else:
            print("[info] init failed. exit.")
            pass 
    else:
        print("[info] band bad authenticated")

    print("[info] test connection")
    time.sleep(3)
    band.send_alert(ALERT_TYPES.MESSAGE)

    time.sleep(3)
    print ('[info] Soft revision:',band.get_revision())
    print ('[info] Hardware revision:',band.get_hrdw_revision())
    print ('[info] Serial:',band.get_serial())
    print ('[info] Battery:', band.get_battery_info())
    print ('[info] Time:', band.get_current_time())
    print ('[info] Steps:', band.get_steps())
    # print ('[info] Heart rate oneshot:', band.get_heart_rate_one_time())

    return band

    
def disconnect(band):
    if band == None:
        return
    print("[info] disconnected")
    band.disconnect()

    
def alert(band, _type):
    if band == None or _type == None:
        return
    band.send_alert(_type)

    
def testType(band):
    if band == None:
        return
    msg_list = [struct.pack('B', x) for x in range(16*16)]
    alert(band, ALERT_TYPES.NONE)
    for msg in msg_list:
        print("test msg: ", struct.unpack('B', msg))
        alert(band, msg)
        time.sleep(0.5)
        alert(band, ALERT_TYPES.NONE)

    
def testUUIDSOne(band, type = UUIDS.CHARACTERISTIC_BATTERY):
    if band == None:
        return
    try:
        ch = p.getCharacteristics(uuid=uuid)[0]
        if (ch.supportsRead()):
            print(uuid + " : " + ch.read())

    
def testUUIDS(band):
    if band == None:
        return
    try:
        ch = p.getCharacteristics(uuid=uuid)[0]
        if (ch.supportsRead()):
            print(uuid + " : " + ch.read())
    time.sleep(0.2)


if __name__ == '__main__':
    main()


