from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import Qt
from status_bar import StatusBar

class Menu(QWidget):
    def __init__(self):
        super().__init__()

        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 800

        self.BACK_BUTTON_X = 0
        self.BACK_BUTTON_Y = 0
        self.BACK_BUTTON_WIDTH = 40
        self.BACK_BUTTON_HEIGHT = 40

        self.TILE_SPACING_X = 80
        self.TILE_SPACING_Y = 100
        self.TILE_WIDTH = 210
        self.TILE_HEIGHT = 210
        self.TILE_X_OFFSET = 100
        self.TILE_Y_OFFSET = 80

        self.setStyleSheet("""
                            QWidget {
                                background-color: rgba(0, 0, 0, 255);
                            }
                           """)
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.init_menu()

    def init_menu(self):
        self.tile_row = 1
        self.tile_col = 1

        self.navigate = QPushButton(self)
        self.navigate.resize(self.TILE_WIDTH, self.TILE_HEIGHT)
        self.navigate.setStyleSheet("background-color: #696969; border-radius: 20px; border: 1px solid black;")
        self.navigate.setText("Navigate")
        # self.navigate.setAlignment(Qt.AlignCenter)
        self.navigate.move(self.TILE_X_OFFSET + ((self.TILE_WIDTH + self.TILE_SPACING_X) * (self.tile_col - 1)), self.TILE_Y_OFFSET + (self.TILE_HEIGHT * (self.tile_row - 1)))
        self.navigate.setFocusPolicy(Qt.NoFocus)

        self.tile_row = 1
        self.tile_col = 2

        self.joystick = QPushButton(self)
        self.joystick.resize(self.TILE_WIDTH, self.TILE_HEIGHT)
        self.joystick.setStyleSheet("background-color: #696969; border-radius: 20px; border: 1px solid black;")
        self.joystick.setText("Joystick")
        # self.joystick.setAlignment(Qt.AlignCenter)
        self.joystick.move(self.TILE_X_OFFSET + ((self.TILE_WIDTH + self.TILE_SPACING_X) * (self.tile_col - 1)), self.TILE_Y_OFFSET + (self.TILE_HEIGHT * (self.tile_row - 1)))
        self.joystick.setFocusPolicy(Qt.NoFocus)

        self.tile_row = 1
        self.tile_col = 3

        self.wifi = QPushButton(self)
        self.wifi.resize(self.TILE_WIDTH, self.TILE_HEIGHT)
        self.wifi.setStyleSheet("background-color: #696969; border-radius: 20px; border: 1px solid black;")
        self.wifi.setText("WiFi config")
        # self.wifi.setAlignment(Qt.AlignCenter)
        self.wifi.move(self.TILE_X_OFFSET + ((self.TILE_WIDTH + self.TILE_SPACING_X) * (self.tile_col - 1)), self.TILE_Y_OFFSET + (self.TILE_HEIGHT * (self.tile_row - 1)))
        self.wifi.setFocusPolicy(Qt.NoFocus)

        self.status_bar = StatusBar(self)
        self.status_bar.move(0, 0)

        self.back_button = QPushButton(self)
        self.back_button.resize(self.BACK_BUTTON_WIDTH, self.BACK_BUTTON_HEIGHT)
        self.back_button.setStyleSheet("background-color: red;")
        self.back_button.move(self.BACK_BUTTON_X, self.BACK_BUTTON_Y)
        self.back_button.setFocusPolicy(Qt.NoFocus)
