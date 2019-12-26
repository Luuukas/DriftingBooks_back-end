import requests
from lxml import etree
from search import get_url_book_number

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


def get_img(et):  # 封面图
    t = (et.xpath('//*[@id="mainpic"]/a/img')[0])
    if t == []:
        img = '无'
        return img
    else:
        img = t.xpath('@src')[0]
        return img


def get_content_intro(et):  # 内容简介
    content = ''
    q = et.xpath('//div[@class="intro"]')[0]
    t = (q.xpath('p'))
    if t == []:
        content = '无'
        return content
    else:
        for i in t:
            if (i.text is not None):
                content = content + i.text + '\n'
        return content


def get_author_intro(et):  # 作者简介
    author = ''
    t = et.xpath('//div[@class="indent "]/div[1]/div[1]/p')
    if t == []:
        author = '无'
        return author
    else:
        for i in t:
            author = author + i.text + '\n'
        return author


def get_book_info(book_name, writer, press):
    q = book_name + ' ' + writer + ' ' + press
    url = get_url_book_number(q)
    html = requests.get(url, headers=headers)  # 'https://book.douban.com/subject/25862578/'
    bs = etree.HTML(html.text)

    img = get_img(bs)
    content_intro = get_content_intro(bs)
    author_intro = get_author_intro(bs)

    book = {
        'img': img,
        'content_intro': content_intro,
        'author_intro': author_intro,
    }

    return book


# book = get_book_info('活着', '余华', '')
# print('封面图：\n'+book['img'])
# print('内容简介：\n'+book['content_intro'])
# print('作者简介：\n'+book['author_intro'])
