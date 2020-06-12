from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
import sys

from gui_main import LoginWindow


class ClientWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 640, 480)
        self.center()
        self.acc_button = QPushButton("ИМЯ ПОЛЬЗОВАТЕЛЯ")
        self.make_appointment = QPushButton("ЗАПИСАТЬСЯ НА ОСМОТР")
        self.go_to_my_cats = QPushButton("МОИ ПИТОМЦЫ")
        self.buy_medication = QPushButton("КУПИТЬ СРЕДСТВА")
        self.show_medications = QPushButton("МОИ ПОКУПКИ")
        self.make_appointment.clicked.connect(self.go_to_appointment_window)
        self.go_to_my_cats.clicked.connect(self.go_to_my_pets_window)
        self.buy_medication.clicked.connect(self.go_to_buy_med_window)
        self.acc_button.clicked.connect(self.exit_from_acc)

        v_box_left = QVBoxLayout()
        v_box_left.addWidget(self.make_appointment)
        v_box_left.addWidget(self.go_to_my_cats)
        v_box_left.addWidget(self.buy_medication)
        v_box_left.addWidget(self.show_medications)
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
        self.new_window = AppointmentWindow()
        #self.close()

    def go_to_my_pets_window(self):
        self.new_window = MyPetsWindow()
        # self.close()

    def go_to_buy_med_window(self):
        self.new_window= BuyMedWindow()

    def exit_from_acc(self):
        self.new_window = LoginWindow()
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class AppointmentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 400, 400)
        self.center()
        h_box_date=QHBoxLayout()
        h_box_doc=QHBoxLayout()
        h_box_cat=QHBoxLayout()
        h_box_footer=QHBoxLayout()
        v_box_main=QVBoxLayout()
        v_box_lbl=QVBoxLayout()
        v_box_results=QVBoxLayout()

        self.chose_date_lbl=QLabel("выберите дату")
        calendar=QCalendarWidget(self)
        calendar.setGridVisible(True)
        calendar.clicked[QDate].connect(self.date_chosed)
        h_box_date.addWidget(self.chose_date_lbl)
        h_box_date.addWidget(calendar)

        self.chose_doc_lbl=QLabel("выберите доктора")
        docs_list = QComboBox(self)
        docs_list.addItems(["Bob", "John"])
        docs_list.activated[str].connect(self.doc_chosed)
        h_box_doc.addWidget(self.chose_doc_lbl)
        h_box_doc.addWidget(docs_list)

        self.chose_cat_lbl=QLabel("выберите питомца")
        cats_list = QComboBox(self)
        cats_list.addItems(["Dysia", "Barsik"])
        cats_list.activated[str].connect(self.cat_chosed)
        h_box_cat.addWidget(self.chose_cat_lbl)
        h_box_cat.addWidget(cats_list)

        self.chose_date_lbl2=QLabel("выбранный день: ")
        self.chose_doc_lbl2=QLabel("выбранный доктор:")
        self.chose_cat_lbl2=QLabel("выбранный  питомец:")
        v_box_lbl.addWidget(self.chose_date_lbl2)
        v_box_lbl.addWidget(self.chose_doc_lbl2)
        v_box_lbl.addWidget(self.chose_cat_lbl2)

        self.chose_date_result = QLabel("день не выбран")
        self.chose_doc_result = QLabel("доктор не выбран")
        self.chose_cat_result = QLabel("питомец не выбран")
        v_box_results.addWidget(self.chose_date_result)
        v_box_results.addWidget(self.chose_doc_result)
        v_box_results.addWidget(self.chose_cat_result)

        self.create_appointment_btn=QPushButton("сформироать запись")
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

    def date_chosed(self, date):
        self.chose_date_result.setText(date.toString())

    def doc_chosed(self, text):
        self.chose_doc_result.setText(text)

    def cat_chosed(self, text):
        self.chose_cat_result.setText(text)

    def create_appointment(self):
        #перед закрытикм должен формироваться осмотр
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class MyPetsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 300, 300)
        self.center()
        v_box_main=QVBoxLayout()

        self.operation_lbl=QLabel("функции:")
        self.show_option=QRadioButton("показать данные питомца")
        self.edit_option=QRadioButton("изменить данные питомца")
        self.add_option=QRadioButton("добавить питомца")
        self.delete_option=QRadioButton("удалить питомца")

        self.button_pressed=False
        self.button_group=QButtonGroup()
        self.button_group.addButton(self.show_option)
        self.button_group.addButton(self.edit_option)
        self.button_group.addButton(self.add_option)
        self.button_group.addButton(self.delete_option)
        self.button_group.buttonClicked.connect(self.option_chosed)

        self.cats_list = QComboBox(self)
        #cats_list должен заполняться котами этого пользователя
        self.get_cats_list()

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

    def option_chosed(self, button):
        if self.button_pressed:
            self.delete_last_fragment()
        if button.text() == "показать данные питомца":
            self.show_pet_info()
        elif button.text() == "изменить данные питомца":
            self.edit_pet_info()
        elif button.text() == "добавить питомца":
            self.add_new_pet()
        elif button.text() == "удалить питомца":
            self.delete_pet()
        self.button_pressed = True

    def get_cats_list(self):
        # cats_list должен заполняться котами этого пользователя из БД
        self.cats_list.addItems(["Dysia", "Barsik", "Begemot"])

    def update_cats_list(self):
        #при удалении питомца он также исчезает из списка
        pass

    #clearLayout и delete_last_fragment нужны для удаления предыдущего layout с экрана
    #layout удаляется когда выбрана другая опция
    def clearLayout(self,layout):
        if layout != None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def delete_last_fragment(self):
        v_box_main = self.layout()
        w=v_box_main.itemAt(v_box_main.count()-1)
        self.clearLayout(w)
        v_box_main.removeItem(w)
        self.setLayout(v_box_main)

    def show_pet_info(self):
        #значения полей у питома должны помещаться  соответствубщие Qlabel
        v_box_main = self.layout()
        v_box_lbl=QVBoxLayout()
        v_box_info=QVBoxLayout()
        h_box=QHBoxLayout()

        self.name_lbl=QLabel("Имя:")
        self.age_lbl=QLabel("Возраст:")
        self.breed_lbl=QLabel("Порода:")
        v_box_lbl.addWidget(self.name_lbl)
        v_box_lbl.addWidget(self.age_lbl)
        v_box_lbl.addWidget(self.breed_lbl)
        v_box_lbl.addStretch()

        self.name_text=QLabel("Dysia")
        self.age_text=QLabel("5")
        self.breed_text=QLabel("Scottish Straight")
        v_box_info.addWidget(self.name_text)
        v_box_info.addWidget(self.age_text)
        v_box_info.addWidget(self.breed_text)
        v_box_info.addStretch()

        h_box.addLayout(v_box_lbl)
        h_box.addLayout(v_box_info)

        v_box_main.addLayout(h_box)
        self.setLayout(v_box_main)

    def edit_pet_info(self):
        #значения полей у питома должны помещаться  соответствубщие Qlabel
        v_box_main = self.layout()
        v_box=QVBoxLayout()
        h_box_name_edit=QHBoxLayout()
        h_box_age_edit=QHBoxLayout()
        h_box_breed_edit=QHBoxLayout()
        h_box_footer=QHBoxLayout()

        self.name_lbl=QLabel("Имя:")
        self.name_text=QLineEdit("Dysia")
        h_box_name_edit.addWidget(self.name_lbl)
        h_box_name_edit.addWidget(self.name_text)
        self.age_lbl=QLabel("Возраст:")
        self.age_text=QLineEdit("5")
        h_box_age_edit.addWidget(self.age_lbl)
        h_box_age_edit.addWidget(self.age_text)
        self.breed_lbl=QLabel("Порода:")
        self.breed_text=QLineEdit("Scottish Straight")
        h_box_breed_edit.addWidget(self.breed_lbl)
        h_box_breed_edit.addWidget(self.breed_text)

        #по нажатию save изменения поля питомца в БД должны измениться
        self.save_btn=QPushButton("сохранить")
        h_box_footer.addStretch()
        h_box_footer.addWidget(self.save_btn)

        v_box.addLayout(h_box_name_edit)
        v_box.addLayout(h_box_age_edit)
        v_box.addLayout(h_box_breed_edit)
        v_box.addLayout(h_box_footer)
        v_box_main.addLayout(v_box)
        self.setLayout(v_box_main)

    def add_new_pet(self):
        v_box_main = self.layout()
        v_box=QVBoxLayout()
        h_box_name_edit=QHBoxLayout()
        h_box_age_edit=QHBoxLayout()
        h_box_breed_edit=QHBoxLayout()
        h_box_footer=QHBoxLayout()

        self.name_lbl=QLabel("Имя:")
        self.name_text=QLineEdit("")
        h_box_name_edit.addWidget(self.name_lbl)
        h_box_name_edit.addWidget(self.name_text)
        self.age_lbl=QLabel("Возраст:")
        self.age_text=QLineEdit("")
        h_box_age_edit.addWidget(self.age_lbl)
        h_box_age_edit.addWidget(self.age_text)
        self.breed_lbl=QLabel("Порода:")
        self.breed_text=QLineEdit("")
        h_box_breed_edit.addWidget(self.breed_lbl)
        h_box_breed_edit.addWidget(self.breed_text)

        #по нажатию save изменения поля питомца в БД должны измениться
        self.save_btn=QPushButton("создать питомца")
        h_box_footer.addStretch()
        h_box_footer.addWidget(self.save_btn)

        v_box.addLayout(h_box_name_edit)
        v_box.addLayout(h_box_age_edit)
        v_box.addLayout(h_box_breed_edit)
        v_box.addLayout(h_box_footer)
        v_box_main.addLayout(v_box)
        self.setLayout(v_box_main)

    def delete_pet(self):
        #значения полей у питома должны помещаться  соответствубщие Qlabel
        v_box_main = self.layout()
        v_box_lbl=QVBoxLayout()
        v_box_info=QVBoxLayout()
        v_box=QVBoxLayout()
        h_box=QHBoxLayout()
        h_box_footer=QHBoxLayout()

        self.name_lbl=QLabel("Имя:")
        self.age_lbl=QLabel("Возраст:")
        self.breed_lbl=QLabel("Порода:")
        v_box_lbl.addWidget(self.name_lbl)
        v_box_lbl.addWidget(self.age_lbl)
        v_box_lbl.addWidget(self.breed_lbl)
        v_box_lbl.addStretch()

        self.name_text=QLabel("Dysia")
        self.age_text=QLabel("5")
        self.breed_text=QLabel("Scottish Straight")
        v_box_info.addWidget(self.name_text)
        v_box_info.addWidget(self.age_text)
        v_box_info.addWidget(self.breed_text)
        v_box_info.addStretch()

        h_box.addLayout(v_box_lbl)
        h_box.addLayout(v_box_info)
        v_box.addLayout(h_box)
        h_box_footer.addStretch()
        self.save_btn=QPushButton("удалить питомца")
        h_box_footer.addWidget(self.save_btn)
        v_box.addLayout(h_box_footer)

        v_box_main.addLayout(v_box)
        self.setLayout(v_box_main)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class BuyMedWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 500, 300)
        self.center()
        v_box_main=QVBoxLayout()
        v_box_info=QVBoxLayout()
        h_box=QHBoxLayout()

        self.chose_med_lbl=QLabel("выберите лекарство:")
        self.meds_list=QComboBox()
        self.get_meds_list()
        self.meds_list.activated[str].connect(self.med_chosed)

        self.notify_lbl=QLabel("ВНИМАНИЕ! В данный момент работает только самовызов.")
        self.chose_payment_method_lbl=QLabel("выберите способ оплаты:")
        self.chose_payment_yandex=QRadioButton("Яндекс.Деньги")
        self.chose_payment_card=QRadioButton("Оплата картой")
        self.chose_payment_cash=QRadioButton("Оплата наличными при получении")
        self.button_group=QButtonGroup()
        self.button_group.addButton(self.chose_payment_yandex)
        self.button_group.addButton(self.chose_payment_card)
        self.button_group.addButton(self.chose_payment_cash)
        self.button_group.buttonClicked.connect(self.option_chosed)
        self.buy_btn=QPushButton("Оформить заказ")

        self.med_title=QLabel("НАЗВАНИЕ:")
        self.med_title_res = QLabel("")
        self.med_description=QLabel("ОПИСАНИЕ:")
        self.med_med_description_res = QLabel("")
        self.med_cost=QLabel("СТОИМОСТЬ:")
        self.med_cost_res = QLabel("")

        items=[self.med_title,self.med_title_res,self.med_description,self.med_med_description_res,self.med_cost,self.med_cost_res]
        v_box_info.addStretch()
        self.fill_layout(v_box_info,items)
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
        #значения title,description и cost должны браться из БД и помещаться в нужные поля
        self.med_title_res.setText(text)
        self.med_med_description_res.setText("уникальное лекарство, еще бы кто-то знал что оно делает")
        self.med_cost_res.setText("999.0")

    def buy(self):
        #понадобится еще таблица для заказов. она уже создана
        self.close()

    def get_meds_list(self):
        # meds_list должен заполняться лекартствами из БД
        self.meds_list.addItems(["Фармакс", "Агроветзащита", "Астрафрм","Талисмед", "Novartis"])

    def fill_layout(self,layout,items):
        for item in items:
            layout.addWidget(item)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())