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
        self.record_value = kwargs.get("value", "").decode("utf-8")
        STYLE = wx.TE_MULTILINE | wx.TE_READONLY | wx.BRUSHSTYLE_TRANSPARENT
        style = STYLE | kwargs.get("style") if kwargs.get("style") else STYLE
        kwargs.update(style=style)
        #: decode network transmitted ascii string to utf-8 string
        super(StaticTextCtrl, self).__init__(*args, **kwargs)
        self.SetFont(font(12))
        self.set_bg_color(kwargs.get("parent"))
        self.set_size()

    @property
    def lines_number(self):
        lines_number = (
                               len(self.record_value) +
                               (len(re.findall(CHINESE_REGEX, self.record_value)) * 1.0) +
                               (self.record_value.count(u"\t") * 3.0) -
                               self.record_value.count(u"\n")
                       ) / RECORD_CHATS_PER_LINE + self.record_value.count(u"\n")
        return math.ceil(lines_number)

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
