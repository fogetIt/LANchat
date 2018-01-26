# -*- coding: utf-8 -*-
# @Date:   2018-01-26 13:23:04
# @Last Modified time: 2018-01-26 13:23:12
import wx
from .sizer import Sizer
from .views import MessageSender


class MainFrame(wx.Frame, Sizer):

    def __init__(self):
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
        Sizer.__init__(self, self.panel)
        self.Show(True)  # TODO == MainFrame().Show()

    def show_tip(self, msg):
        self.tip = wx.MessageDialog(
            parent=None,
            message="\n%s" % msg,
            pos=(60, 25),
            style=wx.ICON_EXCLAMATION | wx.OK_DEFAULT
        )
        self.tip.ShowModal()


class MainWindow(MainFrame, MessageSender):
    app = wx.App()

    def __init__(self):
        MainFrame.__init__(self)
        MessageSender.__init__(self)

        self.Bind(wx.EVT_CLOSE, self.close_window_event)
        self.user_list_box.Bind(wx.EVT_LEFT_UP, self.choose_user_event)
        self.send_button.Bind(wx.EVT_BUTTON, self.send_message_event)

    def close_window_event(self, e):
        self.logout()
        MainWindow.app.Destroy()  # TODO  noticing
        wx.Exit()                 # TODO  better than exit(0)

    def send_message_event(self, e):
        value = self.input_field.GetValue().strip()
        if not self.selected_user:
            self.show_tip(u"未选择用户")
        elif not value:
            self.show_tip(u"发送信息为空")
        elif self.selected_user == "group":
            if self.user_list_box.GetItems():
                self.group(value)
                self.create_chat_record("group", value)
                self.show_chat_records(self.selected_user)
            else:
                self.show_tip(u"群聊为空")
        else:
            self.private(value, self.selected_user)
            self.create_chat_record(self.selected_user, value)
            self.show_chat_records(self.selected_user)

    def choose_user_event(self, e):
        if self.user_list_box.GetItems():
            self.selected_user = self.user_list_box.GetStringSelection()
            n = self.user_list_box.GetSelection()
            if n != -1:
                self.user_name_text.SetLabel(self.selected_user)
                self.show_chat_records(self.selected_user)
