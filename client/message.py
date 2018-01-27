# -*- coding: utf-8 -*-
# @Date:   2018-01-26 13:14:16
# @Last Modified time: 2018-01-26 13:14:34
import json
import socket
import wx
from .utils import Single


class Client(Single):

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(1)
        self.user_name = socket.gethostname()


class MessageSender(Client):

    @staticmethod
    def create_message(title, receiver="", ext_data=None):
        message_dict = {"title": title}
        if receiver:
            message_dict.update({"receiver": receiver})
        if ext_data:
            message_dict.update(ext_data)
        return json.dumps(message_dict)

    def login(self, host, port):
        self.client.connect((host, port))
        self.client.send(
            self.create_message("login", ext_data={"name": self.user_name})
        )

    def logout(self):
        self.client.send(self.create_message("logout"))
        self.client.close()

    def private(self, value, receiver):
        self.client.send(
            self.create_message("private", receiver=receiver, ext_data={"ext_data": value})
        )

    def group(self, value):
        self.client.send(
            self.create_message("group", ext_data={"ext_data": value})
        )


class MessageReceiver(Client):

    def __init__(self):
        super(MessageReceiver, self).__init__()
        from .main_frame import MainWindow
        self.window = MainWindow()

    def private_handler(self, message_dict):
        sender = message_dict.get("sender")
        selected_user = self.window.selected_user
        wx.CallAfter(
            self.window.add_record,
            sender, message_dict.get("ext_data")
        )
        wx.CallAfter(
            self.window.refresh_chat_records,
            selected_user
        )
        wx.CallAfter(
            self.window.refresh_unread_tip
        )
