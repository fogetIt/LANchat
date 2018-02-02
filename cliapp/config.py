# -*- coding: utf-8 -*-
# @Date:   2018-02-02 15:16:27
# @Last Modified time: 2018-02-02 15:16:39
import wx


BUFFER_SIZE = 4096
COLOR_RED = wx.Colour(255, 0, 0)
COLOR_BLUE = wx.Colour(30, 144, 255)
COLOR_WHITE = wx.Colour(250, 250, 250)
COLOR_GREEN = wx.Colour(0, 139, 69)
CHINESE_REGEX = u"[\u4e00-\u9fa5]"
MAX_CHAT_RECORD_SIZE = 100
RECORD_CHATS_PER_LINE = 57


def font(size):
    # 1 Chinese == 2 English == 2 digit
    return wx.Font(
        pointSize=size,
        family=wx.SWISS,
        style=wx.NORMAL,
        weight=wx.BOLD
    )


from better import UniqueTuple
NUMBER_ICONS = UniqueTuple(
    (u"⓿", u"➊", u"➋", u"➌", u"➍", u"➎", u"➏", u"➐", u"➑", u"➒", u"➓", u"∞")
)
