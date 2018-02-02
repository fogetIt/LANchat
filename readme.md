##### server
- include
    + [server/](./server)
    + [run.py](./run.py)
- run
```bash
pip install bidict==0.13.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
python server.py
```
##### client
- include
    + [client/](./client)
    + [setup.py](./setup.py)
    + [cliapp.py](cliapp/cliapp.py)
- install
```bash
sudo pip install git+https://github.com/fogetIt/LANchat.git
# sudo pip uninstall cliapp
```
- run
```python
import cliapp
cliapp.run(host="***")
```

<!--use setup.py
build:    python setup.py build
compress: python setup.py sdist
install:  python setup.py install [--prefix=path/to/project]
-->

##### flow
```
客户端
    启动时，自动与服务器建立连接
    关闭时，自动关闭与服务器的连接
服务器
    监听客户端的登录/退出，保存连接信息，并广播在线用户列表
    监听用户发送的 json 数据，进行广播/转发
```

<!--p2p flow(not safety)
服务器保存用户名、客户端ip。
客户端之间需要通话时，由服务器发送对方ip，帮助双方建立连接。
-->

<!--wxPython concurrent
    wx.App().MainLoop() 用一个死循环来维持 GUI
    GUI 操作必须发生在 main thread 或者 wx.App().MainLoop() thread
    所以，无法通过共用 class object 来更新 GUI
python threading
    只能利用到一个计算机核（同一时刻干一件事）
    如果线程工作时间过长，容易造成 GUI 卡死
python multiprocessing
    非 GUI 进程，无法更新 GUI
solution1:
    # 非 GUI 线程调用 GUI 线程
    wx.CallAfter(guiObj.func, arg1, arg2, ...)
solution2
    from wx.lib.pubsub import pub
    # 发布订阅事件(gui thread)
    wx.lib.pubsub.pub.subscribe(callback, topicName)
    # 发送全局消息，启动事件(other thread)
    wx.lib.pubsub.pub.sendMessage(topicName, **kwargs)
-->

##### install wxPython
```bash
# in system
sudo apt-get install python-wxtools
# in venv
sudo apt-get install python-wxgtk3.0
ln -sf /usr/lib/python2.7/dist-packages/wx* ../venv/lib/python2.7/site-packages/
```
