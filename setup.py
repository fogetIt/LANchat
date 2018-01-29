# -*- coding: utf-8 -*-
# @Date:   2018-01-23 10:53:20
# @Last Modified time: 2018-01-23 10:53:26
import sys
import platform
from subprocess import Popen
from setuptools import setup


if platform.version().lower().find("ubuntu") != -1:
    Popen([
        "/bin/bash", "-c",
        """
        python -c 'import wx; exit()' || (
            apt-get install python-wxtools -y
            python %s
        )
        """ % sys.argv[0]
    ]).wait()
else:
    print("error: please install wxPython in your system")
    exit(1)


setup(
    name="simple-chat client",
    version="0.0.1",
    description="client for simple-chat",
    url="https://github.com/forgetIt/simple-chat.git",
    packages=["client", "client.views"],
    install_requires=["wxPython==3.0.2"],
    platforms=["ubuntu"],
    author="zdd",
    author_email = "2271404280@qq.com",
    py_modules=['app']
)
