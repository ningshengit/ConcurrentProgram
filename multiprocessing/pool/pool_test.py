# -*- coding: utf-8 -*-
# @Date    : 2021-01-18 12:56:33
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 进程池小例子
# @Version : $Id$

import os
from multiprocessing import Pool
import time

def fun(name):
    print(name, os.getpid())
    time.sleep(1)
    print("end") 

# if __name__ == '__main__':
#     pool = Pool(5)
#     for i in range(5):
#         pool.apply_async(fun, args=(i,))

#     pool.close()
#     pool.join()#等待所有的子进程返回。

#     print("main done")


if __name__ == '__main__':
    pool = Pool(5)
    map_list = [1, 2, 3, 4]

    pool.map(fun, map_list)

    pool.close()
    pool.join()#等待所有的子进程返回。

    print("main done")