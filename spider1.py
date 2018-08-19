# 传统的同步下载方式
#

import requests
from lxml import etree
import os,re
import urllib.request
import urllib3
urllib3.disable_warnings()


def parse_url(url):
    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
    }
    resp = requests.get(url,headers=headers,verify=False)
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
        title = re.sub('[\?？\. \*,，。!！]',"",title)
        filename = title+suffix
        print(img_url)
        urllib.request.urlretrieve(img_url,"images/"+filename)

def main():
    for i in range(1,100):
        url = "http://www.doutula.com/photo/list/?page=%s" % i
        parse_url(url)
        break

if __name__ == '__main__':
    main()