#!/usr/bin/env python3

import sys
from face import Face
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont


class LoadScreen(QWidget):

    def __init__(self):
        super().__init__()

        self.WINDOW_WIDTH = 600
        self.WINDOW_HEIGHT = 1024

        self.setStyleSheet("background-color: blue;")
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)


class Application:

    def __init__(self):
        app = QApplication([sys.argv])
        app.setFont(QFont("Comic Sans", 50))

        self.load_screen = LoadScreen()
        self.load_screen.show()

        QTimer.singleShot(500, self.initialize)

        sys.exit(app.exec_())

    def initialize(self):
        self.face = Face()

        self.load_screen.hide()
        self.face.show()


if __name__ == "__main__":
    app = Application()
