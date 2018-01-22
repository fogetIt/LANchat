# -*- coding: utf-8 -*-
# @Date:   2018-01-19 10:54:33
# @Last Modified time: 2018-01-19 10:55:27
from bidict import bidict
from .mixin import Single


class ClientStore(Single):

    def __init__(self):
        self.user_socket_dict = bidict()

    def add_client(self, user_name=None, client_socket=None):
        if user_name in self.user_socket_dict:
            return "{user_name} is already online".format(user_name=user_name)
        self.user_socket_dict.update({user_name: client_socket})
        return None

    def remove_client(self, user_name=None, client_socket=None):
        self.user_socket_dict.pop(user_name)
        self.user_socket_dict.inv.pop(client_socket)

    def get_client(self, user_name=None, client_socket=None):
        if not user_name:
            user_name = self.get_user(client_socket=client_socket)
        if not client_socket:
            client_socket = self.get_socket(user_name=user_name)
        if not client_socket:
            return False
        return {"user": user_name, "socket": client_socket}

    def get_user(self, client_socket=None):
        user_name = None
        if client_socket:
            user_name = self.user_socket_dict.inv.get(client_socket)
        return user_name

    def get_socket(self, user_name=None):
        client_socket = None
        if user_name:
            client_socket = self.user_socket_dict.get(user_name)
        return client_socket

    @property
    def socket_iterator(self):
        return self.user_socket_dict.itervalues()

    @property
    def user_list(self):
        return self.user_socket_dict.keys()
