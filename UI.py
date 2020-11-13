from tkinter import *
from DES_encrypt import *
from DES_decrypt import *
from tkinter import scrolledtext
import re
import tkinter.messagebox
import time
import socket
import threading
import Server
import Client
(text_msglist, text_msg, a, b, aa, event) = ('', '', '','', 1,'')
root_1 = Tk()
ture = True
s_sock = []
# root_3 = Tk()

def quit_sock(sock,root_3):
    sock.close()
    root_3.destroy()

def send_message_Adaptor(fun, *args):
	return lambda event,fun=fun,argss=args: fun(event, *args)

def rec_msg(types,sock):
    global text_msglist
    while ture:
        text_msglist.config(state=NORMAL)
        msg = sock.recv(1024).decode('utf-8')  # 函数的核心语句就一条接收方法
        msg = integration(2, main('ABCDEFGH', message_pretreatment(1, msg)))
        a = re.search(str(sock.getpeername()), msg)
        print(str(sock.getsockname()),msg,a)
        if a == None:
            text_msglist.insert(END, msg)
        text_msglist.see(END)
    # text_msglist.config(state=DISABLED)

def ser_rec(sock):
    global text_msglist
    while ture:
        text_msglist.config(state=NORMAL)
        msg = sock.recv(1024).decode('utf-8')  # 函数的核心语句就一条接收方法
        msg = integration(2, main('ABCDEFGH', message_pretreatment(1, msg)))
        text_msglist.insert(END, msg)
        text_msglist.see(END)
        for s in s_sock[1:len(s_sock)]:
            a = re.search(str(s.getpeername()),msg)
            print(str(s.getpeername()),msg,a)
            if a == None:
                Server.send(s, msg)
                text_msglist.config(state=DISABLED)
    # text_msglist.config(state=DISABLED)


# 发送按钮事件
def send_message(event,types,sock):
    global text_msglist
    text_msglist.config(state=NORMAL)
    # 在聊天内容上方加一行 显示发送人及发送时间
    if types == 0:
        a = 1
        for s in s_sock[1:len(s_sock)]:
            if text_msg.get('0.0', END) != '\n' and text_msg.get('0.0', END) != '':
                msgcontent = '服务器:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n  '
                msg = msgcontent + text_msg.get('0.0', END)
                print(text_msg.get('0.0', END))
                Server.send(s, msg)
                text_msglist.see(END)
                if a == len(s_sock)-1:
                    text_msglist.insert(END, msg)
                    text_msg.delete('0.0', END)
                a = a + 1
    if types == 1:
        msgcontent = '客户端'+str(sock.getsockname()) +'  '+ time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n  '
        msg = msgcontent + text_msg.get('0.0', END)
        print(msg)
        text_msglist.insert(END, msg)
        text_msg.delete('0.0', END)
        Client.send(sock, msg)
        text_msglist.see(END)




def chat_ui(sock, types, l = []):
    global text_msglist
    global text_msg
    global aa
    global s_sock
    root_3 = Tk()
    if types == 0:
        root_3.title('与客户端聊天中')
        s_sock = l
    elif types == 1:
        root_3.title('与服务端聊天中' )
    # 创建几个frame作为容器ipadx=10, padx=10,
    frame_left_top = Frame(width=380, height=270, bg='white')
    frame_left_center = Frame(width=380, height=100, bg='white')
    frame_left_bottom = Frame(width=380, height=25)
    frame_right = Frame(width=170, height=400, bg='white')

    # 创建需要的几个元素 ,font="Helvetica 12 bold"
    text_msglist = scrolledtext.ScrolledText(frame_left_top,width=52,height=21,wrap=WORD)
    user_list = Listbox(frame_right,selectmode=EXTENDED,height=18)
    if types == 0:
        user_list.insert(END, str(s_sock[0].getsockname()))
    for item in s_sock[1:len(s_sock)]:
        user_list.insert(END, str(item.getpeername()))
    text_msg = Text(frame_left_center)
    button_sendmsg = Button(frame_left_bottom, text='发送', command=lambda:send_message(event,types,sock))
    button_clear = Button(frame_right, text='清除', command=lambda x=user_list:x.delete(ACTIVE))
    button_private_chat = Button(frame_right, text='私聊')
    button_quit = Button(frame_right, text='退出', command=lambda:quit_sock(sock,root_3))
    text_msg.bind("<Return>", send_message_Adaptor(send_message, types, sock))


    # scrolW = 370  # 设置文本框的长度
    # scrolH = 270  # 设置文本框的高度
    # scr = scrolledtext.ScrolledText(frame_left_top, width=380, height=270,wrap=tk.WORD)  # wrap=tk.WORD   这个值表示在行的末尾如果
    # 有一个单词跨行，会将该单词放到下一行显示,比如输入hello，he在第一行的行尾,llo在第二行的行首, 这时如果wrap=tk.WORD，则表示会将 hello
    # 这个单词挪到下一行行首显示, wrap默认的值为tk.CHAR
    # scr.grid(column=0, columnspan=3)  # columnspan 个人理解是将3列合并成一列   也可以通过 sticky=tk.W  来控制该文本框的对齐方式

    # 创建的tag
    text_msglist.tag_config('green', foreground='#008B00')
    text_msglist.tag_config('blue', foreground='#0000FF')
    # text_msglist.config(yscrollcommand= scrollbar.set)
    # scrollbar.config(command=text_msglist.yview)

    # 使用grid设置各个容器位置
    frame_left_top.grid(row=0, column=0, padx=2, pady=5)
    frame_left_center.grid(row=1, column=0, padx=2, pady=5)
    frame_left_bottom.grid(row=2, column=0)
    frame_right.grid(row=0, column=1, rowspan=3, padx=4, pady=5)
    frame_left_top.grid_propagate(0)
    frame_left_center.grid_propagate(0)
    frame_left_bottom.grid_propagate(0)

    # 把元素填充进frame
    user_list.grid(row=0,sticky='N')
    button_clear.grid(row=1,sticky='SW')
    button_private_chat.grid(row=1,sticky='S')
    button_quit.grid(row=1,sticky='SE')
    text_msglist.grid()
    text_msg.grid()
    button_sendmsg.grid(sticky='E')
    # scrollbar.grid(column=6, row=5, rowspan=2,sticky='N'+'S'+'W')
    if  types == 1:
        thread_2 = threading.Thread(target=rec_msg, args=(types,sock))
        thread_2.start()
    if  types == 0:
        for s in s_sock[1:len(s_sock)]:
            a = threading.Thread(target=ser_rec, args=(s,))
            a.start()
    # 主事件循环
    text_msglist.config(state=DISABLED)
    root_3.mainloop()


def input_ip():
    # 绘制两个label,grid（）确定行列
    Label(root_1, text="请输入目的IP：").grid(row=0, column=0)
    Label(root_1, text="请输入目的端口：").grid(row=1, column=0)
    # 导入两个输入框
    e1 = Entry(root_1)
    e2 = Entry(root_1)
    # 设置输入框的位置
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    # 输入内容获取函数print打印
    def client_enter(a, b):
        global root_1
        print("IP：", a)
        print("端口：", b)
        (aa, sock) = Client.c_socket(a, int(b))
        root_1.destroy()
        chat_ui(sock,1,[])

    # 跳转函数，跳转至其他窗口
    def server_enter():
        global root_1
        aa = True
        print("正在进入服务端程序。。。")
        Server.server_socket.bind((Server.host, Server.port))  # 绑定本地端口
        Server.server_socket.listen(5)  # 等待客户端连接，连接数为5,超过后面排队
        inputs = [Server.server_socket]
        tkinter.messagebox.showinfo('连接中', '等待客户端连接中，请稍等.....')
        while aa:
            rlist, wlist, xlist = Server.select(inputs, [], [])
            for s in rlist:
                if s is Server.server_socket:
                    client_sock, addr = s.accept()
                    print('...connecting from:', client_sock)
                    inputs.append(client_sock)  # 将tcpCliSock插入inputs中
                if len(inputs) == 3:
                    aa = False
                    break
        root_1.destroy()
        chat_ui(0, 0, inputs)

    # 设置两个按钮，点击按钮执行命令 command= 命令函数
    theButton1 = Button(root_1, text="确定", width=10, command=lambda: client_enter(e1.get(), e2.get()))
    theButton2 = Button(root_1, text="本机作为服务端", width=10, command=server_enter)

    # 设置按钮的位置行列及大小
    theButton1.grid(row=3, column=0, sticky='W', padx=10, pady=5)
    theButton2.grid(row=3, column=1, sticky='E', ipadx=10, padx=10, pady=5)
    root_1.mainloop()


input_ip()
