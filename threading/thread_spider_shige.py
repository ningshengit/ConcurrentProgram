# -*- coding: utf-8 -*-
# @Date    : 2021-01-23 21:35:49
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 多线程下载唐诗300首
# @Version : $Id$

import os
import threading
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
 
if __name__ == '__main__':


    for page in range(1, 17):
        url = base_url.format(page)
        result = get_shige_url(url)
        for url in result:
            url_queue.put(url)

    print(f"begin thread--,url len {url_queue.qsize()}\n")
    for i in range(1, 10):
        t = threading.Thread(target=spider_shige, args=(f'spider_{i}',))
        t.start()
    save_t = []
    time.sleep(25)
    print("begin save thread")
    for x in range(1, 5):
        t = threading.Thread(target=save_file, args=(f'save_{i}',))
        save_t.append(t)
        t.start()

    for t in save_t:
        t.join()

