import wx
from crawl import *
from crawl_mt import *
from gaugeframe import *
from global_list import *

class MainFrame(wx.Frame):
    def __init__(self, crawl_type):
        wx.Frame.__init__(self, parent=None, id=-1, title='DoubanBookHelper', size=(600, 320))

        self.crawl_type= crawl_type

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
        hlp = wx.Image('../resource/help.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        help_button = wx.BitmapButton(self.left_panel, -1, hlp)
        data = wx.StaticText(self.left_panel, -1, "All data powered by:")
        douban_logo = wx.Image('../resource/doubanBook.jpg',
                wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        douban_button = wx.BitmapButton(self.left_panel, -1, douban_logo)
        logo = wx.Image('../resource/book.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
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
        global PROGRESS_MAX
        key_word = self.key_word_box.GetValue().encode('utf-8')
        if key_word == "":
            box = wx.MessageDialog(None, 'Input something OK?', 'No input detected', wx.OK)
            answer = box.ShowModal()
            box.Destroy()
            return
        if self.crawl_type == '1':
            gauge = GaugeFrame(self, title="0 of " + str(PROGRESS_MAX),
                    maximum=PROGRESS_MAX)
            gauge.Show()
            crawl = Crawl(key_word)
        else:
            gauge = GaugeFrame(self, title="0 of " + str(PROGRESS_MAX*3),
                    maximum=PROGRESS_MAX*3)
            gauge.Show()
            crawl = CrawlMT(key_word)
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
