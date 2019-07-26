import os
import shutil

import requests
from lxml import etree

class Mzitu:
    def __init__(self):
        self.index_url = "http://www.mzitu.com"
        self.headers = {
            "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            "Referer": "http://www.mzitu.com"
        }
    # 发送request请求
    def send_requests(self, url):
        return requests.get(url, headers = self.headers, timeout=3).content

    # 解析每页的数据
    def parse(self, html_str):
        html = etree.HTML(html_str)
        titles = html.xpath('//img[@class="lazy]')
        content_list = []
        for title in titles:
            item = []
            item['title'] = title.xpath('./@alt')[0]
            item['href'] = title.xpath('./@alt')[1]
            content_list.append(item)
            print(item)
        next_url = html.xpath('//a[contains(text(), "下一页"')
        next_url = next_url[0] if  next_url else None
        return content_list, next_url

    def get_img_url(self, detail_html):
        html = etree.HTML(detail_html)
        img_url = html.xpath('//span[contains(text(), "下一页"')


    def run(self):
        next_page_url = self.index_url
        i = 1
        while True:
            try:
                html_url = self.send_requests(next_page_url).decode()
            except:
                continue

def main():
    mz = Mzitu()
    mz.run()




if __name__ == '__main__':

    main()

