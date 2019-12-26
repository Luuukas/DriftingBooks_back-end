# search book number from DouBan

import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Referer': 'https://www.douban.com/search?cat=1001&q=',
    'Host': 'www.douban.com',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',

}

data = {
    'cat': '1001',
    'q': '',  # 'search_text' 例：'解忧杂货店 东野圭吾 南海出版公司'

}


def get_url_book_number(query):
    data['q'] = query
    html = requests.get('https://www.douban.com/search', headers=headers, params=data)
    bs = etree.HTML(html.text)
    t = (bs.xpath('//*[@class="result-list"]/div[1]/div[1]/a[1]/@onclick')[0])
    # a="moreurl(this,{i: '0', query: '%E5%8F%B2%E8%AE%B0', from: 'dou_search_book', sid: 1836555, qcat: '1001'})"
    book_num = (t.split(',')[-2].strip()[5:])
    url = 'https://book.douban.com/subject/' + book_num + '/'
    return url
