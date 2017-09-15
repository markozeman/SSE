import os
import json
import re
import ast
from collections import OrderedDict



def remove_double_backslashes(b):
    return ast.literal_eval(str(b).replace('\\\\', '\\'))


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


def read_file_by_lines(filepath):
    with open(filepath) as f:
        return f.read().splitlines()


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


def read_file_string(filepath):
    with open(filepath) as f:
        content = f.read().strip("'")
        return content


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
        json.dump(obj, outfile, indent=4)


def read_json_file(filepath):
    try:
        with open(filepath) as data_file:
            return json.load(data_file)
    except IOError:
        print('Cannot open file at: ', filepath)
        return False


def read_ordered_json_file(filepath):
    try:
        with open(filepath) as data_file:
            return json.load(data_file, object_pairs_hook=OrderedDict)
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
        'doc_index': os.path.join('..', 'Private', 'document_index.json'),
        'doc_index_switched': os.path.join('..', 'Server', 'document_index_switched.json'),

        'inverted_index': os.path.join('..', 'Private', 'inverted_index.json'),

        'index_key': os.path.join('..', 'Private', 'keys', 'index_key'),
        'index_key_txt': os.path.join('..', 'Private', 'keys', 'index_key.txt'),
        'document_key': os.path.join('..', 'Private', 'keys', 'document_key'),
        'document_key_txt': os.path.join('..', 'Private', 'keys', 'document_key.txt'),

        'ivs': os.path.join('..', 'Private', 'IVs', 'ivs.json'),

        'encrypted_index': os.path.join('..', 'Server', 'encrypted_index.json'),

        'data': os.path.join('..', 'Data') + os.sep,
        'server': os.path.join('..', 'Server') + os.sep,
        'user_enc': os.path.join('..', 'User', 'encrypted') + os.sep,
        'user_dec': os.path.join('..', 'User', 'decrypted') + os.sep,
    }
    return paths[short_path]


def get_longer_path(short_path):
    return '../' + get_path(short_path)


def correct_lines(enc_list):
    lines = enc_list.split('\n')
    corrected_lines = []
    for i in range(len(lines)):
        if ('--' not in lines[i]):
            corrected_lines = corrected_lines[:-1]
            line = lines[i - 1] + '\n' + lines[i]
            corrected_lines.append(line)
        else:
            corrected_lines.append(lines[i])

    return corrected_lines


def make_json_from_decrypted_file(ordered_dict):
    json = OrderedDict()
    for key, value in ordered_dict.items():
        if (len(key) == 1):
            json[value] = OrderedDict()
        else:
            last_char = key[-1]
            if (last_char != '*'):
                key_chars_without_last = key[:-1]
                keys = [ordered_dict[key_chars_without_last[:(i + 1)]] for i in range(len(key_chars_without_last))]
                curr_json = json
                for k in keys:
                    curr_json = curr_json[k]

                curr_json[value] = OrderedDict()

            else:  # final data
                key_chars_without_last_2 = key[:-2]
                keys = [ordered_dict[key_chars_without_last[:(i + 1)]] for i in range(len(key_chars_without_last_2))]
                curr_json = json
                for k in keys:
                    curr_json = curr_json[k]

                curr_json[ordered_dict[key[:-1]]] = value

    return json
