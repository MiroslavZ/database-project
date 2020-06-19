from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import datetime
import copy
from GUILibrary.HelperMethods import *
from PyQt5.QtCore import Qt, QDate
import sys

class DocWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 640, 480)
        self.center()
        self.acc_button = QPushButton("ИМЯ ПОЛЬЗОВАТЕЛЯ")
        self.add_doc_button = QPushButton("СПИСОК ВРАЧЕЙ")
        self.change_data_button = QPushButton("ИЗМЕНИТЬ ДАННЫЕ")
        self.change_work_time_button = QPushButton("ЗАДАТЬ РАБОЧЕЕ ВРЕМЯ")
        self.change_med_button = QPushButton("СПИСОК ЛЕКАРСТВ")
        self.show_checkups_button = QPushButton("СПИСОК ОСМОТРОВ")
        self.add_client_button = QPushButton("СПИСОК КЛИЕНТОВ")
        self.acc_button.clicked.connect(self.exit_from_acc)
        self.change_data_button.clicked.connect(self.goToEditMyData)
        self.change_med_button.clicked.connect(self.goToEditMedicationWindow)
        self.add_doc_button.clicked.connect(self.goToEditDoctorsWindow)
        self.add_client_button.clicked.connect(self.goToEditClientsWindow)
        self.change_work_time_button.clicked.connect(self.goToEditWorktime)

        v_box_left = QVBoxLayout()
        v_box_left.addWidget(self.add_doc_button)
        v_box_left.addWidget(self.change_data_button)
        v_box_left.addWidget(self.change_work_time_button)
        v_box_left.addWidget(self.change_med_button)
        v_box_left.addWidget(self.show_checkups_button)
        v_box_left.addWidget(self.add_client_button)
        v_box_left.addStretch()

        v_box_center = QVBoxLayout()

        v_box_right = QVBoxLayout()
        v_box_right.addWidget(self.acc_button)
        v_box_right.addStretch()

        h_box_main = QHBoxLayout()
        h_box_main.addLayout(v_box_left)
        h_box_main.addStretch()
        h_box_main.addLayout(v_box_center)
        h_box_main.addStretch()
        h_box_main.addLayout(v_box_right)

        self.setLayout(h_box_main)
        self.setWindowTitle("Petclinic")
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'quit', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def goToNextWidget(self):
        pass

    def exit_from_acc(self):
        #self.new_window = LoginWindow()
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def goToEditMyData(self):
        self.new_window = UpdateMyDataWindow()

    def goToEditMedicationWindow(self):
        self.new_window = EditMedicationWindow()

    def goToEditDoctorsWindow(self):
        # изменять данные докторов и добалять новых может только админ!
        # у доктора есть поле is chief
        self.new_window=EditDoctorsWindow()

    def goToEditClientsWindow(self):
        self.new_window=EditClientsWindow()

    def goToEditWorktime(self):
        self.new_window=EditMyWorkTimeWindow()


# доктор может изменить свои данные, например контактный телефон
class UpdateMyDataWindow(QWidget):
    #поля-флаги для проерки было ли изменено что либо
    surnameIsChanged = False
    nameIsChanged = False
    phoneIsChanged = False
    emailIsChanged = False
    passwordIsChanged = False

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 500, 300)
        self.center()
        v_box_left = QVBoxLayout()
        v_box_right = QVBoxLayout()
        v_box_center = QVBoxLayout()
        h_box_main = QHBoxLayout()

        self.help1 = QLabel("Введите новые данные")
        self.help2 = QLabel("Если данные не изменились, оставьте поле пустым")

        self.new_surname_title = QLabel("Фамилия:")
        self.new_name_title = QLabel("Имя:")
        self.new_phone_title = QLabel("Телефон:")
        self.new_email_title = QLabel("Эл. почта:")
        self.new_password_title = QLabel("Пароль:")

        self.new_surname = QLineEdit()
        self.new_surname.textChanged[str].connect(self.surname_changed)
        self.new_name = QLineEdit()
        self.new_name.textChanged[str].connect(self.name_changed)
        self.new_phone = QLineEdit()
        self.new_phone.textChanged[str].connect(self.phone_changed)
        self.new_email = QLineEdit()
        self.new_email.textChanged[str].connect(self.email_changed)
        self.new_password = QLineEdit()
        self.new_password.textChanged[str].connect(self.name_changed)

        h_box_surname = QHBoxLayout()
        h_box_name = QHBoxLayout()
        h_box_phone = QHBoxLayout()
        h_box_email = QHBoxLayout()
        h_box_password = QHBoxLayout()

        h_box_surname.addWidget(self.new_surname_title)
        h_box_name.addWidget(self.new_name_title)
        h_box_phone.addWidget(self.new_phone_title)
        h_box_email.addWidget(self.new_email_title)
        h_box_password.addWidget(self.new_password_title)

        h_box_surname.addWidget(self.new_surname)
        h_box_name.addWidget(self.new_name)
        h_box_phone.addWidget(self.new_phone)
        h_box_email.addWidget(self.new_email)
        h_box_password.addWidget(self.new_password)

        v_box_left.addWidget(self.help1)
        v_box_left.addWidget(self.help2)
        v_box_left.addLayout(h_box_surname)
        v_box_left.addLayout(h_box_name)
        v_box_left.addLayout(h_box_phone)
        v_box_left.addLayout(h_box_email)
        v_box_left.addLayout(h_box_password)
        v_box_left.addStretch()

        self.actual_data_title = QLabel("Актуальные данные")
        self.actual_surname_title = QLabel("Фамилия - ")
        self.actual_name_title = QLabel("Имя - ")
        self.actual_phone_title = QLabel("Телефон - ")
        self.actual_email_title = QLabel("Эл. почта - ")
        self.actual_password_title = QLabel("Пароль - ")

        self.actual_surname = QLabel("ПУСТО")
        self.actual_name = QLabel("ПУСТО")
        self.actual_phone = QLabel("ПУСТО")
        self.actual_email = QLabel("ПУСТО")
        self.actual_password = QLabel("ПУСТО")
        # при вызове метода данные пользователя должны поместится
        # в соответсятвующие поля вместо "ПУСТО"
        self.update_actual_data()

        self.cancel_button=QPushButton("ОТМЕНА")
        self.cancel_button.clicked.connect(self.return_to_doc_window)
        self.save_button=QPushButton("СОХРАНИТЬ")
        self.save_button.clicked.connect(self.save_changes)

        h_box_actual_surname = QHBoxLayout()
        h_box_actual_name = QHBoxLayout()
        h_box_actual_phone = QHBoxLayout()
        h_box_actual_email = QHBoxLayout()
        h_box_actual_password = QHBoxLayout()
        h_box_buttons=QHBoxLayout()

        h_box_actual_surname.addWidget(self.actual_surname_title)
        h_box_actual_name.addWidget(self.actual_name_title)
        h_box_actual_phone.addWidget(self.actual_phone_title)
        h_box_actual_email.addWidget(self.actual_email_title)
        h_box_actual_password.addWidget(self.actual_password_title)

        h_box_actual_surname.addWidget(self.actual_surname)
        h_box_actual_name.addWidget(self.actual_name)
        h_box_actual_phone.addWidget(self.actual_phone)
        h_box_actual_email.addWidget(self.actual_email)
        h_box_actual_password.addWidget(self.actual_password)

        h_box_buttons.addWidget(self.cancel_button)
        h_box_buttons.addWidget(self.save_button)

        v_box_right.addWidget(self.actual_data_title)
        v_box_right.addLayout(h_box_actual_surname)
        v_box_right.addLayout(h_box_actual_name)
        v_box_right.addLayout(h_box_actual_phone)
        v_box_right.addLayout(h_box_actual_email)
        v_box_right.addLayout(h_box_actual_password)
        v_box_right.addLayout(h_box_buttons)
        v_box_right.addStretch()

        h_box_main.addLayout(v_box_left)
        h_box_main.addLayout(v_box_center)
        h_box_main.addLayout(v_box_right)
        self.setLayout(h_box_main)
        self.setWindowTitle("изменение личных данных")
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def save_changes(self):
        # перед закрытием окна данные которые пользователь обновил должны обновиться в БД
        self.close()

    def return_to_doc_window(self):
        self.close()

    # набор методов изменяющих поля на экране
    def email_changed(self,text):
        # pattern = compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
        # is_valid = pattern.match(text)
        # if is_valid:
        if check_correct_email(text):
            self.actual_email.setText(text)
            self.emailIsChanged=True

    def name_changed(self,text):
        # if len(text)>1:
        #     match1 = re.match("^[АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ]*$", text[0])
        #     match2 = re.match("^[абвгдеёжзиклмнопрстуфхцчшщъыьэюя]*$", text[1:])
        #     if match1 is not None and match2 is not None:
        if check_correct_name(text):
                self.actual_surname.setText(text)
                self.nameIsChanged=True

    def surname_changed(self,text):
        # if len(text)>1:
        #     match1 = re.match("^[АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ]*$", text[0])
        #     match2 = re.match("^[абвгдеёжзиклмнопрстуфхцчшщъыьэюя]*$", text[1:])
        #     if match1 is not None and match2 is not None:
        if check_correct_name(text):
                self.actual_surname.setText(text)
                self.surnameIsChanged=True

    def phone_changed(self,text):
        # match = re.match("^[0123456789]*$", text)
        # if match is not None and len(text)==11:
        if check_correct_phone(text):
            self.actual_phone.setText(text)
            self.passwordIsChanged=True

    def password_changed(self,text):
        if len(text)>0:
            self.actual_password.setText(text)


    # при вызове метода данные пользователя должны поместится
    # в соответсятвующие поля вместо "ПУСТО"
    # в классе есть поля-флаги для проерки было ли изменено что либо
    def update_actual_data(self):
        pass


class EditMedicationWindow(QWidget):
    medications=[]
    current_chosed_med=""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 300, 300)
        self.center()

        v_box_left = QVBoxLayout()
        v_box_right = QVBoxLayout()
        v_box_center = QVBoxLayout()
        h_box_main = QHBoxLayout()
        h_box_buttons=QHBoxLayout()

        self.options_title=QLabel("выберите опцию")
        self.button_pressed = False
        self.edit_option=QRadioButton("изменить лекарство")
        self.add_option=QRadioButton("добавить новое лекарство")
        self.button_group=QButtonGroup()
        self.button_group.addButton(self.edit_option)
        self.button_group.addButton(self.add_option)
        self.button_group.buttonClicked.connect(self.option_chosed)
        self.meds_list = QComboBox(self)
        self.fill_meds_list()
        self.meds_list.activated[str].connect(self.med_chosed)

        self.title_text=QLabel("Название:")
        self.title=QLineEdit()
        self.description_text=QLabel("Описание:")
        self.description=QLineEdit()
        self.cost_text=QLabel("Стоимость:")
        self.cost=QLineEdit()

        self.save_button=QPushButton("сохранить")
        self.delete_button=QPushButton("удалить")
        self.save_button.clicked.connect(self.save_changes)
        self.delete_button.clicked.connect(self.delete_med)

        v_box_left.addWidget(self.options_title)
        v_box_left.addWidget(self.edit_option)
        v_box_left.addWidget(self.add_option)
        v_box_left.addWidget(self.meds_list)
        v_box_left.addStretch()

        v_box_right.addWidget(self.title_text)
        v_box_right.addWidget(self.title)
        v_box_right.addWidget(self.description_text)
        v_box_right.addWidget(self.description)
        v_box_right.addWidget(self.cost_text)
        v_box_right.addWidget(self.cost)
        h_box_buttons.addWidget(self.delete_button)
        h_box_buttons.addWidget(self.save_button)
        v_box_right.addStretch()
        v_box_right.addLayout(h_box_buttons)

        h_box_main.addLayout(v_box_left)
        h_box_main.addLayout(v_box_center)
        h_box_main.addLayout(v_box_right)
        self.setLayout(h_box_main)
        self.setWindowTitle("список лекарств")
        self.show()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def save_changes(self):
        # сохранение измненений названия/описания/стоимости лекарства в бд
        # название изменяемого лекарства в self.current_chosed_med
        # обновление списка
        index=self.medications.index(self.current_chosed_med)
        self.medications[index]=str(self.title.text())
        self.fill_meds_list()
        pass

    def delete_med(self):
        # удаление лекарства
        if self.medications.__contains__(str(self.title.text())):
            self.medications.remove(str(self.title.text()))
            self.fill_meds_list()
        pass

    def add_med(self):
        # добавление нового лекарства в базу + обновление списка на экране
        # self.title, self.description, self.cost
        # список обновляется fill_meds_list
        if not self.medications.__contains__(str(self.title.text())):
            self.medications.append(str(self.title.text()))
            self.fill_meds_list()
        pass

    def return_to_doc_window(self):
        self.close()

    def option_chosed(self, button):
        self.delete_buttons_fragment()
        if button.text() == "изменить лекарство":
            self.show_edit_save_buttons()
        elif button.text() == "добавить новое лекарство":
            self.show_add_button()
        self.button_pressed=True

    def med_chosed(self,text):
        # щелчок по эл-ту списка
        # при выборе лекарства показать его поля,
        # поместить их в self.title, self.description, self.cost
        self.current_chosed_med=copy.copy(text)
        self.title.setText(text)
        pass

    # метод для заполнения списка лекарств (список состоит из названий)
    # после удаления/добавления лекарста надо обновить список
    def fill_meds_list(self):
        # это для примера
        self.meds_list.clear()
        self.meds_list.addItems(self.medications)
        #self.meds_list.addItems(["Фармакс", "Агроветзащита", "Астрафрм","Талисмед", "Novartis"])

    # clearLayout и delete_last_fragment нужны для удаления предыдущего layout с экрана
    # layout удаляется когда выбрана другая опция
    def clearLayout(self,layout):
        if layout != None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def delete_buttons_fragment(self):
        h_box_main = self.layout()
        v_box_right=h_box_main.itemAt(h_box_main.count()-1)
        h_box_buttons=v_box_right.itemAt(v_box_right.count()-1)
        self.clearLayout(h_box_buttons)
        h_box_main.removeItem(h_box_buttons)
        self.setLayout(h_box_main)

    def show_edit_save_buttons(self):
        h_box_main = self.layout()
        v_box_right=h_box_main.itemAt(h_box_main.count()-1)
        print(type(v_box_right))
        self.save_button=QPushButton("сохранить")
        self.delete_button=QPushButton("удалить")
        self.save_button.clicked.connect(self.save_changes)
        self.delete_button.clicked.connect(self.delete_med)
        h_box_buttons=QHBoxLayout()
        h_box_buttons.addWidget(self.delete_button)
        h_box_buttons.addWidget(self.save_button)
        v_box_right.addLayout(h_box_buttons)
        self.setLayout(h_box_main)

    def show_add_button(self):
        h_box_main = self.layout()
        v_box_right=h_box_main.itemAt(h_box_main.count()-1)
        print(type(v_box_right))
        self.save_button=QPushButton("добавить")
        self.save_button.clicked.connect(self.add_med)
        h_box_buttons=QHBoxLayout()
        h_box_buttons.addWidget(self.save_button)
        v_box_right.addLayout(h_box_buttons)
        self.setLayout(h_box_main)


# изменять данные докторов и добалять новых может только админ!
class EditDoctorsWindow(QWidget):
    doctors=[]
    current_chosed_doctor=""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 600, 300)
        self.center()

        v_box_left = QVBoxLayout()
        v_box_right = QVBoxLayout()
        v_box_center = QVBoxLayout()
        h_box_main = QHBoxLayout()
        h_box_buttons=QHBoxLayout()

        self.options_title=QLabel("выберите опцию")
        self.button_pressed = False
        self.edit_option=QRadioButton("изменить данные доктора")
        self.add_option=QRadioButton("добавить нового доктора")
        self.button_group=QButtonGroup()
        self.button_group.addButton(self.edit_option)
        self.button_group.addButton(self.add_option)
        self.button_group.buttonClicked.connect(self.option_chosed)
        self.doctors_list = QComboBox(self)
        self.fill_docs_list()
        self.doctors_list.activated[str].connect(self.doctor_chosed)
        self.help=QLabel("")

        self.surname_title = QLabel("Фамилия:")
        self.name_title = QLabel("Имя:")
        self.patronymic_title = QLabel("Отчество:")
        self.phone_title = QLabel("Телефон:")
        self.email_title = QLabel("Эл. почта:")
        self.password_title = QLabel("Пароль:")
        self.surname = QLineEdit()
        self.name = QLineEdit()
        self.patronymic=QLineEdit()
        self.phone = QLineEdit()
        self.email = QLineEdit()
        self.password = QLineEdit()

        self.save_button=QPushButton("сохранить")
        self.delete_button=QPushButton("удалить")
        self.save_button.clicked.connect(self.save_changes)
        self.delete_button.clicked.connect(self.delete_doctor)

        v_box_left.addWidget(self.options_title)
        v_box_left.addWidget(self.edit_option)
        v_box_left.addWidget(self.add_option)
        v_box_left.addWidget(self.doctors_list)
        v_box_left.addWidget(self.help)
        v_box_left.addStretch()

        v_box_right.addWidget(self.surname_title)
        v_box_right.addWidget(self.surname)
        v_box_right.addWidget(self.name_title)
        v_box_right.addWidget(self.name)
        v_box_right.addWidget(self.patronymic_title)
        v_box_right.addWidget(self.patronymic)
        v_box_right.addWidget(self.phone_title)
        v_box_right.addWidget(self.phone)
        v_box_right.addWidget(self.email_title)
        v_box_right.addWidget(self.email)
        v_box_right.addWidget(self.password_title)
        v_box_right.addWidget(self.password)
        v_box_right.addStretch()
        v_box_right.addLayout(h_box_buttons)

        h_box_main.addLayout(v_box_left)
        h_box_main.addLayout(v_box_center)
        h_box_main.addLayout(v_box_right)
        self.setLayout(h_box_main)
        self.setWindowTitle("список врачей")
        self.show()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def save_changes(self):
        #изменили данные доктора и обноили их в БД
        #и изменили его в списке(если фио стало другое)
        index=self.doctors.index(self.current_chosed_doctor)
        surname_new=str(self.surname.text())
        name_new=str(self.name.text())
        patronymic_new=str(self.patronymic.text())
        phone_new=str(self.phone.text())
        email_new=str(self.email.text())
        password_new=str(self.password.text())
        if check_correct_name(surname_new) or check_correct_name(name_new) or check_correct_name(patronymic_new) \
            or check_correct_phone(phone_new) or check_correct_email(email_new) or check_correct_password(password_new):
            self.doctors[index]=surname_new+" "+name_new+" "+patronymic_new
            self.fill_docs_list()


    def delete_doctor(self):
        #удаление доктора из БД
        deleting_doc = str(self.surname.text()) + " " + str(self.name.text()) + " " + str(self.patronymic.text())
        if self.doctors.__contains__(deleting_doc):
            self.doctors.remove(deleting_doc)
            self.fill_docs_list()


    def add_new_doctor(self):
        #добавление нового доктора в БД
        #добаление его в список на экране
        surname=str(self.surname.text())
        name=str(self.name.text())
        patronymic=str(self.patronymic.text())
        phone=str(self.phone.text())
        email=str(self.email.text())
        password=str(self.password.text())
        print(str(surname+" "+name+" "+patronymic))
        if check_correct_name(surname) or check_correct_name(name) or check_correct_name(patronymic) \
            or check_correct_phone(phone) or check_correct_email(email) or check_correct_password(password):
            new_doc=str(surname+" "+name+" "+patronymic)
            self.doctors.append(new_doc)
            self.fill_docs_list()

    def return_to_doc_window(self):
        self.close()

    def option_chosed(self, button):
        self.delete_buttons_fragment()
        if button.text() == "изменить данные доктора":
            self.show_edit_save_buttons()
            self.help.setText("после изменения полей или удаления\n нажмите \"сохранить\"")
        elif button.text() == "добавить нового доктора":
            self.show_add_button()
            self.help.setText("перед добалением заполните все поля")
            self.surname.setText("")
            self.name.setText("")
            self.patronymic.setText("")
            self.phone.setText("")
            self.email.setText("")
            self.password.setText("")
        self.button_pressed=True

    def doctor_chosed(self, text):
        array=text.split(" ")
        self.current_chosed_doctor=copy.copy(text)
        self.surname.setText(array[0])
        self.name.setText(array[1])

    def fill_docs_list(self):
        # это для примера
        self.doctors_list.clear()
        self.doctors_list.addItems(self.doctors)
        #self.doctors_list.addItems(["Иванов Иван Иваноич", "Иванов Неиван Иваноич", "Иванов Иван Неиваноич"])

    # clearLayout и delete_last_fragment нужны для удаления предыдущего layout с экрана
    # layout удаляется когда выбрана другая опция
    def clearLayout(self,layout):
        if layout != None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def delete_buttons_fragment(self):
        h_box_main = self.layout()
        v_box_right=h_box_main.itemAt(h_box_main.count()-1)
        h_box_buttons=v_box_right.itemAt(v_box_right.count()-1)
        self.clearLayout(h_box_buttons)
        h_box_main.removeItem(h_box_buttons)
        self.setLayout(h_box_main)

    def show_edit_save_buttons(self):
        h_box_main = self.layout()
        v_box_right=h_box_main.itemAt(h_box_main.count()-1)
        print(type(v_box_right))
        self.save_button=QPushButton("сохранить")
        self.delete_button=QPushButton("удалить")
        self.save_button.clicked.connect(self.save_changes)
        self.delete_button.clicked.connect(self.delete_doctor)
        h_box_buttons=QHBoxLayout()
        h_box_buttons.addWidget(self.delete_button)
        h_box_buttons.addWidget(self.save_button)
        v_box_right.addLayout(h_box_buttons)
        self.setLayout(h_box_main)

    def show_add_button(self):
        h_box_main = self.layout()
        v_box_right=h_box_main.itemAt(h_box_main.count()-1)
        print(type(v_box_right))
        self.save_button=QPushButton("добавить")
        self.save_button.clicked.connect(self.add_new_doctor)
        h_box_buttons=QHBoxLayout()
        h_box_buttons.addWidget(self.save_button)
        v_box_right.addLayout(h_box_buttons)
        self.setLayout(h_box_main)


# по хорошему можно запретить обычному доктору изменять данные уже созданных клиентов
# но не факт что это так важно
class EditClientsWindow(QWidget):
    clients=[]
    current_chosed_client=""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 600, 300)
        self.center()

        v_box_left = QVBoxLayout()
        v_box_right = QVBoxLayout()
        v_box_center = QVBoxLayout()
        h_box_main = QHBoxLayout()
        h_box_buttons=QHBoxLayout()

        self.options_title=QLabel("выберите опцию")
        self.button_pressed = False
        self.edit_option=QRadioButton("изменить данные пользователя")
        self.add_option=QRadioButton("добавить нового пользователя")
        self.button_group=QButtonGroup()
        self.button_group.addButton(self.edit_option)
        self.button_group.addButton(self.add_option)
        self.button_group.buttonClicked.connect(self.option_chosed)
        self.clients_list = QComboBox(self)
        self.fill_clients_list()
        self.clients_list.activated[str].connect(self.client_chosed)
        self.help=QLabel("")

        self.surname_title = QLabel("Фамилия:")
        self.name_title = QLabel("Имя:")
        self.patronymic_title = QLabel("Отчество:")
        self.phone_title = QLabel("Телефон:")
        self.email_title = QLabel("Эл. почта:")
        self.password_title = QLabel("Пароль:")
        self.surname = QLineEdit()
        self.name = QLineEdit()
        self.patronymic=QLineEdit()
        self.phone = QLineEdit()
        self.email = QLineEdit()
        self.password = QLineEdit()

        self.save_button=QPushButton("сохранить")
        self.delete_button=QPushButton("удалить")
        self.save_button.clicked.connect(self.save_changes)
        self.delete_button.clicked.connect(self.delete_client)

        v_box_left.addWidget(self.options_title)
        v_box_left.addWidget(self.edit_option)
        v_box_left.addWidget(self.add_option)
        v_box_left.addWidget(self.clients_list)
        v_box_left.addWidget(self.help)
        v_box_left.addStretch()

        v_box_right.addWidget(self.surname_title)
        v_box_right.addWidget(self.surname)
        v_box_right.addWidget(self.name_title)
        v_box_right.addWidget(self.name)
        v_box_right.addWidget(self.patronymic_title)
        v_box_right.addWidget(self.patronymic)
        v_box_right.addWidget(self.phone_title)
        v_box_right.addWidget(self.phone)
        v_box_right.addWidget(self.email_title)
        v_box_right.addWidget(self.email)
        v_box_right.addWidget(self.password_title)
        v_box_right.addWidget(self.password)
        v_box_right.addStretch()
        v_box_right.addLayout(h_box_buttons)

        h_box_main.addLayout(v_box_left)
        h_box_main.addLayout(v_box_center)
        h_box_main.addLayout(v_box_right)
        self.setLayout(h_box_main)
        self.setWindowTitle("список ползователей")
        self.show()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def save_changes(self):
        #изменили данные user-a и обноили их в БД
        #и изменили его в списке(если фио стало другое)
        index=self.clients.index(self.current_chosed_client)
        surname_new=str(self.surname.text())
        name_new=str(self.name.text())
        patronymic_new=str(self.patronymic.text())
        phone_new=str(self.phone.text())
        email_new=str(self.email.text())
        password_new=str(self.password.text())
        if check_correct_name(surname_new) or check_correct_name(name_new) or check_correct_name(patronymic_new) \
            or check_correct_phone(phone_new) or check_correct_email(email_new) or check_correct_password(password_new):
            self.clients[index]=surname_new+" "+name_new+" "+patronymic_new
            self.fill_clients_list()


    def delete_client(self):
        #удаление user-a из БД
        deleting_usr = str(self.surname.text()) + " " + str(self.name.text()) + " " + str(self.patronymic.text())
        if self.clients.__contains__(deleting_usr):
            self.clients.remove(deleting_usr)
            self.fill_docs_list()


    def add_new_client(self):
        #добавление нового user-a в БД
        #добаление его в список на экране
        surname=str(self.surname.text())
        name=str(self.name.text())
        patronymic=str(self.patronymic.text())
        phone=str(self.phone.text())
        email=str(self.email.text())
        password=str(self.password.text())
        print(str(surname+" "+name+" "+patronymic))# это для отладки
        #if not (surname=="" or name==""or patronymic==""or phone==""or email==""or password==""):
        if check_correct_name(surname) or check_correct_name(name) or check_correct_name(patronymic) \
            or check_correct_phone(phone) or check_correct_email(email) or check_correct_password(password):
            new_client=str(surname+" "+name+" "+patronymic)
            self.clients.append(new_client)
            self.fill_clients_list()

    def return_to_doc_window(self):
        self.close()

    def option_chosed(self, button):
        self.delete_buttons_fragment()
        if button.text() == "изменить данные пользователя":
            self.show_edit_save_buttons()
            self.help.setText("после изменения полей или удаления\n нажмите \"сохранить\"")
        elif button.text() == "добавить нового пользователя":
            self.show_add_button()
            self.help.setText("перед добалением заполните все поля")
            self.surname.setText("")
            self.name.setText("")
            self.patronymic.setText("")
            self.phone.setText("")
            self.email.setText("")
            self.password.setText("")
        self.button_pressed=True

    def client_chosed(self, text):
        array=text.split(" ")
        self.current_chosed_client=copy.copy(text)
        self.surname.setText(array[0])
        self.name.setText(array[1])

    def fill_clients_list(self):
        # заполнение списка фио пользоателей
        # это для примера
        self.clients_list.clear()
        self.clients_list.addItems(self.clients)

    # clearLayout и delete_last_fragment нужны для удаления предыдущего layout с экрана
    # layout удаляется когда выбрана другая опция
    def clearLayout(self,layout):
        if layout != None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def delete_buttons_fragment(self):
        h_box_main = self.layout()
        v_box_right=h_box_main.itemAt(h_box_main.count()-1)
        h_box_buttons=v_box_right.itemAt(v_box_right.count()-1)
        self.clearLayout(h_box_buttons)
        h_box_main.removeItem(h_box_buttons)
        self.setLayout(h_box_main)

    def show_edit_save_buttons(self):
        h_box_main = self.layout()
        v_box_right=h_box_main.itemAt(h_box_main.count()-1)
        print(type(v_box_right))
        self.save_button=QPushButton("сохранить")
        self.delete_button=QPushButton("удалить")
        self.save_button.clicked.connect(self.save_changes)
        self.delete_button.clicked.connect(self.delete_client)
        h_box_buttons=QHBoxLayout()
        h_box_buttons.addWidget(self.delete_button)
        h_box_buttons.addWidget(self.save_button)
        v_box_right.addLayout(h_box_buttons)
        self.setLayout(h_box_main)

    def show_add_button(self):
        h_box_main = self.layout()
        v_box_right=h_box_main.itemAt(h_box_main.count()-1)
        print(type(v_box_right))
        self.save_button=QPushButton("добавить")
        self.save_button.clicked.connect(self.add_new_client)
        h_box_buttons=QHBoxLayout()
        h_box_buttons.addWidget(self.save_button)
        v_box_right.addLayout(h_box_buttons)
        self.setLayout(h_box_main)


class EditMyWorkTimeWindow(QWidget):
    one_day_is_changing=True
    current_selected_day="Понедельник"
    # словарь день <-> пара время начала/время окончания
    # в бд у нас blob поле для этого словаря
    work_times={}

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 600, 400)
        self.center()
        h_box_main=QHBoxLayout()
        v_box_left=QVBoxLayout()
        v_box_center=QVBoxLayout()
        v_box_right=QVBoxLayout()

        self.help=QLabel("выберите день из списка или\nопцию \"ко всем дням\"")
        v_box_left.addWidget(self.help)

        self.days_list = QComboBox(self)
        self.fill_days_list()
        v_box_left.addWidget(self.days_list)
        self.days_list.activated[str].connect(self.day_chosed)
        self.start_time_title=QLabel("время начала работы")
        v_box_left.addWidget(self.start_time_title)

        self.increase_start_hour=QPushButton("+")
        self.increase_start_hour.clicked.connect(self.inc_start_hour)
        self.decrease_start_hour = QPushButton("-")
        self.decrease_start_hour.clicked.connect(self.dec_start_hour)
        self.start_time=QLineEdit("00:00")
        self.start_time.adjustSize()
        self.increase_start_minute=QPushButton("+")
        self.increase_start_minute.clicked.connect(self.inc_start_minute)
        self.decrease_start_minute = QPushButton("-")
        self.decrease_start_minute.clicked.connect(self.dec_start_minute)

        v_box_s_h_buttons=QVBoxLayout()
        v_box_s_h_buttons.addWidget(self.increase_start_hour)
        v_box_s_h_buttons.addWidget(self.decrease_start_hour)
        h_box_start=QHBoxLayout()
        h_box_start.addLayout(v_box_s_h_buttons)
        h_box_start.addWidget(self.start_time)
        v_box_s_m_buttons=QVBoxLayout()
        v_box_s_m_buttons.addWidget(self.increase_start_minute)
        v_box_s_m_buttons.addWidget(self.decrease_start_minute)
        h_box_start.addLayout(v_box_s_m_buttons)
        v_box_left.addLayout(h_box_start)

        self.end_time_title=QLabel("время окончания работы")
        v_box_left.addWidget(self.end_time_title)

        self.increase_end_hour = QPushButton("+")
        self.increase_end_hour.clicked.connect(self.inc_end_hour)
        self.decrease_end_hour = QPushButton("-")
        self.decrease_end_hour.clicked.connect(self.dec_end_hour)
        self.end_time=QLineEdit("23:59")
        self.end_time.adjustSize()
        self.increase_end_minute=QPushButton("+")
        self.increase_end_minute.clicked.connect(self.inc_end_minute)
        self.decrease_end_minute = QPushButton("-")
        self.decrease_end_minute.clicked.connect(self.dec_end_minute)

        self.days_table=QTableWidget()
        self.days_table.setRowCount(2)
        self.days_table.setColumnCount(7)
        self.days_table.setVerticalHeaderLabels(["время начала","время окончания"])
        self.days_table.setHorizontalHeaderLabels(["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"])
        self.fill_days_table()

        v_box_e_h_buttons=QVBoxLayout()
        v_box_e_h_buttons.addWidget(self.increase_end_hour)
        v_box_e_h_buttons.addWidget(self.decrease_end_hour)
        h_box_end=QHBoxLayout()
        h_box_end.addLayout(v_box_e_h_buttons)
        h_box_end.addWidget(self.end_time)
        v_box_e_m_buttons=QVBoxLayout()
        v_box_e_m_buttons.addWidget(self.increase_end_minute)
        v_box_e_m_buttons.addWidget(self.decrease_end_minute)
        h_box_end.addLayout(v_box_e_m_buttons)
        v_box_left.addLayout(h_box_end)
        v_box_left.addWidget(self.days_table)

        self.set_default_button=QPushButton("рабочее время\n по умолчанию")
        v_box_right.addWidget(self.set_default_button)

        self.settings_for_day=QLabel("применять настройку времени:")
        self.set_current_day=QRadioButton("к выбранному дню")
        self.set_all_days=QRadioButton("ко всем дням")
        self.button_group=QButtonGroup()
        self.button_group.addButton(self.set_current_day)
        self.button_group.addButton(self.set_all_days)
        self.button_group.buttonClicked.connect(self.option_chosed)
        v_box_right.addWidget(self.settings_for_day)
        v_box_right.addWidget(self.set_current_day)
        v_box_right.addWidget(self.set_all_days)
        self.set_current_day.setChecked(True)

        self.save_button=QPushButton("сохранить")
        self.save_button.clicked.connect(self.save_changes)
        v_box_right.addWidget(self.save_button)

        v_box_left.addStretch()
        v_box_center.addStretch()
        v_box_right.addStretch()
        h_box_main.addLayout(v_box_left)
        h_box_main.addLayout(v_box_center)
        h_box_main.addLayout(v_box_right)
        self.setLayout(h_box_main)
        self.setWindowTitle("установка рабочего времени")
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def day_chosed(self, text):
        # при выборе дня время начала,конца должно подгружаться в нужные поля
        self.current_selected_day=text
        pass

    def save_changes(self):
        if check_correct_worktime(str(self.start_time.text())) and check_correct_worktime(str(self.end_time.text())):
            st = self.start_time.text().split(":")
            en = self.end_time.text().split(":")
            if self.one_day_is_changing:
                self.work_times[self.current_selected_day]=\
                    [datetime.time(int(st[0]),int(st[1])),datetime.time(int(en[0]),int(en[1]))]
                print(self.work_times)
            else:
                keys=self.work_times.keys()
                for k in keys:
                    self.work_times[k] = \
                        [datetime.time(int(st[0]), int(st[1])), datetime.time(int(en[0]), int(en[1]))]
                print(self.work_times)
            self.fill_days_table()
            self.save_changes_in_database()

    def save_changes_in_database(self):
        # сохранение слоаря days_list в поле worktime у доктора у БД
        pass

    def option_chosed(self, button):
        # применение настройки времени для выбранного дня
        # или для все дней сразу (чтоб быстрее настраивать)
        if button.text() == "к выбранному дню":
            self.one_day_is_changing=True
        else:
            self.one_day_is_changing = False

    def fill_days_list(self):
        # по идее days_list должен хранить копию рабоих часов из поял из базы
        temp_list=["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
        self.days_list.addItems(temp_list)
        for i in temp_list:
            self.work_times[i]=[datetime.time(0,0),datetime.time(0,0)]
        print(self.work_times)

    def inc_start_hour(self):
        list=parse_work_time(str(self.start_time.text()))
        if list is not None:
            new_hour=int(list[0])+1
            if new_hour>23:
                new_hour=0
            if new_hour<10:
                new_hour='0'+str(new_hour)
            new_work_time = str(new_hour) + ':' + str(list[1])
            self.start_time.setText(new_work_time)

    def dec_start_hour(self):
        list = parse_work_time(str(self.start_time.text()))
        if list is not None:
            new_hour = int(list[0]) - 1
            if new_hour < 0:
                new_hour = 23
            if new_hour<10:
                new_hour='0'+str(new_hour)
            new_work_time = str(new_hour) + ":" + str(list[1])
            self.start_time.setText(new_work_time)

    def inc_start_minute(self):
        list = parse_work_time(str(self.start_time.text()))
        if list is not None:
            new_minute = int(list[1]) + 1
            if new_minute > 59:
                new_minute = 0
            if new_minute<10:
                new_minute='0'+str(new_minute)
            new_work_time = str(list[0])+":"+str(new_minute)
            self.start_time.setText(new_work_time)

    def dec_start_minute(self):
        list = parse_work_time(str(self.start_time.text()))
        if list is not None:
            new_minute = int(list[1]) - 1
            if new_minute < 0:
                new_minute = 59
            if new_minute<10:
                new_minute='0'+str(new_minute)
            new_work_time = str(list[0])+":"+str(new_minute)
            self.start_time.setText(new_work_time)

    def inc_end_hour(self):
        list = parse_work_time(str(self.end_time.text()))
        if list is not None:
            new_hour = int(list[0]) + 1
            if new_hour > 23:
                new_hour = 0
            if new_hour<10:
                new_hour='0'+str(new_hour)
            new_work_time = str(new_hour) + ':' + str(list[1])
            self.end_time.setText(new_work_time)

    def dec_end_hour(self):
        list = parse_work_time(str(self.end_time.text()))
        if list is not None:
            new_hour = int(list[0]) - 1
            if new_hour < 0:
                new_hour = 23
            if new_hour<10:
                new_hour='0'+str(new_hour)
            new_work_time = str(new_hour) + ':' + str(list[1])
            self.end_time.setText(new_work_time)

    def inc_end_minute(self):
        list = parse_work_time(str(self.end_time.text()))
        if list is not None:
            new_minute = int(list[1]) + 1
            if new_minute > 59:
                new_minute = 0
            if new_minute<10:
                new_minute='0'+str(new_minute)
            new_work_time = str(list[0]) + ":" + str(new_minute)
            self.end_time.setText(new_work_time)

    def dec_end_minute(self):
        list = parse_work_time(str(self.end_time.text()))
        if list is not None:
            new_minute = int(list[1]) - 1
            if new_minute < 0:
                new_minute = 59
            if new_minute<10:
                new_minute='0'+str(new_minute)
            new_work_time = str(list[0]) + ":" + str(new_minute)
            self.end_time.setText(new_work_time)

    def fill_days_table(self):
        i=0
        keys=self.work_times.keys()
        for k in keys:
            for r in range(0,2):
                cellinfo = QTableWidgetItem(deparse_work_time(self.work_times[k][r]))
                self.days_table.setItem(r, i, cellinfo)
            i+=1


class MyAppointmentsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 600, 400)
        self.center()
        v_box_main=QVBoxLayout()
        h_box_search=QHBoxLayout()
        v_box_table=QVBoxLayout()

        self.search_title=QLabel("поиск:")
        self.search_category_title=QLabel("категория:")
        self.search=QLineEdit()
        self.search_category=QComboBox(self)
        self.search_category.activated[str].connect(self.category_chosed)
        self.search_category.addItems(["имя питомца","дата","время","результаты осмотра","необходимость лечения"])

        self.setLayout(v_box_main)
        self.setWindowTitle("мои осмотры")
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def categoy_chosed(self):
        pass

