# -*- coding: utf-8 -*-
# @Date    : 2021-01-18 17:59:11
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 进程池实现S/C聊天
# @Version : $Id$

import os
from socket import *


client = socket()
ip_port = ("127.0.0.1", 8001)
client.connect(ip_port)
while 1:  # 循环通讯
    inp = input(">>:").strip()
    if not inp: continue
    if inp.upper() == "Q": break
    client.send(inp.encode('utf-8')) #bytes
    from_server_msg = client.recv(1024).decode('utf-8')
    print("来自服务端的消息:", from_server_msg)
client.close()

