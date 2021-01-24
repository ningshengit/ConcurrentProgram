# python多进程模块介绍multiprocessing

## 主要功能介绍

* 创建子进程，Process类。主要用于创建子进程对象，然后start生成。
* 进程通信，支持Queue类队列和Pipe类管道通信。
* 共享数据，在并发编程时候，通常尽量避免使用共享状态，如果需要共享，可以使用共享内存Value或Array将数据存在共享内存的映射中。
* 进程同步，Lock类实现进程的同步。
* 进程池，pool类

## 更多参考资料

    https://docs.python.org/zh-cn/3/library/multiprocessing.html#synchronization-between-processes

[`multiprocessing`](https://docs.python.org/zh-cn/3/library/multiprocessing.html#module-multiprocessing) --- 基于进程的并行，这是python标准库文档中的介绍。下面将开始介绍Process类和启动多进程的方法。