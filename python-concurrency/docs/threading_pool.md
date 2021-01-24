# 多线程的线程池介绍

threading模块中并没有线程池这一个模块，而是在其他的模块中提供，在python的3.2版本后加入了标准库中，模块是，concurrent.futures，提供异步执行回调的高层接口。模块实现了多线程，多进程的异步执行，继承了class concurrent.futures.Executor，这是一个抽象类。

ThreadPoolExecutor，使用线程实现异步回调，ProcessPoolExecutor使用单独的进程来实现。两者都是实现抽像类Executor定义的接口。抽象类提供异步执行调用方法。要通过它的子类调用，而不是直接调用。

```python
class concurrent.futures.Executor
```

**submit(fn, /, \*args, \*\*kwargs)**，调度可调用对象。以 fn(\*args, \*\*kwargs) 方式执行并返回Future对象，代表可调用对象的执行。使用方法，可以如下：

```python
with ThreadPoolExecutor(max_workers=1) as executor:    
    future = executor.submit(pow, 323, 1235)    
    print(future.result()) 
```

是不是看到很熟悉的方法，pow就是可调用的对象，pow执行后会返回future对象，通过future.result()获得结果。

**map(func, \*iterables, timeout=None, chunksize=1)**，类似于map(func, iterables)函数，除了以下两点：

- iterables是立即执行而不是延迟执行的；
- func是异步执行的，对func的多个调用可以并发执行。
- timeout，默认不限制等待时间。原文档中有一个会发生concurrent.futures.TimeoutError的说法，经过我的翻译，我觉得应该这样理解。如果Executor.map()的原始调用经过timeout秒（timeout可以为 int 或 float 类型）后还不可用，而且\_\_next\_\_\()已被调用,则已返回的迭代器将引发concurrent.futures.TimeoutError。（建议去看原文，我觉得应该是timeout时间后，按理说已经要执行迭代器的下一项，但是发生timeout，就会引发异常）。
- chunksize=1，必须是正整数，指定任务块的大小，大概就是把迭代器进行切分，再和func一起提交到执行池中，**只对ProcessPoolExecutor有效**，对很长的迭代器，使用大的chunksize比默认值性能要高。

**shutdown(wait=True, *, cancel_futures=False)**，当待执行的future对象完成执行后向执行者发送信号，它就会释放正在使用的任何资源。 关闭后不可在调用submit和map方法，会发生异常。

- 如果wait为True则此方法只有在所有待执行的future对象完成执行且释放已分配的资源后才会返回。 
- 如果 wait 为 False，方法立即返回，所有待执行的future对象完成执行后会释放已分配的资源。 

不管wait的值是什么，整个Python程序将等到所有待执行的future对象完成执行后才退出。

如果cancel_futures 为 True，此方法将取消所有执行器还未开始运行的挂起的Future。 任何已完成或正在运行的 Future 将不会被取消，无论 cancel_futures 的值是什么？如果cancel_futures和wait均为 True，则执行器已开始运行的所有Future 将在此方法返回之前完成。 其余的 Future 会被取消。

你可以使用with的方式避免使用该方法。比如如下的使用

```python
import shutil
with ThreadPoolExecutor(max_workers=4) as e:
    e.submit(shutil.copy, 'src1.txt', 'dest1.txt')
    e.submit(shutil.copy, 'src2.txt', 'dest2.txt')
    e.submit(shutil.copy, 'src3.txt', 'dest3.txt')
    e.submit(shutil.copy, 'src4.txt', 'dest4.txt')
```

以上可就是Executor的方法，线程池ThreadPoolExecutor和进程池ProcessPoolExecutor都各自实现了方法。

## class concurrent.futures.ThreadPoolExecutor

线程池原型如下：

```python
class concurrent.futures.ThreadPoolExecutor(max_workers=None, thread_name_prefix='')
```

如果max_workers 为None或没有指定，将默认为机器处理器的个数，假如 [ThreadPoolExecutor则重于I/O操作而不是CPU运算，那么可以乘以 5 ，同时工作线程的数量可以比ProcessPoolExecutor的数量高。

3.6 新版功能: 添加 thread_name_prefix 参数允许用户控制由线程池创建的threading.Thread工作线程名称以方便调试。以一个简单的例子说明如何使用。

```
def test1(name):
    count = 10
    while True:
        print(f'{name},{count}\n')
        time.sleep(2)
        count -=1
        if count < 1:
            break
    return name

def test2(name):
    count = 10
    while True:
        print(f'{name},{count}\n')
        time.sleep(19)
        count -=1
        if count < 1:
            break
    return name
    
if __name__ == '__main__':

    thread_list = []
    save_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for i in range(5):
            t = executor.submit(test1, f'thread_{i}')
            thread_list.append(t)
        for i in range(3):
            t = executor.submit(test2, f'save_{i}')
            save_list.append(t)
            
    for i in thread_list:
        print(i.result())
    for i in save_list:
        print(i.result())  

```

注意，只有当线程池所有的线程都释放的时候，with语句才返回，期间都在阻塞状态。