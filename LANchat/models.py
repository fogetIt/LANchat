# -*- coding: utf-8 -*-
# @Date:   2018-01-27 17:44:21
# @Last Modified time: 2018-01-27 17:44:39
from LANchat import MAX_CHAT_RECORD_SIZE, NUMBER_ICONS
from .better import Single


class RecordStore(Single):

    def __init__(self):
        self.selected_user = u""
        self.user_record_dict = {}
        self.users_set = set()
        self.unread_set = set()

    def add_record(self, user, record):
        self.__add_unread_set(user)
        record_list = self.get_record(user)
        if len(record_list) >= MAX_CHAT_RECORD_SIZE:
            record_list.pop(0)
        record_list.append(record)

    def remove_record(self, user):
        self.__remove_unread_set(user)
        if user not in (self.unread_set | self.users_set):
            self.user_record_dict.pop(user, None)

    def get_record(self, user):
        return self.user_record_dict.get(user)

    def __add_unread_set(self, user):
        if user != self.selected_user:
            self.unread_set.add(user)

    def __remove_unread_set(self, user):
        if user in self.unread_set:
            if user == self.selected_user:
                self.unread_set.remove(user)

    @property
    def notice_icon(self):
        i = len(self.unread_set)
        if i >= len(NUMBER_ICONS):
            i = len(NUMBER_ICONS) - 1
        return NUMBER_ICONS.get(i)

    def update_users(self, users):
        old_users = self.users_set
        new_users = set(users)
        diff_old = old_users - new_users
        diff_new = new_users - old_users
        for user in diff_old:
            self.remove_record(user)
        for user in diff_new:
            self.user_record_dict.update({user: []})
        self.users_set = new_users
