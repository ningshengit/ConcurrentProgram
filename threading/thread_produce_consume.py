# -*- coding: utf-8 -*-
# @Date    : 2021-01-21 22:03:43
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 条件锁测试生产者，消费者
# @Version : $Id$

import os
import shutil
import time
import threading
import random
#产品数量
goods = 0

def producer(conn):
    global goods
    while True:
        with conn:
            good = random.randint(1,3)
            goods += good
            time.sleep(2)
            if goods > 10:
                print("产品太多\n")
                conn.notify()
                conn.wait()
        print(f'producer生产{good},总产品数量{goods}')
 
def comsume(conn):
    global goods
    while True:
        with conn:
            good = random.randint(0,3)
            goods -= good

            time.sleep(1)
            if goods < 1:
                print("产品不够\n")
                conn.notify()
                conn.wait()
        print(f'comsume 消费{good}，总goods{goods}\n')

if __name__ == '__main__':
    #条件变量
    conn = threading.Condition()
    t_p = threading.Thread(target=producer, args=(conn,))
    t_c = threading.Thread(target=comsume, args=(conn,))
    t_p.start()
    t_c.start()
    t_p.join()
    t_c.join()
