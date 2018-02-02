# -*- coding: utf-8 -*-
# @Date:   2018-01-28 20:00:25
# @Last Modified time: 2018-01-28 20:00:32
import json, socket, wx
from config import COLOR_RED, COLOR_BLUE
from better import StaticTextCtrl, Single
from models import RecordStore
from views import Views


class Client(Single):

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(1)
        self.my_name = socket.gethostname()

    @staticmethod
    def create_message(title, receiver="", ext_data=""):
        return json.dumps({"title": title, "receiver": receiver, "ext_data": ext_data})

    def login(self, host, port):
        self.client.connect((host, port))
        self.client.send(self.create_message("login", ext_data=self.my_name))

    def logout(self):
        self.client.send(self.create_message("logout"))
        self.client.close()

    def single(self, value, receiver):
        self.client.send(self.create_message("single", receiver=receiver, ext_data=value))

    def group(self, value):
        self.client.send(self.create_message("group", ext_data=value))


class Service(RecordStore, Views, Client):

    def __init__(self):
        Views.__init__(self)
        Client.__init__(self)
        RecordStore.__init__(self)

    def reset_selected_user(self, user):
        self.selected_user = user
        self.user_name_text.SetLabel(self.selected_user)

    def __refresh_notice_icon(self):
        if self.notice_icon == u"⓿":
            self.notice_button.Enable(False)
            self.notice_button.SetForegroundColour(COLOR_BLUE)
        else:
            self.notice_button.Enable(True)
            self.notice_button.SetForegroundColour(COLOR_RED)
        self.notice_button.SetLabel(self.notice_icon)

    def __reset_unread_list_box(self):
        self.unread_list_box.Clear()
        for user in self.unread_set:
            self.unread_list_box.Append(user)

    def refresh_user_list_box(self, users):
        self.update_users(users, self.my_name)
        self.user_list_box.Clear()
        self.user_list_box.Insert("group", 0)
        for user in self.users_set:
            self.user_list_box.Append(user)

    def add_record_sizer(self, user, value, is_self=True):
        margin_sizer = wx.BoxSizer()
        record = StaticTextCtrl(parent=self.record_panel, value=value)
        margin_sizer.Add(record, proportion=10, border=10, flag=wx.EXPAND | wx.TOP | wx.BOTTOM)
        if is_self:
            if record.lines_number == 1:
                record.SetWindowStyle(record.GetWindowStyle() & ~wx.TE_LEFT | wx.TE_RIGHT)
            self.record_sizer.Add(
                margin_sizer, proportion=0, border=150, flag=wx.EXPAND | wx.LEFT
            )
        else:
            record.SetForegroundColour(COLOR_BLUE)
            self.record_sizer.Add(
                margin_sizer, proportion=0, border=150, flag=wx.EXPAND | wx.RIGHT
            )
        record.Hide()
        self.add_record(user, record)
        self.__refresh_notice_icon()
        self.__reset_unread_list_box()

    def refresh_record_panel(self):
        for i in self.record_panel.GetChildren():
            i.Hide()
        record_list = self.get_record(self.selected_user)
        if record_list:
            for i in record_list:
                i.Show()
            self.record_panel.SetupScrolling()
        self.remove_record()
        self.__refresh_notice_icon()
        self.__reset_unread_list_box()


class Controller(Service):
    app = wx.App()

    def __init__(self):
        Service.__init__(self)
        self.Bind(wx.EVT_CLOSE, self.close_window_event)
        self.user_list_box.Bind(wx.EVT_LEFT_UP, self.click_user_list_event)
        self.unread_list_box.Bind(wx.EVT_LEFT_UP, self.click_unread_list_event)
        self.notice_button.Bind(wx.EVT_BUTTON, self.click_notice_event)
        self.send_button.Bind(wx.EVT_BUTTON, self.send_message_event)
        self.input_field.Bind(wx.EVT_TEXT_ENTER, self.send_message_event)

    def close_window_event(self, e):
        self.logout()
        Controller.app.Destroy()  # TODO  noticing
        wx.Exit()                 # TODO  better than exit(0)

    def click_user_list_event(self, e):
        if self.user_list_box.GetItems():
            n = self.user_list_box.GetSelection()
            if n != -1:
                self.reset_selected_user(self.user_list_box.GetStringSelection())
                self.refresh_record_panel()

    def click_unread_list_event(self, e):
        if self.unread_list_box.GetItems():
            n = self.unread_list_box.GetSelection()
            if n != -1:
                self.reset_selected_user(self.unread_list_box.GetStringSelection())
                self.close_unread_tip()
                self.refresh_record_panel()

    def click_notice_event(self, e):
        self.show_unread_tip()

    def send_message_event(self, e):
        value = self.input_field.GetValue().strip()
        if not value:
            self.show_tip(u"发送信息为空")
        elif not self.selected_user:
            self.show_tip(u"未选择用户")
        elif self.selected_user == "group":
            if not self.users_set:
                self.show_tip(u"群聊为空")
            else:
                self.group(value)
                self.add_record_sizer("group", value)
                self.refresh_record_panel()
                self.input_field.Clear()
        else:
            self.single(value, self.selected_user)
            self.add_record_sizer(self.selected_user, value)
            self.refresh_record_panel()
            self.input_field.Clear()
