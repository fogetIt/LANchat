# -*- coding: utf-8 -*-
# @Date:   2018-01-19 10:54:33
# @Last Modified time: 2018-01-19 10:55:27
from bidict import bidict
from .mixin import Single


class ClientStore(Single):

    def __init__(self):
        self.user_socket_dict = bidict()

    def add_client(self, user_name, client_socket):
        if user_name in self.user_socket_dict:
            return "{user_name} is already online".format(user_name=user_name)
        self.user_socket_dict.update({user_name: client_socket})
        return None

    def remove_client(self, user_name=None, client_socket=None):
        self.user_socket_dict.pop(user_name, None)
        self.user_socket_dict.inv.pop(client_socket, None)

    def get_user(self, client_socket):
        user_name = None
        if client_socket:
            user_name = self.user_socket_dict.inv.get(client_socket)
        return user_name

    def get_socket(self, user_name):
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
