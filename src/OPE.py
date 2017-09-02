from Crypto.Cipher import AES
from collections import OrderedDict

import copy

from help_functions import *

import SSE
from SSE import SSE


class OPE:
    def __init__(self):
        self.sse = SSE()

    def create_inverted_keyword_index(self):
        index_json = read_json_file(get_longer_path('doc_index'))

        all_words = []
        keyword_index = {}
        files = os.listdir(get_longer_path('data'))
        for file in files:
            json = read_json_file(get_longer_path('data') + file)
            # print(file, content)

            content = self.recursive_json(json, [], [])
            print(content)

            keyword_index[index_json[file]] = content
            all_words += content

        all_words = list(set(all_words))  # make words list unique
        # print(keyword_index)
        # print(all_words)

        inverted_index = {word: [txt for txt, words in keyword_index.items() if word in words] for word in all_words}
        # print(inverted_index)

        ordered_inverted_index = OrderedDict(sorted(inverted_index.items(), key=lambda x: x[0]))
        print(ordered_inverted_index)

        write_obj_to_json_file(ordered_inverted_index, get_longer_path('inverted_index'))


    def recursive_json(self, json, path, file_content):
        for key, value in json.items():
            curr_path = path[:]
            if not isinstance(value, dict):
                path.extend((str(key), str(value)))
                file_content.append('//'.join(path))
            else:
                path.append(str(key))
                self.recursive_json(value, path, file_content)
            path = curr_path
        return file_content


    def encrypt_index(self):
        inverted_index = read_ordered_json_file(get_longer_path('inverted_index'))
        index_key = read_bin_file(get_longer_path('index_key'))
        ivs = read_json_file(get_longer_path('ivs'))

        encrypted_index = []
        encrypted_index.append(('number_of_files', len(os.listdir(get_longer_path('data')))))
        for word, document_ids in inverted_index.items():
            for doc_id in document_ids:
                iv = string_2_bytes(ivs[str(doc_id)], 'latin-1')
                ciphertext = bytes_2_string(self.sse.encrypt(index_key, iv, [word])[0])
                encrypted_index.append((ciphertext, doc_id))

        ordered_encrypted_index = OrderedDict(encrypted_index)
        # print(ordered_encrypted_index)

        write_obj_to_json_file(ordered_encrypted_index, get_longer_path('encrypted_index'))


    def encrypt_documents(self):
        # files_source is path to directory with files
        files_source = get_longer_path('data')
        # files_destination is path to directory with newly encrypted files
        files_destination = get_longer_path('server')

        key = read_bin_file(get_longer_path('document_key'))
        ivs = read_json_file(get_longer_path('ivs'))
        doc_index = read_json_file(get_longer_path('doc_index'))

        files = os.listdir(files_source)
        for file in files:
            json = read_ordered_json_file(files_source + file)

            doc_id = doc_index[file]
            iv = string_2_bytes(ivs[str(doc_id)], 'latin-1')

            encryption_list = self.recursive_encryption(json, [], [], key, iv)

            print(file)
            print(type(encryption_list), encryption_list)
            print('+++++++++++++++++++++++++++++++++++')

            enc_list = '\n'.join(encryption_list)
            print(enc_list)

            new_path = files_destination + file.split('.')[0] + '.txt'
            write_to_file(new_path, enc_list)

        test = read_file_by_lines('../../Server/JanezNovak.txt')
        print(test)



    def recursive_encryption(self, json, path, lst, doc_key, iv):
        for key, value in json.items():
            saved_path = path[:]
            curr_path = str(list(json.keys()).index(key))
            path.append(curr_path)
            cipherbytes = self.sse.encrypt(doc_key, iv, [key])
            ciphertext = bytes_2_string(cipherbytes[0])
            lst.append(''.join(path) + '--' + ciphertext)

            if isinstance(value, dict):
                self.recursive_encryption(value, path, lst, doc_key, iv)
            else:
                path.append('0')
                cipherbytes = self.sse.encrypt(doc_key, iv, [value])
                ciphertext = bytes_2_string(cipherbytes[0])
                lst.append(''.join(path) + '--' + ciphertext)

            path = saved_path

        return lst






if __name__ == '__main__':
    ope = OPE()

    # ope.create_inverted_keyword_index()
    # ope.encrypt_index()
    ope.encrypt_documents()