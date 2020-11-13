# !/usr/bin/python3
# --coding:utf-8--
from DES_BOX import *
import math


# 对输入信息进行预处理,返回处理完毕的二进制数据块列表 st
def message_pretreatment(xx, message):
    (a, st) = ("", [])      # 使用元组的方式赋值，美观点
    if xx == 1:
        length = 8
    elif xx == 2:
        length = 16
    for i in message:
        a += bin(ord(i))[2:].zfill(length)   # 字符转成ascii，再转成二进制，并去掉前面的0b
    # print('"' + message + '" ' + "的Ascii为 ", ord(i))
    for j in range(0, math.ceil(len(a)/64)):    # 数据按每64位分块，若最后数据不足64位单独一块
        st.append(a[64*j:64*j+64])
        if len(a) % 64 > 0 and j == math.ceil(len(a)/64)-1:     # 未满64位的数据块左对齐补零
            st[j] = st[j].ljust(64, '0')
    return st


# 子密钥生成   参数为8位待加密密钥  不建议中文
def generate_sub_key(key):
    (b_tmp, k_tmp, cd) = ['', '', '']   # 转换为二进制的暂存数据
    for i in key:
        tmp = bin(ord(i))[2:].zfill(8)  # 字符转成ascii，再转成二进制，并去掉前面的0b
        b_tmp += tmp
    # print('Key[64bits]数量为：', b_tmp)
    for i in range(0, 56):
        cd += b_tmp[PC_1[i]-1]
    # print('PC-1(key)数量为：', cd)
    c = [cd[0:28]]
    d = [cd[28:]]
    k = list(range(16))
    for i in range(0, 16):
        c.append(c[i][Loop_table[i]:] + c[i][:Loop_table[i]])
        d.append(d[i][Loop_table[i]:] + d[i][:Loop_table[i]])
        #  = c[i+1] + d[i+1]
        for j in range(0, 48):
            k_tmp += (c[i+1] + d[i+1])[PC_2[j]-1]
        k[i] = k_tmp
        k_tmp = ""
    return k


# 加密主体
def encrypt(m=[], k=[]):
    c = []
    for i in range(0, len(m)):  # 循环数据块
        (m_tmp, c_tmp) = ('', '')
        (left, right) = ([], [])
        for j in range(0, 64):                # 初始置换
            m_tmp += m[i][IP_table[j]-1]
        print('m_tmp =', m_tmp)
        for j in range(0, 16):                # 16轮代换
            (e_tmp, s_tmp, p_tmp) = ('', '', '')
            if j == 0:
                left.append(m_tmp[:32])
                right.append(m_tmp[32:])
            for z in range(0, 48):            # E盒置换
                e_tmp += right[j][E[z] - 1]
            # print('E(R0)[48bits] = ' + e_tmp)
            e_tmp = bin(int(e_tmp, 2) ^ int(k[j], 2))[2:].zfill(len(k[j]))   # R 与 K异或

            # print('E(R)⊕K[48bits] = ' + e_tmp)

            for z in range(0, 8):           # S盒置换
                r_6 = e_tmp[6*z:6*(z+1)]
                row = int(r_6[0:6:5], 2)
                column = int(r_6[1:5], 2)
                # print('S[', row, ',', column, ']的值为', S[z][16*row+column],
                #       '其4位二进制为：', bin(S[z][16*row+column])[2:].zfill(4))
                s_tmp += bin(S[z][16*row+column])[2:].zfill(4)
            # print('s_tmp的值为', s_tmp)
            for z in range(0, 32):                # 初始置换
                p_tmp += s_tmp[P[z]-1]
            # print('p_tmp的值为', p_tmp)
            right.append(bin(int(p_tmp, 2) ^ int(left[j], 2))[2:].zfill(32))
            left.append(right[j])
            if j == 15:

                # print('第', i+1, '个数据块的L16的值为', left[j+1], '长度为', len(left[j+1]))
                # print('第', i+1, '个数据块的R16的值为', right[j+1], '长度为', len(right[j+1]), '\n')
                for z in range(0, 17):
                    print('（加密）第', i + 1, '个数据块的L',z,'的值为', left[z], '长度为', len(left[z]))
                    print('（加密）第', i + 1, '个数据块的R',z,'的值为', right[z], '长度为', len(right[z])
                )
                for z in range(0, 64):
                    c_tmp += (right[j+1] + left[j+1])[IP_re_table[z] - 1]
                c.append(c_tmp)
    return c


# 整合
def integration(a, cip=[]):
    str_c = ''
    if a == 1:
        length = 8
    elif a == 2:
        length = 16
    for i in range(0, len(cip)):
        for j in range(0, int(64/length)):
            c_tmp = cip[i][j * length:j * length + length]
            if i == len(cip) and c_tmp == '0000000000000000' and a == 2:
                return str_c
            if i == len(cip) and c_tmp == '00000000' and a == 1:
                return  str_c
            str_c += chr(int(c_tmp, 2))
    return str_c


'''test_m = encrypt(['0000000000110100000000000011100000000000001101100000000000110010'], generate_sub_key('ABCDEFGH'))
for u in test_m:
    print(u)'''
'''print(ord('A'))
print(bin(ord('A')))
print(bin(ord('A'))[2:])
print(bin(ord('A'))[2:].zfill(16))'''


'''
a = bytes.fromhex('00000000000000000000000000011011100000111000')
print(a, type(a))
a = ''.join(['%02x' % x for x in a])
print(a, type(a))

lst = message_pretreatment('这就是所谓的快乐吗？，爱了爱了')
abc = generate_sub_key('ABCDEFGH')
ymt = encrypt(lst, abc)
for aa in range(0, len(ymt)):
    print(ymt[aa])'''



