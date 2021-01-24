# 多线程的同步与通信

由于在多线程中，全局变量是可以被所有线程共享，所以，任何一个变量都可能被一个线程读/写。因此，线程之间共享数据是需要进行同步，比如加锁等操作，保证安全的。先看一个不加锁，不安全的例子。

```python
import time, threading
# 假定这是你的银行存款:
balance = 0
def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(2000000):
        change_it(n)
t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)

#输出
85
```

这级借了[廖雪峰](https://www.liaoxuefeng.com/wiki/1016959663602400/1017629247922688)大佬的案例。当生成2个线程，每个线程都做了200万次的循环修改全局变量balance之后，最后居然balance只有85。这就是没有对全局变量保护的原因。

## Lock对象

```python
class threading.Lock()#原始锁
```

实现原始锁对象的类。一旦一个线程获得一个锁，会阻塞随后尝试获得锁的线程，直到它被释放；任何线程都可以释放它。这个Lock和多进程的比较像，也包含了acquire和release方法。

**acquire(blocking=True, timeout=-1)**，可以阻塞或非阻塞地获得锁。

- ​    blocking=True，阻塞等待，如果为False，将不会阻塞。如果调用的时候blocking为True ，阻塞并立即返回False，否则将锁锁定，返回True。
- ​    timeout=-1，默认是阻塞等待。blocking为False 时，timeout 指定的值将被忽略。

​        （注意，多进程中的锁参数为block，多线程的为blocking）

**release()**，释放一个锁。**这个方法可以在任何线程中调用，不单指获得锁的线程。**当锁被锁定，将它重置为未锁定，并返回。如果其他线程正在等待这个锁解锁而被阻塞，只允许其中一个允许。在未锁定的锁调用时，会引发RuntimeError 异常。没有返回值。（我试着在一个线程获得了锁之后，另一个线程release(),会发生RuntimeError，所以这里不太理解。文档原文：When invoked on an unlocked lock, a RuntimeError is raised.）

**locked()**，如果获得了锁则返回真值。

案例可以用上面的案例加锁之后再次测试。文档中还有一种RLock，和原始锁差不多。

```python
class threading.RLock()#递归锁
```

可重入锁，它在基元锁的锁定/非锁定状态上附加了 "**所属线程**" 和 "**递归等级**" 的概念。在锁定状态下，某些线程拥有锁 ； 在非锁定状态下， 没有线程拥有它。其他方法也同样有acquire和release方法。

## 条件对象Condition Objects

我把这种这种条件对象成为条件变量同步，有一些场景，需要满足条件之后的线程才能执行。所以提供了threading.Condition对象支持。默认会创建锁对象，这属于Condition的一部分，不必单独跟踪。当多个条件需要共享一个锁，这种场景比较适用。支持上下文管理器（最后会讲）。

```python
class threading.Condition(lock=None)
```

acquire(*args)，请求底层锁。参考Lock的锁。

release()，释放底层锁。参考Lock的锁。

wait(timeout=None)，等待，直到得到通知(另外一个线程调用notify()），或者发生超时。必须在获得锁的情况调用，不然发生RuntimeError异常。这个方法释放底层锁，然后阻塞，**直到在另外一个线程中调用同一个条件变量的notify()或notify_all()唤醒它**，或者直到可选的超时发生。一旦被唤醒或者超时，它重新获得锁并返回。

wait_for(predicate, timeout=None)，等待，直到条件为真，predicate应该是一个可调用的对象且返回值可被解释成bool值。可提供timeout参数给出等待的最大时间。这个方法相当于重复调用wait()，知道满足判断式或超时。返回值是判断式最后一个返回值，而且发生超时返回False。同样，必须在获得锁的情况下调用。

notify(n=1)，默认唤醒一个等待这个条件的线程。需要获得锁的情况下调用，否则会引发RuntimeError异常。**这个方法唤醒最多n个正在等待这个条件变量的线程**；如果没有线程在等待，这是一个空操作。当前实现中，如果至少有n个线程正在等待，准确唤醒 n个线程。然而，这个并不安全，（后面我不懂怎么翻译，中文文档我看感觉不舒服不够正确）。

**注意：被唤醒的线程实际上不会返回它调用的 wait()，直到它可以重新获得锁。因为notify()不会释放锁，只有notify()的调用者应该这样做。**

notify_all()，唤醒所有正在等待这个条件的线程。这个方法行为与 notify()相似，但并不只唤醒单一线程，而是唤醒所有等待线程。如果调用线程在调用这个方法时没有获得锁，会引发 RuntimeError异常。

这里我看了些大佬做的案例，notify和wait是成对出现，好比说，当你notify唤醒其他线程，那么接着自己就wait等待了，而被唤醒的线程同样，当条件又成熟，同样也是先notify再wait，目前还不清楚这样做的道理在哪里。下面我们看一个生产者/消费者代码。

```
import time
import threading
import random
#产品数量
goods = 0
def producer(conn):
    global goods
    while True:
        with conn:
            good = random.randint(1,3)
            goods += good
            time.sleep(2)
            if goods > 10:
                print("产品太多\n")
                conn.notify()
                conn.wait()
        print(f'producer 生产{good},总goods {goods}')
 
def comsume(conn):
    global goods
    while True:
        with conn:
            good = random.randint(0,3)
            goods -= good
            time.sleep(1)
            if goods < 1:
                print("产品不够\n")
                conn.notify()
                conn.wait()
        print(f'comsume 消费{good}，总goods{goods}\n')

if __name__ == '__main__':
    conn = threading.Condition()
    t_p = threading.Thread(target=producer, args=(conn,))
    t_c = threading.Thread(target=comsume, args=(conn,))
    t_p.start()
    t_c.start()
    t_p.join()
    t_c.join()
```

一开始goods为0，所以生产者开始生产，当生产超过10，就选择唤醒消费者线程；消费者消费太多，也会沉睡，等待生产过剩，我感觉这是一个有问题的模型。

## 事件对象Event Objects

文档中说明，这是线程之间通信的最简单机制之一，一个线程发出信号，而其他线程等待该信号。

```python
class threading.Event
```

实现事件对象的类。事件对象管理一个内部标志，调用 set()方法可将其设置为true。调用 clear() 方法可将其设置为false。调用wait()方法将进入阻塞直到标志为true。**这个标志初始时为false。**，在 3.3 版更改: 从工厂函数变为类。

**is_set()**，当且仅当内部标志为true时返回true。

**set()**，将内部标志设置为true。所有正在等待这个事件的线程将被唤醒。当标志为true时，调用wait()方法的线程不会被被阻塞。

**clear()**，将内部标志设置为false。之后调用wait()方法的线程将会被阻塞，直到调用set()方法将内部标志再次设置为true。

**wait(timeout=None)**，阻塞线程直到内部变量为true。如果调用时内部标志为true，将立即返回。否则将阻塞线程，直到调用set()方法将标志设置为true或者发生可选的超时。当提供了timeout参数且不是 None 时，它应该是一个浮点数，代表操作的超时时间，以秒为单位（可以为小数）。

方法就是以上的几个方法，感觉和条件变量类似，这里用一个红绿灯的模拟进行测试。

```python
import threading
import time
def car(name, event):
    while not event.isSet():
        print(f'{name} is wait\n')
        time.sleep(2)
    event.wait()
    while event.isSet():
        print(f'{name} is running\n')
        time.sleep(2)
        
def bus(name, event):
    while not event.isSet():
        print(f'{name} is wait\n')
        time.sleep(2)
    event.wait()
    while event.isSet():
        print(f'{name} is running\n')
        time.sleep(2)

def ambulance(name):
    while True:
        time.sleep(3)
        print(f'{name}, is running\n')

if __name__ == '__main__':

    event = threading.Event()
    t = threading.Thread(target=car, args=('car', event))
    t.start()
    t = threading.Thread(target=bus, args=('bus', event))
    t.start()
    t = threading.Thread(target=ambulance, args=('ambulance',))
    t.start()
    while True:
        event.set()
        print("等红绿灯\n")
        time.sleep(10)
        event.clear()
```

公交车，汽车每10秒中都会进入一次红绿灯状态，但是救护车因为没有event等待标记，所以不需要等待，一直会运行。Event状态预计使用场景是用在多线程通信，同步等都可以用，可以结合锁Lock，条件变量condition，事件event考虑用哪种合适。