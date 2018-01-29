# -*- coding: utf-8 -*-
# @Date:   2018-01-23 15:26:09
# @Last Modified time: 2018-01-23 15:26:21
import wx
import socket


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


class Single(object):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Single, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class Client(Single):

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(1)
        self.user_name = socket.gethostname()


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


from .controller import Controller
