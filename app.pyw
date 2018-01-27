# -*- coding: utf-8 -*-
# @Date:   2018-01-25 17:00:02
# @Last Modified time: 2018-01-25 17:00:22
import json
from threading import Thread
from client import BUFFER_SIZE, MainFrame, MessageReceiver


class GUI(Thread, MainFrame):

    def __init__(self, host, port):
        Thread.__init__(self)
        MainFrame.__init__(self)
        self.login(host, port)

    def run(self):
        MainFrame.app.MainLoop()


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
                    REPL.__dict__.get("%s_handler" % message_dict.get("title"))
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
