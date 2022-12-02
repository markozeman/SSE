from Crypto.Cipher import AES

from shutil import copy

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
        paths = [get_longer_path('index_key'), get_longer_path('document_key')]
        write_keys_to_file(keys, paths, bin=True)

        # write keys to text files
        keys = [bytes_2_string(self.index_key), bytes_2_string(self.document_key)]
        paths = [get_longer_path('index_key_txt'), get_longer_path('document_key_txt')]
        write_keys_to_file(keys, paths)

    def update_IVs_and_doc_index(self):
        obj, changed_ids = self.make_document_index(get_longer_path('data'))

        curr_ivs = read_json_file(get_longer_path('ivs'))

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

        write_obj_to_json_file(curr_ivs, get_longer_path('ivs'))

    def make_document_index(self, path):
        files = os.listdir(path)

        curr_json = read_json_file(get_longer_path('doc_index'))

        # -1 because of 'current_value' key
        if (len(files) == len(curr_json) - 1):
            print('Document index is already up to date.')
            return [curr_json, []]

        # update json file
        changed_ids = []
        current_value = curr_json['current_value'] if 'current_value' in curr_json else 0
        if (len(files) > len(curr_json) - 1):
            for i in range(len(files)):
                if (files[i] not in curr_json):
                    curr_json[files[i]] = current_value
                    changed_ids.append(current_value)
                    current_value += 1
            curr_json['current_value'] = current_value
        else:
            delete_keys = []
            for key, value in curr_json.items():
                if (key not in files and key != 'current_value'):
                    delete_keys.append(key)
                    changed_ids.append(value)

            for del_key in delete_keys:
                curr_json.pop(del_key, None)

        # save updated version
        write_obj_to_json_file(curr_json, get_longer_path('doc_index'))

        # update switched document index
        self.create_switched_document_index()

        return [curr_json, changed_ids]

    def encrypt(self, key, IV, message):
        # key and IV are bytes, message is list of strings
        # returns list of bytes
        aes = AES.new(key, AES.MODE_OFB, IV)

        ciphertext = []
        for m in message:
            cipher = aes.encrypt(pad(string_2_bytes(m, 'utf-8')))
            ciphertext.append(cipher)
        return ciphertext

    def decrypt(self, key, IV, ciphertext):
        # key and IV are bytes, ciphertext is list of bytes
        # returns string
        aes = AES.new(key, AES.MODE_OFB, IV)

        plaintext = []
        for cipher in ciphertext:
            if (len(cipher) > 0):
                plain = unpad(aes.decrypt(cipher)).decode()
                plaintext.append(plain)
            else:
                print('Cipher has no length.')
        return plaintext

    def create_switched_document_index(self):
        curr_json = read_json_file(get_longer_path('doc_index'))
        switched_json = {value: key for key, value in curr_json.items() if (key != 'current_value')}
        write_obj_to_json_file(switched_json, get_longer_path('doc_index_switched'))

    def create_inverted_keyword_index(self, files_destination):
        # files_destination is path to directory with files
        index_json = read_json_file(get_longer_path('doc_index'))

        all_words = []
        keyword_index = {}
        files = os.listdir(files_destination)
        for file in files:
            content = read_file(files_destination + file)
            # print(file, content)
            keyword_index[index_json[file]] = content
            all_words += content

        all_words = list(set(all_words))  # make words list unique
        # print(keyword_index)
        # print(all_words)

        inverted_index = {word: [txt for txt, words in keyword_index.items() if word in words] for word in all_words}
        # print(inverted_index)

        write_obj_to_json_file(inverted_index, get_longer_path('inverted_index'))

    def update_inverted_keyword_index(self, changed_files):
        # can apply to only new files
        # changed_files is a list of strings
        index_json = read_json_file(get_longer_path('doc_index'))

        all_words = []
        new_keyword_index = {}
        for path in changed_files:
            content = read_file(get_longer_path('data') + path)
            # print(path, content)
            new_keyword_index[index_json[path]] = content
            all_words += content

        all_words = list(set(all_words))  # make words list unique

        curr_inverted_index = read_json_file(get_longer_path('inverted_index'))
        new_inverted_index = {word: [txt for txt, words in new_keyword_index.items() if word in words] for word in all_words}
        # print(curr_inverted_index)
        # print(new_inverted_index)

        for key, value in new_inverted_index.items():
            if (key in curr_inverted_index):
                curr_inverted_index[key] += value
                curr_inverted_index[key] = list(set(curr_inverted_index[key]))
            else:
                curr_inverted_index[key] = value

        # print(curr_inverted_index)
        write_obj_to_json_file(curr_inverted_index, get_longer_path('inverted_index'))

    def encrypt_index(self):
        inverted_index = read_json_file(get_longer_path('inverted_index'))
        index_key = read_bin_file(get_longer_path('index_key'))
        ivs = read_json_file(get_longer_path('ivs'))

        encrypted_index = {}
        for word, document_ids in inverted_index.items():
            for doc_id in document_ids:
                iv = string_2_bytes(ivs[str(doc_id)], 'latin-1')
                ciphertext = bytes_2_string(self.encrypt(index_key, iv, [word])[0])
                encrypted_index[ciphertext] = doc_id
        # print(len(encrypted_index), encrypted_index)

        write_obj_to_json_file(encrypted_index, get_longer_path('encrypted_index'))

    def encrypt_documents(self, files_source, files_destination):
        # files_source is path to directory with files
        # files_destination is path to directory with newly encrypted files

        key = read_bin_file(get_longer_path('document_key'))
        ivs = read_json_file(get_longer_path('ivs'))
        doc_index = read_json_file(get_longer_path('doc_index'))

        files = os.listdir(files_source)
        for file in files:
            content = read_file(files_source + file)

            doc_id = doc_index[file]
            iv = string_2_bytes(ivs[str(doc_id)], 'latin-1')

            cipherbytes = self.encrypt(key, iv, content)

            ciphertext = [bytes_2_string(cb) for cb in cipherbytes]
            ciphertext = ' '.join(map(str, ciphertext))

            new_path = files_destination + file
            write_to_file(new_path, ciphertext)

    def generate_search_token(self, keyword):
        index_key = read_bin_file(get_longer_path('index_key'))
        ivs = read_json_file(get_longer_path('ivs'))

        search_token = []

        for doc_id, iv in ivs.items():
            search_token += self.encrypt(index_key, string_2_bytes(iv, 'latin-1'), [keyword])

        return search_token

    def search(self, search_token):
        encrypted_index = read_json_file(get_longer_path('encrypted_index'))
        doc_index_switched = read_json_file(get_longer_path('doc_index_switched'))
        str_search_token = [bytes_2_string(token) for token in search_token]

        doc_ids2return = [encrypted_index[token] for token in str_search_token if token in encrypted_index]
        print(doc_ids2return)

        for doc_id in doc_ids2return:
            file = doc_index_switched[str(doc_id)]
            filepath = get_longer_path('server') + file
            # copy encrypted file to user
            copy(filepath, get_longer_path('user_enc'))

    def decrypt_documents(self):
        doc_index = read_json_file(get_longer_path('doc_index'))
        doc_key = read_bin_file(get_longer_path('document_key'))
        ivs = read_json_file(get_longer_path('ivs'))

        files = os.listdir(get_longer_path('user_enc'))

        for file in files:
            content = enc_read_file(get_longer_path('user_enc') + file)
            content = [string_2_bytes(c, 'latin-1') for c in content]
            content = repair_data(content)

            doc_id = doc_index[file]
            iv = string_2_bytes(ivs[str(doc_id)], 'latin-1')

            plaintext = self.decrypt(doc_key, iv, content)

            stripped_plaintext = []
            for p in plaintext:
                if not p.isalnum() and len(p) > 1:
                    strip_p = re.sub(r'[^0-9a-žA-Ž\-]+', '', p)
                    stripped_plaintext.append(strip_p)
                else:
                    stripped_plaintext.append(p)

            stripped_plaintext = ' '.join(map(str, stripped_plaintext))

            # write to decrypted folder
            write_to_file(get_longer_path('user_dec') + file, stripped_plaintext)

    def delete_user_directories(self):
        enc_path = get_longer_path('user_enc')
        dec_path = get_longer_path('user_dec')
        enc_files = os.listdir(enc_path)
        dec_files = os.listdir(dec_path)
        [os.remove(enc_path + f) for f in enc_files]
        [os.remove(dec_path + f) for f in dec_files]

    def delete_server_text_files(self):
        server_path = get_longer_path('server')
        text_files = os.listdir(server_path)
        [os.remove(server_path + txt) for txt in text_files if txt.endswith(".txt")]




if __name__ == '__main__':
    sse = SSE()

    # sse.generate_and_save_keys()
    # sse.update_IVs_and_doc_index()
    # sse.create_switched_document_index()
    # sse.create_inverted_keyword_index(get_longer_path('data'))
    # sse.encrypt_index()
    # sse.encrypt_documents(get_longer_path('data'), get_longer_path('server'))

    # sse.delete_user_directories()

    # token = sse.generate_search_token('kruh')
    # sse.search(token)
    # sse.decrypt_documents()



    # sse.delete_user_directories()
    # sse.delete_server_text_files()




    '''
    key = read_bin_file(get_longer_path('document_key'))

    res = read_json_file(get_longer_path('ivs'))
    # print(res)
    iv = string_2_bytes(res['2'], 'latin-1')

    # mess = read_file(get_longer_path('data') + 'text_SLO_ZGO.txt')
    # print('mess', mess)

    a = sse.encrypt(key, iv, ['personal//name//Marko'])
    b = sse.encrypt(key, iv, ['personal//name//Janez'])

    dec_A = sse.decrypt(key, get_random_bytes(16), a)
    dec_B = sse.decrypt(key, iv, b)

    print(a)
    print(b)
    print(dec_A)
    print(dec_B)

    
    cipher = sse.encrypt(key, iv, mess)
    print('cipher', cipher)

    print(len(mess), len(cipher))

    ciphertext = [bytes_2_string(c) for c in cipher]
    ciphertext = ' '.join(map(str, ciphertext))
    # print('ciphertext')
    # print(ciphertext)

    write_to_file('../testing.txt', ciphertext)

    content = enc_read_file('../testing.txt')
    # print('read content')
    # print(content)

    content = [string_2_bytes(c, 'latin-1') for c in content]
    # print('\ncontent')
    # print(content)
    # print('len content: ', len(content))

    repaired = []
    i = 0
    while (i < len(content)):
        val = content[i]
        if (i < len(content)-1):
            next_val = content[i+1]
        if (len(val) == 15 and len(next_val) != 0):
            if (b'\n' in val):
                new_val = val.replace(b'\n', b'\r\n')
            else:
                new_val = b' ' + val

            # print('\nval', val)
            # print('rep', new_val)
            # print(new_val == val)
            # print(len(next_val))

            repaired.append(new_val)
            i += 1
            continue
        elif not (len(val) / 16).is_integer():
            # print(i)
            # print(val, next_val)
            repaired.append(val + string_2_bytes(' ', 'latin-1') + next_val)
            i += 1
        elif (len(val) != 0):
            repaired.append(val)
        i += 1

    print('\n\nrepaired', len(repaired), repaired)

    # repaired[87] = b' \xa9*\xf4U,\xa2V\xc2\x8a\xa8tf=E\xf3'


    # for i in range(len(repaired)):
    #     if (len(repaired[i]) != len(cipher[i])):
    #         print(i)
    #         print(len(repaired[i]), len(cipher[i]))
    #         print(repaired[i], cipher[i])
            # print(mess[i])
            # print()

    # print(len(cipher))
    # print(len(repaired))
    # print(len(cipher) == len(repaired))


    sse_2 = SSE()
    plain = sse_2.decrypt(key, iv, repaired)
    print(plain)
    '''



    '''
    key = read_bin_file(get_longer_path('document_key'))

    res = read_json_file(get_longer_path('ivs'))
    # print(res)
    iv = string_2_bytes(res['2'], 'latin-1')

    mess = ['riž', 'bučka', 'češnja']

    cipher = sse.encrypt(key, iv, mess)
    print(cipher)


    sse_2 = SSE()

    plain = sse_2.decrypt(key, iv, cipher)
    print(plain)
    '''

