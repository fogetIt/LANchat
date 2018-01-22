# -*- coding: utf-8 -*-
# @Date:   2018-01-20 14:59:10
# @Last Modified time: 2018-01-20 14:59:46
import json
import hashlib
from functools import partial
from core import App


app = App()


def create_message(sender=None, title=None, ext_data=None):
    if not sender or not title or not ext_data:
        return None
    message_dict = {"title": title, "sender": sender}
    message_dict.update(ext_data)
    return json.dumps(message_dict)


group_message = partial(create_message, title="group")
private_message = partial(create_message, title="private")
user_list_message = partial(create_message, sender="system", ext_data=app.user_list)
error_message = partial(create_message, sender="system", title="error")
success_message = partial(create_message, sender="system", title="success")


class Utils(object):
    secret_key = "zdd.qwert"

    @classmethod
    def make_password(cls, password):
        m = hashlib.md5()
        m.update(cls.secret_key)
        m.update(password)
        return m.hexdigest()

    @classmethod
    def get_user_password(cls, name):
        with open("user_password.json", "r") as reader:
            _dict = json.loads(reader.read())
            return _dict.get(name)

    @classmethod
    def add_user_password(cls, name, password):
        if not cls.get_user_password(name):
            password = cls.make_password(password)
            with open("user_password.json", "r") as reader:
                _dict = json.loads(reader.read())
                _dict.update({name: password})
                with open("password.json", "w") as writer:
                    writer.write(json.dumps(_dict))
                    return True
        return False

    @classmethod
    def check_password(cls, name, password):
        if name:
            if cls.make_password(password) == cls.get_user_password(name):
                return True
        return False


class Views(Utils):

    def close_client(self, client_socket):
        result = app.remove_client(client_socket=client_socket)
        if result:
            app.broadcast(user_list_message())

    @app.route("register")
    def register(self, message_dict, client_socket):
        name = message_dict.get("name")
        password = message_dict.get("password")
        if not self.add_user_password(name, password):
            app.send_message(
                error_message(ext_data="user name has already existed!"),
                app.get_user(client_socket),
                client_socket
            )
        else:
            app.send_message(
                success_message(ext_data="register successful!"),
                app.get_user(client_socket),
                client_socket
            )

    @app.route("login")
    def login(self, message_dict, client_socket):
        if message_dict.get("title") != "login":
            result = "title error!"
        else:
            name = message_dict.get("name")
            password = message_dict.get("password")
            if not self.check_password(name, password):
                result = "name or password error!"
            else:
                result = app.add_client(user_name=name, client_socket=client_socket)
        if result:
            app.logger.warning(result)
            app.send_message(
                error_message(ext_data=result),
                app.get_user(client_socket),
                receiver_socket=client_socket
            )
        else:
            app.broadcast(user_list_message())
            app.logger.info("{name} login successful".format(name=name))

    @app.route("logout")
    def logout(self, message_dict, client_socket):
        self.close_client(client_socket=client_socket)

    @app.route("private")
    def private(self, message_dict, client_socket):
        ext_data = message_dict.get("ext_data")
        receiver = message_dict.get("receiver")
        app.send_message(
            private_message(sender=app.get_user(client_socket), ext_data=ext_data),
            receiver,
            app.get_socket(receiver)
        )

    @app.route("group")
    def group(self, message_dict, client_socket):
        ext_data = message_dict.get("ext_data")
        app.broadcast(
            group_message(sender=app.get_user(client_socket), ext_data=ext_data),
            sender=app.get_user(client_socket),
            sender_socket=client_socket
        )
