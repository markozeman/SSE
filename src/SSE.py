import os

from cryptography.fernet import Fernet
from Crypto.Cipher import DES3, AES
import pyDes

from help_functions import *


class SSE:
    def __init__(self):
        # self.generate_and_save_keys()
        self.generate_and_save_IVs()
        pass

    def generate_and_save_keys(self):
        self.index_key = get_random_bytes(32)
        self.document_key = get_random_bytes(32)

        # write keys to binary files
        keys = [self.index_key, self.document_key]
        paths = ['../Private/keys/index_key', '../Private/keys/document_key']
        write_keys_to_file(keys, paths, bin=True)

        # write keys to text files
        keys = [bytes_2_string(self.index_key), bytes_2_string(self.document_key)]
        paths = ['../Private/keys/index_key.txt', '../Private/keys/document_key.txt']
        write_keys_to_file(keys, paths)

    def generate_and_save_IVs(self):
        obj, changed_ids = files_in_dir('../Data')

        try:
            curr_ivs = read_json_file('../Private/IVs/ivs.json')
        except IOError:
            print('Cannot open file at: ../Private/IVs/ivs.json')
            return False

        # -1 because of 'current_value' key
        if (len(obj)-1 == len(curr_ivs)):
            print('IVs are already up to date.')
            return

        diff = len(obj)-1 - len(curr_ivs)
        if (diff > 0):
            for i in range(diff):
                iv = get_random_bytes(16)
                curr_ivs[changed_ids[i]] = bytes_2_string(iv)
        else:
            for ch_id in changed_ids:
                curr_ivs.pop(str(ch_id), None)

        write_obj_to_json_file(curr_ivs, '../Private/IVs/ivs.json')

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

    '''
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

