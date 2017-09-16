from Crypto.Cipher import AES
from collections import OrderedDict

from shutil import copy

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QButtonGroup, QSpacerItem, QVBoxLayout, QSizePolicy, \
    QLabel, QLineEdit

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
            # print(content)

            keyword_index[index_json[file]] = content
            all_words += content

        all_words = list(set(all_words))  # make words list unique
        # print(keyword_index)
        # print(all_words)

        inverted_index = {word: [txt for txt, words in keyword_index.items() if word in words] for word in all_words}
        # print(inverted_index)

        ordered_inverted_index = OrderedDict(sorted(inverted_index.items(), key=lambda x: x[0]))
        # print(ordered_inverted_index)

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

            # print(file)
            # print(type(encryption_list), encryption_list)
            # print('+++++++++++++++++++++++++++++++++++')

            enc_list = '|||'.join(encryption_list)
            # print(enc_list)

            new_path = files_destination + file.split('.')[0] + '.txt'
            write_to_file(new_path, repr(enc_list))


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
                path.append('*')
                cipherbytes = self.sse.encrypt(doc_key, iv, [value])
                ciphertext = bytes_2_string(cipherbytes[0])
                lst.append(''.join(path) + '--' + ciphertext)

            path = saved_path

        return lst


    def generate_search_token(self, keyword):
        index_key = read_bin_file(get_longer_path('index_key'))
        ivs = read_json_file(get_longer_path('ivs'))

        search_token = []
        for doc_id, iv in ivs.items():
            search_token += self.sse.encrypt(index_key, string_2_bytes(iv, 'latin-1'), [keyword])

        return search_token


    def search(self, search_token, operator):
        # possible operators: 'eq', 'ne', 'gt', 'gte', 'lt', 'lte'
        encrypted_index = read_ordered_json_file(get_longer_path('encrypted_index'))
        str_search_token = [bytes_2_string(token) for token in search_token]

        doc_ids2return = get_docs2return(encrypted_index, str_search_token, operator)

        # self.copy_encrypted_files_to_user(doc_ids2return)

        return set(doc_ids2return)


    def copy_encrypted_files_to_user(self, doc_ids2return):
        doc_index_switched = read_json_file(get_longer_path('doc_index_switched'))

        print(doc_ids2return)

        for doc_id in doc_ids2return:
            file = doc_index_switched[str(doc_id)]
            filepath = get_longer_path('server') + file.split('.')[0] + '.txt'
            # copy encrypted file to user
            copy(filepath, get_longer_path('user_enc'))


    def decrypt_documents(self):
        doc_index = read_json_file(get_longer_path('doc_index'))
        doc_key = read_bin_file(get_longer_path('document_key'))
        ivs = read_json_file(get_longer_path('ivs'))

        files = os.listdir(get_longer_path('user_enc'))

        for file in files:
            file_name = str(file.split('.')[0]) + '.json'

            doc_id = doc_index[file_name]
            iv = string_2_bytes(ivs[str(doc_id)], 'latin-1')

            content = read_file_string(get_longer_path('user_enc') + file).split('|||')

            ordered_dict = OrderedDict()
            for item in content:
                item_split = item.split('--')
                item_num = item_split[0]
                item_hash = string_2_bytes(item_split[1], 'latin-1')
                item_hash = remove_double_backslashes(item_hash)

                decrypted_hash = self.sse.decrypt(doc_key, iv, [item_hash])

                ordered_dict[item_num] = decrypted_hash[0]

            json = make_json_from_decrypted_file(ordered_dict)

            # write to decrypted folder
            write_obj_to_json_file(json, get_longer_path('user_dec') + file_name)


    def delete_user_directories(self):
        enc_path = get_longer_path('user_enc')
        dec_path = get_longer_path('user_dec')
        enc_files = os.listdir(enc_path)
        dec_files = os.listdir(dec_path)
        [os.remove(enc_path + f) for f in enc_files]
        [os.remove(dec_path + f) for f in dec_files]




class SearhGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.height = 480
        self.width = 720

        self.setGeometry(700, 150, self.width, self.height)
        self.setWindowTitle('SSE')

        self.init_UI()


    def init_UI(self):
        ver_spacing = 100
        hor_spacing = 20

        left_bracket = QPushButton('(', self)
        right_bracket = QPushButton(')', self)
        left_bracket.move(hor_spacing, hor_spacing)
        right_bracket.move(ver_spacing+hor_spacing, hor_spacing)

        self.horizontal_line(3*hor_spacing)

        properties_widget = QWidget(self)
        properties_widget.move(hor_spacing, 4*hor_spacing)
        properties_button_group = QButtonGroup()
        birth_date = QPushButton('birthDate', properties_widget)
        properties_button_group.addButton(birth_date)
        first_name = QPushButton('firstName', properties_widget)
        first_name.move(ver_spacing, 0)
        properties_button_group.addButton(first_name)
        last_name = QPushButton('lastName', properties_widget)
        last_name.move(2*ver_spacing, 0)
        properties_button_group.addButton(last_name)
        street = QPushButton('street', properties_widget)
        street.move(3*ver_spacing, 0)
        properties_button_group.addButton(street)
        house_number = QPushButton('houseNum', properties_widget)
        house_number.move(4*ver_spacing, 0)
        properties_button_group.addButton(house_number)
        city = QPushButton('city', properties_widget)
        city.move(5*ver_spacing, 0)
        properties_button_group.addButton(city)
        post_code = QPushButton('postCode', properties_widget)
        post_code.move(6*ver_spacing, 0)
        properties_button_group.addButton(post_code)
        country = QPushButton('country', properties_widget)
        country.move(0, 2*hor_spacing)
        properties_button_group.addButton(country)
        type_of = QPushButton('type', properties_widget)
        type_of.move(ver_spacing, 2 * hor_spacing)
        properties_button_group.addButton(type_of)
        temperature = QPushButton('temperature', properties_widget)
        temperature.move(2*ver_spacing, 2*hor_spacing)
        properties_button_group.addButton(temperature)
        heart_rate = QPushButton('heartRate', properties_widget)
        heart_rate.move(3*ver_spacing, 2*hor_spacing)
        properties_button_group.addButton(heart_rate)
        diastolic = QPushButton('diastolic', properties_widget)
        diastolic.move(4*ver_spacing, 2*hor_spacing)
        properties_button_group.addButton(diastolic)
        systolic = QPushButton('systolic', properties_widget)
        systolic.move(5*ver_spacing, 2*hor_spacing)
        properties_button_group.addButton(systolic)
        spO2 = QPushButton('spO2', properties_widget)
        spO2.move(6*ver_spacing, 2*hor_spacing)
        properties_button_group.addButton(spO2)

        self.horizontal_line(8*hor_spacing)

        operators_widget = QWidget(self)
        operators_widget.move(hor_spacing, 9*hor_spacing)
        operators_button_group = QButtonGroup()
        eq = QPushButton('=', operators_widget)
        operators_button_group.addButton(eq)
        ne = QPushButton('≠', operators_widget)
        ne.move(ver_spacing, 0)
        operators_button_group.addButton(ne)
        lt = QPushButton('<', operators_widget)
        lt.move(2*ver_spacing, 0)
        operators_button_group.addButton(lt)
        lte = QPushButton('≤', operators_widget)
        lte.move(3*ver_spacing, 0)
        operators_button_group.addButton(lte)
        gt = QPushButton('>', operators_widget)
        gt.move(4*ver_spacing, 0)
        operators_button_group.addButton(gt)
        gte = QPushButton('≥', operators_widget)
        gte.move(5*ver_spacing, 0)
        operators_button_group.addButton(gte)

        self.horizontal_line(11*hor_spacing)

        value_widget = QWidget(self)
        value_widget.move(hor_spacing, 12*hor_spacing)
        val_label = QLabel('Value: ', value_widget)
        val_label.move(0, 4)
        val_line_edit = QLineEdit(value_widget)
        val_line_edit.setFixedWidth(2 * ver_spacing)
        val_line_edit.move(ver_spacing-hor_spacing, 0)
        val_button = QPushButton('OK', value_widget)
        val_button.move(3*ver_spacing, 0)

        self.horizontal_line(14*hor_spacing)

        and_or_widget = QWidget(self)
        and_or_widget.move(hor_spacing, 15*hor_spacing)
        and_button = QPushButton('AND', and_or_widget)
        or_button = QPushButton('OR', and_or_widget)
        or_button.move(ver_spacing, 0)

        self.horizontal_line(17*hor_spacing)

        info_widget = QWidget(self)
        info_widget.move(hor_spacing, 18*hor_spacing)
        query_label = QLabel('Selected query: ', info_widget)
        query = QLabel('abba', info_widget)
        query.move(0, int(1.5*hor_spacing))
        query.setStyleSheet("QLabel {color : blue;}")

        self.horizontal_line(21*hor_spacing)

        commit_widget = QWidget(self)
        commit_widget.move(hor_spacing, 22*hor_spacing)
        search_button = QPushButton('Search!', commit_widget)
        info_label = QLabel('test', commit_widget)
        info_label.move(ver_spacing, 4)






    def horizontal_line(self, y):
        horizontal_line = QWidget(self)
        horizontal_line.setFixedSize(self.width, 1)
        horizontal_line.setStyleSheet("background-color: black;")
        horizontal_line.move(0, y)






if __name__ == '__main__':
    ope = OPE()

    # ope.create_inverted_keyword_index()
    # ope.encrypt_index()
    # ope.encrypt_documents()

    # ope.delete_user_directories()
    #
    # token = ope.generate_search_token(path_strings('heartRate') + '50')
    # doc_ids_1 = ope.search(token, 'gt')
    # print(doc_ids_1)
    #
    # token = ope.generate_search_token(path_strings('spO2') + '99')
    # doc_ids_2 = ope.search(token, 'eq')
    # print(doc_ids_2)
    #
    # intersection = doc_ids_1.intersection(doc_ids_2)
    # print('intersection', intersection)
    #
    # union = doc_ids_1.union(doc_ids_2)
    # print('union', union)


    # ope.copy_encrypted_files_to_user(union)
    # ope.decrypt_documents()


    app = QApplication([])
    w = SearhGUI()
    w.show()
    app.exec_()


    # def sayHello():
    #     print ("Hello World!")
    #
    # app = QApplication([])
    # button = QPushButton("Click me")
    # button.clicked.connect(sayHello)
    # button.show()
    # app.exec_()


