# -*- coding: utf-8 -*-
# @Date:   2018-01-28 19:51:47
# @Last Modified time: 2018-01-28 19:51:58
import wx
from .components import Components


class Layout(Components):

    def __init__(self, panel):
        """
        use BoxSizer to avoid hard-coded widget's pos and size
        """
        super(Layout, self).__init__(panel)
        self.main_sizer = wx.BoxSizer()
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.layout({
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
                                        "proportion": 4.5, "border": 230, "flag": wx.EXPAND | wx.RIGHT
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
        })

    def layout(self, d):
        if isinstance(d, dict):
            object = d.get("object")
            items = d.get("items", [])
            for item in items:
                object.Add(self.layout(item), **item.get("style"))
            return object
