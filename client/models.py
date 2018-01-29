# -*- coding: utf-8 -*-
# @Date:   2018-01-27 17:44:21
# @Last Modified time: 2018-01-27 17:44:39
from client import Single


class StaticListDict(tuple):

    def __init__(self, seq=()):
        super(StaticListDict, self).__init__(set(seq))

    def get(self, i):
        try:
            return None if i < 0 else self.__getitem__(i)
        except Exception as e:
            print(e)
            return None

    def inv_get(self, value):
        try:
            return self.index(value)
        except Exception as e:
            print(e)
            return None


class RecordStore(Single):

    def __init__(self):
        self.selected_user = u""
        self.max_size = 100
        self.user_record_dict = {}
        self.users_set = set()
        self.unread_set = set()
        self.number_icons = StaticListDict(
            [u"⓿", u"➊", u"➋", u"➌", u"➍", u"➎", u"➏", u"➐", u"➑", u"➒", u"➓", u"∞"]
        )

    def add_record(self, user, record):
        self.__add_unread_set(user)
        record_list = self.user_record_dict.get(user)
        if not record_list:
            self.user_record_dict.update({user: []})
        elif len(record_list) >= self.max_size:
            record_list.pop(0, None)
        record_list.append(record)

    def reduce_record(self, user):
        self.__reduce_unread_set(user)
        if user not in self.unread_set:
            self.user_record_dict.pop(user, None)

    def get_record(self, user):
        return self.user_record_dict.get(user)

    def __add_unread_set(self, user):
        if user != self.selected_user:
            self.unread_set.add(user)

    def __reduce_unread_set(self, user):
        if user in self.unread_set:
            if user == self.selected_user:
                self.unread_set.remove(user)

    @property
    def notice_icon(self):
        i = len(self.unread_set)
        if i >= len(self.number_icons):
            i = len(self.number_icons) - 1
        return self.number_icons.get(i)
