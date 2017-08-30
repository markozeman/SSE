from Crypto.Cipher import AES
from collections import OrderedDict

from help_functions import *

import SSE
from SSE import SSE


class OPE:
    def __init__(self):
        self.sse = SSE()
        self.back = '../'

    def create_inverted_keyword_index(self):
        index_json = read_json_file(self.back + get_path('doc_index'))

        all_words = []
        keyword_index = {}
        files = os.listdir(self.back + get_path('data'))
        for file in files:
            json = read_json_file(self.back + get_path('data') + file)
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

        write_obj_to_json_file(ordered_inverted_index, self.back + get_path('inverted_index'))


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
        inverted_index = read_ordered_json_file(self.back + get_path('inverted_index'))
        index_key = read_bin_file(self.back + get_path('index_key'))
        ivs = read_json_file(self.back + get_path('ivs'))

        encrypted_index = []
        for word, document_ids in inverted_index.items():
            for doc_id in document_ids:
                iv = string_2_bytes(ivs[str(doc_id)], 'latin-1')
                ciphertext = bytes_2_string(self.sse.encrypt(index_key, iv, [word])[0])
                encrypted_index.append((ciphertext, doc_id))

        print(encrypted_index)
        ordered_encrypted_index = OrderedDict(encrypted_index)
        # print(ordered_encrypted_index)

        write_obj_to_json_file(ordered_encrypted_index, self.back + get_path('encrypted_index'))











if __name__ == '__main__':
    ope = OPE()

    # ope.create_inverted_keyword_index()
    ope.encrypt_index()
