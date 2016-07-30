import requests
import time
import sys
from bs4 import *
from export import export
from urllib import quote
from requests.exceptions import *

reload(sys)
sys.setdefaultencoding('utf8')

def getContent(url, rankList):
    page = requests.get(url, timeout=1).text
    bs = BeautifulSoup(page, 'html.parser')
    ls = bs.findAll('li', class_ = 'subject-item')
    for item in ls:
        title = ' '.join(item.h2.text.split())
        pubinfo = ' '.join(item.find(class_ = 'pub').text.split())
        try:
            pl = ' '.join(item.find(class_ = 'pl').text.split())
        except AttributeError:
            pl = ' '.join(item.find(class_ = 'sub-count').text.split())
        try:
            rate = float(item.find(class_ = 'rating_nums').text)
        except AttributeError:
            rate = 0
        dic = {'title': title, 'pub': pubinfo, 'read': pl, 'rate': rate}
        rankList.append(dic)

if __name__ == '__main__':
    url = "https://book.douban.com/subject_search?search_text="
    key_word = raw_input('key word:')
    tag = quote(key_word)
    url = url + tag
    rankList = []
    index = 0
    while index < 3:
        wurl = url + '&start=' + str(index * 15)
        try:
            getContent(wurl, rankList)
        except Timeout:
            continue
        except HTTPError:
            break
        index += 1
    export(rankList, key_word)
