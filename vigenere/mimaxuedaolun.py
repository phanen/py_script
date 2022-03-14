import string
from typing import Optional

# 有意义的英文频度序列
std_freq = [0.0788,
            0.0156,
            0.0268,
            0.0389,
            0.1268,
            0.0256,
            0.0187,
            0.0573,
            0.0707,
            0.0010,
            0.0060,
            0.0394,
            0.0244,
            0.0706,
            0.0776,
            0.0186,
            0.0009,
            0.0594,
            0.0634,
            0.0978,
            0.0280,
            0.0102,
            0.0214,
            0.0016,
            0.0202,
            0.0006]

def cipher_slice(cipher, m) -> list:
    """将密文字符串分为多组, 字符索引模m同余的为一组"""
    cipher_lst = []
    for i in range(m):
        cipher_lst.append(cipher[i::m])
    return cipher_lst


def freq_calc(s: str) -> list[int]:
    """统计字符串中各字母频数"""
    freq_dict = dict(zip(string.ascii_lowercase, [0] * 26))
    for c in s:
        freq_dict[c] += 1
    return list(freq_dict.values())


def ci_calc(s: str) -> float:
    """计算字符串的重合指数"""
    # 统计各个字符的频数
    freq = freq_calc(s)
    # 计算重合指数
    l = len(s)
    a = l * l - l
    b = 0
    for v in freq:
        b += v * v - v
    return b / a


def get_key_length(cipher: str, lbound=14) -> Optional[int]:
    """获取密钥长度"""
    m_ = lbound
    min_dis = 1
    for m in range(1, lbound):
        # 分 m 组
        cipher_lst = cipher_slice(cipher, m)

        # 计算各个组平均ci值
        n = len(cipher_lst)
        a = 0
        for sub_cipher in cipher_lst:
            a += ci_calc(sub_cipher)
        avg_ci = a / n

        # 找到第一个平均重合指数最接近0.065的分组方式
        new_dis = abs(avg_ci - 0.065)
        if new_dis < min_dis:
            min_dis = new_dis
            m_ = m
    return m_


def caesar_get_key(s: str) -> int:
    """移位密码破解"""
    # 密文的字母频数
    freq = freq_calc(s)
    # 密文分别左移 0-25 次
    max_a = 0  # 记录最大拟合度
    key = 0  # 记录最大拟合度对应的移位数
    for k in range(26):
        # 密文左移 k 位后的频数(相当于freq循环左移 k 位)
        k_left_freq = freq[k:] + freq[0:k]
        a = 0
        for p, q in zip(k_left_freq, std_freq):
            a += p * q
        # 取 与有意义英文分布 拟合度最高的移位数
        if a > max_a:
            max_a = a
            key = k
    # 密文左移 key 位得到原文 (原文右移 key 位得到密文) 所以key就是密钥
    return key


def get_key(cipher: str) -> list:
    key_length = get_key_length(cipher)
    cipher_lst = cipher_slice(cipher, key_length)
    key_lst = []
    for sub_cipher in cipher_lst:
        key_lst.append(caesar_get_key(sub_cipher))
    return key_lst


def decrypt(cipher, key) -> str:
    """解密"""
    plain = []
    n = len(key)
    for i, c in enumerate(cipher):
        plain.append(
            string.ascii_lowercase[(ord(c) - ord("a") - key[i % n]) % 26]
        )
    return "".join(plain)


def main():
    with open('.\ciphers\cipher1.txt') as f:
        ciphers = f.readlines()

    for i in range(1, len(ciphers) + 1):
        cipher = ciphers[i - 1][1:-1] # 去掉首序列号和尾换行符
        # 获取密钥
        key_lst = get_key(cipher)
        # 获取明文
        plain = decrypt(cipher, key_lst)
        # 密钥文本
        key = "".join([string.ascii_lowercase[i] for i in key_lst])
        # key2key = caesar_get_key(key)
        # plain2key = "".join([string.ascii_lowercase[i]
        #                      for i in [(ord(c) - ord("a") - key2key) for c in key]])

        # 打印
        # print(f"第{i}段密文：")
        print(f"密钥: {key}({len(key)}位)")
        # print("明文", plain)
        # print()

if __name__ == '__main__':
    main()
