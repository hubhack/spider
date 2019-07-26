import requests
from bs4 import BeautifulSoup


class NovelSpider:
    """某书网，小说爬虫"""

    def __init__(self):
        self.session = requests.Session()

    def get_novel(self, url):  # 主逻辑
        """下载小说"""
        # 下载小说首页html
        index_html = self.download(url, encoding="gbk")
        # 小说的标题
        soup = BeautifulSoup(index_html, "html.parser")
        article_title = soup.find('a', class_="article_title").get_text()

        # 提取章节信息，url 网址
        novel_chapter_infos = self.get_chapter_info(index_html)
        # 创建一个文件 小说名.txt
        fb = open(f"{article_title}.txt", "w", encoding="utf-8")

        # 下载章节信息 循环
        for chapter_info in novel_chapter_infos:
            # 写章节
            fb.write(f"{chapter_info[1]}\n")
            # 下载章节
            content = self.get_chapter_content(chapter_info[0])
            fb.write(f"{content}\n")
            print(chapter_info)
        fb.close()

    def download(self, url, encoding):
        """下载html源码"""
        r = self.session.get(url)
        r.encoding = encoding
        return r.content

    def get_chapter_info(self, index_html):
        """提取章节信息"""
        soup = BeautifulSoup(index_html, "html.parser")
        chapterNum = soup.find('div', class_="chapterNum")
        data = []
        for link in chapterNum.find_all("li"):
            link = link.find('a')
            data.append((link["href"], link.get_text()))

        return data

    def get_chapter_content(self, chapter_url):
        """下载章节内容"""
        chapter_html = self.download(chapter_url, encoding="gbk")

        soup = BeautifulSoup(chapter_html, "html.parser")
        content = soup.find("div", class_="mainContenr")
        content = content.get_text().replace("style5();", '')
        return content


if __name__ == '__main__':
    novel_url = 'http://www.quanshuwang.com/book/9/9055'
    spider = NovelSpider()
    spider.get_novel(novel_url)