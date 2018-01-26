# -*- coding: utf-8 -*-
# @Date:   2018-01-23 15:26:09
# @Last Modified time: 2018-01-23 15:26:21
import json
import socket
import wx


BUFFER_SIZE = 4096
COLOR_RED = wx.Colour(255, 0, 0)
COLOR_BLUE = wx.Colour(30, 144, 255)
COLOR_WHITE = wx.Colour(250, 250, 250)
COLOR_GREEN = wx.Colour(0, 139, 69)


def font(size):
    return wx.Font(
        pointSize=size,
        family=wx.SWISS,
        style=wx.NORMAL,
        weight=wx.BOLD
    )

FONT12 = font(12)
FONT13 = font(13)


class Single(object):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Single, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class Client(Single):

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(1)

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
            self.create_message("login", ext_data={"name": socket.gethostname()})
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