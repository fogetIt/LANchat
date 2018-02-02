# -*- coding: utf-8 -*-
# @Date:   2018-01-23 10:53:20
# @Last Modified time: 2018-01-23 10:53:26
import platform
from subprocess import Popen
from setuptools import setup


if platform.platform().lower().find("ubuntu") != -1:
    Popen([
        "/bin/bash", "-c",
        """
        python -c 'import wx; exit()' || sudo apt-get install python-wxtools -y
        """
    ]).wait()
elif platform.platform().lower().find("win") != -1:
    Popen("pip install -U wxPython").wait()


setup(
    name="cliapp",
    version="0.0.2",
    description="client for LANchat",
    url="https://github.com/forgetIt/LANchat.git",
    packages=["cliapp", "cliapp.views"],
    py_modules=[],
    install_requires=["wxPython>=3.0.2"],
    platforms=["ubuntu"],
    author="zdd",
    author_email = "2271404280@qq.com",
)
