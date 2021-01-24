# 多线程用队列通信

本来想说多线程的队列类，看但是看了又看，多线程并没有自己实现队列的类，直接可以通过Queue模块来实现。（多进程有**multiprocessing**.**Queue**([maxsize])，也是在Queue基础上实现的）。

## 队列Queue

Python的Queue模块中提供了**同步的、线程安全的队列类**，这说明使用队列至少是安全的。Queue实现的队列包括：

FIFO（先入先出)队列Queue。

LIFO（后入先出）队列LifoQueue。

PriorityQueue（优先级队列）。

这些队列都实现了锁原语，能够在多线程中直接使用，实现线程间的同步。基本的队列类型有以下几个。

```python
#FIFO
class queue.Queue(maxsize=0)
#LIFO
class queue.LifoQueue(maxsize=0)
#优先级队列
class queue.PriorityQueue(maxsize=0)
```

队列的公共方法，和多进程的差不多，关键方法有，put，get，empty，full等。

**Queue.qsize()**，返回队列的大致大小。注意，qsize() > 0不保证后续的get() 不被阻塞，qsize() < maxsize 也不保证put()不被阻塞。

**Queue.empty()**，如果队列为空，返回True ，否则返回False。如果 empty()返回True ，不保证后续调用的put()不被阻塞。类似的，如果empty()返回False ，也不保证后续调用的 get() 不被阻塞。

**Queue.full()**，如果队列是满的返回 True ，否则返回 False 。如果full() 返回True不保证后续调用的get()不被阻塞。类似的，如果full() 返回False也不保证后续调用的 put() 不被阻塞。

**Queue.put(*item*, *block=True*, *timeout=None*)**，将item放入队列。默认是阻塞直到有空间可用。

​    timeout，最多阻塞timeout秒，如阻塞时间内，有空间，则将item放入队列。超时仍然没有空间，则引发Full异常。如果block=False，则有空间则立刻插入队列，否则马上引发FULL异常。

**Queue.put_nowait(*item*)**，相当于 put(item, False) 。

**Queue.get(*block=True*, *timeout=None*)**，从队列中移除并返回一个项目。默认阻塞直到至少有1给item可以获取。

​    timeout，最多阻塞timeout秒，如阻塞时间内，有空间，则将item拿出队列。超时仍然没有item，则引发Empty异常。如果block=False，则有空间则立刻拿出队列，否则马上引发Empyt异常。

**Queue.get_nowait()**，相当于get(False) 。

**Queue.join()**，阻塞至队列中所有的元素都被接收和处理完毕，阻塞被解除。

这次用一个多线程爬取唐诗300首来做下说明，总共16页，这里写了简单的方法进行爬取，这里可以加上循环就能实现一个单进程的爬虫。

```python
start_url = 'https://www.shicimingju.com/shicimark/tangshisanbaishou_0_0__0.html'
def get_shige_content(url):
    '''爬取诗歌正文，赏析'''
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content.decode('utf-8'), 'lxml')
        zs_title = soup.select('#zs_title')[0].get_text()
        if '/' in zs_title:
            zs_title = zs_title.replace('/', '')
        auther = soup.select('.niandai_zuozhe')[0].get_text().replace(' ', '')
        content = soup.select('#zs_content')[0].get_text().replace(' ', '').replace('\n', '')
        #print(content)
        shangxi_content = soup.select('.shangxi_content')
        if shangxi_content:
            shangxi = shangxi_content[0].get_text().replace(' ', '').replace('\n', '')
        else:
            shangxi = "-"
        return [zs_title, auther, content, shangxi]

def save_shige(shige):
    '''保存到文件'''
    with open(f'shige/{shige[0]}.txt', 'w', encoding='utf-8') as fp:
            fp.writelines(shige)
            fp.write('\n')

def get_shige_url(url):
    '''获取每一页的诗歌链接'''
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        temp = soup.find_all('div', attrs={'class':'card shici_card'})[0]
        urls = []
        for url in temp.select('h3 a'):
           shige_url = 'https://www.shicimingju.com' + url['href']
           urls.append(shige_url)
        return urls
    else:
        return
```

加入多线程，队列实现。首先是url队列，诗歌正文的队列，spider_shige不断爬取诗歌正文，put进shige_queue中，save_file不断get诗歌保持文件，过程很简单。

```python
url_queue = queue.Queue()
shige_queue = queue.Queue(100)

def spider_shige(name):
    global url_queue
    global shige_queue
    while not url_queue.empty():
        url = url_queue.get()
        shige = get_shige_content(url)
        shige_queue.put(shige)
        print(f'thread{name}, claw,{url},{shige_queue.qsize()}\n')
        time.sleep(random.randint(1, 3))

def save_file(name):
    global shige_queue
    while not shige_queue.full():
        time.sleep(1)
    while 1:
        shige_d = shige_queue.get()
        save_shige(shige_d)
        title = shige_d[0] 
        print(f'save {title}\n')
        time.sleep(1)
        if shige_queue.empty() and url_queue.empty():
            break
 
if __name__ == '__main__':
    for page in range(1, 17):
        url = base_url.format(page)
        result = get_shige_url(url)
        for url in result:
            url_queue.put(url)
    print(f"begin thread--,url len {url_queue.qsize()}\n")
    for i in range(1, 10):
        t = threading.Thread(target=spider_shige, args=(f'spider_{i}',))
        t.start()
    save_t = []
    time.sleep(25)
    print("begin save thread")
    for x in range(1, 2):
        t = threading.Thread(target=save_file, args=(f'save_{i}',))
        save_t.append(t)
        t.start()
    for t in save_t:
        t.join()

```

