# -*- coding: utf-8 -*-
# @Date:   2018-01-26 18:16:19
# @Last Modified time: 2018-01-26 18:16:36
from client import wx, Single, FONT13, COLOR_RED, COLOR_BLUE


class StaticListMap(tuple):

    def __init__(self, seq=()):
        super(StaticListMap, self).__init__(set(seq))

    def get(self, i):
        try:
            return None if i < 0 else self.__getitem__(i)
        except Exception as e:
            print(e)
            return None

    def inv_get(self, value):
        try:
            return self.index(value)
        except Exception as e:
            print(e)
            return None


class NumberIcons(Single):

    def __init__(self):
        self.number_icons = StaticListMap(
            [u"⓿", u"➊", u"➋", u"➌", u"➍", u"➎", u"➏", u"➐", u"➑", u"➒", u"➓", u"∞"]
        )

    def get_icon(self, i):
        if i > len(self.number_icons):
            i = len(self.number_icons) - 1
        return self.number_icons.get(i)


class NoticeButton(NumberIcons):

    def __init__(self, panel):
        """
        ♡ ♥
        """
        super(NoticeButton, self).__init__()
        self.notice_button = wx.Button(
            parent=panel, id=21, size=(0, 30), label=u"⓿", style=wx.ALIGN_LEFT
        )
        self.notice_button.SetFont(FONT13)
        self.notice_button.SetForegroundColour(COLOR_BLUE)

    def set_notice_icon(self, label):
        if label == u"♥":
            self.notice_button.SetForegroundColour(COLOR_RED)
        self.notice_button.SetLabel(label)
