import wx
import sys
import time
import requests
import threading
from urllib import quote
from bs4 import BeautifulSoup
from requests.exceptions import *
reload(sys)
sys.setdefaultencoding('utf8')

lock = threading.Lock()

PROGRESS_MAX = 10
counter = 0

class Crawl():
    def __init__(self, key_word):
        url = "https://book.douban.com/subject_search?search_text="
        self.key_word = key_word
        tag = quote(key_word.encode('utf-8'))
        self.url = url + tag 
        self.rankList = []

    def start(self, gauge):
        index = 0 
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
        gauge.Destroy()
        if gauge.isValid:
            self.export()
            box = wx.MessageDialog(None, 'Done!', 'Successfully Exported', wx.OK)
            box.ShowModal()
            box.Destroy()

    def getContent(self, index, gauge):
        i = 0
        global counter
        while i < PROGRESS_MAX and gauge.isValid() == True:
            wurl = self.url + '&start=' + str(index * 15)
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

    def export(self):
        sortedList = sorted(self.rankList, key = lambda k: k['rate'], reverse = True)
        lst = open('booklist of ' + self.key_word, 'w+')
        for item in sortedList:
            lst.write('book titile: <<' + item['title'] + '>>' + '\n')
            lst.write('pub info: ' + item['pub'] + '\n')
            lst.write('rate: ' + str(item['rate']) + ' ')
            lst.write(item['read'])
            lst.write('\n\n')

class Frame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='doubanBookHelper'):
        wx.Frame.__init__(self, parent, id, title, size=(600, 320))

        self.panel = wx.Panel(self)
        self.left_panel = wx.Panel(self.panel)
        self.right_panel = wx.Panel(self.panel)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.GridBagSizer(6, 6)
        right_sizer =wx.GridBagSizer(5, 5)
        self.panel.SetSizer(sizer)
        self.left_panel.SetSizer(left_sizer)
        self.right_panel.SetSizer(right_sizer)
        prompt = wx.StaticText(self.left_panel, 
                label='Input key words, press START to search!')
        self.key_word_box = wx.TextCtrl(self.left_panel,
                style=wx.TE_PROCESS_ENTER)
        start_button = wx.Button(self.left_panel, label='Start!')
        exit_button = wx.Button(self.left_panel, label='Exit')
        hlp = wx.Image('help.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap() 
        help_button = wx.BitmapButton(self.left_panel, -1, hlp)
        data = wx.StaticText(self.left_panel, -1, "All data powered by:")
        douban_logo = wx.Image('doubanBook.jpg', 
                wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        douban_button = wx.BitmapButton(self.left_panel, -1, douban_logo)
        logo = wx.Image('book.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        logo_button = wx.BitmapButton(self.right_panel, -1, logo)

        sizer.Add(self.left_panel)
        sizer.Add(self.right_panel)
        left_sizer.Add(prompt, (1, 1))
        left_sizer.Add(self.key_word_box, (2, 1))
        left_sizer.Add(start_button, (4, 1))
        left_sizer.Add(exit_button, (5, 1))
        left_sizer.Add(help_button, (6, 1))
        left_sizer.Add(data, (7, 1))
        left_sizer.Add(douban_button, (8, 1))
        right_sizer.Add(logo_button, (1, 1))

        self.Bind(wx.EVT_BUTTON, self.startToSearch, start_button)
        self.Bind(wx.EVT_BUTTON, self.exit, exit_button)
        self.Bind(wx.EVT_BUTTON, self.displayInfo, logo_button)
        self.Bind(wx.EVT_BUTTON, self.displayHelp, help_button)
        self.Bind(wx.EVT_BUTTON, self.displayDouban, douban_button)
        
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnter, self.key_word_box)

    def startToSearch(self, event):
        key_word = self.key_word_box.GetValue()
        if key_word == "":
            box = wx.MessageDialog(None, 'Input something OK?', 'No input detected', wx.OK)
            answer = box.ShowModal()
            box.Destroy()
            return
        global counter
        counter = 0
        gauge = GaugeFrame(self, title="0 of " + str(PROGRESS_MAX*3), maximum=PROGRESS_MAX*3)
        gauge.Show()
        crawl = Crawl(key_word)
        working_thread = threading.Thread(target=crawl.start, args=(gauge,))
        working_thread.start()

    def exit(self, event):
        self.Destroy()
    
    def onEnter(self, event):
        self.startToSearch(wx.EVT_BUTTON)

    def displayInfo(self, event):
        box = wx.MessageDialog(None,
                "Author: Rafael Cheng\
                \nContact: rafaelcheng13@gmail.com",
                "About...", wx.OK)
        box.ShowModal()
         
    def displayHelp(self, event):
        box = wx.MessageDialog(None,
                "1. Input book info you want to query.\
                 \n2. Press START to start searching.\
                 \n3. Book list will be output as a txt file.\
                 \nFor more information, check help document:)",
                "Helper", wx.OK)
        box.ShowModal()

    def displayDouban(self, event):
        box = wx.MessageDialog(None, 
                "For more book information, check: https://book.douban.com",
                "About book.douban", wx.OK)
        box.ShowModal()

class GaugeFrame(wx.Frame):
    def __init__(self, parent, title, maximum):
        wx.Frame.__init__(self, parent, -1, title=title, size=(300, 80))
        self.bar = wx.Gauge(self, range=maximum, size=(300, 20))
        self.button_cancel = wx.Button(self, label='Cancel')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.bar)
        sizer.Add(self.button_cancel, flag=wx.CENTER)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.onCncel, self.button_cancel)
        self.validity = True
    
    def UpdateGauge(self, value, message=""):
        self.bar.SetValue(value)
        if message != "":
            self.SetTitle(message)

    def onCncel(self, event):
        self.SetTitle("Cancelling...")
        self.validity = False

    def isValid(self):
        return self.validity

if __name__ == '__main__':
    app = wx.App()
    frame = Frame()
    frame.Show()
    app.MainLoop()
