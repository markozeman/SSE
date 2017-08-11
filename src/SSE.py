import os

from cryptography.fernet import Fernet
from Crypto.Cipher import DES3, AES
import pyDes

from help_functions import *


class SSE:
    def __init__(self):
        # self.generate_and_save_keys()
        # self.update_IVs_and_doc_index()
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

    def update_IVs_and_doc_index(self):
        obj, changed_ids = make_document_index('../Data')

        curr_ivs = read_json_file('../Private/IVs/ivs.json')

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
        # returns list of bytes
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

    def create_switched_document_index(self):
        curr_json = read_json_file('../Private/document_index.json')
        switched_json = {value: key for key, value in curr_json.items() if (key != 'current_value')}
        write_obj_to_json_file(switched_json, '../Private/document_index_switched.json')

    def create_inverted_keyword_index(self, files_destination):
        # files_destination is a list of strings
        index_json = read_json_file('../Private/document_index.json')

        all_words = []
        keyword_index = {}
        files = os.listdir(files_destination)
        for path in files:
            content = read_file(files_destination + path)
            # print(path, content)
            keyword_index[index_json[path]] = content
            all_words += content

        all_words = list(set(all_words))  # make words list unique
        # print(keyword_index)
        # print(all_words)

        inverted_index = {word: [txt for txt, words in keyword_index.items() if word in words] for word in all_words}
        print(inverted_index)

        write_obj_to_json_file(inverted_index, '../Private/inverted_index.json')

    def update_inverted_keyword_index(self, changed_files):
        # can apply to only new files
        # changed_files is a list of strings
        index_json = read_json_file('../Private/document_index.json')

        all_words = []
        new_keyword_index = {}
        for path in changed_files:
            content = read_file('../Data/' + path)
            # print(path, content)
            new_keyword_index[index_json[path]] = content
            all_words += content

        all_words = list(set(all_words))  # make words list unique

        curr_inverted_index = read_json_file('../Private/inverted_index.json')
        new_inverted_index = {word: [txt for txt, words in new_keyword_index.items() if word in words] for word in all_words}
        print(curr_inverted_index)
        print(new_inverted_index)

        for key, value in new_inverted_index.items():
            if (key in curr_inverted_index):
                curr_inverted_index[key] += value
                curr_inverted_index[key] = list(set(curr_inverted_index[key]))
            else:
                curr_inverted_index[key] = value

        print(curr_inverted_index)
        write_obj_to_json_file(curr_inverted_index, '../Private/inverted_index.json')

    def encrypt_index(self):
        inverted_index = read_json_file('../Private/inverted_index.json')
        index_key = read_bin_file('../Private/keys/index_key')
        ivs = read_json_file('../Private/IVs/ivs.json')

        encrypted_index = {}
        for word, document_ids in inverted_index.items():
            for doc_id in document_ids:
                iv = string_2_bytes(ivs[str(doc_id)], 'latin-1')
                ciphertext = bytes_2_string(self.encrypt(index_key, iv, [word])[0])
                encrypted_index[ciphertext] = doc_id
        print(len(encrypted_index), encrypted_index)

        write_obj_to_json_file(encrypted_index, '../Private/encrypted_index.json')



if __name__ == '__main__':
    sse = SSE()

    # sse.create_inverted_keyword_index('../Data/')

    sse.encrypt_index()


    # sse.update_inverted_keyword_index(['text_18.txt'])


    '''
    key = read_bin_file('../Private/keys/index_key')
    # print(key)

    res = read_json_file('../Private/IVs/ivs.json')
    # print(res)
    iv = string_2_bytes(res['2'], 'latin-1')
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
