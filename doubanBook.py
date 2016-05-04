from selenium import *
from bs4 import *
from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import *
import time

def getContent(url, rankList):
    page = urlopen(url)
    bs = BeautifulSoup(page, 'lxml')
    ls = bs.findAll('li', class_ = 'subject-item')
    for item in ls:
        title = ' '.join(item.h2.text.split())
        try:
            pl = ' '.join(item.find(class_ = 'pl').text.split())
        except AttributeError:
            pl = ' '.join(item.find(class_ = 'sub-count').text.split())
        try:
            rate = float(item.find(class_ = 'rating_nums').text)
        except AttributeError:
            rate = 0
        dic = {'title': title, 'read': pl, 'rate': rate}
        rankList.append(dic)

def export(rankList):
    sortedList = sorted(rankList, key = lambda k: k['rate'], reverse = True)
    lst = open('booklist' + text, 'w+')
    for item in sortedList:
        lst.write('book title: <<' + item['title'] + '>>' + '\n')
        lst.write('rate: ' + str(item['rate']) + ' ')
        lst.write(item['read'])
        lst.write('\n\n')

url = "https://book.douban.com/subject_search?search_text="
text = input('key word:')
tag = quote(text)
url = url + tag
rankList = []
index = 0
while index < 10:
    wurl = url + '&start=' + str(index * 15)
    try:
        getContent(wurl, rankList)
    except HTTPError:
        break
    index += 1
export(rankList)
