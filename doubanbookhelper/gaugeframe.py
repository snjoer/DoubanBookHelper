import wx

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
