# -*- coding: utf-8 -*-
# @Date    : 2021-01-18 17:58:11
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 进程池实现server/client并发聊天
# @Version : $Id$

import os
from socket import *
from multiprocessing import Pool


def talk(conn):
    while 1: 
        try:
            from_client_msg = conn.recv(1024).decode('utf-8')
            if not from_client_msg:
                break
            print("进程(%s)来自客户端的消息:%s" %(os.getpid(), from_client_msg))
            conn.send(from_client_msg.encode('utf-8'))
        except:
            break
    conn.close()


if __name__ == '__main__':
    server = socket()
    ip_port = ("127.0.0.1", 8001)
    server.bind(ip_port)
    server.listen(5)
    pool = Pool(4) 
    try:
        while 1:  # 循环连接
            conn, addr = server.accept()
            pool.apply_async(talk, args=(conn,))  
        pool.close() 
        pool.join() 
        server.close()
    except KeyboardInterrupt:
        print('catch keyboardinterupterror')
        pid=os.getpid()
        os.popen('taskkill.exe /f /pid:%d'%pid)
    except Exception as e:
        print(e)
