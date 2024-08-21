import re
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QProcess
from virtual_keyboard import VirtualKeyboard

class WiFiPassword(QWidget):
    def __init__(self):
        super().__init__()

        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 800
        
        self.SSID_LABEL_WIDTH = 500
        self.SSID_LABEL_HEIGHT = 60
        self.SSID_LABEL_X = 390
        self.SSID_LABEL_Y = 100

        self.PASSWORD_LINE_WIDTH = 500
        self.PASSWORD_LINE_HEIGHT = 60
        self.PASSWORD_LINE_X = 390
        self.PASSWORD_LINE_Y = 200

        self.BACK_BUTTON_WIDTH = 40
        self.BACK_BUTTON_HEIGHT = 40
        self.BACK_BUTTON_X = 0
        self.BACK_BUTTON_Y = 0

        self.CONNECT_BUTTON_WIDTH = 100
        self.CONNECT_BUTTON_HEIGHT = 50
        self.CONNECT_BUTTON_X = 590
        self.CONNECT_BUTTON_Y = 300

        self.KEYBOARD_WIDTH = 1280
        self.KEYBOARD_HEIGHT = 350
        self.KEYBOARD_X = 0
        self.KEYBOARD_Y = 450

        self.setStyleSheet("""
                            QWidget {
                                background-color: rgba(0, 0, 0, 255);
                            }
                           """)
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.init_wifi_password()

    def init_wifi_password(self):
        self.ssid_label = QLineEdit(self)
        self.ssid_label.resize(self.SSID_LABEL_WIDTH, self.SSID_LABEL_HEIGHT)
        self.ssid_label.move(self.SSID_LABEL_X, self.SSID_LABEL_Y)
        self.ssid_label.setAlignment(Qt.AlignCenter)
        self.ssid_label.setFont(QFont("Comic Sans", 55))
        self.ssid_label.setStyleSheet("background-color: black; color: white;")
        self.ssid_label.setReadOnly(True)

        self.password_line = QLineEdit(self)
        self.password_line.resize(self.PASSWORD_LINE_WIDTH, self.PASSWORD_LINE_HEIGHT)
        self.password_line.move(self.PASSWORD_LINE_X, self.PASSWORD_LINE_Y)
        self.password_line.setStyleSheet("background-color: white;")
        self.password_line.setFont(QFont("Comic Sans", 55))

        self.keyboard = VirtualKeyboard(self, input_field=self.password_line)
        self.keyboard.resize(self.KEYBOARD_WIDTH, self.KEYBOARD_HEIGHT)
        self.keyboard.move(self.KEYBOARD_X, self.KEYBOARD_Y)

        self.back_button = QPushButton(self)
        self.back_button.resize(self.BACK_BUTTON_WIDTH, self.BACK_BUTTON_HEIGHT)
        self.back_button.setStyleSheet("background-color: red;")
        self.back_button.move(self.BACK_BUTTON_X, self.BACK_BUTTON_Y)
        self.back_button.setFocusPolicy(Qt.NoFocus)

        self.connect_button = (QPushButton('Connect', self))
        self.connect_button.resize(self.CONNECT_BUTTON_WIDTH, self.CONNECT_BUTTON_HEIGHT)
        self.connect_button.move(self.CONNECT_BUTTON_X, self.CONNECT_BUTTON_Y)
        self.connect_button.setFocusPolicy(Qt.NoFocus)
        self.connect_button.setStyleSheet("""
                                            QPushButton {
                                                background-color: green;
                                                color: black;
                                            }
                                            QPushButton:pressed {
                                                background-color: gray
                                                color: black;
                                            }
                                        """)
        self.connect_button.clicked.connect(self.connect_wifi)

    def connect_wifi(self):
        self.connect_button.setDisabled(True)
        process = QProcess()
        process.start()

    def show(self, ssid: str):
        self.ssid = ssid
        self.ssid_label.setText("Enter password for " + self.ssid)
        super().show()
        self.keyboard.show()

