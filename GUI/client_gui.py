import hashlib

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from validate_email import validate_email

import sys
import gui_main
import client
from Petclinic.ClientClass import ClientClass
from Petclinic.DoctorClass import DoctorClass

class ClientWindow(QWidget):
    this_client = None

    def __init__(self, this_client: ClientClass):
        super().__init__()
        self.this_client = client.get_client_class_by_email(
            this_client.email)
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 640, 480)
        self.center()
        self.acc_button = QPushButton(self.this_client.fio)
        self.make_appointment = QPushButton("ЗАПИСАТЬСЯ НА ОСМОТР")
        self.go_to_my_cats = QPushButton("МОИ ПИТОМЦЫ")
        self.buy_medication = QPushButton("КУПИТЬ СРЕДСТВА")
        # self.show_medications = QPushButton("МОИ ПОКУПКИ")
        self.make_appointment.clicked.connect(self.go_to_appointment_window)
        self.go_to_my_cats.clicked.connect(self.go_to_my_pets_window)
        self.buy_medication.clicked.connect(self.go_to_buy_med_window)
        self.acc_button.clicked.connect(self.exit_from_acc)

        v_box_left = QVBoxLayout()
        v_box_left.addWidget(self.make_appointment)
        v_box_left.addWidget(self.go_to_my_cats)
        v_box_left.addWidget(self.buy_medication)
        # v_box_left.addWidget(self.show_medications)
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

    def go_to_appointment_window(self):
        self.new_window = AppointmentWindow(self.this_client)
        # self.close()

    def go_to_my_pets_window(self):
        self.new_window = MyPetsWindow(self.this_client)
        # self.close()

    def go_to_buy_med_window(self):
        self.new_window = BuyMedWindow(self.this_client)

    def exit_from_acc(self):
        self.new_window = gui_main.LoginWindow()
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class AppointmentWindow(QWidget):
    this_client = None

    def __init__(self, this_client: ClientClass):
        super().__init__()
        self.this_client = this_client
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 400, 400)
        self.center()
        h_box_date = QHBoxLayout()
        h_box_doc = QHBoxLayout()
        h_box_cat = QHBoxLayout()
        h_box_footer = QHBoxLayout()
        v_box_main = QVBoxLayout()
        v_box_lbl = QVBoxLayout()
        v_box_results = QVBoxLayout()

        self.chose_date_lbl = QLabel("выберите дату")
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked[QDate].connect(self.date_chosed)
        h_box_date.addWidget(self.chose_date_lbl)
        h_box_date.addWidget(self.calendar)

        self.chose_doc_lbl = QLabel("выберите доктора")
        self.docs_list = QComboBox(self)
        fio_doctors = self.get_fio_doctors()
        self.docs_list.addItems(fio_doctors)
        self.docs_list.activated[str].connect(self.doc_chosed)
        h_box_doc.addWidget(self.chose_doc_lbl)
        h_box_doc.addWidget(self.docs_list)

        self.chose_cat_lbl = QLabel("выберите питомца")
        self.cats_list = QComboBox(self)
        cats_name = self.get_client_cats_name()
        self.cats_list.addItems(cats_name)
        self.cats_list.activated[str].connect(self.cat_chosed)
        h_box_cat.addWidget(self.chose_cat_lbl)
        h_box_cat.addWidget(self.cats_list)

        self.chose_date_lbl2 = QLabel("выбранный день: ")
        self.chose_doc_lbl2 = QLabel("выбранный доктор:")
        self.chose_cat_lbl2 = QLabel("выбранный  питомец:")
        v_box_lbl.addWidget(self.chose_date_lbl2)
        v_box_lbl.addWidget(self.chose_doc_lbl2)
        v_box_lbl.addWidget(self.chose_cat_lbl2)

        self.chose_date_result = QLabel("день не выбран")
        self.chose_doc_result = QLabel("доктор не выбран")
        self.chose_cat_result = QLabel("питомец не выбран")
        v_box_results.addWidget(self.chose_date_result)
        v_box_results.addWidget(self.chose_doc_result)
        v_box_results.addWidget(self.chose_cat_result)

        self.create_appointment_btn = QPushButton("сформироать запись")
        self.create_appointment_btn.clicked.connect(self.create_appointment)
        h_box_footer.addLayout(v_box_lbl)
        h_box_footer.addLayout(v_box_results)
        h_box_footer.addWidget(self.create_appointment_btn)
        h_box_footer.addStretch()

        v_box_main.addLayout(h_box_date)
        v_box_main.addLayout(h_box_doc)
        v_box_main.addLayout(h_box_cat)
        v_box_main.addStretch()
        v_box_main.addLayout(h_box_footer)
        v_box_main.addStretch()

        self.setLayout(v_box_main)
        self.setWindowTitle("appointment...")
        self.show()

    def get_fio_doctors(self) -> list:
        self.doctors = client.get_all_doctors()
        fio_doctors = ['']
        for key in self.doctors:
            fio_doctors.append(self.doctors[key].fio)
        return fio_doctors

    def get_client_cats_name(self) -> list:
        self.cats = client.get_my_pets(self.this_client.getId())
        cats_name = ['']
        for key in self.cats:
            cats_name.append(self.cats[key].name)
        return cats_name

    def date_chosed(self, date):
        self.chose_date_result.setText(date.toString())

    def doc_chosed(self, text):
        self.chose_doc_result.setText(text)

    def cat_chosed(self, text):
        self.chose_cat_result.setText(text)

    def create_appointment(self):

        if self.chose_date_result.text() == "день не выбран" or \
                self.chose_doc_result.text() == "доктор не выбран" or \
                self.chose_cat_result.text() == "питомец не выбран" or \
                self.chose_date_result.text() == "" or \
                self.chose_doc_result.text() == "" or \
                self.chose_cat_result.text() == "":
            QMessageBox.critical(self, "Ошибка ", "Не выбрана дата, питомец или доктор", QMessageBox.Ok)
        else:
            doc_fio = self.docs_list.currentText()
            cat_name = self.cats_list.currentText()

            doc_id = self.get_doc_id(doc_fio)
            cat = self.get_client_cat(cat_name)
            date = self.get_date_in_figures(self.calendar)
            state = 'True'
            need_med = 'True'
            client.add_appointment(date, doc_id, cat.id, state, need_med)
            QMessageBox.information(self, "Успешно ", "Запись на осмотр добавлена ", QMessageBox.Ok)
            self.close()

    def get_doc_id(self, doc_fio: str) -> int:
        for key in self.doctors:
            if self.doctors[key].fio == doc_fio:
                return self.doctors[key].id
        raise Exception

    def get_client_cat(self, cat_name: str):
        for key in self.cats:
            if self.cats[key].name == cat_name:
                return self.cats[key]
        raise Exception

    def get_date_in_figures(self, date: QCalendarWidget) -> str:
        date_wish_name_month = self.calendar.selectedDate().toString()
        date_s = date_wish_name_month.split()
        month = ''
        if date_s[1] == 'янв':
            month = '01'
        elif date_s[1] == 'фев':
            month = '02'
        elif date_s[1] == 'мар':
            month = '03'
        elif date_s[1] == 'апр':
            month = '04'
        elif date_s[1] == 'май':
            month = '05'
        elif date_s[1] == 'июн':
            month = '06'
        elif date_s[1] == 'июл':
            month = '07'
        elif date_s[1] == 'авг':
            month = '08'
        elif date_s[1] == 'сен':
            month = '09'
        elif date_s[1] == 'окт':
            month = '10'
        elif date_s[1] == 'ноя':
            month = '11'
        elif date_s[1] == 'дек':
            month = '12'

        return f"{date_s[2]}.{month}.{date_s[3]}"

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class MyPetsWindow(QWidget):
    this_client = None

    def __init__(self, this_client: ClientClass):
        super().__init__()
        self.this_client = this_client
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 300, 300)
        self.center()
        v_box_main = QVBoxLayout()

        self.operation_lbl = QLabel("функции:")
        self.show_option = QRadioButton("показать данные питомца")
        self.edit_option = QRadioButton("изменить данные питомца")
        self.add_option = QRadioButton("добавить питомца")
        self.delete_option = QRadioButton("удалить питомца")

        self.button_pressed = False
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.show_option)
        self.button_group.addButton(self.edit_option)
        self.button_group.addButton(self.add_option)
        self.button_group.addButton(self.delete_option)
        self.button_group.buttonClicked.connect(self.option_chosed)

        self.cats_list = QComboBox(self)
        self.doctors = client.get_all_doctors()
        self.cats = client.get_my_pets(self.this_client.getId())

        cats_name = self.get_client_cats_name()
        self.cats_list.addItems(cats_name)

        v_box_main.addWidget(self.cats_list)
        v_box_main.addWidget(self.operation_lbl)
        v_box_main.addWidget(self.show_option)
        v_box_main.addWidget(self.edit_option)
        v_box_main.addWidget(self.add_option)
        v_box_main.addWidget(self.delete_option)
        v_box_main.addStretch()

        self.setLayout(v_box_main)
        self.setWindowTitle("my pets...")
        self.show()

    def get_fio_doctors(self) -> list:
        fio_doctors = ['']
        for key in self.doctors:
            fio_doctors.append(self.doctors[key].fio)
        return fio_doctors

    def get_client_cats_name(self) -> list:
        cats_name = ['']
        for key in self.cats:
            cats_name.append(self.cats[key].name)
        return cats_name

    def get_doc_id(self, doc_fio: str) -> int:
        for key in self.doctors:
            if self.doctors[key].fio == doc_fio:
                return self.doctors[key].id
        raise Exception

    def get_client_cat(self, cat_name: str):
        for key in self.cats:
            if self.cats[key].name == cat_name:
                return self.cats[key]
        raise Exception

    def option_chosed(self, button):
        if self.button_pressed:
            self.delete_last_fragment()

        if button.text() == "показать данные питомца":
            if self.cats_list.currentText() == '':
                self.button_pressed = False
                QMessageBox.critical(self, "Ошибка ", "Питомец не выбран", QMessageBox.Ok)
            else:
                self.button_pressed = True
                self.show_pet_info()
        elif button.text() == "изменить данные питомца":
            if self.cats_list.currentText() == '':
                self.button_pressed = False
                QMessageBox.critical(self, "Ошибка ", "Питомец не выбран", QMessageBox.Ok)
            else:
                self.button_pressed = True
                self.edit_pet_info()
        elif button.text() == "удалить питомца":
            if self.cats_list.currentText() == '':
                self.button_pressed = False
                QMessageBox.critical(self, "Ошибка ", "Питомец не выбран", QMessageBox.Ok)
            else:
                self.button_pressed = True
                self.delete_pet()
        elif button.text() == "добавить питомца":
            self.button_pressed = True
            self.add_new_pet()

    # def get_cats_list(self):
    #     # cats_list должен заполняться котами этого пользователя из БД
    #     self.cats_list.addItems(["Dysia", "Barsik", "Begemot"])

    def update_cats_list(self):
        # при удалении питомца он также исчезает из списка
        pass

    # clearLayout и delete_last_fragment нужны для удаления предыдущего layout с экрана
    # layout удаляется когда выбрана другая опция
    def clearLayout(self, layout):
        if layout != None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def delete_last_fragment(self):
        v_box_main = self.layout()
        w = v_box_main.itemAt(v_box_main.count() - 1)
        self.clearLayout(w)
        v_box_main.removeItem(w)
        self.setLayout(v_box_main)

    def show_pet_info(self):
        # значения полей у питома должны помещаться  соответствубщие Qlabel
        v_box_main = self.layout()
        v_box_lbl = QVBoxLayout()
        v_box_info = QVBoxLayout()
        h_box = QHBoxLayout()

        self.name_lbl = QLabel("Имя:")
        self.age_lbl = QLabel("Возраст:")
        self.breed_lbl = QLabel("Порода:")
        v_box_lbl.addWidget(self.name_lbl)
        v_box_lbl.addWidget(self.age_lbl)
        v_box_lbl.addWidget(self.breed_lbl)
        v_box_lbl.addStretch()

        self.set_data_pet()

        v_box_info.addWidget(self.name_text)
        v_box_info.addWidget(self.age_text)
        v_box_info.addWidget(self.breed_text)
        v_box_info.addStretch()

        h_box.addLayout(v_box_lbl)
        h_box.addLayout(v_box_info)

        v_box_main.addLayout(h_box)
        self.setLayout(v_box_main)

    def set_data_pet(self):
        name_cat = self.cats_list.currentText()
        cat = self.get_client_cat(name_cat)

        self.name_text = QLabel(cat.name)
        self.age_text = QLabel(cat.age.__str__())
        self.breed_text = QLabel(cat.cat_breed)

    def edit_pet_info(self):
        # значения полей у питома должны помещаться  соответствубщие Qlabel
        v_box_main = self.layout()
        v_box = QVBoxLayout()
        h_box_name_edit = QHBoxLayout()
        h_box_age_edit = QHBoxLayout()
        h_box_breed_edit = QHBoxLayout()
        h_box_footer = QHBoxLayout()

        self.name_lbl = QLabel("Имя:")
        name_cat = self.cats_list.currentText()
        self.cat = self.get_client_cat(name_cat)
        self.name_text = QLineEdit(self.cat.name)
        h_box_name_edit.addWidget(self.name_lbl)
        h_box_name_edit.addWidget(self.name_text)
        self.age_lbl = QLabel("Возраст:")
        self.age_text = QLineEdit(self.cat.age.__str__())
        h_box_age_edit.addWidget(self.age_lbl)
        h_box_age_edit.addWidget(self.age_text)
        self.breed_lbl = QLabel("Порода:")
        self.breed_text = QLineEdit(self.cat.cat_breed)
        h_box_breed_edit.addWidget(self.breed_lbl)
        h_box_breed_edit.addWidget(self.breed_text)

        # по нажатию save изменения поля питомца в БД должны измениться
        self.save_btn = QPushButton("сохранить")
        self.save_btn.clicked.connect(self.change_data_cat)

        h_box_footer.addStretch()
        h_box_footer.addWidget(self.save_btn)

        v_box.addLayout(h_box_name_edit)
        v_box.addLayout(h_box_age_edit)
        v_box.addLayout(h_box_breed_edit)
        v_box.addLayout(h_box_footer)
        v_box_main.addLayout(v_box)
        self.setLayout(v_box_main)

    def change_data_cat(self):
        name = self.name_text.text()
        age = self.age_text.text()
        breed = self.breed_text.text()

        if name.__len__() > 255 or age.__len__() > 5 or breed.__len__() > 255:
            QMessageBox.critical(self, "Ошибка ", "Превышена допустимая длина полей или поля", QMessageBox.Ok)
        elif name.isspace() or age.isspace() or breed.isspace() \
                or name == '' or age == '' or breed == '':
            QMessageBox.critical(self, "Ошибка ", "Не заполнены обязательные поля имя, возраст или порода", QMessageBox.Ok)
        elif not age.isdigit():
            QMessageBox.critical(self, "Ошибка ", "В поле возраст нужно ввести целое неотрицательное число", QMessageBox.Ok)
        else:
            client.change_cat(self.cat.id, name, int(age), breed)
            QMessageBox.information(self, "Успешно ", "Питомец изменен", QMessageBox.Ok)
            self.close()

    def add_new_pet(self):
        v_box_main = self.layout()
        v_box = QVBoxLayout()
        h_box_name_edit = QHBoxLayout()
        h_box_age_edit = QHBoxLayout()
        h_box_breed_edit = QHBoxLayout()
        h_box_footer = QHBoxLayout()

        self.name_lbl = QLabel("Имя:")
        self.name_text = QLineEdit("")
        h_box_name_edit.addWidget(self.name_lbl)
        h_box_name_edit.addWidget(self.name_text)
        self.age_lbl = QLabel("Возраст:")
        self.age_text = QLineEdit("")
        h_box_age_edit.addWidget(self.age_lbl)
        h_box_age_edit.addWidget(self.age_text)
        self.breed_lbl = QLabel("Порода:")
        self.breed_text = QLineEdit("")
        h_box_breed_edit.addWidget(self.breed_lbl)
        h_box_breed_edit.addWidget(self.breed_text)

        # по нажатию save изменения поля питомца в БД должны измениться
        self.save_btn_add_pet = QPushButton("создать питомца")
        self.save_btn_add_pet.clicked.connect(self.add_pet)
        h_box_footer.addStretch()
        h_box_footer.addWidget(self.save_btn_add_pet)

        v_box.addLayout(h_box_name_edit)
        v_box.addLayout(h_box_age_edit)
        v_box.addLayout(h_box_breed_edit)
        v_box.addLayout(h_box_footer)
        v_box_main.addLayout(v_box)
        self.setLayout(v_box_main)

    def add_pet(self):
        name = self.name_text.text()
        owner_id = self.this_client.getId()
        age = self.age_text.text()
        breed = self.breed_text.text()

        if name.__len__() > 255 or age.__len__() > 5 or breed.__len__() > 255:
            QMessageBox.critical(self, "Ошибка ", "Превышена допустимая длина полей или поля", QMessageBox.Ok)
        elif name.isspace() or age.isspace() or breed.isspace() \
                or name == '' or age == '' or breed == '':
            QMessageBox.critical(self, "Ошибка ", "Не заполнены обязательные поля имя, возраст или порода",
                                 QMessageBox.Ok)
        elif not age.isdigit():
            QMessageBox.critical(self, "Ошибка ", "В поле возраст нужно ввести целое неотрицательное число",
                                 QMessageBox.Ok)
        else:
            client.add_cat(name, owner_id, int(age), breed)
            QMessageBox.information(self, "Успешно ", "Питомец добавлен", QMessageBox.Ok)
            self.close()

    def delete_pet(self):
        # значения полей у питома должны помещаться  соответствубщие Qlabel
        v_box_main = self.layout()
        v_box_lbl = QVBoxLayout()
        v_box_info = QVBoxLayout()
        v_box = QVBoxLayout()
        h_box = QHBoxLayout()
        h_box_footer = QHBoxLayout()

        self.name_lbl = QLabel("Имя:")
        self.age_lbl = QLabel("Возраст:")
        self.breed_lbl = QLabel("Порода:")
        v_box_lbl.addWidget(self.name_lbl)
        v_box_lbl.addWidget(self.age_lbl)
        v_box_lbl.addWidget(self.breed_lbl)
        v_box_lbl.addStretch()

        cat_name = self.cats_list.currentText()
        self.cat = self.get_client_cat(cat_name)
        self.name_text = QLabel(self.cat.name)
        self.age_text = QLabel(self.cat.age.__str__())
        self.breed_text = QLabel(self.cat.cat_breed)
        v_box_info.addWidget(self.name_text)
        v_box_info.addWidget(self.age_text)
        v_box_info.addWidget(self.breed_text)
        v_box_info.addStretch()

        h_box.addLayout(v_box_lbl)
        h_box.addLayout(v_box_info)
        v_box.addLayout(h_box)
        h_box_footer.addStretch()
        self.save_btn_del = QPushButton("удалить питомца")
        self.save_btn_del.clicked.connect(self.delete_cat)
        h_box_footer.addWidget(self.save_btn_del)
        v_box.addLayout(h_box_footer)

        v_box_main.addLayout(v_box)
        self.setLayout(v_box_main)

    def delete_cat(self):
        client.delete_cat(self.cat.id)
        QMessageBox.information(self, "Успешно ", "Питомец удален", QMessageBox.Ok)
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class BuyMedWindow(QWidget):
    this_client = None

    def __init__(self, this_client: ClientClass):
        super().__init__()
        self.this_client = this_client
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 500, 300)
        self.center()
        v_box_main = QVBoxLayout()
        v_box_info = QVBoxLayout()
        h_box = QHBoxLayout()

        self.chose_med_lbl = QLabel("выберите лекарство:")
        self.meds_list = QComboBox()
        self.get_meds_list()
        self.meds_list.activated[str].connect(self.med_chosed)

        self.notify_lbl = QLabel("ВНИМАНИЕ! В данный момент работает только самовызов.")
        self.chose_payment_method_lbl = QLabel("выберите способ оплаты:")
        self.chose_payment_yandex = QRadioButton("Яндекс.Деньги")
        self.chose_payment_card = QRadioButton("Оплата картой")
        self.chose_payment_cash = QRadioButton("Оплата наличными при получении")
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.chose_payment_yandex)
        self.button_group.addButton(self.chose_payment_card)
        self.button_group.addButton(self.chose_payment_cash)
        self.button_group.buttonClicked.connect(self.option_chosed)
        self.buy_btn = QPushButton("Оформить заказ")

        self.med_title = QLabel("НАЗВАНИЕ:")
        self.med_title_res = QLabel("")
        self.med_description = QLabel("ОПИСАНИЕ:")
        self.med_med_description_res = QLabel("")
        self.med_cost = QLabel("СТОИМОСТЬ:")
        self.med_cost_res = QLabel("")

        items = [self.med_title, self.med_title_res, self.med_description, self.med_med_description_res, self.med_cost,
                 self.med_cost_res]
        v_box_info.addStretch()
        self.fill_layout(v_box_info, items)
        v_box_info.addStretch()
        h_box.addLayout(v_box_info)
        h_box.addStretch()
        h_box.addWidget(self.buy_btn)

        v_box_main.addWidget(self.chose_med_lbl)
        v_box_main.addWidget(self.meds_list)
        v_box_main.addWidget(self.chose_payment_method_lbl)
        v_box_main.addWidget(self.chose_payment_yandex)
        v_box_main.addWidget(self.chose_payment_card)
        v_box_main.addWidget(self.chose_payment_cash)
        v_box_main.addWidget(self.notify_lbl)
        v_box_main.addLayout(h_box)

        self.setLayout(v_box_main)
        self.setWindowTitle("у мышки боли, у собачки боли, а у кошки не боли...")
        self.show()

    def option_chosed(self, button):
        pass

    def med_chosed(self, text):
        # значения title,description и cost должны браться из БД и помещаться в нужные поля
        self.med_title_res.setText(text)
        self.med_med_description_res.setText("уникальное лекарство, еще бы кто-то знал что оно делает")
        self.med_cost_res.setText("999.0")

    def buy(self):
        # понадобится еще таблица для заказов. она уже создана
        self.close()

    def get_meds_list(self):
        # meds_list должен заполняться лекартствами из БД
        self.meds_list.addItems(["Фармакс", "Агроветзащита", "Астрафрм", "Талисмед", "Novartis"])

    def fill_layout(self, layout, items):
        for item in items:
            layout.addWidget(item)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
