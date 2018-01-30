# -*- coding: utf-8 -*-
# @Date:   2018-01-20 15:20:48
# @Last Modified time: 2018-01-20 15:20:56
import json


PORT = 8888
BUFFER_SIZE = 4096
LISTEN_NUMBER = 15
SERVER_TIMEOUT = None
SELECT_TIMEOUT = 3


class Single(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Single, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class RouterError(Exception):

    def __init__(self, err=""):
        super(RouterError, self).__init__(err)


def create_message(title=None, sender=None, ext_data=None):
    if title and sender and ext_data:
        return json.dumps({"title": title, "sender": sender, "ext_data": ext_data})
    return None


from .events import app
