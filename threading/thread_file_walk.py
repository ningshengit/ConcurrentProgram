# -*- coding: utf-8 -*-
# @Date    : 2021-01-19 21:38:18
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 文件遍历
# @Version : $Id$

import os
import shutil
import time
import threading

path = 'E:\\python日记\\python并发编程\\threading\\test_path'
#path = 'E:\\python日记\\python并发编程\\threading\\test'
new_path = 'E:\\python日记\\python并发编程\\threading\\new_path'

#print(test_str.split(path))

def thread_move_file(new_dir, file_path, lock):
    if not os.path.exists(new_dir) or not os.path.exists(file_path):
        return
    #创建新文件的全路径，需要进行进一步处理
    #目前想到的方法就是，把文件和源文件根目录切割
    #得到一个新的相对路径和目标文件夹组合成新的完整路径 
    new_file_path = new_dir + file_path.split(path)[1]
    #通过新文件路径，进行目录，分离，并且递归创建新目录下的路径
    lock.acquire()
    fpath,fname = os.path.split(new_file_path)
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    lock.release()

    #开始复制
    shutil.copy(file_path, new_file_path)
    return

def move_file(new_dir, file_path):
    if not os.path.exists(new_dir) or not os.path.exists(file_path):
        return
    #创建新文件的全路径，需要进行进一步处理
    #目前想到的方法就是，把文件和源文件根目录切割
    #得到一个新的相对路径和目标文件夹组合成新的完整路径  
    new_file_path = new_dir + file_path.split(path)[1]
    #通过新文件路径，进行目录，分离，并且递归创建新目录下的路径
    fpath, fname = os.path.split(new_file_path)
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    #开始复制 
    shutil.copy(file_path, new_file_path)


if __name__ == '__main__':

    #单线程复制文件
    # start_time = time.time() * 1000
    # for root, dirs, files in os.walk(path, topdown=True):
    #     for file in files:
    #         move_file(new_path, os.path.join(root, file))
    # end_time = time.time() * 1000
    # total_time = end_time - start_time
    # print("sum total_time %.2f"%total_time)
    #sum total_time 872.73  
    #sum total_time 367.77

    #多线程执行
    start_time = time.time() * 1000
    lock = threading.Lock()
    #file_ = []
    for root, dirs, files in os.walk(path, topdown=True):
        for file in files:
            #file_.append(os.path.join(root, file))
            t = threading.Thread(target=thread_move_file, args=(new_path, os.path.join(root, file), lock))
            t.start()

    end_time = time.time() * 1000
    total_time = end_time - start_time
    print("threading sum total_time %.2f"%total_time)
    #sum total_time 75.00