import hashlib

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from validate_email import validate_email
from GUI import client_gui, doctor_gui

import sys

import client
from Petclinic.ClientClass import ClientClass
from Petclinic.DoctorClass import DoctorClass


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 300, 200)
        self.center()
        v_box = QVBoxLayout()

        self.user_email_field = QLineEdit("bobemail@test.com")
        self.password_field = QLineEdit("bobpassword")
        self.is_doc = QCheckBox("I am doctor")
        self.btn_login = QPushButton("Войти")
        self.btn_register = QPushButton("Зарегистрироваться")
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.register)

        v_box.addWidget(self.user_email_field)
        v_box.addWidget(self.password_field)
        v_box.addWidget(self.is_doc)
        v_box.addWidget(self.btn_login)
        v_box.addWidget(self.btn_register)

        self.setLayout(v_box)
        self.setWindowTitle("login, please :)")
        self.show()

    def login(self):
        email = self.user_email_field.text()
        password = self.password_field.text()

        if email.__len__() > 255 or password.__len__() > 255:
            QMessageBox.critical(self, "Ошибка ", "Превышена допустимая длина полей или поля", QMessageBox.Ok)
        elif email.isspace() or password.isspace():
            QMessageBox.critical(self, "Ошибка ", "Не заполнены обязательные поля email или password", QMessageBox.Ok)
        elif not validate_email(email) or ('.' not in email):
            QMessageBox.critical(self, "Ошибка ", "Неверный формат email", QMessageBox.Ok)
        else:
            if self.is_doc.isChecked():
                self.login_doctor(email, password)
            else:
                self.login_client(email, password)

    def login_doctor(self, email: str, password: str):
        if client.is_doctor_with_email(email):
            self.doctor = DoctorClass.decrypt(client.get_doctor_by_email(email))
            has_password = hashlib.md5(bytes(password, 'utf-8')).hexdigest()
            if self.doctor.password == has_password:
                self.new_window = doctor_gui.DocWindow(self.doctor)
                self.close()
            else:
                QMessageBox.critical(self, "Ошибка ", "Неверный email или пароль", QMessageBox.Ok)

        else:
            QMessageBox.critical(self, "Ошибка ", "Доктора с таким email нет в базе", QMessageBox.Ok)

    def login_client(self, email: str, password: str):
        if client.is_client_with_email(email):
            self.client = ClientClass.decrypt(client.get_client_by_email(email))
            has_password = hashlib.md5(bytes(password, 'utf-8')).hexdigest()
            if self.client.password == has_password:
                self.new_window = client_gui.ClientWindow(self.client)
                self.close()
            else:
                QMessageBox.critical(self, "Ошибка ", "Неверный email или пароль", QMessageBox.Ok)

        else:
            QMessageBox.critical(self, "Ошибка ", "Клиент с таким email не зарегистрирован", QMessageBox.Ok)

    def register(self):
        if self.is_doc.isChecked():
            QMessageBox.information(self, "Внимание", "Доктора уже зарегистрированны", QMessageBox.Ok)
        else:
            self.new_window = RegisterDialog()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class RegisterDialog(QDialog):
    exp_dialog = None

    def __init__(self):
        super().__init__()
        v_box_main = QVBoxLayout()
        h_box_buttons = QHBoxLayout()
        self.surname_title = QLabel("Фамилия:")
        self.surname = QLineEdit()
        self.name_title = QLabel("Имя:")
        self.name = QLineEdit()
        self.patronymic_title = QLabel("Отчество:")
        self.patronymic = QLineEdit()
        self.email_title = QLabel("адрес эл. почты:")
        self.email = QLineEdit()
        self.phone_title = QLabel("номер телефона (сотовый):")
        self.phone = QLineEdit()
        self.password_title = QLabel("пароль:")
        self.password = QLineEdit()
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

        self.btn_cancel = QPushButton("отмена")
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_register = QPushButton("загеристрироваться")
        self.btn_register.clicked.connect(self.register)
        h_box_buttons.addWidget(self.btn_cancel)
        h_box_buttons.addWidget(self.btn_register)
        v_box_main.addLayout(h_box_buttons)
        self.setWindowTitle("Регистрация")
        self.setLayout(v_box_main)
        self.show()

    def cancel(self):
        self.close()

    def register(self):
        surname = str(self.surname.text())
        name = str(self.name.text())
        patronymic = str(self.patronymic.text())
        email = str(self.email.text())

        phone = str(self.phone.text())
        password = str(self.password.text())
        new_fio = f'{surname} {name} {patronymic}'

        if client.is_client_with_email(email):
            QMessageBox.critical(self, "Ошибка", "Клиент с таким email уже зарегистрирован", QMessageBox.Ok)
        elif self.is_pass(surname, name, patronymic, email, phone, password):
            QMessageBox.critical(self, "Ошибка", "Остались незаполненные поля", QMessageBox.Ok)
        elif new_fio.__len__() > 255 or phone.__len__() > 10 or \
                email.__len__() > 255 or password.__len__() > 255:
            QMessageBox.critical(self, "Ошибка", "Превышена допустимая длина полей или поля", QMessageBox.Ok)
        elif not phone.isdigit():
            QMessageBox.critical(self, "Ошибка", "В поле телефон можно вводить только цифры без разделителей",
                                 QMessageBox.Ok)
        elif not validate_email(email) or ('.' not in email):
            QMessageBox.critical(self, "Ошибка ", "Неверный формат email", QMessageBox.Ok)
        else:
            client.add_client(new_fio, email, phone, 1, password)
            QMessageBox.information(self, "Успешно", "Регистрация завершена", QMessageBox.Ok)
            self.close()

    def is_pass(self, *lines) -> bool:
        for line in lines:
            if line == '' or line.isspace():
                return True
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = LoginWindow()
    sys.exit(app.exec_())
