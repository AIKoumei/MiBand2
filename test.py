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
import sys
import time
from lib.miband2 import * 
from lib.miband2.base import MiBand2
from lib.miband2.constants import ALERT_TYPES
from lib.miband2.constants import UUIDS
import struct
import threading
import asyncio
from tqdm import tqdm


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

    # time.sleep(3)
    # print ('[info] Soft revision:',band.get_revision())
    # print ('[info] Hardware revision:',band.get_hrdw_revision())
    # print ('[info] Serial:',band.get_serial())
    # print ('[info] Battery:', band.get_battery_info())
    # print ('[info] Time:', band.get_current_time())
    # print ('[info] Steps:', band.get_steps())

    testServiceSimpleAsync(band)
    
    band.disconnect()

    
def getMiBand2(timeout = 5):
    result = bluetooth.scan(timeout)
    print("[info] find devices:", result)

    miband2_device = None
    for device in result:
        if device["name"] == "MI Band 2":
            miband2_device = device
            break
    
    print("[info] find MI Band 2:", miband2_device)

    if miband2_device == None:
        print("[info] no miband2 device found. exit.")
        return 

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
    band.send_alert(ALERT_TYPES.MESSAGE)

    time.sleep(3)
    print ('[info] Soft revision:',band.get_revision())
    print ('[info] Hardware revision:',band.get_hrdw_revision())
    print ('[info] Serial:',band.get_serial())
    print ('[info] Battery:', band.get_battery_info())
    print ('[info] Time:', band.get_current_time())
    print ('[info] Steps:', band.get_steps())

    return band

    
def disconnect(band):
    if band == None:
        return
    print("[info] disconnected")
    band.disconnect()

    
def find_band(band):
    if band == None:
        return
    band.send_alert(ALERT_TYPES.FIND_DEVICE)

    
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

    
def testUUIDSOne(band, uuid = UUIDS.CHARACTERISTIC_BATTERY):
    if band == None:
        return
    try:
        print("test one uuid : " + uuid)
        ch = band.getCharacteristics(uuid = uuid)[0]
        data = ch.read()
        print("test one uuid : " + uuid + " : " + data)
        if (ch.supportsRead()):
            print("test one uuid supportsRead : " + uuid + " : " + data)
        return data
    except :
        pass


def testServiceOne(band, uuid = UUIDS.SERVICE_MIBAND1):
    if band == None:
        return
    try:
        service = band.getServiceByUUID(uuid)
        print("service found : " + uuid)
        print("service : ", service)
        return uuid, service
    except :
        return None, None


@asyncio.coroutine
def testServiceOneAsync(band, uuid = UUIDS.SERVICE_MIBAND1, file = None, bar = None):
    if band == None:
        return

    # print("test uuid : "+ uuid)
    if file :
        file.write("test uuid : " + uuid +'\n')

    try:
        service = yield from band.getServiceByUUID(uuid)
        # print("service found : " + uuid)
        # print("service : ", service)
        if file :
            file.write({'uuid' : uuid, 'service' : service,} + '\n')
        return 
    except :
        # print("no service with uuid : " + uuid)
        pass
    finally:
        if bar :
            bar.update(1)
    return uuid, service


progress_bar = None
def testServiceSimpleAsync(band):
    if band == None:
        return
        
    file = open('testServiceSimple.log', 'w', encoding='utf8')
    # 写入文件内容

    base = UUIDS.BASE
    _uuid= None

    loop = asyncio.get_event_loop()
    tasks = []

    # progress bar
    make_progress_bar = tqdm(total=(16**4-1 + (16**30-1)), unit_scale=True, position=1)
    progress_bar = tqdm(total=(16**4-1 + (16**30-1)), unit_scale=True, position=2)
    
    # make tasks
    for i in range(16**4 - 1):
        _uuid = base % "{:0>4s}".format(str(hex(i))[2:])[-4:]
        tasks.append(testServiceOneAsync(band, _uuid, file))
        make_progress_bar.update(1)
        # print("task uuid : " + _uuid)
        
    for i in range(16**8 - 1):
        a = "{:0>8s}".format(str(hex(i))[2:])[-8:]
        for i in range(16**4 - 1):
            b = "{:0>4s}".format(str(hex(i))[2:])[-4:]
            for i in range(16**4 - 1):
                c = "{:0>4s}".format(str(hex(i))[2:])[-4:]
                for i in range(16**4 - 1):
                    d = "{:0>4s}".format(str(hex(i))[2:])[-4:]
                    for i in range(16**12 - 1):
                        e = "{:0>12s}".format(str(hex(i))[2:])[-12:]
                        _uuid = "%s-%s-%s-%s-%s" % (a, b, c, d, e)
                        # print("task uuid : " + _uuid)
                        make_progress_bar.update(1)
                        tasks.append(testServiceOneAsync(band, _uuid, file = file, bar = progress_bar))
    print("task len : " + str(len(tasks)))

    # run
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    # close file
    file.close()
    progress_bar.close()
    # return loop, progress_bar

    
def testServiceSimple(band):
    if band == None:
        return
        
    file = open('testServiceSimple.log', 'w', encoding='utf8')
    # 写入文件内容

    base = UUIDS.BASE
    _uuid, uuid, service = None, None, None
    for i in range(16**4 - 1):
        _uuid = base % "{:0>4s}".format(str(hex(i))[2:])[-4:]
        print("test uuid : "+ _uuid)
        uuid, service = testServiceOne(band, _uuid)
        if uuid == None :
            pass
        d = {
            'uuid' : uuid,
            'service' : service,
        }
        file.write(d + '\n')
    
    for i in range(16**8 - 1):
        a = "{:0>8s}".format(str(hex(i))[2:])[-8:]
        for i in range(16**4 - 1):
            b = "{:0>4s}".format(str(hex(i))[2:])[-4:]
            for i in range(16**4 - 1):
                c = "{:0>4s}".format(str(hex(i))[2:])[-4:]
                for i in range(16**4 - 1):
                    d = "{:0>4s}".format(str(hex(i))[2:])[-4:]
                    for i in range(16**12 - 1):
                        e = "{:0>12s}".format(str(hex(i))[2:])[-12:]
                        _uuid = "%s-%s-%s-%s-%s" % (a, b, c, d, e)
                        print("test uuid : " + _uuid)
                        uuid, service = testServiceOne(band, _uuid)
                        if uuid == None :
                            pass
                        d = {
                            'uuid' : uuid,
                            'service' : service,
                        }
                        file.write(d + '\n')

    # 关闭文件
    file.close()

    
def reimport():
    try :
        del sys.modules['test']
    except :
        pass


# #############################################################################
# # async test
# #############################################################################
@asyncio.coroutine
def async_test_gen():
    print('Hello world! (%s)' % threading.currentThread())
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())


def async_test():
    loop = asyncio.get_event_loop()
    tasks = [async_test_gen(), async_test_gen()]
    loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()

if __name__ == '__main__':
    main()


