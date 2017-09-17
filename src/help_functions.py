import datetime
import os
import json
import re
import ast
import math
from collections import OrderedDict
from dateutil.parser import parse



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
        content = f.read().strip("'\"")
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
    return os.path.join('..', get_path(short_path))


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


def path_strings(string):
    paths = {
        'birthDate': 'personal//birthDate//',
        'firstName': 'personal//firstName//',
        'lastName': 'personal//lastName//',

        'houseNum': 'personal//address//houseNumber//',
        'street': 'personal//address//street//',
        'country': 'personal//address//country//',
        'city': 'personal//address//city//',
        'postCode': 'personal//address//postCode//',

        'type': 'type//',

        'temperature': 'health//temperature//',
        'heartRate': 'health//heartRate//',
        'diastolic': 'health//diastolic//',
        'systolic': 'health//systolic//',
        'spO2': 'health//spO2//',
    }
    return paths[string]


def get_docs2return(encrypted_index, str_search_token, operator):
    if (operator == 'eq'):
        doc_ids2return = [encrypted_index[token] for token in str_search_token if token in encrypted_index]
    else:
        num_of_files = encrypted_index['number_of_files']
        indices = []
        doc_ids2return = []
        for token in str_search_token:
            if (token in encrypted_index):
                index = list(encrypted_index.keys()).index(token)
                indices.append(index)

        indices.sort()

        if (operator == 'lt' or operator == 'gte' or operator == 'ne'):     # for 'ne' it doesn't matter
            index = indices[0]
        elif (operator == 'gt' or operator == 'lte'):
            index = indices[-1]

        if (index % num_of_files != 0):
            start_index = math.floor(index / num_of_files) * num_of_files + 1
            end_index = math.ceil(index / num_of_files) * num_of_files
        else:
            start_index = index - num_of_files + 1
            end_index = index

        ordered_list = list(encrypted_index.items())

        if (operator == 'ne'):
            from_start_to_end = set([i for i in range(start_index, end_index + 1)])
            indices_set = set(indices)
            not_equals = from_start_to_end - indices_set
            for ind in not_equals:
                doc_ids2return.append(ordered_list[ind][1])
        elif (operator == 'gt'):
            for i in range(index + 1, end_index + 1):
                doc_ids2return.append(ordered_list[i][1])
        elif (operator == 'gte'):
            for i in range(index, end_index + 1):
                doc_ids2return.append(ordered_list[i][1])
        elif (operator == 'lt'):
            for i in range(index - 1, start_index - 1, -1):
                doc_ids2return.append(ordered_list[i][1])
        elif (operator == 'lte'):
            for i in range(index, start_index - 1, -1):
                doc_ids2return.append(ordered_list[i][1])

    return doc_ids2return


def matched_brackets(string):
    count = 0
    for i in string:
        if i == "(":
            count += 1
        elif i == ")":
            count -= 1
        if count < 0:
            return False
    return count == 0


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_date_format(string):
    date_reg_exp = re.compile('\d{4}[-]\d{2}[-]\d{2}')
    match = re.match(date_reg_exp, string)
    if (match is not None):
        try:
            parse(string)
            return True
        except ValueError:
            return False
    return False


def operator_string(operator):
    op = {
        '=': 'eq',
        '≠': 'ne',
        '<': 'lt',
        '≤': 'lte',
        '>': 'gt',
        '≥': 'gte',
    }
    return op[operator]

