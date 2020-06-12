from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
import sys

from gui_main import LoginWindow


class DocWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 640, 480)
        self.center()
        self.acc_button = QPushButton("ИМЯ ПОЛЬЗОВАТЕЛЯ")
        self.add_doc_button = QPushButton("ДОБАВИТЬ ДОКТОРА/ИЗМЕНИТЬ СТАТУС")
        self.change_data_button = QPushButton("ИЗМЕНИТЬ ДАННЫЕ")
        self.change_work_time_button = QPushButton("ЗАДАТЬ РАБОЧЕЕ ВРЕМЯ")
        self.change_med_button = QPushButton("ДОБАВИТЬ/ИЗМЕНИТЬ ЛЕКАРСТВО")
        self.show_checkups_button = QPushButton("СПИСОК ОСМОТРОВ")
        self.acc_button.clicked.connect(self.exit_from_acc)

        v_box_left = QVBoxLayout()
        v_box_left.addWidget(self.add_doc_button)
        v_box_left.addWidget(self.change_data_button)
        v_box_left.addWidget(self.change_work_time_button)
        v_box_left.addWidget(self.change_med_button)
        v_box_left.addWidget(self.show_checkups_button)
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
        self.new_window = LoginWindow()
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())