# -*- coding: utf-8 -*-
# @Date:   2018-01-25 17:00:02
# @Last Modified time: 2018-01-25 17:00:22
import json
from threading import Thread
from client import wx, BUFFER_SIZE, Controller, Client


class GUI(Thread, Controller):

    def __init__(self, host, port):
        Thread.__init__(self)
        Controller.__init__(self)
        self.login(host, port)

    def run(self):
        Controller.app.MainLoop()


class REPL(Thread, Client):

    def __init__(self, window):
        Thread.__init__(self)
        Client.__init__(self)
        # self.window = window
        self.window = Controller()

    def private_receiver(self, message_dict):
        sender = message_dict.get("sender")
        wx.CallAfter(self.window.add_record_sizer, sender, message_dict.get("ext_data"))
        if sender == self.window.selected_user:
            wx.CallAfter(self.window.refresh_record_panel)

    group_receiver = private_receiver

    def error_receiver(self, message_dict):
        wx.CallAfter(self.window.show_tip, message_dict.get("ext_data"))

    def user_list_receiver(self, message_dict):
        users = message_dict.get("users")

    def run(self):
        while True:
            try:
                message = self.client.recv(BUFFER_SIZE)
                try:
                    message_dict = json.loads(message)
                    REPL.__dict__.get("%s_receiver" % message_dict.get("title"))
                except Exception as e:
                    self.window.show_tip(
                        u"数据格式错误：%s" % (message)
                    )
            except Exception as e:
                self.window.show_tip(e)
                break


def main(host, port):
    t1 = GUI(host, port)
    t2 = REPL(t1)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    main("127.0.0.1", 8888)
