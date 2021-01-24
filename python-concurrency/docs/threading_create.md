# threading模块方法介绍

threading模块是基于thread模块，在底层多线程 API之上，提供了更多高级线程API。如果要更多了解[\_thread](https://docs.python.org/zh-cn/3.6/library/_thread.html#module-_thread)。threading 模块除了包含 _thread 模块中的所有方法外，还提供的其他方法：

- threading.currentThread()， 返回当前的线程变量。
- threading.enumerate()， 返回一个包含正在运行的线程的list。**正在运行指线程启动后、结束前**，不包括启动前和终止后的线程。
- threading.activeCount()，返回正在运行的线程数量，与len(threading.enumerate())有相同的结果。

更多了解去看文档[threading](https://docs.python.org/zh-cn/3.6/library/threading.html#)

## Thread类相关方法

**start()**，开始线程活动。它在一个线程里最多只能被调用一次。它安排对象的 [run()](https://docs.python.org/zh-cn/3.6/library/threading.html#threading.Thread.run) 方法在一个独立的控制进程中调用。如果同一个线程对象中调用这个方法的次数大于一次，会抛出RuntimeError。

**run()**，代表线程活动的方法，你可以在子类中重写这个方法。

**join(*timeout=None*)**，等待，直到线程终结。这会阻塞调用这个方法的线程，直到被调用join()的线程终结 – 不管是正常终结还是抛出未处理异常 – 或者直到发生超时，超时选项是可选的。当 timeout参数存在而且不是None时，它应该是一个用于指定操作超时的以秒为单位的浮点数（或者分数）。因为join()总是返回None，所以你一定要在 join()后调用 is_alive()才能判断是否发生超时 – 如果线程仍然存活，则join() 超时。**当 timeout参数不存在或者是None，这个操作会阻塞直到线程终结。**一个线程可以被join()很多次。如果尝试加入当前线程会导致死锁， join()会引起RuntimeError异常。如果尝试join() 一个尚未开始的线程，也会抛出相同的异常。

**name**，只用于识别的字符串。它没有语义。多个线程可以赋予相同的名称。 初始名称由构造函数设置。

**getName()，setName()**，旧的name取值/设值 API；直接当做特征属性使用它。

**ident**，这个线程的 ‘线程标识符’，如果线程尚未开始则为 None 。这是个非零整数。参见get_ident()函数。当一个线程退出而另外一个线程被创建，线程标识符会被复用。即使线程退出后，仍可得到标识符。

**is_alive()**，返回线程是否存活。当run()方法刚开始直到run()方法刚结束，这个方法返回True 。模块函数enumerate()返回包含所有存活线程的列表。

**daemon**，一个表示这个线程是（True）否（False）守护线程的布尔值。一定要在调用start()前设置好，不然会抛出RuntimeError 。初始值继承于创建线程；主线程不是守护线程，因此主线程创建的所有线程默认都是daemon= False。当没有存活的非守护线程时，整个Python程序才会退出。

**isDaemon()，setDaemon()**，旧的 name取值/设值 API；建议直接当做特征属性使用它。



## 测试多线程的小实例

之前说到过，由于python有GIL锁的存在，实际上多线程无法真正并行利用多核执行，只能单线程执行。因此，用在合适的场景是最好的提升效率方法---I/O中，这次我们打算实现一个多线程文件复制案例，测试多线程的效果。

单进程的代码如下，遍历所有的文件，子文件夹一起遍历，所以用了os.walk，关于该方法，请自行研究。最后一个个文件传给move_file方法中，进行复制。

不过，要注意，如果文件在子文件夹内，想把文件夹和文件按照原来的格式复制过去，这里处理的方法是把原文件的全路径和原文件根目录路径进行切割再和目标目录组合成新的全路径文件，然后递归进行文件夹创建。所有复制后的仍然和复制前的结构是一样的。

```python
import os
import shutil
import time
import threading

path = 'E:\\python日记\\python并发编程\\threading\\test_path'
new_path = 'E:\\python日记\\python并发编程\\threading\\new_path'
def move_file(new_dir, file_path):
    if not os.path.exists(new_dir) or not os.path.exists(file_path):
        return
    #创建新文件的全路径，需要进行进一步处理
    #目前想到的方法就是，把文件和源文件根目录切割
    #得到一个新的相对路径和目标文件夹组合成新的完整路径  
    new_file_path = new_dir + file_path.split(path)[1]
    #通过新文件路径，进行目录，分离，并且递归创建新目录下的路径
    fpath,fname = os.path.split(new_file_path)
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    #开始复制
    shutil.copy(file_path, new_file_path)

if __name__ == '__main__':
    start_time = time.time() * 1000
    for root, dirs, files in os.walk(path, topdown=True):
        for file in files:
            move_file(new_path, os.path.join(root, file))
    end_time = time.time() * 1000
    total_time = end_time - start_time
    print("sum total_time %.2f"%total_time) 
```

多线程方法差不多，遍历所有文件后，为每一个文件开启线程，然后复制。文件夹同样和单进程的一样，递归创建，不过这里遇到问题，因为多线程中全局变量是可以共享的，因此单同时有线程要创建目录的时候，会遇到问题，所有多线程这里我加了线程锁，保证进入临界区代码的安全。

```python
import os
import shutil
import time
import threading

path = 'E:\\python日记\\python并发编程\\threading\\test_path'
new_path = 'E:\\python日记\\python并发编程\\threading\\new_path'

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

if __name__ == '__main__':
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
    print("sum total_time %.2f"%total_time)
```

如果你们有更好的办法，请多指导，目前能想出的办法就这个。开始对比两者的效率吧。