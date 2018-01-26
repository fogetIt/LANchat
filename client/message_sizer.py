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
        self.user_record_dict = {}
        self.unread_dict = {}
        self.selected_user = u""
        self.user_list = []

    def add_record(self, user, record, is_selected_user=False):
        if not is_selected_user:
            unread_num = int(self.unread_dict.get(user, 0))
            self.unread_dict.update({user: unread_num + 1})
        record_list = self.user_record_dict.get(user)
        if not record_list:
            self.user_record_dict.update({user: []})
        elif len(record_list) >= self.max_size:
            record_list.pop(0)
        record_list.append(record)

    def reduce_record(self, user):
        if not self.unread_dict.get(user):
            self.user_record_dict.pop(user)

    def get_record(self, user):
        unread_num = int(self.unread_dict.get(user, 0))
        record_list = self.user_record_dict.get(user)
        return unread_num, record_list


class MessageSizer(MessageStore):

    def __init__(self, panel):
        MessageStore.__init__(self)
        self.message_sizer = wx.BoxSizer(wx.VERTICAL)
        self.message_panel = scrolled.ScrolledPanel(
            parent=panel, id=30, style=wx.SIMPLE_BORDER
        )
        self.message_panel.SetSizer(self.message_sizer)

    def create_chat_record(self, user, value, is_self=True):
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
        is_selected_user = user == self.selected_user
        self.add_record(user, record, is_selected_user)

    def show_chat_records(self, user):
        """
        销毁 message_panel 的所有子对象
        self.message_panel.RemoveChild() 销毁后的子对象，不能再 ADD()
        """
        self.message_panel.DestroyChildren()
        self.message_sizer.Clear(deleteWindows=False)
        unread_num, record_list = self.get_record(user)
        if record_list:
            for i in record_list:
                i.Show()
            self.message_panel.SetupScrolling()
        if user not in self.user_list:
            pass
