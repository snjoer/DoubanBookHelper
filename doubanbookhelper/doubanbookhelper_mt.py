import sys
import time
import requests
import threading
from bs4 import *
from export import *
from urllib import quote
from requests.exceptions import *

reload(sys)
sys.setdefaultencoding('utf8')

lock = threading.Lock()

def getContent(url, index, rankList):
    i = 0
    while i < 10:
        wurl = url + '&start=' + str(index * 15)
        try:
            page = requests.get(wurl, timeout=1).text
            print "connected"
        except Timeout:
            print "connecting error..."
            continue
        except HTTPError:
            break;
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
            lock.acquire()
            try:
                rankList.append(dic)
            finally:
                lock.release()
        index += 1
        i += 1

if __name__ == '__main__':
    url = "https://book.douban.com/subject_search?search_text="
    key_word = raw_input('key word:')
    tag = quote(key_word.encode('utf-8'))
    url = url + tag
    rankList = []
    index = 0
    thread0 = threading.Thread(target = getContent, args = (url, index, rankList))
    index += 10
    thread1 = threading.Thread(target = getContent, args = (url, index, rankList))
    index += 10
    thread2 = threading.Thread(target = getContent, args = (url, index, rankList))
    thread0.start()
    thread1.start()
    thread2.start()
    thread0.join()
    thread1.join()
    thread2.join()
    export(rankList, key_word)
