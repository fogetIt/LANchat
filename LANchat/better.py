# -*- coding: utf-8 -*-
# @Date:   2018-01-30 09:54:24
# @Last Modified time: 2018-01-30 09:54:32
import re, math, wx
from LANchat import font, CHINESE_REGEX, RECORD_CHATS_PER_LINE


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
        self.style = wx.TE_MULTILINE | wx.TE_READONLY | wx.BRUSHSTYLE_TRANSPARENT
        self.style = self.style | kwargs.get("style") if kwargs.get("style") else self.style
        kwargs.update(style=self.style)
        self.lines_number = self.get_lines_number(kwargs.get("value", ""))
        super(StaticTextCtrl, self).__init__(*args, **kwargs)
        self.SetFont(font(12))
        self.set_bg_color(kwargs.get("parent"))
        self.set_size()

    @staticmethod
    def get_lines_number(_str):
        lines_number = (len(_str) + len(re.findall(CHINESE_REGEX, _str))) * 0.1 / RECORD_CHATS_PER_LINE
        return math.ceil(lines_number * 10)

    def set_bg_color(self, parent):
        if parent:
            self.SetBackgroundColour(parent.BackgroundColour)

    def set_size(self):
        height = int(self.GetCharHeight() * self.lines_number)
        self.SetMinSize((-1, height))
        self.SetMaxSize((-1, height))
        self.SetSize((-1, height))


class UniqueTuple(tuple):

    def __init__(self, seq=()):
        super(UniqueTuple, self).__init__(set(seq))

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
