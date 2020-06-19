from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from GUILibrary.client_ui import ClientWindow
from GUILibrary.doctor_ui import DocWindow
import sys


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 300, 200)
        self.center()
        v_box = QVBoxLayout()
        self.username_field = QLineEdit("email")
        self.password_field = QLineEdit("password")
        self.is_doc = QCheckBox("I am doctor")
        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.login)

        v_box.addWidget(self.username_field)
        v_box.addWidget(self.password_field)
        v_box.addWidget(self.is_doc)
        v_box.addWidget(self.btn_login)

        self.setLayout(v_box)
        self.setWindowTitle("login, please :)")
        self.show()

    def login(self):
        # тут должна быть проверка есть ли пользователь, но ее пока нет
        if self.is_doc.isChecked():
            self.new_window = DocWindow()
        else:
            self.new_window = ClientWindow()
        # self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myWindow = DocWindow()
    # myWindow.show()
    sys.exit(app.exec_())
