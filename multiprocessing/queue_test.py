# -*- coding: utf-8 -*-
# @Date    : 2021-01-16 09:41:27
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : queue 多进程通信
# @Version : $Id$

import os
from multiprocessing import Process, Queue
from queue import Empty, Full
import random
import time

#goods = 1000

def producer(name, queue):
    print(name)
    while True:
        new_good = random.randint(1, 10)
        if not queue.full():
            queue.put(new_good)
            print("%s生产了%s个产品"%(name, new_good))
        else:
            break
        time.sleep(1)
    print("%s生产满了"%name)
    return

def consumer(name, queue):
    print(name)
    while True:
        if not queue.empty():
            good = queue.get()
            print("%s消费了%s个产品"%(name, good))
        else:
            break
        time.sleep(1)
    print("%s没有商品消费了"%name)
    return

if __name__ == '__main__':

    q = Queue(10)

    #两个生产产品，苦工1号，苦工2号
    kg_1 = Process(target=producer, args=('kg_1', q))
    kg_2 = Process(target=producer, args=('kg_2', q))

    #kg_1.start()
    #kg_2.start()
    #3个消费者，美美，香香，如花
    p_mm = Process(target=consumer, args=('mm', q))
    p_xx = Process(target=consumer, args=('xx', q))
    p_rh = Process(target=consumer, args=('rh', q))

    kg_1.start()
    kg_2.start()
    p_mm.start()
    p_xx.start()
    p_rh.start()
    print("begin test")
