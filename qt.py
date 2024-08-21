#!/usr/bin/env python3 

import os
import sys
from face import Face
from menu import Menu
from wifi_config import WiFiConfig
from wifi_password import WiFiPassword
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

class Application:
    def __init__(self):
        app = QApplication([sys.argv])
        app.setFont(QFont("Comic Sans", 50))
        self.face = Face()
        self.menu = Menu()
        self.wifi_config = WiFiConfig()
        self.wifi_password = WiFiPassword()

        self.face.long_press_timer = QTimer()
        self.face.long_press_timer.setInterval(400)
        self.face.long_press_timer.setSingleShot(True)
        self.face.long_press_timer.timeout.connect(self.face_to_menu)

        self.menu.back_button.clicked.connect(self.menu_to_face)
        self.menu.wifi.clicked.connect(self.menu_to_wifi_config)
        
        self.wifi_config.back_button.clicked.connect(self.wifi_config_to_menu)
        self.wifi_config.select_button.clicked.connect(self.wifi_config_to_wifi_password)

        self.wifi_password.back_button.clicked.connect(self.wifi_password_to_wifi_config)

        self.face.show()
        sys.exit(app.exec_())

    def face_to_menu(self):
        self.face.hide()
        self.menu.show()

    def menu_to_face(self):
        self.menu.hide()
        self.face.show()

    def menu_to_wifi_config(self):
        self.menu.hide()
        self.wifi_config.show(reset=True)

    def wifi_config_to_menu(self):
        self.wifi_config.hide()
        self.menu.show()

    def wifi_config_to_wifi_password(self):
        self.wifi_config.hide()
        self.wifi_password.show(ssid=self.wifi_config.result_list.selectedItems()[0].text())

    def wifi_password_to_wifi_config(self):
        self.wifi_password.hide()
        self.wifi_config.show(reset=False)
        
if __name__ == "__main__":
    app = Application()
    app.main()