# -*- coding: utf-8 -*-
# @Date:   2018-01-20 14:59:10
# @Last Modified time: 2018-01-25 18:41:23
from .app import App


app = App()


@app.route("login")
def login(message_dict, client_socket):
    user_name = message_dict.get("name")
    result = app.add_client(user_name, client_socket)
    if result:
        app.logger.warning(result)
        app.send_message(
            app.error_message(ext_data=result), client_socket
        )
    else:
        app.broadcast(app.users_message())
        app.logger.info("{user_name} login successful".format(user_name=user_name))


@app.route("logout")
def logout(message_dict, client_socket):
    app.close_client(client_socket)


@app.route("private")
def private(message_dict, client_socket):
    ext_data = message_dict.get("ext_data")
    app.send_message(
        app.private_message(sender=app.get_user(client_socket), ext_data=ext_data),
        app.get_socket(message_dict.get("receiver"))
    )


@app.route("group")
def group(message_dict, client_socket):
    ext_data = message_dict.get("ext_data")
    app.broadcast(
        app.group_message(sender=app.get_user(client_socket), ext_data=ext_data),
        app.get_user(client_socket),
        client_socket
    )
