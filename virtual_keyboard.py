from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect

class VirtualKeyboard(QWidget):
    def __init__(self, parent: QWidget, input_field: QLineEdit):
        super().__init__()
        self.shift_pressed = False
        self.symbols_pressed = False
        self.input_field = input_field

        self.BUTTON_HEIGHT = 70
        self.SPACEBAR_WIDTH = 800

        self.init_keyboard()

    def init_keyboard(self):
        self.setStyleSheet("background-color: #1A1A1A;")
        
        vbox = QVBoxLayout()
        hbox_keys = QVBoxLayout()

        # Define keyboard buttons with some empty spaces
        self.keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Backspace'],
            ['Symbols', 'Space', '']
        ]

        self.symbol_keys = [
            ['!', '@', '#', '$', '%', '^', '&&', '*', '(', ')'],
            ['~', '`', '|', '\\', '{', '}', '[', ']'],
            ['-', '_', '=', '+', '/', '?', ':', ';'],
            ["'", '"', '.', ',', '<', '>', 'Backspace'],
            ['Letters', 'Space', '']
        ]

        # Create keyboard layout
        self.hbox_keys = hbox_keys
        self.update_keyboard_layout()

        # Add input field and keyboard to the main layout
        vbox.addLayout(hbox_keys)
        self.setLayout(vbox)

        self.pop_up_animation = QPropertyAnimation(self, b'geometry')
        self.pop_down_animation = QPropertyAnimation(self, b'geometry')

        self.setup_pop_up_animation()
        self.setup_pop_down_animation()

    def setup_pop_up_animation(self):
        self.pop_up_animation.setDuration(100)
        self.pop_up_animation.setStartValue(QRect(0, 800, 1280, 350))
        self.pop_up_animation.setEndValue(QRect(0, 450, 1280, 350))

    def setup_pop_down_animation(self):
        self.pop_down_animation.setDuration(100)
        self.pop_down_animation.setStartValue(QRect(0, 450, 1280, 350))
        self.pop_down_animation.setEndValue(QRect(0, 800, 1280, 350))

    def update_keyboard_layout(self):
        # Clear existing layout
        while self.hbox_keys.count():
            child = self.hbox_keys.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        current_keys = self.symbol_keys if self.symbols_pressed else self.keys

        for row in current_keys:
            hbox_row = QHBoxLayout()
            for key in row:
                if key == 'Space':
                    button = QPushButton(' ', self)
                    button.setFixedHeight(self.BUTTON_HEIGHT)
                    button.setFixedWidth(self.SPACEBAR_WIDTH)
                    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    button.setStyleSheet("""
                                            QPushButton {
                                                background-color: #3a3a3a;
                                                color: white;
                                                border: 1px solid #5a5a5a;
                                                font-size: 25px;
                                            }
                                            QPushButton:pressed {
                                                background-color: #5a5a5a;
                                            }
                                        """)
                elif key == 'Done':
                    button = QPushButton('Done', self)
                    button.setFixedHeight(self.BUTTON_HEIGHT)
                    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    button.setStyleSheet("""
                                            QPushButton {
                                                background-color: green;
                                                color: white;
                                                font-size: 25px;
                                            }
                                            QPushButton:pressed {
                                                background-color: white;
                                                color: green;
                                            }
                                        """)
                elif key == '':
                    spacer = QSpacerItem(40, self.BUTTON_HEIGHT, QSizePolicy.Expanding, QSizePolicy.Minimum)
                    hbox_row.addItem(spacer)
                    continue
                else:
                    button = QPushButton(key, self)
                    button.setFixedHeight(self.BUTTON_HEIGHT)
                    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    button.setStyleSheet("""
                                            QPushButton {
                                                background-color: #3a3a3a;
                                                color: white;
                                                border: 1px solid #5a5a5a;
                                                font-size: 25px;
                                            }
                                            QPushButton:pressed {
                                                background-color: #5a5a5a;
                                            }
                                        """)
                
                button.setFocusPolicy(Qt.NoFocus)
                button.clicked.connect(self.on_key_press)
                hbox_row.addWidget(button)
            self.hbox_keys.addLayout(hbox_row)

    def on_key_press(self):
        sender = self.sender()
        key = sender.text()
        
        if key == 'Done':
            self.hide()
        elif key == 'Shift':
            self.shift_pressed = not self.shift_pressed
            self.toggle_shift()
        elif key == 'Backspace':
            current_text = self.input_field.text()
            self.input_field.setText(current_text[:-1])
        elif key == 'Space':
            self.input_field.setText(self.input_field.text() + ' ')
        elif key == 'Symbols':
            self.symbols_pressed = True
            self.update_keyboard_layout()
        elif key == 'Letters':
            self.symbols_pressed = False
            self.update_keyboard_layout()
        elif key == '&&':
            self.input_field.setText(self.input_field.text() + '&')
        else:
            if self.shift_pressed and not self.symbols_pressed:
                self.input_field.setText(self.input_field.text() + key.upper())
                self.shift_pressed = False
                self.toggle_shift()
            else:
                self.input_field.setText(self.input_field.text() + key)

    def toggle_shift(self):
        for i in range(len(self.keys)):
            for j in range(len(self.keys[i])):
                if len(self.keys[i][j]) > 1:
                    continue
                if self.keys[i][j].isalpha():
                    if self.shift_pressed:
                        self.keys[i][j] = self.keys[i][j].upper()
                    else:
                        self.keys[i][j] = self.keys[i][j].lower()
        self.update_keyboard_layout()

    def show(self):
        super().show()
        self.pop_up_animation.start()

    def hide(self):
        self.pop_down_animation.start()
        self.pop_down_animation.finished.connect(super().hide)
