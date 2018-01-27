# -*- coding: utf-8 -*-
# @Date:   2018-01-23 15:26:09
# @Last Modified time: 2018-01-23 15:26:21
import wx


BUFFER_SIZE = 4096
COLOR_RED = wx.Colour(255, 0, 0)
COLOR_BLUE = wx.Colour(30, 144, 255)
COLOR_WHITE = wx.Colour(250, 250, 250)
COLOR_GREEN = wx.Colour(0, 139, 69)


def font(size):
    return wx.Font(
        pointSize=size,
        family=wx.SWISS,
        style=wx.NORMAL,
        weight=wx.BOLD
    )

FONT11 = font(11)
FONT12 = font(12)
FONT13 = font(13)


from .frame import MainFrame
from .message import MessageReceiver
