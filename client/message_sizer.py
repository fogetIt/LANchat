# -*- coding: utf-8 -*-
# @Last Modified time: 2018-01-24 21:21:12
import wx
import wx.lib.scrolledpanel as scrolled
from client import Single, FONT12


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


class MessageStore(Single):

    def __init__(self):
        self.max_size = 100
        self.message_store = {}

    def add_message_store(self, name, record):
        message_list = self.message_store.get(name)
        if not message_list:
            self.message_store.update({name: []})
        elif len(message_list) >= self.max_size:
            message_list.pop(0)
        message_list.append(record)

    def reduce_message_store(self, name):
        self.message_store.pop(name)


class MessageSizer(MessageStore):

    def __init__(self, panel):
        MessageStore.__init__(self)
        self.message_sizer = wx.BoxSizer(wx.VERTICAL)
        self.message_panel = scrolled.ScrolledPanel(
            parent=panel, id=30, style=wx.SIMPLE_BORDER
        )
        self.message_panel.SetSizer(self.message_sizer)

    def create_chat_record(self, name, value, is_self=True):
        record = StaticTextCtrl(parent=self.message_panel, value=value)
        record.SetFont(FONT12)
        if is_self:
            self.message_sizer.Add(
                record, proportion=0, border=150, flag=wx.EXPAND | wx.LEFT
            )
        else:
            self.message_sizer.Add(
                record, proportion=0, border=150, flag=wx.EXPAND | wx.RIGHT
            )
        record.Hide()
        self.add_message_store(name, record)

    def show_chat_records(self, name):
        """
        销毁 message_panel 的所有子对象
        self.message_panel.RemoveChild() 销毁后的子对象，不能再 ADD()
        """
        self.message_panel.DestroyChildren()
        self.message_sizer.Clear(deleteWindows=False)
        message_list = self.message_store.get(name)
        if message_list:
            for i in message_list:
                i.Show()
            self.message_panel.SetupScrolling()
