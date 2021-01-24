# 多线程的同步与通信2

这里接上一期，仍然是继续讲多线程的同步和通信。上次讲到了条件变量以及一个简单的案例，这里准备将一个事件类对象Event。

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

## Timer Objects计时器

Timer类是Thread类的子类，因此可以像一个自定义线程一样工作。 Timer相当于一个定时器，表示一个操作应该在等待一定的时间之后运行。与线程一样，通过调用 start()方法启动定时器。而cancel()方法可以停止计时器（在计时结束前），**定时器在执行其操作之前的等待时间，可能和用户指定的时间不会很精确相同。**（这翻译真难）。我试过用定时器，自己调用自己达到一种目的。下面用文档的例子来说明，同时会讲一个自己做过的例子。

```python
class threading.Timer(interval, function, args=None, kwargs=None)
#简单的例子
def hello():
    print("hello, world")
t = Timer(30.0, hello)
t.start()  # after 30 seconds, "hello, world" will be printed
```

每30S中，定时器都启动一次，而调用的方法也是hello，所以会不断输出hello，world。