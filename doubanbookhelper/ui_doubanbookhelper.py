import sys
from mainframe import *

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(sys.argv[1])
    frame.Show()
    app.MainLoop()
