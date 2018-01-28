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


class MessageReceiver(Client):

    def __init__(self):
        super(MessageReceiver, self).__init__()
        self.window = Controller()

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


class REPL(Thread, MessageReceiver):

    def __init__(self, window):
        Thread.__init__(self)
        MessageReceiver.__init__(self)
        self.window = window

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
    main("", 8888)
