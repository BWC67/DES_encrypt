# ！/usr/bin/python3
# --coding:utf-8--

import socket
import threading
from DES_encrypt import *
from DES_decrypt import *
msg = ''
true = True
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 建立socket对象


def send(sock, t):
    t = encrypt(message_pretreatment(2, t), generate_sub_key('ABCDEFGH'))
    t = integration(1, t)
    print(t)
    sock.send(t.encode('utf-8'))


def c_socket(host, port):
    global s
    a = s.connect_ex((host, port))  # 绑定本地端口
    if a == 0:
        print('已连接服务端：', host, '端口:', port)
    return a, s


def c_sr():
    def rec(sock):
        global true
        global msg
        while true:
            msg = sock.recv(1024).decode('utf-8')  # 函数的核心语句就一条接收方法
            msg = integration(2, main('ABCDEFGH', message_pretreatment(1, msg)))
            if msg == "exit":
                true = False
            print('Server端：', msg)
    thread_2 = threading.Thread(target=rec, args=(s,))
    thread_2.start()
    return msg
    # send(s, t)
    # s.close()

# c_socket('172.55.55.1', 9999)
