# -*- coding: utf-8 -*-
# @Date:   2018-01-23 15:26:09
# @Last Modified time: 2018-01-23 15:26:21
"""
LANchat client
"""
from functools import partial
from .app import main


run = partial(main, port=8888)

