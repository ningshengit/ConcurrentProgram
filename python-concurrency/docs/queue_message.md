# 多进程通讯：队列和管道

进程彼此之间互相隔离，要实现进程间通信（IPC），multiprocessing模块支持两种形式：队列和管道，这两种方式都是使用消息传递的。Queue模块实现多生产者，多消费者队列。关于什么是队列，建议移步看数据结构，大概就是**排队打饭，先排的先能吃到饭**。看下Queue的方法。

```python
class multiprocessing.Queue([maxsize])
```

Queue会返回一个共享队列实例。maxsize是队列中允许的最大数量，创建时候不设置，则无限制大小。队列使用一个管道和少量的锁和信号量，当一个进程将一个对象放进队列中，一个写入线程就启动并将对象从缓冲区写入。

Queue主要会用到一下几个方法，：

**put(*obj*[, *block*[, *timeout*]])**，将 obj 放入队列。

block，默认True，且timeout（默认None）为None则阻塞至队列有剩余空间，如果timeout为正值，则阻塞至timeout指定时间，如果超时，则抛出Queue.Full异常；如果blocked为False，如Queue已满，会立即抛出Queue.Full异常。

**get([*block*[, *timeout*]])**从队列中取出并返回对象，读取并且删除一个元素。

 *block*默认True ，且timeout（默认None）则阻塞直到队列中出现可用的对象。如果 *timeout* 是正值，则阻塞至timeout指定时间，如果超时，则抛出Queue.Empty异常；如果blocked为False，如Queue已空，会立即抛出Queue.Empty异常，如果Queue有值，会立即返回该值。

**这里要注意的是，一旦超时，将抛出标准库 queue中的queue.Empty或者queue.Full，这说明如果需要抛出异常，需要导入标准库的queue模块才能识别Empty和Full异常。**

**get_nowait()**，相当于 get(False) 。

**put_nowait(*obj*)**，相当于put(obj, False)。

**empty()**，如果队列是空的，返回 True ，反之返回 False 。 由于多线程或多进程的环境，该状态是不可靠的。

**full()**，如果队列是满的，返回 True，反之返回 False 。 由于多线程或多进程的环境，该状态是不可靠的。

**qsize()**，返回队列的大致长度。由于多线程或者多进程的上下文，这个数字是不可靠的。

另外还有几个其他方法。

close()，指示当前进程将不会再往队列中放入对象。

join_thread()，等待后台线程。这个方法仅在调用了 close()方法之后可用。这会阻塞当前进程，直到后台线程退出，确保所有缓冲区中的数据都被写入管道中。

cancel_join_thread()，防止 join_thread()方法阻塞当前进程。

看到put，get就应该想到，这就是队列的关键用法。下面我们来做一个小实验。

## Queue队列使用实例

这里我们以一个经典生产者/消费者模式来演示一个Queue的过程。

```python
import os
from multiprocessing import Process, Queue
from queue import Empty, Full
import random
import time

def producer(name, queue):
    print(name)
    while True:
        new_good = random.randint(1, 10)
        if not queue.full():
            queue.put(new_good)
            print("%s生产了%s个产品"%(name, new_good))
        else:
            break
        time.sleep(1)
    print("%s生产满了"%name)
    return

def consumer(name, queue):
    print(name)
    while True:
        if not queue.empty():
            good = queue.get()
            print("%s消费了%s个产品"%(name, good))
        else:
            break
        time.sleep(1)
    print("%s没有商品消费了"%name)
    return

if __name__ == '__main__':
    q = Queue(10)
    #两个生产产品，苦工1号，苦工2号
    kg_1 = Process(target=producer, args=('kg_1', q))
    kg_2 = Process(target=producer, args=('kg_2', q))

    #2个消费者，香香，如花
    #p_mm = Process(target=consumer, args=('mm', q))
    p_xx = Process(target=consumer, args=('xx', q))
    p_rh = Process(target=consumer, args=('rh', q))

    kg_1.start()
    kg_2.start()
    p_xx.start()
    p_rh.start()
    print("begin test")
```

这里还可以做些调整，比如把消费者的time.sleep(1)，和生产者的time.sleep(1)，做成不同的，造成生产和消费节奏不一样，看看会发生什么情况。

## Pipe([duplex])进行管道通信

Pipe()函数返回**2个由管道连接的连接对象**，默认情况下是双工（双向），我把管道想象成一条独木桥，一次只能过一个人，不能两边同时过人。每个连接对象都有 send() 和 recv() 方法（相互之间的），要注意的是，如果同时有两个进程（或线程）对管道的同一端进行写入/读取，可能会损坏管道。安全情况下，不同的进程（或线程）都应该使用管道的不同端口。pipe方法有duplex参数，默认True，就是全双工模式，也就是说conn1和conn2均可收发；如果duplex为False，conn1只负责接受消息，conn2只负责发送消息。

```python
#方法原型
(conn1, conn2) = Pipe([duplex])
```

这里展示了一个简单的管道通讯。

```python
from multiprocessing import Process, Pipe

def fun1(conn):
    while True:
        try:
            message = conn.recv()
            print(message)
        except Exception as e:
            print(e)
            break
def fun2(conn):
    for i in range(0, 5):
        message = "你好，我是fun2"
        conn.send(message)
    conn.close()
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
    
    print("main end")
```

