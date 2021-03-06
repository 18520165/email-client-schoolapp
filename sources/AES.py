from Crypto.Cipher import AES
from Crypto.Util import Padding

import base64


def pad(plainbytes, block_size, style):
    return Padding.pad(plainbytes, block_size, style)


def unpad(cipherbytes, block_size, style):
    return Padding.unpad(cipherbytes, block_size, style)


def AES_Encrypt(plaintext, key, iv):
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    ciphertext = cipher.encrypt(pad(plaintext.encode(), 16, "pkcs7"))

    result = base64.b64encode(ciphertext).decode()
    return result


def AES_Decrypt(ciphertext, key, iv):
    text = base64.b64decode(ciphertext)

    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    plaintext = cipher.decrypt(text)

    result = unpad(plaintext, 16, "pkcs7").decode()
    return result


# mess = "abcdef"
# key = "0123456789abcdef"
# iv = "0123456789abcdef"

# print(AES_Encrypt(mess, key, iv))
# print(AES_Decrypt(AES_Encrypt(mess, key, iv), key, iv))
