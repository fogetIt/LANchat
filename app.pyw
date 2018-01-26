# -*- coding: utf-8 -*-
# @Date:   2018-01-25 17:00:02
# @Last Modified time: 2018-01-25 17:00:22
import json
from threading import Thread
from wx.lib.pubsub import pub
from client.frame import wx, MainFrame
from client import Client


BUFFER_SIZE = 4096


class MainWindow(Client, MainFrame):
    app = wx.App()

    def __init__(self):
        Client.__init__(self)
        MainFrame.__init__(self)
        self.choiced_user = u""

        self.Bind(wx.EVT_CLOSE, self.close_window_event)
        self.user_list_box.Bind(wx.EVT_LEFT_UP, self.choose_user_event)
        self.send_button.Bind(wx.EVT_BUTTON, self.send_message_event)

        pub.subscribe(self.pub_sender, "pub_sender")
        pub.subscribe(self.pub_user_list, "pub_user_list")

    def close_window_event(self, e=None):
        self.logout()
        MainWindow.app.Destroy()  # TODO  noticing
        wx.Exit()                 # TODO  better than exit(0)

    def send_message_event(self, e):
        value = self.input_field.GetValue().strip()
        if not self.choiced_user:
            self.show_tip(u"未选择用户")
        elif not value:
            self.show_tip(u"发送信息为空")
        elif self.choiced_user == "group":
            if self.user_list_box.GetItems():
                self.group(value)
                self.create_chat_record("group", value)
                self.show_chat_records(self.choiced_user)
            else:
                self.show_tip(u"群聊为空")
        else:
            self.private(value, self.choiced_user)
            self.create_chat_record(self.choiced_user, value)
            self.show_chat_records(self.choiced_user)

    def choose_user_event(self, e):
        if self.user_list_box.GetItems():
            self.choiced_user = self.user_list_box.GetStringSelection()
            n = self.user_list_box.GetSelection()
            if n != -1:
                self.user_name_text.SetLabel(self.choiced_user)
                self.show_chat_records(self.choiced_user)

    def pub_sender(self, sender):
        self.find_sender = self.user_list_box.FindString(sender)

    def pub_user_list(self):
        self.user_list = [user for user in self.user_list_box.GetItems()]


class GUI(Thread, MainWindow):

    def __init__(self, host, port):
        Thread.__init__(self)
        MainWindow.__init__(self)
        self.login(host, port)

    def run(self):
        MainWindow.app.MainLoop()


class REPL(Thread, Client, MainWindow):

    def __init__(self, window):
        Thread.__init__(self)
        Client.__init__(self)
        # self.window = window
        self.window = MainWindow()

    def private_handler(self, message_dict):
        sender = message_dict.get("sender")
        choiced_user = self.window.choiced_user
        wx.CallAfter(
            self.window.add_message_store,
            sender,
            message_dict.get("ext_data")
        )
        if choiced_user == sender:
            wx.CallAfter(
                self.window.show_chat_records,
                choiced_user
            )
        else:
            pub.sendMessage("find_sender", sender=sender)
            n = self.window.find_sender
            if n != -1:
                wx.CallAfter(
                    self.window.user_list_box.Delete,
                    n
                )
                wx.CallAfter(
                    self.window.user_list_box.Insert,
                    sender + u"♥", n
                )

    def run(self):
        while True:
            try:
                message = self.client.recv(BUFFER_SIZE)
                try:
                    message_dict = json.loads(message)
                    REPL.__dict__.get("%s_handler" % message_dict.get("title"))
                except Exception as e:
                    self.window.show_tip(
                        u"数据格式错误：%s" % (message)
                    )
            except Exception as e:
                self.window.show_tip(e)
                break
