# -*- coding: utf-8 -*-
# @Date:   2018-01-27 17:22:26
# @Last Modified time: 2018-01-27 17:22:32
from client import wx, FONT11, COLOR_RED


class Single(object):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Single, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class StaticTextCtrl(wx.TextCtrl):
    """
    StaticText
        默认会在空格处进行切换
        如果没有空格，需要添加'\n'来进行换行
    TextCtrl
        在一行显示满之后自动进行换行，不需要空白字符提示
    """
    def __init__(self, *args, **kwargs):
        kwargs.update(
            style=wx.TE_READONLY | wx.TE_MULTILINE | wx.BORDER_NONE | wx.BRUSHSTYLE_TRANSPARENT
        )
        super(StaticTextCtrl, self).__init__(*args, **kwargs)
        parent = kwargs.get("parent")
        if parent:
            self.SetBackgroundColour(parent.BackgroundColour)


class StaticListDict(tuple):

    def __init__(self, seq=()):
        super(StaticListDict, self).__init__(set(seq))

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


class UnreadListBox(Single):

    def __init__(self):
        self.unread_list_box = wx.ListBox(
            parent=None, id=11, name='unread_list', choices=[], style=wx.LB_SINGLE
        )
        self.unread_list_box.SetFont(FONT11)
        self.unread_list_box.SetForegroundColour(COLOR_RED)


class Tip(Single, wx.MessageDialog):

    def __init__(self, msg):
        super(Tip, self).__init__(
            parent=None,
            message="\n%s" % msg,
            pos=(60, 25),
            style=wx.ICON_EXCLAMATION | wx.OK_DEFAULT
        )

    @staticmethod
    def show(msg):
        Tip(msg).ShowModal()
