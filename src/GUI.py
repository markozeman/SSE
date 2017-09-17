from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QButtonGroup, QSizePolicy, QLabel, QLineEdit, \
    QAbstractButton


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
        left_bracket.move(hor_spacing, hor_spacing)
        self.connect_button(left_bracket)
        right_bracket = QPushButton(')', self)
        right_bracket.move(ver_spacing+hor_spacing, hor_spacing)
        self.connect_button(right_bracket)

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

        self.horizontal_line(11*hor_spacing)

        value_widget = QWidget(self)
        value_widget.move(hor_spacing, 12*hor_spacing)
        val_label = QLabel('Value: ', value_widget)
        val_label.move(0, 4)
        self.val_line_edit = QLineEdit(value_widget)
        self.val_line_edit.setFixedWidth(2 * ver_spacing)
        self.val_line_edit.move(ver_spacing-hor_spacing, 0)
        ok_button = QPushButton('OK', value_widget)
        ok_button.move(3*ver_spacing, 0)
        ok_button.clicked.connect(self.ok_clicked)

        self.horizontal_line(14*hor_spacing)

        and_or_widget = QWidget(self)
        and_or_widget.move(hor_spacing, 15*hor_spacing)
        and_button = QPushButton('AND', and_or_widget)
        self.connect_button(and_button)
        or_button = QPushButton('OR', and_or_widget)
        or_button.move(ver_spacing, 0)
        self.connect_button(or_button)

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
        clear_button = QPushButton('Clear', commit_widget)
        clear_button.move(ver_spacing, 0)
        clear_button.clicked.connect(self.clear_clicked)
        info_label = QLabel('test', commit_widget)
        info_label.move(2*ver_spacing, 4)
        info_label.setFixedWidth(self.width-2*ver_spacing)

    def horizontal_line(self, y):
        horizontal_line = QWidget(self)
        horizontal_line.setFixedSize(self.width, 1)
        horizontal_line.setStyleSheet("background-color: black;")
        horizontal_line.move(0, y)

    def button_clicked(self, button):
        new_text = self.query.text() + button.text() + ' '
        self.query.setText(new_text)

    def clear_clicked(self):
        self.query.clear()

    def ok_clicked(self):
        val = self.val_line_edit.text()
        self.query.setText(self.query.text() + val + ' ')

    def connect_button(self, btn):
        btn.clicked.connect(lambda: self.button_clicked(btn))




