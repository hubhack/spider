import os
import shutil

import requests
from lxml import etree


class MZiTu:

    # 初始化对象属性
    def __init__(self):
        self.index_url = "https://www.mzitu.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Referer": "https://www.mzitu.com/"
        }
        self.path = input('请输入保存的文件夹名(默认为--meizitu--):')

    # 发送request请求
    def send_request(self, url):
        return requests.get(url, headers=self.headers, timeout=3).content

    # 解析每页的数据
    def parse(self, html_str):
        html = etree.HTML(html_str)
        titles = html.xpath('//img[@class="lazy"]')
        content_list = []
        for title in titles:
            item = {}
            item['title'] = title.xpath('./@alt')[0]
            item['href'] = title.xpath('../@href')[0]
            content_list.append(item)
            # print(item)
        # print(content_list)
        next_url = html.xpath('//a[contains(text(),"下一页")]/@href')
        next_url = next_url[0] if next_url else None
        return content_list, next_url

    # 获取每张写真集的img_url
    def get_img_url(self, detail_html):
        html = etree.HTML(detail_html)
        img_url = html.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
        next_img_url = html.xpath('//span[contains(text(),"下一页")]/../@href')
        next_url = next_img_url[0] if next_img_url else None
        return img_url, next_url

    # 判断文件夹是否存在,不存在创建文件夹
    def mkdir(self, dir_name, img_url_list):
        total_image = len(img_url_list)
        meizi_dir = self.path if self.path else 'meizitu'
        final_dir = meizi_dir + '/' + '[{}P]'.format(str(total_image)) + dir_name
        if os.path.exists(final_dir):
            shutil.rmtree(final_dir)
        os.makedirs(final_dir)
        return final_dir

    # 保存img
    def save_image(self, j, final_dir, img_url_list):
        for img_url in img_url_list:
            try:
                image_data = self.send_request(img_url)
            except:
                continue
            file_name = final_dir + '/' + img_url[-9:]
            with open(file_name, 'wb') as image:
                image.write(image_data)
            print("*" * 14, img_url, '下载完成', "*" * 14)
        print("-" * 29 + '第{}张写真集保存完毕'.format(int(j)) + "-" * 30 + '\n\n')

    # 运行爬虫
    def run(self):
        # 1. 获取url
        next_page_url = self.index_url
        i = 1
        # 获取每页的url地址并解析
        while True:
            # 2. 发送请求,获取响应
            try:
                html_str = self.send_request(next_page_url).decode()
            except:
                continue
            # 3. 解析数据
            content_list, next_page_url = self.parse(html_str)
            # 4. 获取详情页的img
            j = 1
            # 获取每张写真集并解析
            for content in content_list:
                img_url_list = []
                print("-" * 30 + '正在获取第{}张写真集'.format(int(j)) + "-" * 30)
                # 获取每张写真集的img_url
                # 第一页的img地址
                dir_name = content['title']
                next_url = content['href']
                # print(next_url)
                # 获取每张写真集每页的img_url
                while True:
                    try:
                        detail_html = self.send_request(next_url).decode()
                    except:
                        continue
                    img_url, next_url = self.get_img_url(detail_html)
                    # 第二页的img地址
                    # detail_html = self.send_request(next_url)
                    # img_url, next_url =self.get_img_url(detail_html)
                    img_url_list.append(img_url)
                    if next_url is None:
                        break
                # 保存图片
                if img_url_list:
                    final_dir = self.mkdir(dir_name, img_url_list)
                    self.save_image(j, final_dir, img_url_list)
                j += 1
            print("-" * 32 + '第{}页获取完成'.format(int(i)) + "-" * 32 + '\n\n')
            i += 1
            if next_page_url is None:
                break


def main():
    mz = MZiTu()
    mz.run()


if __name__ == '__main__':
    main()