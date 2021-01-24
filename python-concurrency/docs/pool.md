# 进程池Pool

进程池非常形象的解释了当进程很多很多的时候，该怎么维护的情况。可以指定一个包含若干数量的进程池，当有新的请求到，如果pool还没有满，就创建新的子进程执行请求。如果满了，就等待，直到进程池中有进程结束，再创建新进程执行。下面看进程池的原型。

```python
class multiprocessing.pool.Pool([processes[,initializer[,initargs[,maxtasksperchild[,context]]]]])
```

processes 是要使用的工作进程数目。如果 processes 为 None，则使用系统的cpu核心数量。创建一个简单的进程池很简单。只需要导入模块后，用Pool类创建即可，如

```
import multiprocessing
pool = multiprocessing.Pool(5)#5个进程数量的池
#或者
pool = multiprocessing.Pool()#默认的cpu核心数量
```

如果 *initializer* 不为 None，则每个工作进程将会在启动时调用 initializer(*initargs)。这里我是可以指定一个方法fun，fun的参数由initargs给出，比如（用了进程池和Lock锁，由于子进程不能传递锁，所以可以用initializer指定一个调用方法fun传递，网上有案例）。

maxtasksperchild是一个工作进程在它退出或被一个新的工作进程代替之前能完成的任务数量，为了释放未使用的资源。默认的 maxtasksperchild是 None，意味着工作进程寿与池齐。

context 可被用于指定启动的工作进程的上下文。通常一个进程池是使用函数 multiprocessing.Pool()或者一个上下文对象的 Pool()方法创建的。在这两种情况下， context都是适当设置的。

## 一个简单的例子

```python
import os
from multiprocessing import Pool
import time

def fun(name):
    print(name, os.getpid())
    time.sleep(3)
    print("end") 

if __name__ == '__main__':
    pool = Pool(5)
    for i in range(5):
        pool.apply_async(fun, args=(i,))
    pool.close()
    pool.join()
```

这里展示了Pool该如何使用，创建了一个能容纳5个进程的池，接着使用pool调用即可。下面看下Pool关键的方法都有哪些。

**apply(func[, args[, kwds]])**，这里和Process中创建是的target参数，func就是要调用的方法，而且后面的args，kwds参数和Process的类似，这里不多讲，这个方法会阻塞。所以，apply_async()更适合并行化工作。另外 func只会在一个进程池中的一个工作进程中执行。

**apply_async(func[, args[, kwds[, callback[, error_callback]]]])**，apply()方法的一个变种，返回一个结果对象。这里多了一个callback，与error_callback参数。

​    如果指定了 callback , 它必须是一个接受单个参数的可调用对象。当执行成功时， callback 会被用于处理执行后的返回结果，否则，调用 error_callback 。

​    如果指定了 error_callback , 它必须是一个接受单个参数的可调用对象。当目标函数执行失败时， 会将抛出的异常对象作为参数传递给 error_callback执行。

​    **回调函数应该立即执行完成，否则会阻塞负责处理结果的线程。**

**map(func, iterable[, chunksize])**，这个方法会将**可迭代对象分割为许多块**，然后提交给进程池。可以将 chunksize 设置为一个正整数从而（近似）指定每个块的大小可以。

**map_async(func, iterable[, chunksize[, callback[, error_callback]]])**，和 map() 方法类似，但是返回一个结果对象。

​    如果指定了 callback , 它必须是一个接受单个参数的可调用对象。当执行成功时， callback 会被用于处理执行后的返回结果，否则，调用 error_callback 。

​    如果指定了 error_callback , 它必须是一个接受单个参数的可调用对象。当目标函数执行失败时， 会将抛出的异常对象作为参数传递给 error_callback 执行。

​    **回调函数应该立即执行完成，否则会阻塞负责处理结果的线程。**

close()，阻止后续任务提交到进程池，当所有任务执行完成后，工作进程会退出。

terminate()，不必等待未完成的任务，立即停止工作进程。当进程池对象呗垃圾回收时， terminate()会立即调用。

join()等待工作进程结束。调用join()前，请先调用close()或者terminate()。

还有几个其他方法，请移步去[multiprocessing](https://docs.python.org/zh-cn/3.6/library/multiprocessing.html#module-multiprocessing.pool)文档中看。

## 使用进程池实现简单聊天室功能

```python
import os
from socket import *
from multiprocessing import Pool

def talk(conn):
    while 1:  # 循环通讯
        try:
            from_client_msg = conn.recv(1024).decode('utf-8')
            if not from_client_msg:
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
    pool = Pool(5) 
    while 1:
        conn, addr = server.accept()
        pool.apply_async(talk, args=(conn,))
    pool.close() 
    pool.join() 
    server.close()
```

以上是server端，创建完之后，阻塞等客户端连接。有新连接到就创建新的进程接送和发回。

```python
import os
from socket import *

client = socket()
ip_port = ("127.0.0.1", 8001)
client.connect(ip_port)
while 1:
    inp = input(">>:").strip()
    if not inp: continue
    if inp.upper() == "Q": break
    client.send(inp.encode())
    from_server_msg = client.recv(1024).decode('utf-8')
    print("来自服务端的消息:", from_server_msg)
client.close()
```

以上是client端，连接server之后，就可以输入字符与服务器沟通。