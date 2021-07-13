import base64


# 用于base64加密密码
class BaseSec:
    def __init__(self):
        pass

    def base_en(self, string):
        """
        string-->传入字符串进行base64加密,str类型
        """
        msg = base64.b64encode(string.encode('utf-8'))
        return msg.decode()

    def base_de(self, string):
        """
        string-->传入字符串进行base64解密,str类型
        """
        msg = base64.b64decode(string)
        return msg.decode()


if __name__ == "__main__":
    base = BaseSec()
    str1 = base.base_en('jlbtest@238#')
    print(str1)
    str2 = base.base_de(str1)
    print(str2)
