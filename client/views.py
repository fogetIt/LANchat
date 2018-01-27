# -*- coding: utf-8 -*-
# @Last Modified time: 2018-01-24 21:21:12
import wx.lib.scrolledpanel as scrolled
from client import (
    wx, FONT11, FONT12, FONT13, COLOR_BLUE, COLOR_RED
)
from .utils import Single, StaticTextCtrl
from .models import RecordStore


class RecordPanel(RecordStore):

    def __init__(self, panel):
        super(RecordPanel, self).__init__()
        self.record_sizer = wx.BoxSizer(wx.VERTICAL)
        self.record_panel = scrolled.ScrolledPanel(
            parent=panel, id=30, style=wx.SIMPLE_BORDER
        )
        self.record_panel.SetSizer(self.record_sizer)

    def create_record_sizer(self, user, value, is_self=True):
        record = StaticTextCtrl(parent=self.record_panel, value=value)
        record.SetFont(FONT12)
        if is_self:
            self.record_sizer.Add(
                record, proportion=0, border=150, flag=wx.EXPAND | wx.LEFT
            )
        else:
            self.record_sizer.Add(
                record, proportion=0, border=150, flag=wx.EXPAND | wx.RIGHT
            )
        record.Hide()
        self.add_record(user, record)

    def refresh_records_panel(self, user):
        """
        Destroy record_panel's sub object, and try to reduce record.
        self.record_panel.RemoveChild()  # 销毁后的子对象，不能再 Add()
        """
        self.record_panel.DestroyChildren()
        self.record_sizer.Clear(deleteWindows=False)
        unread_num, record_list = self.get_record(user)
        if record_list:
            for i in record_list:
                i.Show()
            self.record_panel.SetupScrolling()
        self.reduce_record(user)


class UserNameText(Single):

    def __init__(self, panel):
        self.user_name_text = wx.StaticText(
            parent=panel, id=22, size=(0, 30), label="", style=wx.ALIGN_CENTER
        )
        self.user_name_text.SetFont(FONT13)
        self.user_name_text.SetForegroundColour(COLOR_BLUE)


class UnreadListBox(Single):

    def __init__(self, panel):
        self.unread_list_box = wx.ListBox(
            parent=panel, id=11, name='unread_list', choices=[], style=wx.LB_SINGLE
        )
        self.unread_list_box.SetFont(FONT11)
        self.unread_list_box.SetForegroundColour(COLOR_RED)


class InputField(Single):
    def __init__(self, panel):
        self.input_field = wx.TextCtrl(
            parent=panel, id=23, value="", style=wx.TE_MULTILINE | wx.TE_RICH2
        )
        self.input_field.SetFont(FONT12)
