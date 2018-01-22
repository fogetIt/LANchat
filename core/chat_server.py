# -*- coding: utf-8 -*-
# @Date:   2018-01-20 17:14:06
# @Last Modified time: 2018-01-20 17:14:28
import socket
from .mixin import Single
from .logger import Logger
from .client_store import ClientStore


PORT = 8888
BUFFER_SIZE = 4096
LISTEN_NUMBER = 15
SERVER_TIMEOUT = None


class ServerSocket(Single):

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(SERVER_TIMEOUT)
        self.server_socket.bind(("0.0.0.0", PORT))
        self.server_socket.listen(LISTEN_NUMBER)


class ChartServer(Logger, ServerSocket, ClientStore):

    def __init__(self):
        Logger.__init__(self)
        ServerSocket.__init__(self)
        ClientStore.__init__(self)

    def send_message(self, message, receiver, receiver_socket):
        if not message:
            self.logger.error("message empty error")
        else:
            try:
                receiver_socket.send(message)
                self.logger.info(
                    "send message to {receiver} success".format(receiver=receiver)
                )
                return True
            except Exception as e:
                self.logger.error(e)
                self.remove_client(
                    user_name=receiver,
                    client_socket=receiver_socket
                )
        return False

    def broadcast(self, message, sender="system", sender_socket=None):
        success = failed = 0
        if sender == "system" or sender_socket:
            for tcp_socket in self.socket_iterator:
                if tcp_socket != sender_socket:
                    result = self.send_message(message, receiver_socket=tcp_socket)
                    if result:
                        success += 1
                    else:
                        failed += 1
        return success, failed

    def receive_message(self, client_socket):
        try:
            return client_socket.recv(BUFFER_SIZE)
        except Exception as e:
            self.logger.error(e)
            self.remove_client(client_socket=client_socket)
        return False
