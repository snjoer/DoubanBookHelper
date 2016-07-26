#-*- coding: utf-8 -*-

from bs4 import *
from urllib import urlopen
from urllib import pathname2url
from urllib2 import HTTPError
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def getContent(url, rankList):
    page = urlopen(url)
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

def export(rankList):
    sortedList = sorted(rankList, key = lambda k: k['rate'], reverse = True)
    lst = open('booklist of ' + text, 'w+')
    for item in sortedList:
        lst.write('book title: <<' + item['title'] + '>>' + '\n')
        lst.write('pub info: ' + item['pub']+ '\n')
        lst.write('rate: ' + str(item['rate']) + ' ')
        lst.write(item['read'])
        lst.write('\n\n')

url = "https://book.douban.com/subject_search?search_text="
text = raw_input('key word:')
tag = pathname2url(text)
url = url + tag
rankList = []
index = 0
while index < 3:
    wurl = url + '&start=' + str(index * 15)
    try:
        getContent(wurl, rankList)
    except HTTPError:
        break
    index += 1
export(rankList)
