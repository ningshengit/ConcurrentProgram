# -*- coding: utf-8 -*-
# @Date    : 2021-01-17 15:43:00
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 使用Lock体会多进程同步
# @Version : $Id$

# import os
# import time
# import random
# from multiprocessing import Process, Lock


# def work(n, lock):
#     #while True:
#     lock.acquire()
#     print('{} : {} is running'.format(n, os.getpid()))
#     time.sleep(random.random())
#     print('{} : {} is done'.format(n, os.getpid()))
#     lock.release()

# if __name__ == '__main__':
#     lock = Lock()
#     for i in range(3):
#         p = Process(target=work, args=(i, lock))  
#         p.start()


from multiprocessing import Process, Value, Array
def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]
    print('f',n.value)
    for i in range(len(a)):
        print(a[i])
def f1(n, a):
    n.value = 3.14
    for i in range(len(a)):
        a[i] = -a[i]
    print('f1',n.value)
    for i in range(len(a)):
        print(a[i])
if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))
    p = Process(target=f, args=(num, arr))
    p2 = Process(target=f1, args=(num, arr))
    p.start()
    p2.start()
    #@p.join()
    print(num.value)
    print(arr[:])
