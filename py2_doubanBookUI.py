import requests
import time
import sys
import wx
from bs4 import *
from requests.exceptions import *
from urllib import quote

# add utf-8 support
reload(sys)
sys.setdefaultencoding('utf8')

class Crawl():
    def __init__(self, key_word):
        url = "https://book.douban.com/subject_search?search_text="
        self.key_word = key_word
        tag = quote(key_word)
        print tag
        self.url = url + tag 
        self.rankList = []

    def start(self, count, progress_max, keep_going, dialog):
        while count < progress_max:
            wurl = self.url + '&start=' + str(count * 15) 
            try:
                self.getContent(wurl, self.rankList)
                keep_going = dialog.Update(count)
            except Timeout:
                continue
            except HTTPError:
                keep_going = False
                break
            count += 1
        self.export(self.rankList)
        return 

    def getContent(self, url, rankList):
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

    def export(self, rankList):
        sortedList = sorted(rankList, key = lambda k: k['rate'], reverse = True)
        lst = open('booklist of ' + self.key_word, 'w+')
        for item in sortedList:
            lst.write('book title: <<' + item['title'] + '>>' + '\n')
            lst.write('pub info: ' + item['pub']+ '\n')
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
        key_word = self.key_word_box.GetValue().encode('utf-8')
        if key_word == "":
            box = wx.MessageDialog(None, 'Input something OK?', 'No input detected', wx.OK)
            answer = box.ShowModal()
            box.Destroy()
            return
        progress_max = 5
        dialog = wx.ProgressDialog("Processing...", "Time remaining:",
                progress_max,
                style = wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        keep_going = True
        count = 0
        crawl = Crawl(key_word)
        crawl.start(count, progress_max, keep_going, dialog)
        dialog.Destroy()
        box = wx.MessageDialog(None, 'Done!', 
                'Successfully Exported', wx.OK)
        box.ShowModal()
        box.Destroy()

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

if __name__ == '__main__':
    app = wx.App()
    frame = Frame()
    frame.Show()
    app.MainLoop()
