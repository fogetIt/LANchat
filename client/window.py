# -*- coding: utf-8 -*-
# @Date:   2018-01-26 13:23:04
# @Last Modified time: 2018-01-26 13:23:12
from client import wx
from .message import MessageSender
from .controller import NoticeButton, UserListBox, SendButton
from .views import RecordPanel, UserNameText, InputField


class LeftSizer(UserListBox):

    def __init__(self, panel):
        """
        use BoxSizer to avoid hard-coded widget's pos and size
        """
        UserListBox.__init__(self, panel)
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.left_sizer.Add(
            self.user_list_box, proportion=10, border=0, flag=wx.EXPAND | wx.ALL
        )


class RightTopSizer(NoticeButton, UserNameText):

    def __init__(self, panel):
        NoticeButton.__init__(self, panel)
        UserNameText.__init__(self, panel)
        self.right_top_sizer = wx.BoxSizer()
        self.right_top_sizer.Add(
            self.notice_button, proportion=4.5, border=240, flag=wx.EXPAND | wx.RIGHT
        )
        self.right_top_sizer.Add(
            self.user_name_text, proportion=5.5, border=0, flag=wx.EXPAND | wx.LEFT
        )


class RightSizer(RightTopSizer, RecordPanel, InputField, SendButton):

    def __init__(self, panel):
        InputField.__init__(self, panel)
        SendButton.__init__(self, panel)
        RecordPanel.__init__(self, panel)
        RightTopSizer.__init__(self, panel)

        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer.Add(
            self.right_top_sizer, proportion=0, border=0, flag=wx.EXPAND | wx.LEFT
        )
        self.right_sizer.Add(
            self.record_panel, proportion=8, border=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT
        )
        self.right_sizer.Add(
            self.input_field, proportion=2, border=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT,
        )
        self.right_sizer.Add(
            self.send_button, proportion=0, border=250, flag=wx.EXPAND | wx.LEFT | wx.RIGHT,
        )


class Sizer(LeftSizer, RightSizer):

    def __init__(self, panel):
        LeftSizer.__init__(self, panel)
        RightSizer.__init__(self, panel)

        self.main_sizer = wx.BoxSizer()
        self.main_sizer.Add(
            self.left_sizer, proportion=2.5, border=5, flag=wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM
        )
        self.main_sizer.Add(
            self.right_sizer, proportion=7.5, border=5, flag=wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM
        )
        panel.SetSizer(self.main_sizer)


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

    def close_window_event(self, e):
        self.logout()
        MainWindow.app.Destroy()  # TODO  noticing
        wx.Exit()                 # TODO  better than exit(0)
