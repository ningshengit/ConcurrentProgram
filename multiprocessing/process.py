# -*- coding: utf-8 -*-
# @Date    : 2021-01-14 20:27:55
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 
# @Version : $Id$

import os
from multiprocessing import Process
import time
import math
import random
from   multiprocessing  import  Pool

# def isprime(n):

#     if n < 2: 
#         return False
#     for i in range(2,int(math.sqrt(n))+1):
#         if n % i == 0:
#             return
#     print("%d is prime"%n)
#     return 

# def get_prime(*num_):
#     for num in num_:
#         isprime(num)

def sum(n):
    #start_time = time.time() * 1000
    add = 0
    for i in range(0, n):
        add += i
    print('0-%d, add is %d'%(n,add))
    #end_time = time.time() * 1000
    #total_time = end_time - start_time
    #print("pid:%s,multiprocessing sum total_time %.2f"%(os.getpid(),total_time))

def  func1(fn):
    time.sleep( 1 )
    print(os.getpid())
    return  fn  *  fn
 
if __name__ == '__main__':


    start_time = time.time() * 1000
    sum(100000000)
    sum(100000000)
    sum(100000000)
    end_time = time.time() * 1000
    total_time = end_time - start_time
    print("sum total_time %.2f"%total_time)

    start_time = time.time() * 1000
    p_obj = [] 
    for i in range(0, 8):
        p = Process(target=sum, args=(100000000, ))
        p.start()
        p_obj.append(p) 

    for obj in p_obj:
        obj.join()        
    end_time = time.time() * 1000
    total_time = end_time - start_time
    print("multiprocessing sum total_time %.2f"%total_time)

    # a  =  [ 1 , 2 , 3 , 4 , 5 , 6 ]
    # print("顺序执行的方式开始...")
    # s  =  time.time()
    # for  i  in  a:
    #     func1(i)
    # el  =  time.time()
    # print("顺序执行时间为:" , int (el  -  s))

    # print("创建多个进程，并行执行开始")
    # pool  =  Pool( 5 )  #创建拥有5个进程数量的进程池,也就是说可以同时跑5个线程
    # p1  =  pool.map (func1, a)
    # pool.close()  #关闭进程池，不再接受新的进程
    # pool.join()  #主进程阻塞等待子进程的退出
    # e3  =  time.time()
    # print("多进程并行时间为:" ,  int (e3  -  el))
 
    # print(p1)























# #继续扩展案例
# from multiprocessing import Process
# import os

# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())#获取父进程pid
#     print('process id:', os.getpid())#获取进程pid

# def f(name):
#     info('function f')
#     print('hello', name)

# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()