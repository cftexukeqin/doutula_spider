# 采用Queue队列的方式，
# 生产者 --> 产生 表情url,img_queue
# 消费者，进行图片下载
# page_queue 是在主函数中进行数据添加

# 传统的同步下载方式

import requests
from lxml import etree
import os,re
import urllib.request
import urllib3
urllib3.disable_warnings()
import threading
from queue import Queue

class Producer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Producer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
            "Host":"www.doutula.com",
            # "Referer":"www.doutula.com"
        }

    # 定义run方法。判断page_url 是否为空
    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_url(url)

    def parse_url(self,url):
        resp = requests.get(url, headers=self.headers, verify=False)
        text = resp.text
        html = etree.HTML(text)

        # xpath 语法可以使用!= 进行标签过滤
        imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
        for img in imgs:
            img_url = img.get('data-original')
            # os.path.splittext()是将文件名和扩展名分开
            # os.path.split()是将路径和文件名分隔开
            suffix = os.path.splitext(img_url)[1]
            title = img.get('alt')
            title = re.sub('[\?？\. \*,，。!！]', "", title)
            filename = title+suffix
            self.img_queue.put((img_url,filename))
            # print(self.img_queue.qsize())


class Customer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Customer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url,filename = self.img_queue.get()
            print(filename+' 下载完成！')
            urllib.request.urlretrieve(img_url,"images2/"+filename)


def main():
    # 创建一个size大小为100的队列，用来存储page_url
    page_queue = Queue(100)
    # 创建一个size大小为1000的队列，用来存储img_url
    img_queue = Queue(1000)
    for i in range(1,101):
        url = "http://www.doutula.com/photo/list/?page=%s" % i
        # 吧产生的url放入队列
        page_queue.put(url)

    for i in range(5):
        p = Producer(page_queue=page_queue,img_queue=img_queue)
        p.start()

    for i in range(5):
        c = Customer(page_queue=page_queue,img_queue=img_queue)
        c.start()

if __name__ == '__main__':
    main()
