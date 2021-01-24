# 多进程的同步

 在系统中，多进程的并发/并行，提高了系统的效率，但是可能存在**竞争资源或者相互合作**，会可能多个进程想同时多共享数据进行读/写，由于多进程的执行顺序不固定，所以保持数据一致性是非常重要的，需要以**适当的策略读写数据**。

需要注意的是，**进程之间默认是不能共享全局变量的(子进程不能改变主进程中全局变量的值)**，比如下面的代码，是无法修改全局变量A的，进程之间的数据是独立的。子进程中虽然有同名的全局变量A，但是和主进程中的全局变量A，是不同的id。要修改建议用上一节说的队列和管道进行通信。

```python
from multiprocessing import Process

A = 100
def fun1():
    global A
    A = 300 * A
    print(id(A), A)

if __name__ == '__main__':
    p1 = Process(target=fun1)
    p1.start()
    p1.join()
    print('global A ID(%d),value is %d'%(id(A), A))
    
#输出
40209232 30000
global A ID(8791170540288),value is 100
```

但是在并发过程中，仍然可能会遇到同步的问题。假设有2个并发的进程P1，P2。共享变量A，以及P1，P2的私有变量a和b。在运行过程中，P1，P2分别对共享变量A进行改变，就有可能发生数据和预期的不一致。

![](\img\共享数据同步.PNG)

如果，t2的时候，P2进程先执行了 A=b+100，那么就有可能最后A的值并非是预期的。

## 同步，互斥机制

同步：多个进程协同完成对某个临界资源（**同一时刻只能一个进程读写的共享资源**）的读写。

互斥：多个进程之间的一种制约关系，由于竞争同一种共享资源的相互制约。比如说多个进程同时想操作临界资源，那么就产生一种竞争状态，谁取得操作权限就能访问，没有权限的进程就阻塞。在运行的时候并没有明显的先后顺序。下图展示2个进程竞争资源的示例图。

值得注意的是：进程之间的执行是乱序的

![](\img\互斥演示.PNG)

临界区：每一个进程开始访问临界资源的代码去（代码片段）。获得临界区权限的进程是独占的，不受干扰的。

要是现实多进程之间的同步，需要用到一个锁来对临界区进行保护，只有获得了Lock的进程才能对临界区资源进行读/写。

***class* multiprocessing.Lock**，原始锁（非递归锁）对象，类似于threading.Lock 。一旦一个进程或者线程拿到了锁，**后续的任何其他进程或线程的其他请求都会被阻塞直到锁被释放**。任何进程或线程都可以释放锁。除非另有说明，否则 threading.Lock 一致。

**acquire(block=True, timeout=None)**，请求锁，调用该方法的进程在获得锁之前都会阻塞，获得后上锁，并返回True。timeout为正值，则最多阻塞等待timeout秒，如timeout<=0,或者=None，阻塞无限长。（该方法与 threading.Lock.acquire()线程中的锁有细节上的不同）。如果block为False，不阻塞，且timeout无效果。

**release()**，释放锁，可以在任何进程、线程使用，并不限于锁的拥有者。其行为与threading.Lock.release()一样，只不过当尝试释放一个没有被持有的锁时，会抛出 ValueError异常。

**class multiprocessing.RLock**，递归锁对象: 类似于threading.RLock。递归锁必须由持有线程、进程亲自释放。如果某个进程或者线程拿到了递归锁，这个进程或者线程可以再次拿到这个锁而不需要等待。但是这个进程或者线程的拿锁操作和释放锁操作的次数必须相同。

## 使用Lock实现进程的同步

最开头提到，进程之间无法共享全局变量，每个进程都保存有自己的一份变量，而且启动子进程的时候不一定顺序，我们将以一个简单的例子查看加锁的前，后运行上有什么变化来体会Lock的作用。

```python
import os
import time
import random
from multiprocessing import Process, Lock

def work(n, lock):
    lock.acquire()
    print('{} : {} is running'.format(n, os.getpid()))
    time.sleep(random.random())
    print('{} : {} is done'.format(n, os.getpid()))
    lock.release()

if __name__ == '__main__':
    lock = Lock()
    for i in range(3):
        p = Process(target=work, args=(i, lock))  
        p.start()
```

多进程（多线程）的锁机制下，注意临界区代码独占，只有获得锁的资源才能对临界区进行操作。虽然加了锁之后程序会降低速度，但保证了数据的安全。

## 使用 Value和Array将数据存储在共享内存映射中

multiprocessing提供了两种方法达成进程之间共享数据，Value和Array。

```python
multiprocessing.Value(typecode_or_type, *args, lock=True)
```

Value，返回一个从共享内存上创建的 [`ctypes`](https://docs.python.org/zh-cn/3.6/library/ctypes.html#module-ctypes) 对象。默认情况下返回的实际上是经过了同步包装器包装过的。可以通过 Value的value属性访问这个对象本身。比如Value.value就可以访问数据值。ctypes是Python 的外部函数库。它提供了与 C 兼容的数据类型，并允许调用 DLL 或共享库中的函数。

typecode_or_type，指定该数据类型，指明了返回的对象类型: 它可能是一个 ctypes 类型或者 array模块中每个类型对应的单字符长度的字符串。

args，可以看是成初始化参数，比如你初始该值是多少就传入多少，Value('i', 1000)，就是构造一个值为1000的int类型数据。

lock，默认会新建一个递归锁锁用于同步该value的操作。如果为False，则该进程不安全。

```
multiprocessing.Array(typecode_or_type, size_or_initializer, *, lock=True)
```

Array，返回一个从共享内存上创建的 [`ctypes`](https://docs.python.org/zh-cn/3.6/library/ctypes.html#module-ctypes) 数组对象。参数与上面的Value差不多。

size_or_initializer 是一个整数，那就会当做数组的长度，并且整个数组的内存会初始化为0。否则，如果 size_or_initializer会被当成一个序列用于初始化数组中的内一个元素，并且会根据元素个数自动判断数组的长度。这意味着，如果你传入一个列表，元组等，就会一一初始化成相应的类型数组。

```python
from multiprocessing import Process, Value, Array
def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))
    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()
    print(num.value)
    print(arr[:])
#输出
3.1415927
[0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
```

更多扩展请去看 [`ctypes`](https://docs.python.org/zh-cn/3.6/library/ctypes.html#module-ctypes) 以及，[array](https://docs.python.org/zh-cn/2.7/library/array.html#module-array)，会提到Value('d')中的d以及其他类型的定义。

