# -*- coding: utf-8 -*-
# @Date:   2018-01-26 18:16:19
# @Last Modified time: 2018-01-26 18:16:36
from client import wx, Single, FONT13, COLOR_RED


class ListMap(list):

    def get(self, i):
        try:
            return self.__getitem__(i)
        except Exception as e:
            print(e)
            return None


class NumberMap(Single):

    def __init__(self):
        self.number_icons = ["⓿", "➊", "➋", "➌", "➍", "➎", "➏", "➐", "➑", "➒", "➓"]


class NoticeButton(Single):

    def __init__(self, panel):
        """♡ ♥"""
        self.notice_button = wx.Button(
            parent=panel, id=21, size=(0, 30), label=u"⓿", style=wx.ALIGN_LEFT
        )
        self.notice_button.SetFont(FONT13)

    def set_notice_icon(self, label):
        if label == u"♥":
            self.notice_button.SetForegroundColour(COLOR_RED)
        self.notice_button.SetLabel(label)
