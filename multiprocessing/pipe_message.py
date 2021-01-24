# -*- coding: utf-8 -*-
# @Date    : 2021-01-16 18:21:29
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 管道通信
# @Version : $Id$

import os
from multiprocessing import Process, Pipe


def fun1(conn):
    while True:
        try:
            #如果conn2 conn.close()
            message = conn.recv()
            print(message)
        except Exception as e:
            print(e)
            break

def fun2(conn):
    for i in range(0, 5):
        message = "你好，我是fun2"
        conn.send(message)

    #conn.close()
    return 

if __name__ == '__main__':
    #创建管道
    conn1, conn2 = Pipe()
    p1 = Process(target=fun1, args=(conn1,))
    p1.start()    
    p2 = Process(target=fun2, args=(conn2,))
    p2.start()
    conn2.close()

    p1.join()
    p2.join()
    print("main")