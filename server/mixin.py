# -*- coding: utf-8 -*-
# @Date:   2018-01-19 10:54:33
# @Last Modified time: 2018-01-19 10:55:27
import types
import socket
from bidict import bidict
from server import (
    Single, RouterError,
    PORT, LISTEN_NUMBER, SERVER_TIMEOUT
)


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
    def users(self):
        return self.user_socket_dict.keys()


class ServerSocket(Single):

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(SERVER_TIMEOUT)
        self.server_socket.bind(("0.0.0.0", PORT))
        self.server_socket.listen(LISTEN_NUMBER)
        self.server_socket.setblocking(1)  # blocking default 1


class RouterMap(Single):

    def __init__(self):
        self.router_map = dict()

    def add_rule(self, title, func):
        if not title:
            raise RouterError(err="title empty")
        elif not isinstance(func, types.FunctionType):
            raise RouterError(err="view func error")
        elif self.router_map.get(title):
            raise RouterError(err="router {title} has existed".format(title=title))
        self.router_map.update({title: func})

    def find_view(self, title):
        return self.router_map.get(title)
