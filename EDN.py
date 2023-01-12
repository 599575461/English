import base64
import uuid
from Crypto.Cipher import AES


class EDNCrypto:
    def __init__(self):
        self.encrypted_text = b''
        self.decrypted_text = ''

    def en(self, text):
        """
        password->uuid(去掉-)->ord->str->chr->password
        text->encode('utf-8')->b64encode->decode('utf-8')->ord->add_to_16->AES_encrypt->b64encode
        加密
        :return: list
        """
        password = ''.join(list(map(lambda x: str(x), [ord(i) for i in list(str(uuid.uuid1()).replace("-", "")) if
                                                       not str(i).isdigit()]))).replace('0', '')
        for i in [
            base64.b64encode(AES.new(self.add_to_16(password[:6]), AES.MODE_ECB).encrypt(self.add_to_16(str(i))))[:-2]
            for i in [ord(i) for i in
                      base64.b64encode(text.encode('utf-8')).decode('utf-8')]]:
            self.encrypted_text += i

        dncrypted_text = self.cut(self.encrypted_text.decode(), 5)
        dncrypted_text.append([chr(int(i)) for i in self.cut(password, 2)])
        return dncrypted_text

    def dn(self, encrypted_text: list):
        """
        解密
        :param encrypted_text
        :return: None
        """
        password = ''.join(str(i) for i in [str(ord(i)) for i in encrypted_text[-1]])
        encrypted_text.pop()
        try:
            for i in [
                AES.new(self.add_to_16(password[:6]), AES.MODE_ECB).decrypt(
                    base64.b64decode(i.encode() + b'==')).replace(
                    b'\x00', b'').decode() for i in [i + '==' for i in self.cut(''.join(encrypted_text), 22)]]:
                self.decrypted_text += chr(int(i))
            return base64.b64decode(self.decrypted_text.encode('utf-8')).decode('utf-8')
        except UnicodeDecodeError:
            return str(base64.b16encode('密码错了,嘿嘿'.encode('GBK')).decode('utf-8'))

    @staticmethod
    def add_to_16(value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)

    @staticmethod
    def cut(obj, sec):
        return [obj[i:i + sec] for i in range(0, len(obj), sec)]
