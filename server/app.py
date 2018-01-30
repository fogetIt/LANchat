# -*- coding: utf-8 -*-
# @Date:   2018-01-20 17:14:06
# @Last Modified time: 2018-01-20 17:14:28
import json
from functools import partial
from server import BUFFER_SIZE
from .logger import Logger
from .mixin import (
    ServerSocket, ClientStore, RouterMap
)


class ChartServer(Logger, ServerSocket, ClientStore):

    def __init__(self):
        Logger.__init__(self)
        ServerSocket.__init__(self)
        ClientStore.__init__(self)
        self.single_msg = partial(self.create_message, "single")
        self.group_msg = partial(self.create_message, "group")
        self.error_msg = partial(self.create_message, "error", sender="system")
        self.users_msg = partial(self.create_message, "users", sender="system")

    @staticmethod
    def create_message(title, sender=None, ext_data=None):
        if title and sender and ext_data:
            return json.dumps({"title": title, "sender": sender, "ext_data": ext_data})
        return None

    def send_message(self, message, receiver_socket, receiver=None):
        if not message:
            self.logger.error("message empty error")
        else:
            receiver = self.get_user(receiver_socket) if not receiver else receiver
            try:
                receiver_socket.send(message)
                self.logger.info(
                    "send message to {receiver} success".format(receiver=receiver)
                )
                return True
            except Exception as e:
                self.logger.error(e)
                self.close_client(receiver_socket)
        return False

    def broadcast(self, message, sender="system", sender_socket=None):
        success = failed = 0
        if sender == "system" or sender_socket:
            for tcp_socket in self.socket_iterator:
                if tcp_socket != sender_socket:
                    result = self.send_message(message, tcp_socket)
                    if result:
                        success += 1
                    else:
                        failed += 1
        return success, failed

    def close_client(self, client_socket):
        client_socket.close()
        self.remove_client(client_socket=client_socket)
        self.broadcast(self.users_msg(ext_data=self.users))


class App(ChartServer, RouterMap):

    def __init__(self):
        ChartServer.__init__(self)
        RouterMap.__init__(self)

    def parser(self, client_socket):
        try:
            message = client_socket.recv(BUFFER_SIZE)
            if not message:
                self.logger.error("socket error")
                self.close_client(client_socket)
                return None
            else:
                try:
                    return json.loads(message)
                except Exception as e:
                    print(e)
                    self.logger.error("message formatting error")
        except Exception as e:
            self.logger.error(e)
            self.close_client(client_socket)
            return None


    def route(self, title):
        """
        不修改被装饰的函数的行为，只是想获得它的引用
        参照 Flask.route
        """
        def decorator(func):
            self.add_rule(title, func)
            return func
        return decorator
