import os

from cryptography.fernet import Fernet
from Crypto.Cipher import DES3, AES
import pyDes

from help_functions import *


class SSE:
    def __init__(self):
        # self.generate_and_save_keys()
        # self.generate_and_save_IVs(True)
        pass

    def generate_and_save_keys(self):
        self.index_key = get_random_bytes(32)
        self.document_key = get_random_bytes(32)

        keys = [self.index_key, self.document_key]
        paths = ['../Private/keys/index_key', '../Private/keys/document_key']
        write_keys_to_file(keys, paths, bin=True)

        keys = [bytes_2_string(self.index_key), bytes_2_string(self.document_key)]
        paths = ['../Private/keys/index_key.txt', '../Private/keys/document_key.txt']
        write_keys_to_file(keys, paths)

    def generate_and_save_IVs(self, save=False):
        obj = files_in_dir('../Data', save=save)

        iv_obj = {}
        for key, value in obj.items():
            iv = get_random_bytes(16)
            iv_obj[value] = bytes_2_string(iv)

        if (save):
            write_obj_to_json_file(iv_obj, '../Private/IVs/ivs.json')

    def encrypt(self, key, IV, message):
        # key and IV are bytes, message is list of strings
        # returns bytes
        aes = AES.new(key, AES.MODE_CBC, IV)

        ciphertext = []
        for m in message:
            cipher = aes.encrypt(pad(string_2_bytes(m, 'utf-8')))
            ciphertext.append(cipher)
        return ciphertext

    def decrypt(self, key, IV, ciphertext):
        # key and IV are bytes, ciphertext is list of bytes
        # returns string
        aes = AES.new(key, AES.MODE_CBC, IV)

        plaintext = []
        for cipher in ciphertext:
            plain = unpad(aes.decrypt(cipher)).decode()
            plaintext.append(plain)
        return plaintext



if __name__ == '__main__':
    sse = SSE()

    key = read_bin_file('../Private/keys/index_key')
    # print(key)

    res = read_json_file('../Private/IVs/ivs.json')
    # print(res)
    iv = string_2_bytes(res['0'], 'latin-1')
    # print(iv, type(iv))

    mess = ['Danes je še lepo, a čudno dežuje...', '123lalala, čeno cieoje']

    print('\n')
    cipher = sse.encrypt(key, iv, mess)
    print('\ncipher: ', cipher)

    print('---------------------------------------------------------')
    print('---------------------------------------------------------')

    sse_222 = SSE()
    plain = sse_222.decrypt(key, iv, cipher)
    print('plain: ', plain)



    '''
    print('---------------------------------------------------------')
    print('AES CBC')

    obj = AES.new(b'This is a key123This is a key123', AES.MODE_CBC, b'This is an IV456')
    message = "Anja je lepa punca.".encode('utf-8')
    message = pad(message)
    ciphertext = obj.encrypt(message)
    print(ciphertext)

    obj_test = AES.new(b'This is a key123This is a key123', AES.MODE_CBC, b'This is an IV456')
    message = "Anja je ".encode('utf-8')
    message = pad(message)
    ciphertext = obj_test.encrypt(message)
    print(ciphertext)

    obj_test_2 = AES.new(b'This is a key123This is a key123', AES.MODE_CBC, b'This is an IV456')
    message = "Anja je ".encode('utf-8')
    message = pad(message)
    ciphertext = obj_test_2.encrypt(message)
    print(ciphertext)

    obj_test_3 = AES.new(b'This is a key123This is a key123', AES.MODE_CBC, b'This is an IV456')
    message = "lepa punca.".encode('utf-8')
    message = pad(message)
    ciphertext = obj_test_3.encrypt(message)
    print(ciphertext)

    obj2 = AES.new(b'This is a key123This is a key123', AES.MODE_CBC, b'This is an IV456')
    dec = obj2.decrypt(ciphertext)
    dec = unpad(dec)
    print(dec.decode())
    '''


    '''
    sse = SSE()
    print(sse.key, type(sse.key))

    # my_str = 'Danes je lep dan. Jutri bo še lepši, če bo sonce že posijalo 222.'
    my_str = "Hello world!"

    enc = sse.encrypt_2(my_str)
    print(enc, type(enc))

    dec = sse.decrypt_2(enc)
    print(dec, type(dec))

    print('---------------------------------------------------------')

    enc_2 = sse.encrypt_2(my_str)
    print(enc_2, type(enc_2), enc_2.decode())

    dec_2 = sse.decrypt_2(enc_2)
    print(dec_2, type(dec_2))

    # write_to_file('../Server/myfile', dec)

    print('---------------------------------------------------------')
    print('---------------------------------------------------------')
    print('---------------------------------------------------------')

    key = b'123456789012345678901234'

    des = DES3.new(key, DES3.MODE_ECB)
    print(des)

    text = '12345678901234  '.encode('utf-8')

    text_11 = '        '.encode('utf-8')

    cipher_text = des.encrypt(text)
    print(cipher_text)

    print(des.decrypt(cipher_text).decode())

    cipher_text_22222 = des.encrypt(text)
    print(cipher_text_22222)

    cipher_text_33333 = des.encrypt(text)
    print(cipher_text_33333)

    print('---------------------------------------------------------')
    print('---------------------------------------------------------')
    print('---------------------------------------------------------')

    data = "Please encrypt my data now now now  io".encode('utf-8')

    data_22 = "Please encrypt encryptčšžđ".encode('utf-8')

    # key = b"123456789012345678901234"
    # write_to_bin_file('../key', key)

    key = read_file('../key')
    key = str(key[0]).encode('utf-8')
    print(str(key[0]).encode('utf-8'))

    k = pyDes.triple_des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5)
    print(k)

    # d = k.encrypt(data)
    # print(type(d))
    # print("Encrypted: %r" % d)
    # print("Decrypted: %r" % k.decrypt(d).decode())

    from binascii import unhexlify

    d_22 = k.encrypt(data_22)

    # a = bytes(bytearray.fromhex(d_22))
    # b = unhexlify(d_22)
    # c = byte_2_hex(str(d_22))

    print("Encrypted 2: %r" % d_22)

    # write_to_bin_file('../encrypted', d_22)

    enc_file = read_bin_file('../encrypted')
    print(enc_file)

    print("Decrypted 2: %r" % k.decrypt(enc_file).decode())


    # print("Decrypted 2: %r" % k.decrypt(d_22).decode())
    '''
