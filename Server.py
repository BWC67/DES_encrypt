# ！/usr/bin/python3
# --coding:utf-8--

import socket
import threading
from select import select
from DES_encrypt import *
from DES_decrypt import *


def send(sock, t):
    t = encrypt(message_pretreatment(2, t), generate_sub_key('ABCDEFGH'))
    t = integration(1, t)
    print(t)
    sock.send(t.encode('utf-8'))


def s_sr():
    def rec(sock):
        global true
        global msg
        while true:
            msg = sock.recv(1024).decode('utf-8')  # 函数的核心语句就一条接收方法
            msg = integration(2, main('ABCDEFGH', message_pretreatment(1, msg)))
            print('Client端：', msg)
    thread_2 = threading.Thread(target=rec, args=(client_socket,))
    thread_2.start()
    return msg
    # send(client_socket, t)

    # client_socket.close()
    # server_socket.close()


def wait_client(aa):
    global client_socket
    server_socket.bind((host, port))  # 绑定本地端口
    server_socket.listen(5)  # 等待客户端连接，连接数为5,超过后面排队
    inputs = [server_socket]
    '''while client_socket == '':
        client_socket, add = server_socket.accept()  # 建立客户端连接
        print('连接地址：%s' % str(add))'''
    return client_socket


true = True
msg = ''
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # 建立socket对象
host = socket.gethostbyname(socket.gethostname())
port = 9999
print('服务器IP为：', host, '端口:', port)


client_socket = ''

# s_socket()
