# -*- coding: utf-8 -*-
# @Date:   2018-01-27 17:44:21
# @Last Modified time: 2018-01-27 17:44:39
from client import Single, StaticListDict


class RecordStore(Single):

    def __init__(self):
        self.max_size = 100
        self.user_record_dict = {}
        self.selected_user = u""
        self.users_set = set()
        self.unread_set = set()
        self.number_icons = StaticListDict(
            [u"⓿", u"➊", u"➋", u"➌", u"➍", u"➎", u"➏", u"➐", u"➑", u"➒", u"➓", u"∞"]
        )

    def add_record(self, user, record):
        self.add_unread_set(user)
        record_list = self.user_record_dict.get(user)
        if not record_list:
            self.user_record_dict.update({user: []})
        elif len(record_list) >= self.max_size:
            record_list.pop(0, None)
        record_list.append(record)

    def reduce_record(self, user):
        self.reduce_unread_set(user)
        if user not in self.unread_set:
            self.user_record_dict.pop(user, None)

    def get_record(self, user):
        return self.user_record_dict.get(user)

    def get_unread_num(self):
        return len(self.unread_set)

    def add_unread_set(self, user):
        if user != self.selected_user:
            self.unread_set.add(user)

    def reduce_unread_set(self, user):
        if user in self.unread_set:
            if user == self.selected_user:
                self.unread_set.remove(user)

    def get_icon(self, i):
        if i >= len(self.number_icons):
            i = len(self.number_icons) - 1
        return self.number_icons.get(i)

    def get_icon_num(self, icon):
        return self.number_icons.inv_get(icon)
