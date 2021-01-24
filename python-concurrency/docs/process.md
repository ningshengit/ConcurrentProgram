# 一个简单的多进程示例

通过创建一个 [`Process`](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Process) 对象然后调用它的 `start()` 方法来生成进程

```python
from multiprocessing import Process

def hello(name):
    print('hi', name)

if __name__ == '__main__':
    p = Process(target=hello, args=('python',))
    p.start()
    p.join()
```

这里简单创建了一个Process对象，而且把函数对象f赋值给target，args很明显就是一个元组，看Process参数列表就知道。这么说，这个例子将会输出hello,bob了。注意，安全导入主模块的原因，要把Process类的创建放在：if __name__ == '\_\_main\_\_':之后。那么多进程启动之后，要怎么看是否成功？

## 能查看进程的PID扩展案例

```python
from multiprocessing import Process
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())#获取父进程pid
    print('process id:', os.getpid())#获取进程pid

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
```

## Process的参数介绍

class multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)
group参数未使用，值始终为None。
target表示调用对象，即子进程要执行的任务。
name为子进程的名称。
args表示调用对象的位置参数元组，args=()。
kwargs表示调用对象的字典。

## Process多进程的一个小案例

上一个案例只是启动了一个子进程，根本没有所谓的多进程的感觉，现在我们开始一个超过3个进程以上的案例。并且计算总的运行时间。

```
def sum(n):
    add = 0
    for i in range(0, n):
        add += i
    print('0-%d, add is %d'%(n,add))


if __name__ == '__main__':
	#单进程
    start_time = time.time() * 1000
    sum(50000000)
    sum(50000000)
    sum(50000000)
    end_time = time.time() * 1000
    total_time = end_time - start_time
    print("sum total_time %.2f"%total_time)

	#多进程
    start_time = time.time() * 1000
    p_obj = []
    for i in range(0, 3):
        p = Process(target=sum, args=(50000000, ))
        p.start()
        p_obj.append(p)

    for obj in p_obj:
        obj.join()        
    end_time = time.time() * 1000
    total_time = end_time - start_time
    print("multiprocessing sum total_time %.2f"%total_time)
#输出
0-500000, add is 124999750000
0-500000, add is 124999750000
0-500000, add is 124999750000
sum total_time 103.01
0-500000, add is 124999750000
0-500000, add is 124999750000
0-500000, add is 124999750000
multiprocessing sum total_time 224.01
```

是不是很意外？多进程的结果居然还比单进程的还多，这是因为多进程还有一个进程切换调度时间的花销所以才会多吗？其实，所有的把100000多加10倍就能看出多进程还是有明显的提升了。