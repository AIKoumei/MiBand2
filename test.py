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
from lib.miband2 import * 
from lib.miband2.base import MiBand2

if __name__ == '__main__':
    result = bluetooth.scan()
    print("'[info] find devices:", result)

    miband2_device = None
    for device in result:
        if device["name"] == "MI Band 2":
            miband2_device = device
            break
    
    print("'[info] find MI Band 2:", miband2_device)

    if miband2_device == None:
        print("[info] no miband2 device found. exit.")
        pass 

    # connect to miband2
    band = MiBand2(miband2_device["mac"], debug=True)
    band.setSecurityLevel(level="medium")

    if not band.authenticate():
        if band.initialize():
            print("[info] init OK")
        else:
            print("[info] init failed. exit.")
            pass 

        
    band.disconnect()
