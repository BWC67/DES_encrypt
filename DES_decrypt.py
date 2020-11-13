# !/usr/bin/python3
# --coding:utf-8--
from DES_BOX import *
import DES_encrypt


def main(key, c_text=[]):
    k = DES_encrypt.generate_sub_key(key)   # 调用加密内得子密钥生成函数
    tmp = len(c_text)
    m = list(range(tmp))
    for i in range(0, tmp):
        c_tmp = ''
        (left, right) = (list(range(17)), list(range(17)))
        for j in range(0, 64):
            c_tmp += c_text[i][IP_table[j] - 1]
        for j in range(0, 16):
            (e_tmp, s_tmp, p_tmp, m_tmp) = ('', '', '', '')
            if j == 0:
                left[16] = c_tmp[32:]
                right[16] = c_tmp[:32]
            right[15-j] = left[16-j]

            for z in range(0, 48):          # E盒置换
                e_tmp += right[15-j][E[z] - 1]
            e_tmp = bin(int(e_tmp, 2) ^ int(k[15-j], 2))[2:].zfill(len(k[15-j]))

            for z in range(0, 8):           # S盒置换
                r_6 = e_tmp[6 * z:6 * (z + 1)]
                row = int(r_6[0:6:5], 2)
                column = int(r_6[1:5], 2)
                s_tmp += bin(S[z][16 * row + column])[2:].zfill(4)

            for z in range(0, 32):          # 初始置换
                p_tmp += s_tmp[P[z] - 1]
            p_tmp = bin(int(p_tmp, 2) ^ int(right[16-j], 2))[2:].zfill(32)
            left[15-j] = p_tmp

        for j in range(0, 64):
            m_tmp += (left[0] + right[0])[IP_re_table[j] - 1]
        m[i] = m_tmp
    return m


'''text_key = 'ABCD1234'
text_m = '你好啊，很高兴认识你。'

bin_key = DES_encrypt.generate_sub_key(text_key)
print('\n\'%s\' 子密钥生成如下：' % text_key)
for u in bin_key:
    print(u)

bin_m = DES_encrypt.message_pretreatment(2, text_m)
print('\n\'%s\' 预处理后二进制如下：' % text_m)
for u in bin_m:
    print(u)

bin_c = DES_encrypt.encrypt(bin_m, bin_key)
print('\n 加密完的二进制数据如下：')
for u in bin_c:
    print(u)

text_c = DES_encrypt.integration(2, bin_c)
print('\n', '加密完的字符串如下', '\n', text_c)

d_bin = main('ABCDEFGH', DES_encrypt.message_pretreatment(2, text_c))
print('\n 解密完的二进制数据如下：')
for u in d_bin:
    print(u)

d_text = DES_encrypt.integration(2, d_bin)
print('\n', '加密完的字符串如下', '\n', d_text)'''
