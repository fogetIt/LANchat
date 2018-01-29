# -*- coding: utf-8 -*-
# @Date:   2018-01-28 19:51:21
# @Last Modified time: 2018-01-28 19:55:08
from client import wx
from .layout import Layout


class Views(wx.Frame, Layout):

    def __init__(self):
        """main frame"""
        pos = (300, 50)
        size = (800, 600)
        wx.Frame.__init__(
            self,
            parent=None,
            id=-1,
            name="main",
            title="simple chat client",
            pos=pos,
            size=size,
            style=wx.DEFAULT_FRAME_STYLE
        )
        self.SetMaxSize(size)
        self.SetMinSize(size)
        self.panel = wx.Panel(parent=self, id=1)
        Layout.__init__(self, self.panel)
        self.panel.SetSizer(self.main_sizer)
