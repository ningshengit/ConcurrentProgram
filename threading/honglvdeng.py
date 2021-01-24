# -*- coding: utf-8 -*-
# @Date    : 2021-01-22 16:22:07
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 红绿灯？
# @Version : $Id$

import os
import threading
import time

def car(name, event):

    while True:
        if event.is_set():
            print(f'{name} is running\n')
            time.sleep(2)
        else:
            print(f'{name} is wait\n')     
            event.wait()

def bus(name, event):
    while True:
        if event.is_set():
            print(f'{name} is running\n')
            time.sleep(2)
        else:
            print(f'{name} is wait\n')     
            event.wait()

def ambulance(name):
    while True:
        time.sleep(3)
        print(f'{name}, is running\n')


if __name__ == '__main__':

    event = threading.Event()

    t = threading.Thread(target=car, args=('car', event))
    t.start()
    t = threading.Thread(target=bus, args=('bus', event))
    t.start()

    t = threading.Thread(target=ambulance, args=('ambulance',))
    t.start()
    while True:
        event.set()
        time.sleep(10)
        event.clear()
        print("等红绿灯\n")
        time.sleep(10)