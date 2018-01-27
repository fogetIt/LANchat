# -*- coding: utf-8 -*-
# @Date:   2018-01-27 17:11:36
# @Last Modified time: 2018-01-27 17:11:47
from client import (
    wx, Single, Client, FONT11, FONT12, FONT13, COLOR_RED, COLOR_BLUE, COLOR_WHITE, COLOR_GREEN
)
from .models import RecordStore
from .views import RecordPanel, UserNameText, InputField, Tip


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


class UserListBox(RecordPanel, UserNameText):

    def __init__(self, panel):
        """
        use BoxSizer to avoid hard-coded widget's pos and size
        """
        RecordPanel.__init__(self, panel)
        UserNameText.__init__(self, panel)
        self.user_list_box = wx.ListBox(
            parent=panel, id=11, name='user_list', choices=[], style=wx.LB_SINGLE
        )
        self.user_list_box.SetFont(FONT12)
        self.user_list_box.SetForegroundColour(COLOR_WHITE)
        self.user_list_box.SetBackgroundColour(COLOR_GREEN)
        self.user_list_box.Insert("group", 0)
        self.user_list_box.Bind(wx.EVT_LEFT_UP, self.choose_user_event)

    def choose_user_event(self, e):
        if self.user_list_box.GetItems():
            n = self.user_list_box.GetSelection()
            if n != -1:
                self.selected_user = self.user_list_box.GetStringSelection()
                self.user_name_text.SetLabel(self.selected_user)
                self.refresh_records_panel(self.selected_user)


class UnreadListTip(Single):

    def __init__(self, panel):
        self.list_tip = wx.Dialog()
        self.unread_list_box = wx.ListBox(
            parent=panel, id=11, name='unread_list', choices=[], style=wx.LB_SINGLE
        )
        self.unread_list_box.SetFont(FONT11)
        self.unread_list_box.SetForegroundColour(COLOR_RED)

    def show_list_tip(self):
        pass


class NoticeButton(RecordStore):

    def __init__(self, panel):
        """
        ♡ ♥
        """
        super(NoticeButton, self).__init__()
        self.notice_button = wx.Button(
            parent=panel, id=21, size=(0, 30), label=u"⓿", style=wx.ALIGN_LEFT
        )
        self.notice_button.SetFont(FONT13)
        self.notice_button.SetForegroundColour(COLOR_BLUE)
        self.notice_button.Bind(wx.EVT_BUTTON, self.get_notice_event)

    def refresh_notice_icon(self, i):
        label = self.get_icon(i)
        if label == u"⓿":
            self.notice_button.SetForegroundColour(COLOR_BLUE)
        else:
            self.notice_button.SetForegroundColour(COLOR_RED)
        self.notice_button.SetLabel(label)

    def get_notice_event(self, e):
        """
        show unread list dialog
        """
        pass


class SendButton(RecordPanel, InputField, Tip, MessageSender):

    def __init__(self, panel):
        RecordStore.__init__(self)
        InputField.__init__(self, panel)
        self.send_button = wx.Button(
            parent=panel, id=24, size=(0, 40), label=u"发送"
        )
        self.send_button.SetFont(FONT13)
        self.send_button.Bind(wx.EVT_BUTTON, self.send_message_event)

    def send_message_event(self, e):
        value = self.input_field.GetValue().strip()
        if not value:
            self.show_tip(u"发送信息为空")
        elif not self.selected_user:
            self.show_tip(u"未选择用户")
        elif self.selected_user == "group":
            if not self.user_list:
                self.show_tip(u"群聊为空")
            else:
                self.group(value)
                self.create_record_sizer("group", value)
                self.refresh_records_panel(self.selected_user)
        else:
            self.private(value, self.selected_user)
            self.create_record_sizer(self.selected_user, value)
            self.refresh_records_panel(self.selected_user)
