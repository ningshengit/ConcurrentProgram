# -*- coding: utf-8 -*-
# @Date    : 2021-01-21 16:40:47
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : bad test threading
# @Version : $Id$

import os
import time, threading

# 假定这是你的银行存款:
balance = 0

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n, lock):
    lock.acquire()
    for i in range(2000000):
        change_it(n)
    lock.release()


if __name__ == '__main__':
    lock = threading.Lock()
    t1 = threading.Thread(target=run_thread, args=(5, lock))
    t2 = threading.Thread(target=run_thread, args=(5, lock))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)
