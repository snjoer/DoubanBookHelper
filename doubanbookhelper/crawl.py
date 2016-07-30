import wx
import sys
from export import *
from urllib import quote
from doubanbookhelper import *
from global_list import PROGRESS_MAX

class Crawl():
    def __init__(self, key_word):
        url = "https://book.douban.com/subject_search?search_text="
        self.key_word = key_word
        tag = quote(key_word)
        self.url = url + tag 
        self.rankList = []
    
    def start(self, gauge):
        global PROGRESS_MAX
        count = 0 
        while count < PROGRESS_MAX and gauge.isValid() == True:
            wurl = self.url + '&start=' + str(count * 15) 
            try:
                getContent(wurl, self.rankList)
            except Timeout:
                continue
            except HTTPError:
                break
            wx.CallAfter(gauge.UpdateGauge, count, "%i of %i"%(count, PROGRESS_MAX))
            count += 1
        if gauge.isValid() == True:
            export(self.rankList, self.key_word)
            box = wx.MessageDialog(None, 'Done!', 'Successfully Exported', wx.OK)
            box.ShowModal()
            box.Destroy()
        gauge.Destroy()
