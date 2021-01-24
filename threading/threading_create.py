# -*- coding: utf-8 -*-
# @Date    : 2021-01-19 12:15:01
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 线程的创建1
# @Version : $Id$

import os
import threading
import time
import random
# def print_time(threadName, delay):

#     print ("%s: %s" % (threadName, time.ctime(time.time())))
#     time.sleep(delay)
    


# if __name__ == '__main__':
#     thread = threading.Thread(target=print_time, name='test', args=('test', 3,))
#     thread.start()
#     # 在调用start之后先打印当前线程信息
#     print(threading.enumerate())
#     thread.join()
# import threading
# import time

def print_time(threadName, delay):
    print ("%s: %s\n" % (threadName, time.ctime(time.time())))
    time.sleep(delay)

def print_time(threadName, delay):
    print ("%s: %s\n" % (threadName, time.ctime(time.time())))
    time.sleep(delay)
if __name__ == '__main__':

    start_time = time.time() * 1000
    thread1 = threading.Thread(target=print_time, name='Thread-1', args=('test1', 1,))
    thread2 = threading.Thread(target=print_time, name='Thread-2', args=('test2', 1,))
    #thread2.setDaemon()
    thread1.start()
    thread2.start()
    print(thread2.name)
    #print(thread2.isDaemon())
    #start_time = time.time() * 1000
    thread1.join()
    thread2.join()
    end_time = time.time() * 1000
    total_time = end_time - start_time
    print("sum total_time %.2f"%total_time)
    #print("main done")


# def sing():
#     """唱歌5秒钟"""
#     for i in range(2000):
#         print("-----正在唱菊花台-----\n")
#         time.sleep(1)

# def dance():
#     """跳舞5秒钟"""
#     for i in range(2000):
#         print("-----正在跳舞-----\n")
#         time.sleep(1)

# def guanz():
#     """鼓掌5秒钟"""
#     for i in range(2000):
#         print("-----正在鼓掌-----\n")
#         time.sleep(random.randint(1,3))

# def main():
#     t_ = []
#     for i in range(8):
#         t = threading.Thread(target=sing)
#         t_.append(t)
#         t.start()


#     for i in t_:
#         i.join()

# if __name__ == '__main__':
#     main()
