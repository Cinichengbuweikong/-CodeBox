import base64

from Crypto.Hash import SHA256
from Crypto.Cipher import Salsa20

from constants import SALT, KEY


def hash(s: str) -> str:
    """
    给定一个字符串 方法会对其进行加盐处理后再哈希 得到一个字符串
    s: str  要被哈希处理的字符串
    """

    s = s + SALT

    hasher = SHA256.new()
    hasher.update(s.encode())

    hashres = base64.b64encode(hasher.digest()).decode()

    return hashres


def encrypt(s: str) -> str:
    """
    给定一个字符串 方法将对其进行非对称加密
    方法返回加密后的结果
    注: 同一输入多次加密的结果不一致
    """

    cipher = Salsa20.new(key=KEY.encode())
    ciphertext: bytes = cipher.encrypt(s.encode())
    return base64.b64encode(ciphertext).decode()


def decrypt(s: str) -> str:
    """
    给定一个非对称加密的字符串 方法将对其进行解密
    方法返回解密后的结果
    """

    data = base64.b64decode(s.encode())
    
    cipher = Salsa20.new(key=KEY.encode())
    plaintext: bytes = cipher.decrypt(data)
    return plaintext.decode()
