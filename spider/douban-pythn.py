
from lxml import etree
import requests

url = 'http://movie.douban.com/'
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36''
with requests.get(url, headers={'User-agent':ua}) as response:
    content = response.text
    html = etree.HTML(content)
    titles = html.xpath('//div[@class="billboard-bd"]//tr/td/a/text()')
    for t in titles:
        print(t)