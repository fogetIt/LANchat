# -*- coding: utf-8 -*-
# @Date:   2018-01-25 17:00:02
# @Last Modified time: 2018-01-25 17:00:22
import sys
import json
from functools import partial
from threading import Thread
from LANchat import wx, BUFFER_SIZE, Controller


reload(sys)
sys.setdefaultencoding("utf-8")


class GUI(Thread, Controller):

    def __init__(self, host, port):
        Thread.__init__(self)
        Controller.__init__(self)
        self.login(host, port)
        self.Show(True)  # TODO == MainFrame().Show()

    def run(self):
        Controller.app.MainLoop()


class REPL(Thread):

    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def single_receiver(self, message_dict):
        sender = message_dict.get("sender")
        wx.CallAfter(self.window.add_record_sizer, sender, message_dict.get("ext_data"), False)
        if sender == self.window.selected_user:
            wx.CallAfter(self.window.refresh_record_panel)

    def group_receiver(self, message_dict):
        wx.CallAfter(
            self.window.add_record_sizer,
            "group",
            "{}:\n\t{}".format(message_dict.get("sender"), message_dict.get("ext_data")), False
        )
        if "group" == self.window.selected_user:
            wx.CallAfter(self.window.refresh_record_panel)

    def error_receiver(self, message_dict):
        wx.CallAfter(self.window.show_tip, message_dict.get("ext_data"))

    def users_receiver(self, message_dict):
        wx.CallAfter(self.window.refresh_user_list_box, message_dict.get("ext_data"))

    def run(self):
        while True:
            try:
                message = self.window.client.recv(BUFFER_SIZE)
                try:
                    message_dict = json.loads(message)
                    REPL.__dict__.get(
                        "{}_receiver".format(message_dict.get("title"))
                    )(self, message_dict)
                except Exception as e:
                    wx.CallAfter(self.window.show_tip, u"数据格式错误：%s" % (message))
            except Exception as e:
                print(e)
                wx.CallAfter(self.window.show_tip, str(e))
                break


def main(host=None, port=None):
    t1 = GUI(host, port)
    t2 = REPL(t1)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


run = partial(main, port=8888)


if __name__ == '__main__':
    main(host="127.0.0.1", port=8888)
