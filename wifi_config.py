import re
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QProcess
from delegate import Delegate
from time import sleep

class WiFiChecker():
    def __init__(self):
        super().__init__()
        self.network_list = {}
        self.pattern = re.compile(r"\S+\s+\d+\s+(-\d+)\s+\[.*\]\s+(.*)")

    def get_network_list(self) -> dict:
        process = QProcess()
        
        process.start("sudo wpa_cli scan")
        process.waitForFinished(-1)
        
        process.close()

        process = QProcess()
        
        process.start("sudo wpa_cli scan_results")
        process.waitForFinished(-1)

        result = process.readAll().data().decode()
        for line in result.splitlines():
            match = self.pattern.match(line)
            if match:
                signal = int(match.group(1))
                ssid = match.group(2)
                if ssid in self.network_list:
                    if signal > self.network_list[ssid]:
                        self.network_list[ssid] = signal
                else:
                    self.network_list[ssid] = signal

        process.close()

        return self.network_list

class WiFiConfig(QWidget):
    def __init__(self):
        super().__init__()

        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 800

        self.CLOSE_BUTTON_WIDTH = 40
        self.CLOSE_BUTTON_HEIGHT = 40
        self.CLOSE_BUTTON_X = self.WINDOW_WIDTH - self.CLOSE_BUTTON_WIDTH
        self.CLOSE_BUTTON_Y = 0

        self.SCAN_BUTTON_WIDTH = 100
        self.SCAN_BUTTON_HEIGHT = 50
        self.SCAN_BUTTON_X = 440 
        self.SCAN_BUTTON_Y = 700

        self.SELECT_BUTTON_WIDTH = 100
        self.SELECT_BUTTON_HEIGHT = 50
        self.SELECT_BUTTON_X = 730 
        self.SELECT_BUTTON_Y = 700

        self.BACK_BUTTON_WIDTH = 40
        self.BACK_BUTTON_HEIGHT = 40
        self.BACK_BUTTON_X = 0
        self.BACK_BUTTON_Y = 0

        self.setStyleSheet("background-color: black;")
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.init_wifi()

    def init_wifi(self):
        self.installEventFilter(self)

        self.back_button = QPushButton(self)
        self.back_button.resize(self.BACK_BUTTON_WIDTH, self.BACK_BUTTON_HEIGHT)
        self.back_button.setStyleSheet("background-color: red;")
        self.back_button.move(self.BACK_BUTTON_X, self.BACK_BUTTON_Y)
        self.back_button.setFocusPolicy(Qt.NoFocus)

        self.close_button = QPushButton(self)
        self.close_button.resize(self.CLOSE_BUTTON_WIDTH, self.CLOSE_BUTTON_HEIGHT)
        self.close_button.setStyleSheet("background-color: red;")
        self.close_button.move(self.CLOSE_BUTTON_X, self.CLOSE_BUTTON_Y)
        self.close_button.setFocusPolicy(Qt.NoFocus)
        self.close_button.clicked.connect(self.quit_app)

        self.scan_button = QPushButton(self)
        self.scan_button.resize(self.SCAN_BUTTON_WIDTH, self.SCAN_BUTTON_HEIGHT)
        self.scan_button.move(self.SCAN_BUTTON_X, self.SCAN_BUTTON_Y)
        self.scan_button.setStyleSheet("""
                                        QPushButton {
                                            background-color: green;
                                            color: black;
                                        }
                                        QPushButton:pressed {
                                            background-color: gray;
                                            color: black;
                                        }
                                    """)
        self.scan_button.setText("Scan")
        self.scan_button.setFocusPolicy(Qt.NoFocus)
        self.scan_button.clicked.connect(self.scan_wifi)

        self.select_button = QPushButton(self)
        self.select_button.resize(self.SELECT_BUTTON_WIDTH, self.SELECT_BUTTON_HEIGHT)
        self.select_button.move(self.SELECT_BUTTON_X, self.SELECT_BUTTON_Y)
        self.select_button.setStyleSheet("""
                                        QPushButton:enabled {
                                            background-color: green;
                                            color: black;
                                        }
                                        QPushButton:disabled {
                                            background-color: gray;
                                            color: black;
                                        }
                                    """)
        self.select_button.setFocusPolicy(Qt.NoFocus)
        self.select_button.setText("Connect")
        self.select_button.setDisabled(True)

        self.result_list = QListWidget(self)
        self.result_list.resize(500, 550)
        self.result_list.move(390, 100)
        self.result_list.setItemDelegate(Delegate())
        self.result_list.setFocusPolicy(Qt.NoFocus)
        self.result_list.setStyleSheet("""
                                        QListWidget:item {
                                            background-color: black;
                                            color: white;
                                        }

                                        QListWidget:item:selected {
                                            background-color: white;
                                            color: black;
                                        }
                                    """)
        self.result_list.itemSelectionChanged.connect(self.selected_ssid)

        self.wifichecker = WiFiChecker()

    def reset_list(self):
        wifi_title = QListWidgetItem("Available WiFi Networks")
        wifi_title.setForeground(QColor(255, 255, 255))
        wifi_title.setTextAlignment(Qt.AlignCenter)
        wifi_title.setFlags(wifi_title.flags() & ~Qt.ItemIsSelectable)
        self.result_list.clear()
        self.result_list.addItem(wifi_title)
        del wifi_title

    def selected_ssid(self):
            selected_items = self.result_list.selectedItems()
            if len(selected_items) > 0:
                self.select_button.setDisabled(False)
            else:
                self.select_button.setDisabled(True)

    def scan_wifi(self):
        self.scan_button.setDisabled(True)
        wifi = self.wifichecker.get_network_list()

        self.reset_list()

        for ssid, signal in wifi.items():
            item = QListWidgetItem(ssid)
            item.setForeground(QColor(255, 255, 255))
            self.result_list.addItem(item)
            del item
        
        self.scan_button.setEnabled(True)
    def show(self, reset: bool):
        if reset:
            self.reset_list()
        
        super().show()

    def quit_app(self):
        QApplication.instance().quit()