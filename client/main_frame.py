# -*- coding: utf-8 -*-
# @Date:   2018-01-26 13:23:04
# @Last Modified time: 2018-01-26 13:23:12
from client import wx
from .message import MessageSender
from .controller import NoticeButton, UserListBox, SendButton
from .views import RecordPanel, UserNameText, InputField


class MainSizer(UserListBox, NoticeButton, RecordPanel, InputField, SendButton, UserNameText):

    def __init__(self, panel):
        """
        use BoxSizer to avoid hard-coded widget's pos and size
        """
        self.main_sizer = wx.BoxSizer()
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_top_sizer = wx.BoxSizer()
        config = {
            "object": self.main_sizer,
            "items": [
                {
                    "object": self.left_sizer,
                    "style": {
                        "proportion": 2.5, "border": 5, "flag": wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM
                    },
                    "items": [
                        {
                            "object": self.user_list_box,
                            "style": {
                                "proportion": 10, "border": 0, "flag": wx.EXPAND | wx.ALL
                            }
                        }
                    ]
                }, {
                    "object": self.right_sizer,
                    "style": {
                        "proportion": 7.5, "border": 5, "flag": wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM
                    },
                    "items": [
                        {
                            "object": self.right_top_sizer,
                            "style": {
                                "proportion": 0, "border": 0, "flag": wx.EXPAND | wx.LEFT
                            },
                            "items": [
                                {
                                    "object": self.notice_button,
                                    "style": {
                                        "proportion": 4.5, "border": 240, "flag": wx.EXPAND | wx.RIGHT
                                    }
                                }, {
                                    "object": self.user_name_text,
                                    "style": {
                                        "proportion": 5.5, "border": 0, "flag": wx.EXPAND | wx.LEFT
                                    }
                                }
                            ]
                        }, {
                            "object": self.record_panel,
                            "style": {
                                "proportion": 8, "border": 0, "flag": wx.EXPAND | wx.LEFT | wx.RIGHT
                            }
                        }, {
                            "object": self.input_field,
                            "style": {
                                "proportion": 2, "border": 0, "flag": wx.EXPAND | wx.LEFT | wx.RIGHT
                            }
                        }, {
                            "object": self.send_button,
                            "style": {
                                "proportion": 0, "border": 250, "flag": wx.EXPAND | wx.LEFT | wx.RIGHT
                            }
                        }
                    ]
                }
            ]
        }
        self.layout(config)
        panel.SetSizer(self.main_sizer)

    def layout(self, d):
        if isinstance(d, dict):
            object = d.get("object")
            items = d.get("items")
            for item in items.iteritems():
                object.Add(self.layout(item), **item.get("style"))
            return object


class MainFrame(wx.Frame, MainSizer, MessageSender):
    app = wx.App()

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
        MainSizer.__init__(self, self.panel)
        MessageSender.__init__(self)
        self.Bind(wx.EVT_CLOSE, self.close_window_event)
        self.Show(True)  # TODO == MainFrame().Show()

    def close_window_event(self, e):
        self.logout()
        MainFrame.app.Destroy()  # TODO  noticing
        wx.Exit()                 # TODO  better than exit(0)
