# coding:utf-8

import socket

# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.connect(("www.sina.com",80))
#
# s.send('GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
#
# buffer = []
#
# while True:
#     d = s.recv(1024)
#     if d:
#         buffer.append(d)
#     else:
#         break
#
# data = "".join(buffer)
#
# s.close()
#
# header,html = data.split("\r\n\r\n",1)
#
# # print header
# #
# # with open('sina.html', 'wb') as f:
# #     f.write(html)
import threading

import time

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(("127.0.0.1",9999))
s.listen(5)
print 'Waiting for connection...'

def tcplink(sock, addr):
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        sock.send('Hello, %s!' % data)
    sock.close()
    print 'Connection from %s:%s closed.' % addr

while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()


