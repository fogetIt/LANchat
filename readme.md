##### flow
```
客户端运行程序时自动与服务器建立连接
客户端关闭时自动关闭与服务器的连接
服务器监听客户端的登录/退出，保存连接信息，并广播在线用户列表
服务端监听用户发送的 json 数据，再进行广播/转发
```

##### p2p flow(not safety)
```
服务器只保存用户名、客户端ip，客户端之间需要通话时，由服务器发送对方ip，帮助双方建立连接。
```

##### run server
```shell
pip install bidict==0.13.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
python server.py
```

##### run client
```
sudo python client.pyw
```
