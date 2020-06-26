import hashlib

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from validate_email import validate_email
from GUI import *
from validate_email import validate_email
import sys

import client
from Petclinic.ClientClass import ClientClass
from Petclinic.DoctorClass import DoctorClass


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        # client.add_doctor('fio', 'email', 'phone', 'password', None, True)
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 300, 200)
        self.center()
        v_box = QVBoxLayout()
		h_box_buttons=QHBoxLayout()
        # client.generate_test_data()

        self.user_email_field = QLineEdit("bobemail@test.com")
        self.password_field = QLineEdit("bobpassword")
        self.is_doc = QCheckBox("I am doctor")
        self.btn_register=QPushButton("Зарегистрироваться")
        self.btn_register.clicked.connect(self.register)
        self.btn_login = QPushButton("Войти")
        self.btn_login.clicked.connect(self.login)

        v_box.addWidget(self.username_field)
        v_box.addWidget(self.password_field)
        v_box.addWidget(self.is_doc)
        h_box_buttons.addWidget(self.btn_register)
        h_box_buttons.addWidget(self.btn_login)
        v_box.addLayout(h_box_buttons)
        self.register_dialog=RegisterDialog(self)

    # Это заходят пользователи которые уже есть в базе
    def login(self):
        # Еще должна быть проверка что все обезательные поля заполнины
        email = self.user_email_field.text()
        password = self.password_field.text()

        if email.__len__() > 255 or password.__len__() > 255:
            QMessageBox.critical(self, "Ошибка ", "Превышена допустимая длина полей или поля", QMessageBox.Ok)
        elif email.isspace() or password.isspace():
            QMessageBox.critical(self, "Ошибка ", "Не заполнены обязательные поля email или password", QMessageBox.Ok)
            # self.new_window = LoginWindow()
        elif not validate_email(email) or ('.' not in email):
            QMessageBox.critical(self, "Ошибка ", "Неверный формат email", QMessageBox.Ok)
        else:
            if self.is_doc.isChecked():
                self.login_doctor(email, password)
            else:
                self.login_client(email, password)
            # self.close()

    def login_doctor(self, email: str, password: str):
        if client.is_doctor_with_email(email):
            self.doctor = DoctorClass.decrypt(client.get_doctor_by_email(email))
            has_password = hashlib.md5(bytes(password, 'utf-8')).hexdigest()
            if self.doctor.password == has_password:
                # self.new_window = doctor_gui.DocWindow(self.doctor)
                self.new_window = doctor_gui.DocWindow(self.doctor)
                self.close()
            else:
                # raise Exception
                QMessageBox.critical(self, "Ошибка ", "Неверный email или пароль", QMessageBox.Ok)
                # self.new_window = LoginWindow()

        else:
            # raise Exception
            QMessageBox.critical(self, "Ошибка ", "Доктора с таким email нет в базе", QMessageBox.Ok)
            # self.new_window = LoginWindow()

    def login_client(self, email: str, password: str):
        if client.is_client_with_email(email):
            self.client = ClientClass.decrypt(client.get_client_by_email(email))
            has_password = hashlib.md5(bytes(password, 'utf-8')).hexdigest()
            if self.client.password == has_password:
                self.new_window = client_gui.ClientWindow(self.client)
                self.close()
            else:
                # raise Exception
                QMessageBox.critical(self, "Ошибка ", "Неверный email или пароль", QMessageBox.Ok)
                # self.new_window = LoginWindow()

        else:
            client.add_client('None', email, 'None', 0, self.password_field.text())
            self.client = ClientClass.decrypt(client.get_client_by_email(email))
            self.new_window = client_gui.ClientWindow(self.client)
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
		
    def register(self):
        self.register_dialog.show()	


class RegisterDialog(QDialog):
    exp_dialog=None

    def __init__(self, root):
        super().__init__(root)
        self.main = root
        v_box_main=QVBoxLayout()
        h_box_buttons=QHBoxLayout()
        self.surname_title=QLabel("Фамилия:")
        self.surname=QLineEdit()
        self.name_title=QLabel("Имя:")
        self.name=QLineEdit()
        self.patronymic_title=QLabel("Отчество:")
        self.patronymic=QLineEdit()
        self.email_title=QLabel("адрес эл. почты:")
        self.email=QLineEdit()
        self.phone_title=QLabel("номер телефона (сотовый):")
        self.phone=QLineEdit()
        self.password_title=QLabel("пароль:")
        self.password=QLineEdit()
        v_box_main.addWidget(self.surname_title)
        v_box_main.addWidget(self.surname)
        v_box_main.addWidget(self.name_title)
        v_box_main.addWidget(self.name)
        v_box_main.addWidget(self.patronymic_title)
        v_box_main.addWidget(self.patronymic)
        v_box_main.addWidget(self.email_title)
        v_box_main.addWidget(self.email)
        v_box_main.addWidget(self.phone_title)
        v_box_main.addWidget(self.phone)
        v_box_main.addWidget(self.password_title)
        v_box_main.addWidget(self.password)

        self.btn_cancel=QPushButton("отмена")
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_register=QPushButton("загеристрироваться")
        self.btn_register.clicked.connect(self.register)
        h_box_buttons.addWidget(self.btn_cancel)
        h_box_buttons.addWidget(self.btn_register)
        v_box_main.addLayout(h_box_buttons)
        self.setWindowTitle("регистрация")
        self.setLayout(v_box_main)

    def cancel(self):
        self.close()

    def register(self):
        #если пользватель с таким email уже есть регистрация не проходит!
        #пользователь вносится в бд (теперь он сможет войти)

        user_is_already_exist=False

        surname=str(self.surname.text())
        name=str(self.name.text())
        patronymic=str(self.patronymic.text())
        email=str(self.email.text())
        phone=str(self.phone.text())
        password=str(self.password.text())
        #методы проверки из GUI/HelperMethods
        if check_correct_name(surname) and check_correct_name(name) and check_correct_name(patronymic) \
            and validate_email(email) and check_correct_phone(phone) and check_correct_password(password)\
                and not user_is_already_exist:
            fio=surname+" "+name+" "+patronymic
            #если данные корректны опользователь вносится в бд
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = LoginWindow()
    # myWindow.show()
    sys.exit(app.exec_())
