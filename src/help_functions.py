import os
import json
import re


def write_to_file(filepath, content):
    f = open(filepath, 'w')
    f.write(content)
    f.close()


def write_to_bin_file(filepath, content):
    f = open(filepath, 'wb')
    f.write(content)
    f.close()


def read_file(filepath):
    regex_remove = re.compile('[,\.\[\]!?():;]')
    with open(filepath) as f:
        content = f.read().split()
        content = [regex_remove.sub('', c) for c in content]
        return content


def enc_read_file(filepath):
    with open(filepath) as f:
        content = f.read().split(' ')
        # content = [c.replace('\n', '\r') for c in content]
        return content


def read_encrypted_file(filepath):
    with open(filepath) as f:
        content = f.readlines()

        bytes_content = []
        for i in range(len(content)):
            if (i == len(content)-1):   # last line
                b = string_2_bytes(content[i], 'latin-1')
            else:
                b = string_2_bytes(content[i][:-1], 'latin-1')
            bytes_content.append(b)

        return bytes_content


def read_bin_file(filepath):
    with open(filepath, "rb") as f:
        B = []
        byte = f.read(1)
        B.append(byte)
        while byte != b"":
            byte = f.read(1)
            B.append(byte)
        return b''.join(B)


def pad(data):
    length = 16 - (len(data) % 16)
    data += bytes([length]) * length
    return data


def unpad(data):
    return data[:-data[-1]]


def get_random_bytes(length):
    return os.urandom(length)


def bytes_2_string(B):
    return B.decode("latin-1")


def bytes_2_utf8_string(B):
    return B.decode("utf-8")


def string_2_bytes(s, encoding):
    return bytes(s, encoding)


def write_keys_to_file(keys, filepaths, bin=False):
    if (len(keys) != len(filepaths)):
        raise SyntaxError('Keys and filepaths lists must have same length.')
    for i in range(len(keys)):
        if (bin):
            write_to_bin_file(filepaths[i], keys[i])
        else:
            write_to_file(filepaths[i], keys[i])


def write_obj_to_json_file(obj, filepath):
    with open(filepath, 'w') as outfile:
        json.dump(obj, outfile)


def read_json_file(filepath):
    try:
        with open(filepath) as data_file:
            return json.load(data_file)
    except IOError:
        print('Cannot open file at: ', filepath)
        return False


def repair_data(content):
    repaired = []
    i = 0
    while (i < len(content)):
        val = content[i]
        if (i < len(content) - 1):
            next_val = content[i + 1]

        if (len(val) == 15 and len(next_val) != 0):
            if (b'\n' in val):
                new_val = val.replace(b'\n', b'\r\n')
            else:
                new_val = b' ' + val
            repaired.append(new_val)
        elif not (len(val) / 16).is_integer():
            repaired.append(val + string_2_bytes(' ', 'latin-1') + next_val)
            i += 1
        elif (len(val) != 0):
            repaired.append(val)
        i += 1

    return repaired


def get_path(short_path):
    paths = {
        'doc_index': '../Private/document_index.json',
        'doc_index_switched': '../Server/document_index_switched.json',

        'inverted_index': '../Private/inverted_index.json',

        'index_key': '../Private/keys/index_key',
        'index_key_txt': '../Private/keys/index_key.txt',
        'document_key': '../Private/keys/document_key',
        'document_key_txt': '../Private/keys/document_key.txt',

        'ivs': '../Private/IVs/ivs.json',

        'encrypted_index': '../Server/encrypted_index.json',

        'data': '../Data/',
        'server': '../Server/',
        'user_enc': '../User/encrypted/',
        'user_dec': '../User/decrypted/'
    }
    return paths[short_path]
