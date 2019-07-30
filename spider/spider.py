import requests
from threading import Event
from bs4 import BeautifulSoup
from bs4.element import Tag
from queue import Queue
from test import Producer, Consumer
import simplejson
from concurrent.futures import ThreadPoolExecutor
# https://www.cnblogs.com/n/page/100
BASE_URL = "https://news.cnblogs.com"
NEWS = "/n/page/"
headers ={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
# 以后用队列, rabbitmq
# urls = Queue() # 待爬取的url
# htmls = Queue() # 待分析的网页
# outputs = Queue()# 待持久化的数据

def start_urls(start, stop ,step = 1):
    p = Producer('148.70.137.191', 5672, 'mwq', 'mwq', 'test', 'news', 'urls')
    for i in range(start, stop+1, step):
        url = "{}{}{}/".format(BASE_URL, NEWS, i)
        print(url)
        # crawl()# 同步调用
        # urls.put(url)
        p.produce(url)

    print('初始url生成完毕')



def crawl(e:Event):
    # 阻塞 非阻塞
    p = Producer('148.70.137.191', 5672, 'mwq', 'mwq', 'test', 'news', 'html')
    c = Consumer('148.70.137.191', 5672, 'mwq', 'mwq', 'test', 'news', 'urls')
    while not e.wait(1):
        # url = urls.get()# 从队列阻塞的取数据
        url = c.consume()
        if url:

            with requests.get(url, headers=headers) as response:

                if response.status_code == 200:
                    html = response.text
                    # print(html)
                    # htmls.put(html)
                    p.produce(html)

# 解析页面
def parse(e:Event):

    p = Producer('148.70.137.191', 5672, 'mwq', 'mwq', 'test', 'news', 'html')
    c = Consumer('148.70.137.191', 5672, 'mwq', 'mwq', 'test', 'news', 'urls')
    while not e.wait(1):

        # html = htmls.get()
        html = c.consume()

        #分析
        if html:
            soup = BeautifulSoup(html, 'lxml')
            titles = soup.select('h2.news_entry > a')
            # count = 0
            for title in titles:
                # print(title.get('href', ''), title.text)
                # count += 1
                # 存入数据库
                href = title.get('href', '')
                if href:
                    url = BASE_URL + title.get('href', '')
                    title = title.text

                    outputs.put((url, title))
            # print(count)
            # print(threading.current_thread())

def persist(e:Event): #
    c = Consumer('148.70.137.191', 5672, 'mwq', 'mwq', 'test', 'news', 'urls')

    while not e.is_set():
        val = outputs.get()
        print(val, '--------')
        val = {
            'title': val[1],
            'url': val[0]
        }
        with open('new.txt', 'a+', encoding='utf-8') as f:
           try:
                f.write(simplejson.dumps(val) + '\n') #  考虑不能持久化的
                f.flush()
           except Exception as e:
               print(e)
# start_urls(1, 1)
# crawl()
event = Event()
executor = ThreadPoolExecutor(10) #线程池

executor.submit(start_urls, 1, 1)
executor.submit(persist, event)

for i in range(5):
    executor.submit(crawl, event)

for i in range(4):
    executor.submit(parse, event)