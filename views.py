# -*- coding: utf-8 -*-
# @Date:   2018-01-20 14:59:10
# @Last Modified time: 2018-01-20 14:59:46
import json
import hashlib
from core import App


app = App()


class Message(object):

    @classmethod
    def create_message(cls, sender=None, title=None, **ext_data):
        if not sender or not title:
            return None
        message_dict = {"title": title, "sender": sender}
        if ext_data:
            message_dict.update(ext_data)
        return json.dumps(message_dict)

    @classmethod
    def private_message(cls, sender=None, text=None):
        if not text:
            return None
        return cls.create_message(sender=sender, title="private", text=text)

    @classmethod
    def group_message(cls, sender=None, text=None):
        if not text:
            return None
        return cls.create_message(sender=sender, title="group", text=text)

    @classmethod
    def user_list_message(cls, user_list=None):
        if not user_list:
            return None
        return cls.create_message(sender="system", title="user_list", user_list=user_list)

    @classmethod
    def error_message(cls, error_text=None):
        if not error_text:
            return None
        return cls.create_message(sender="system", title="error", error_text=error_text)


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
        if cls.make_password(password) == cls.get_user_password(name):
            return True
        return False


class Views(Message, Utils):

    def close_client(self, client_ip=None, client_socket=None):
        result = app.close_client(
            client_ip=client_ip, client_socket=client_socket
        )
        if result:
            app.broadcast(self.user_list_message(app.user_list))

    @app.route("register")
    def register(self, client_ip=None, client_socket=None):
        message_dict = app.parser(client_ip=client_ip, client_socket=client_socket)
        if not message_dict:
            return
        name = message_dict.get("name")
        password = message_dict.get("password")
        if not self.add_user_password(name, password):
            app.send_message(
                self.error_message("user name has already existed!"),
                receiver_socket=client_socket
            )

    @app.route("login")
    def login(self, client_ip=None, client_socket=None):
        message_dict = app.parser(client_ip=client_ip, client_socket=client_socket)
        if not message_dict:
            return
        if message_dict.get("title") != "login":
            result = "title error"
        else:
            name = message_dict.get("name")
            password = message_dict.get("password")
            if not self.check_password(name, password):
                result = "name or password error"
            else:
                result = app.add_client(
                    user_name=name,
                    client_ip=client_ip,
                    client_socket=client_socket
                )

        if result:
            app.logger.warning(result)
            app.send_message(self.error_message(result))
        else:
            app.broadcast(self.user_list_message(app.user_list))
            app.logger.info("{client_ip} login successful".format(client_ip=client_ip))

    @app.route("logout")
    def logout(self, client_ip=None, client_socket=None):
        message_dict = app.parser(client_ip=client_ip, client_socket=client_socket)
        if not message_dict:
            return
        self.close_client(client_ip=client_ip, client_socket=client_socket)

    @app.route("private")
    def private(self, client_ip=None, client_socket=None):
        message_dict = app.parser(client_ip=client_ip, client_socket=client_socket)
        if not message_dict:
            return
        sender_client = app.get_client(client_ip=client_ip, client_socket=client_socket)
        text = message_dict.get("text")
        receiver = message_dict.get("receiver")
        message = self.private_message(sender=sender_client.get("user"), text=text)
        app.send_message(message, receiver=receiver)

    @app.route("group")
    def group(self, client_ip=None, client_socket=None):
        message_dict = app.parser(client_ip=client_ip, client_socket=client_socket)
        if not message_dict:
            return
        sender_client = app.get_client(client_ip=client_ip, client_socket=client_socket)
        text = message_dict.get("text")
        message = self.group_message(sender=sender_client.get("user"), text=text)
        app.broadcast(
            message,
            sender=sender_client.get("user"),
            sender_socket=sender_client.get("socket")
        )
