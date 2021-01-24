# -*- coding: utf-8 -*-
# @Date    : 2021-01-24 17:28:31
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 线程池版本的爬虫下载唐诗三百首
# @Version : $Id$

import os
import threading
import concurrent.futures
from spider_shige import *
import queue
import time
import random

url_queue = queue.Queue()
shige_queue = queue.Queue(100)


def spider_shige(name):
    global url_queue
    global shige_queue
    while not url_queue.empty():
        url = url_queue.get()
        shige = get_shige_content(url)
        shige_queue.put(shige)
        print(f'thread{name}, claw,{url},{shige_queue.qsize()}\n')
        time.sleep(random.randint(1, 3))

def save_file(name):
    global shige_queue
    while not shige_queue.full():
        time.sleep(1)

    while 1:
        shige_d = shige_queue.get()
        save_shige(shige_d)
        title = shige_d[0] 
        print(f'save {title}\n')
        time.sleep(1)
        if shige_queue.empty() and url_queue.empty():
            break


def test1(name):

    count = 10
    while True:
        print(f'{name},{count}\n')
        time.sleep(2)
        count -=1
        if count < 1:
            break
    return name

def test2(name):

    count = 10
    while True:
        print(f'{name},{count}\n')
        time.sleep(1)
        count -=1
        if count < 1:
            break
    return name



if __name__ == '__main__':

    thread_list = []
    save_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for i in range(5):
            t = executor.submit(test1, f'thread_{i}')
            thread_list.append(t)
        

        for i in range(3):
            t = executor.submit(test2, f'save_{i}')
            save_list.append(t)

    for i in save_list:
        print(i.result())  
              
    for i in thread_list:
        print(i.result())
    # for i in save_list:
    #     print(i.result())  
