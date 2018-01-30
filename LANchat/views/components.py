# -*- coding: utf-8 -*-
# @Last Modified time: 2018-01-24 21:21:12
import wx
import wx.lib.scrolledpanel as scrolled
from LANchat import (
    wx, font, COLOR_BLUE, COLOR_RED, COLOR_WHITE, COLOR_GREEN
)
from ..better import Single


class UserListBox(Single):

    def __init__(self, panel):
        self.user_list_box = wx.ListBox(
            parent=panel, id=11, name='user_list', choices=[], style=wx.LB_SINGLE
        )
        self.user_list_box.SetFont(font(12))
        self.user_list_box.SetForegroundColour(COLOR_WHITE)
        self.user_list_box.SetBackgroundColour(COLOR_GREEN)
        self.user_list_box.Insert("group", 0)


class UserNameText(Single):

    def __init__(self, panel):
        self.user_name_text = wx.StaticText(
            parent=panel, id=12, size=(0, 30), label="", style=wx.ALIGN_CENTER
        )
        self.user_name_text.SetFont(font(13))
        self.user_name_text.SetForegroundColour(COLOR_BLUE)


class NoticeButton(Single):

    def __init__(self, panel):
        """♡ ♥"""
        self.notice_button = wx.Button(
            parent=panel, id=13, size=(0, 30), label=u"⓿", style=wx.ALIGN_LEFT
        )
        self.notice_button.SetFont(font(13))
        self.notice_button.SetForegroundColour(COLOR_BLUE)
        self.notice_button.Enable(False)


class RecordPanel(Single):

    def __init__(self, panel):
        self.record_sizer = wx.BoxSizer(wx.VERTICAL)
        self.record_panel = scrolled.ScrolledPanel(
            parent=panel, id=14, style=wx.SIMPLE_BORDER
        )
        self.record_panel.SetSizer(self.record_sizer)


class InputField(Single):

    def __init__(self, panel):
        self.input_field = wx.TextCtrl(
            parent=panel, id=15, value="", style=wx.TE_MULTILINE | wx.TE_RICH2
        )
        self.input_field.SetFont(font(12))


class SendButton(Single):

    def __init__(self, panel):
        self.send_button = wx.Button(
            parent=panel, id=16, size=(0, 40), label=u"发送"
        )
        self.send_button.SetFont(font(13))


class Tip(Single):

    def show_tip(self, msg):
        self.tip = wx.MessageDialog(
            parent=None,
            message="\n%s" % msg,
            caption="warning",
            pos=(60, 25),
            style=wx.ICON_EXCLAMATION | wx.OK_DEFAULT
        )
        self.tip.ShowModal()
        # self.tip.Destroy()


class UnreadTip(Single):

    def __init__(self, panel):
        """
        Don't use any fix sizes, use sizer and then call .Fit() on the Dialog, Panel or Frame.
        """
        self.unread_tip = wx.Dialog(
            parent=panel,
            id=2,
            title=u"未读消息",
        )
        self.unread_sizer = wx.BoxSizer()
        self.unread_tip.SetSizer(self.unread_sizer)

        self.unread_list_box = wx.ListBox(
            parent=self.unread_tip, id=21, name='unread_list', choices=[], style=wx.LB_SINGLE
        )
        self.unread_list_box.SetFont(font(11))
        self.unread_list_box.SetForegroundColour(COLOR_RED)

        self.unread_sizer.Add(self.unread_list_box, proportion=10, border=10, flag=wx.EXPAND | wx.ALL)
        self.unread_sizer.Fit(self.unread_tip)

    def show_unread_tip(self):
        self.unread_tip.ShowModal()
        self.unread_tip.Close()

    def close_unread_tip(self):
        self.unread_tip.Close()


class Components(UserListBox, NoticeButton, UserNameText, RecordPanel, InputField, SendButton, Tip, UnreadTip):

    def __init__(self, panel):
        UserListBox.__init__(self, panel)
        NoticeButton.__init__(self, panel)
        UserNameText.__init__(self, panel)
        RecordPanel.__init__(self, panel)
        InputField.__init__(self, panel)
        SendButton.__init__(self, panel)
        UnreadTip.__init__(self, panel)
