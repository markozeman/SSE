import time

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from help_functions import *

from OPE import OPE


class SearchGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.ope = OPE()

        self.height = 480
        self.width = 720

        self.setGeometry(700, 150, self.width, self.height)
        self.setWindowTitle('SSE')

        self.last_clicked_property = None

        self.init_UI()

    def init_UI(self):
        ver_spacing = 100
        hor_spacing = 20

        left_bracket = QPushButton('(', self)
        left_bracket.move(hor_spacing, hor_spacing)
        self.connect_button(left_bracket)
        right_bracket = QPushButton(')', self)
        right_bracket.move(ver_spacing+hor_spacing, hor_spacing)
        self.connect_button(right_bracket)

        self.brackets_buttons = [left_bracket, right_bracket]

        self.horizontal_line(3*hor_spacing)

        properties_widget = QWidget(self)
        properties_widget.move(hor_spacing, 4*hor_spacing)
        birth_date = QPushButton('birthDate', properties_widget)
        self.connect_button(birth_date)
        first_name = QPushButton('firstName', properties_widget)
        first_name.move(ver_spacing, 0)
        self.connect_button(first_name)
        last_name = QPushButton('lastName', properties_widget)
        last_name.move(2*ver_spacing, 0)
        self.connect_button(last_name)
        street = QPushButton('street', properties_widget)
        street.move(3*ver_spacing, 0)
        self.connect_button(street)
        house_number = QPushButton('houseNum', properties_widget)
        house_number.move(4*ver_spacing, 0)
        self.connect_button(house_number)
        city = QPushButton('city', properties_widget)
        city.move(5*ver_spacing, 0)
        self.connect_button(city)
        post_code = QPushButton('postCode', properties_widget)
        post_code.move(6*ver_spacing, 0)
        self.connect_button(post_code)
        country = QPushButton('country', properties_widget)
        country.move(0, 2*hor_spacing)
        self.connect_button(country)
        type_of = QPushButton('type', properties_widget)
        type_of.move(ver_spacing, 2 * hor_spacing)
        self.connect_button(type_of)
        temperature = QPushButton('temperature', properties_widget)
        temperature.move(2*ver_spacing, 2*hor_spacing)
        self.connect_button(temperature)
        heart_rate = QPushButton('heartRate', properties_widget)
        heart_rate.move(3*ver_spacing, 2*hor_spacing)
        self.connect_button(heart_rate)
        diastolic = QPushButton('diastolic', properties_widget)
        diastolic.move(4*ver_spacing, 2*hor_spacing)
        self.connect_button(diastolic)
        systolic = QPushButton('systolic', properties_widget)
        systolic.move(5*ver_spacing, 2*hor_spacing)
        self.connect_button(systolic)
        spO2 = QPushButton('spO2', properties_widget)
        spO2.move(6*ver_spacing, 2*hor_spacing)
        self.connect_button(spO2)

        self.properties_buttons = [birth_date, first_name, last_name, street, house_number, city, post_code,
                                   country, type_of, temperature, heart_rate, diastolic, systolic, spO2]

        self.horizontal_line(8*hor_spacing)

        operators_widget = QWidget(self)
        operators_widget.move(hor_spacing, 9*hor_spacing)
        eq = QPushButton('=', operators_widget)
        self.connect_button(eq)
        ne = QPushButton('≠', operators_widget)
        ne.move(ver_spacing, 0)
        self.connect_button(ne)
        lt = QPushButton('<', operators_widget)
        lt.move(2*ver_spacing, 0)
        self.connect_button(lt)
        lte = QPushButton('≤', operators_widget)
        lte.move(3*ver_spacing, 0)
        self.connect_button(lte)
        gt = QPushButton('>', operators_widget)
        gt.move(4*ver_spacing, 0)
        self.connect_button(gt)
        gte = QPushButton('≥', operators_widget)
        gte.move(5*ver_spacing, 0)
        self.connect_button(gte)

        self.operators_buttons = [eq, ne, lt, lte, gt, gte]
        self.buttons_state(self.operators_buttons, 'disable')

        self.horizontal_line(11*hor_spacing)

        value_widget = QWidget(self)
        value_widget.move(hor_spacing, 12*hor_spacing)
        val_label = QLabel('Value: ', value_widget)
        val_label.move(0, 4)
        self.val_line_edit = QLineEdit(value_widget)
        self.val_line_edit.setFixedWidth(2 * ver_spacing)
        self.val_line_edit.move(ver_spacing-hor_spacing, 0)
        self.val_line_edit.setDisabled(True)
        self.val_line_edit.returnPressed.connect(self.ok_clicked)
        self.ok_button = QPushButton('OK', value_widget)
        self.ok_button.move(3*ver_spacing, 0)
        self.ok_button.clicked.connect(self.ok_clicked)
        self.ok_button.setDisabled(True)

        self.horizontal_line(14*hor_spacing)

        and_or_widget = QWidget(self)
        and_or_widget.move(hor_spacing, 15*hor_spacing)
        and_button = QPushButton('AND', and_or_widget)
        self.connect_button(and_button)
        or_button = QPushButton('OR', and_or_widget)
        or_button.move(ver_spacing, 0)
        self.connect_button(or_button)

        self.and_or_buttons = [and_button, or_button]
        self.buttons_state(self.and_or_buttons, 'disable')

        self.horizontal_line(17*hor_spacing)

        info_widget = QWidget(self)
        info_widget.move(hor_spacing, 18*hor_spacing)
        query_label = QLabel('Selected query: ', info_widget)
        self.query = QLabel('', info_widget)
        self.query.move(0, int(1.5*hor_spacing))
        self.query.setStyleSheet("QLabel {color : blue;}")
        self.query.setFixedWidth(self.width)

        self.horizontal_line(21*hor_spacing)

        commit_widget = QWidget(self)
        commit_widget.move(hor_spacing, 22*hor_spacing)
        search_button = QPushButton('Search!', commit_widget)
        search_button.clicked.connect(self.search_clicked)
        clear_button = QPushButton('Clear', commit_widget)
        clear_button.move(ver_spacing, 0)
        clear_button.clicked.connect(self.clear_clicked)
        self.info_label = QLabel('', commit_widget)
        self.info_label.move(2*ver_spacing, 4)
        self.info_label.setFixedWidth(self.width-2*ver_spacing)

    def horizontal_line(self, y):
        horizontal_line = QWidget(self)
        horizontal_line.setFixedSize(self.width, 1)
        horizontal_line.setStyleSheet("background-color: black;")
        horizontal_line.move(0, y)

    def button_clicked(self, button):
        btn_txt = button.text()
        if (button in self.properties_buttons):
            self.last_clicked_property = btn_txt
            self.buttons_state(self.properties_buttons, 'disable')
            self.buttons_state(self.brackets_buttons, 'disable')
            self.buttons_state(self.operators_buttons, 'enable')
        elif (button in self.operators_buttons):
            self.buttons_state(self.operators_buttons, 'disable')
            self.val_line_edit.setEnabled(True)
            self.val_line_edit.clear()
            self.val_line_edit.setPlaceholderText(self.type_of_var(self.last_clicked_property)[1])
            self.val_line_edit.setFocus(True)
            self.ok_button.setEnabled(True)
        elif (btn_txt == 'AND' or btn_txt == 'OR'):
            self.buttons_state(self.and_or_buttons, 'disable')
            self.buttons_state(self.properties_buttons, 'enable')

        new_text = self.query.text() + btn_txt + ' '
        self.query.setText(new_text)

    def clear_clicked(self):
        self.query.clear()
        self.info_label.clear()
        self.val_line_edit.clear()
        self.val_line_edit.setDisabled(True)
        self.buttons_state(self.and_or_buttons, 'disable')
        self.buttons_state(self.operators_buttons, 'disable')
        self.buttons_state(self.brackets_buttons, 'enable')
        self.buttons_state(self.properties_buttons, 'enable')

    def ok_clicked(self):
        val = self.val_line_edit.text()

        type_of_var = self.type_of_var(self.last_clicked_property)[0]
        if (type_of_var == 'd'):
            if (not is_date_format(val)):
                self.info_label.setText('Value should be date.')
                return
        elif (type_of_var == 'n'):
            if (not is_number(val)):
                self.info_label.setText('Value should be number with dot separator.')
                return

        self.query.setText(self.query.text() + val + ' ')
        self.val_line_edit.setDisabled(True)
        self.ok_button.setDisabled(True)
        self.buttons_state(self.and_or_buttons, 'enable')
        self.buttons_state(self.brackets_buttons, 'enable')

    def search_clicked(self):
        start_time = time.time()

        query = self.query.text()
        query_split = [x.strip() for x in re.split(r'[()]', query) if x.strip()]

        brackets_ok = matched_brackets(query)
        if (brackets_ok):
            if (len(query_split) == 0):
                self.info_label.setText('Query cannot be empty.')
                return

            res = []
            for q in query_split:
                parameters = q.split(' ')

                if (len(parameters) == 1 and (parameters[0] == 'AND' or parameters[0] == 'OR')):
                    res.append(parameters[0])
                elif ('AND' not in parameters and 'OR' not in parameters):    # only one condition
                    if (len(parameters) != 3):
                        self.info_label.setText('Query is not correct.')
                        return

                    property = parameters[0]
                    path_string = path_strings(property)
                    operator = parameters[1]
                    value = ' '.join(parameters[2:])

                    curr_value, position = find_closest_value(path_string, operator, value, property_type(property))

                    token = self.ope.generate_search_token(path_string + curr_value)
                    doc_ids = self.ope.search(token, operator_string(operator), position)
                    res.append(doc_ids)
                else:
                    and_operators = [i for i, j in enumerate(parameters) if j == 'AND']
                    or_operators = [i for i, j in enumerate(parameters) if j == 'OR']
                    and_or_operators = and_operators + or_operators
                    and_or_operators.sort()

                    i = 0
                    part_res = []
                    while (i < len(parameters)):
                        if (i in and_or_operators):
                            part_res.append(parameters[i])
                        elif (i == 0 or i-1 in and_or_operators):   # property
                            property = parameters[i]
                            path_string = path_strings(property)
                        elif (i == 1 or i-2 in and_or_operators):   # operator
                            operator = parameters[i]
                        elif (i == 2 or i-3 in and_or_operators):   # start of value
                            val = []
                            while (i < len(parameters) and i not in and_or_operators):
                                val.append(parameters[i])
                                i += 1
                            i -= 1
                            value = ' '.join(val)

                            curr_value, position = find_closest_value(path_string, operator, value, property_type(property))

                            token = self.ope.generate_search_token(path_string + curr_value)
                            doc_ids = self.ope.search(token, operator_string(operator), position)
                            part_res.append(doc_ids)
                        i += 1

                    # solve part_res in save into res
                    part_res = solve_expression(part_res)
                    res += part_res

            # solve res
            res = solve_expression(res)

            # clear directory, copy encrypted files and decrypt them
            self.ope.delete_user_directories()
            if (len(res) == 1):
                num_of_files = self.ope.copy_encrypted_files_to_user(res[0])
                self.ope.decrypt_documents()
                end_time = time.time()
                self.info_label.setText('Documents matching query: ' + str(num_of_files) + '.' + 5*' ' +
                                        'Query took ' + "{0:.1f}".format(1000*(end_time - start_time)) + ' ms.')

            else:
                print('res does not have one element.')
        else:
            self.info_label.setText('Brackets are not set correctly.')

    def connect_button(self, btn):
        btn.clicked.connect(lambda: self.button_clicked(btn))

    def buttons_state(self, buttons, state):
        if (state == 'enable'):
            for btn in buttons:
                btn.setEnabled(True)
        elif (state == 'disable'):
            for btn in buttons:
                btn.setDisabled(True)

    def type_of_var(self, string):
        dates = ['birthDate']
        numbers = ['houseNum', 'postCode', 'temperature', 'heartRate', 'diastolic', 'systolic', 'spO2']
        strings = ['firstName', 'lastName', 'street', 'country', 'city', 'type']

        if (string in dates):
            return ['d', 'YYYY-MM-DD']
        elif (string in numbers):
            return ['n', '36.2']
        elif (string in strings):
            return ['s', 'some string']




if __name__ == '__main__':
    app = QApplication([])
    w = SearchGUI()
    w.show()
    app.exec_()
