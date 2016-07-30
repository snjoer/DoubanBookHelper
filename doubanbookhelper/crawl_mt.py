import wx
import sys
import requests
import threading
from export import *
from urllib import quote
from global_list import *
from bs4 import BeautifulSoup
from requests.exceptions import *

reload(sys)
sys.setdefaultencoding('utf8')

lock = threading.Lock()

class CrawlMT():
    def __init__(self, key_word):
        url = "https://book.douban.com/subject_search?search_text="
        self.key_word = key_word
        tag = quote(key_word.encode('utf-8'))
        self.url = url + tag
        self.rankList = []

    def start(self, gauge):
        global counter
        index = 0
        counter = 0
        thread0 = threading.Thread(target = self.getContent, args = (index, gauge))
        index += 10
        thread1 = threading.Thread(target = self.getContent, args = (index, gauge))
        index += 10
        thread2 = threading.Thread(target = self.getContent, args = (index, gauge))
        thread0.start()
        thread1.start()
        thread2.start()
        thread0.join()
        thread1.join()
        thread2.join()
        if gauge.isValid() == True:
            export(self.rankList, self.key_word)
            box = wx.MessageDialog(None, 'Done!', 'Successfully Exported', wx.OK)
            box.ShowModal()
            box.Destroy()
        gauge.Destroy()

    def getContent(self, index, gauge):
        i = 0
        global counter
        while i < PROGRESS_MAX and gauge.isValid() == True:
            wurl = self.url + '&start=' + str(index * 15)
            try:
                page = requests.get(wurl, timeout=1).text
            except Timeout:
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
                    self.rankList.append(dic)
                finally:
                    lock.release()
            lock.acquire()
            try:
                counter += 1
                wx.CallAfter(gauge.UpdateGauge, counter, "%i of %i"%(counter, PROGRESS_MAX*3))
            finally:
                lock.release()
            index += 1
            i += 1
