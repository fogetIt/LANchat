# -*- coding: utf-8 -*-
# @Date:   2018-01-27 17:44:21
# @Last Modified time: 2018-01-27 17:44:39
from client import Single, StaticListDict


class RecordStore(Single):

    def __init__(self):
        self.max_size = 100
        self.user_record_dict = {}
        self.unread_dict = {}
        self.selected_user = u""
        self.user_list = []
        self.number_icons = StaticListDict(
            [u"⓿", u"➊", u"➋", u"➌", u"➍", u"➎", u"➏", u"➐", u"➑", u"➒", u"➓", u"∞"]
        )

    def add_record(self, user, record):
        if not user == self.selected_user:
            unread_num = int(self.unread_dict.get(user, 0))
            self.unread_dict.update({user: unread_num + 1})
        record_list = self.user_record_dict.get(user)
        if not record_list:
            self.user_record_dict.update({user: []})
        elif len(record_list) >= self.max_size:
            record_list.pop(0, None)
        record_list.append(record)

    def reduce_record(self, user):
        if user == self.selected_user:
            if user not in self.user_list:
                self.unread_dict.pop(user, None)
            else:
                self.unread_dict.update({user: 0})
        if not self.unread_dict.get(user):
            self.user_record_dict.pop(user, None)

    def get_record(self, user):
        unread_num = int(self.unread_dict.get(user, 0))
        record_list = self.user_record_dict.get(user)
        return unread_num, record_list

    def get_icon(self, i):
        if i >= len(self.number_icons):
            i = len(self.number_icons) - 1
        return self.number_icons.get(i)
