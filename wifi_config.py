import re
from PyQt5.QtWidgets import QWidget, QPushButton, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QScroller, QScrollerProperties, QAbstractItemView
from PyQt5.QtCore import Qt, QProcess, QPoint, QRunnable, QThreadPool, QObject, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPolygon
from delegate import Delegate
from time import sleep
from wifi_status import WifiStatusWidget

class WifiListItem(QWidget):
    def __init__(self, ssid: str, dbm: int, connected: False, parent: QWidget = None):
        super(WifiListItem, self).__init__(parent)
        
        ssid_label = QLabel(ssid)
        ssid_label.setStyleSheet("""
                                    QLabel {
                                        color: rgba(255, 255, 255, 255);
                                        background-color: rgba(0, 0, 0, 0);
                                    }  
                                 """)
        
        wifi_status = WifiStatusWidget(continuous=False)
        if dbm >= -60:
            wifi_status.set_signal_strength(3)
        elif -60 > dbm >= -80:
            wifi_status.set_signal_strength(2)
        elif -80 > dbm:
            wifi_status.set_signal_strength(1)

        if connected:
            connected_label = QLabel("Connected")
            connected_label.setStyleSheet("""
                                            QLabel {
                                                color: rgba(255, 255, 255, 100)
                                                background-color: rgba(0, 0, 0, 0)
                                            }
                                          """)
        layout = QHBoxLayout()
        layout.addWidget(ssid_label)
        layout.addStretch()
        layout.addWidget(wifi_status)
        
        self.setLayout(layout)

class IndicatorWidget(QWidget):
    def __init__(self, parent=None, position:str = None):
        super().__init__(parent)
        self.setFixedHeight(30)  # Adjust the height as needed
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.position = position
        self.show_triangle = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 0))

        painter.drawRect(self.rect())

        if self.show_triangle:
            if self.position == "top":
                triangle = QPolygon([
                    QPoint(self.width() // 2, 5),
                    QPoint(self.width() // 2 - 10, self.height() - 5),
                    QPoint(self.width() // 2 + 10, self.height() - 5)
                ])
            elif self.position == "bottom":
                triangle = QPolygon([
                    QPoint(self.width() // 2, self.height() - 5),
                    QPoint(self.width() // 2 - 10, 5),
                    QPoint(self.width() // 2 + 10, 5)
                ])
            painter.setBrush(QColor(255, 255, 255, 100))
            painter.drawPolygon(triangle)

    def set_indicator_visibility(self, visible):
        self.show_triangle = visible
        self.update()

class WiFiList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.list = QListWidget(self)
        self.list.setItemDelegate(Delegate())
        self.list.setFocusPolicy(Qt.NoFocus)
        self.list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list.setStyleSheet("""
                                QListWidget:item {
                                    background-color: rgba(0, 0, 0, 255);
                                }

                                QListWidget:item:selected {
                                    background-color: rgba(255, 255, 255, 50);
                                }
                                """)

        layout = QVBoxLayout()
        self.top_indicator = IndicatorWidget(self, "top")
        self.bottom_indicator = IndicatorWidget(self, "bottom")
        layout.addWidget(self.top_indicator)
        layout.addWidget(self.list)
        layout.addWidget(self.bottom_indicator)
        self.setLayout(layout)

        scroller = QScroller.scroller(self.list.viewport())
        scroller.grabGesture(self.list.viewport(), QScroller.LeftMouseButtonGesture)

        properties = scroller.scrollerProperties()
        properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootPolicy.OvershootWhenScrollable)
        properties.setScrollMetric(QScrollerProperties.FrameRate, QScrollerProperties.FrameRates.Fps30)
        scroller.setScrollerProperties(properties)

        self.list.verticalScrollBar().valueChanged.connect(self.update_indicators)
        self.update_indicators()

    def update_indicators(self):
        scrollBar = self.list.verticalScrollBar()
        max_value = scrollBar.maximum()
        min_value = scrollBar.minimum()
        current_value = scrollBar.value()

        self.top_indicator.set_indicator_visibility(current_value > min_value)
        self.bottom_indicator.set_indicator_visibility(current_value < max_value)

    def clear_indicators(self):
        self.top_indicator.set_indicator_visibility(False)
        self.bottom_indicator.set_indicator_visibility(False)
        

class WiFiCheckerSignals(QObject):
    result = pyqtSignal(dict)

class WiFiChecker(QRunnable):
    def __init__(self):
        super().__init__()
        self.network_list = {}
        self.signals = WiFiCheckerSignals()
        self.scan_network_pattern = re.compile(r"\S+\s+\d+\s+(-\d+)\s+\[.*\]\s+(.*)")
        self.list_network_pattern = re.compile(r'(\d+)\s+([^\s]+(?: [^\s]+)*)\s+any\s+\[(\w+)\]')

    def run(self):
        ssid = self.get_network_list()
        self.signals.result.emit(ssid)

    def get_network_list(self) -> dict:
        retries = 0
        while True:
            process = QProcess()
            
            process.start("wpa_cli scan")
            process.waitForFinished(-1)
            
            output = process.readAllStandardOutput().data().decode()
            process.close()

            if "OK" in output or retries > 5:
                break
            
            sleep(0.5)
            retries += 1

        process = QProcess()

        process.start("wpa_cli scan_results")
        process.waitForFinished(-1)

        result = process.readAll().data().decode()
        for line in result.splitlines():
            match = self.pattern.match(line)
            if match:
                signal = int(match.group(1))
                ssid = match.group(2)
                if ssid == "" or signal < -90:
                    continue
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

        self.setStyleSheet("""
                            QWidget {
                                background-color: rgba(0, 0, 0, 255);
                            }
                           """)
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.init_wifi()

    def init_wifi(self):
        self.installEventFilter(self)

        self.back_button = QPushButton(self)
        self.back_button.resize(self.BACK_BUTTON_WIDTH, self.BACK_BUTTON_HEIGHT)
        self.back_button.setStyleSheet("""
                                        QPushButton {
                                            background-color: red;
                                        }
                                       """)
        self.back_button.move(self.BACK_BUTTON_X, self.BACK_BUTTON_Y)
        self.back_button.setFocusPolicy(Qt.NoFocus)

        self.scan_button = QPushButton(self)
        self.scan_button.resize(self.SCAN_BUTTON_WIDTH, self.SCAN_BUTTON_HEIGHT)
        self.scan_button.move(self.SCAN_BUTTON_X, self.SCAN_BUTTON_Y)
        self.scan_button.setStyleSheet("""
                                        QPushButton:enabled {
                                            background-color: rgba(0, 200, 0, 255);
                                            color: rgba(0, 0, 0, 255);
                                        }
                                        QPushButton:disabled {
                                            background-color: gray;
                                            color: rgba(0, 0, 0, 255);
                                        }
                                        QPushButton:pressed {
                                            background-color: gray;
                                            color: rgba(0, 0, 0, 255);
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
                                            background-color: rgba(0, 200, 0, 255);
                                            color: rgba(0, 0, 0, 255);
                                        }
                                        QPushButton:disabled {
                                            background-color: gray;
                                            color: rgba(0, 0, 0, 255);
                                        }
                                        QPushButton:pressed {
                                            background-color: gray;
                                            color: rgba(0, 0, 0, 255);
                                        }
                                         """)
        self.select_button.setFocusPolicy(Qt.NoFocus)
        self.select_button.setText("Connect")
        self.select_button.setDisabled(True)

        self.result = WiFiList(self)
        self.result.resize(900, 560)
        self.result.move(190, 110)
        self.result.list.itemSelectionChanged.connect(self.selected_ssid)

        self.wifi_title = QLabel("Available WiFi Networks", self)
        self.wifi_title.resize(1280, 50)
        self.wifi_title.move(0, 50)
        self.wifi_title.setAlignment(Qt.AlignCenter)
        self.wifi_title.setStyleSheet("""
                                        QLabel {
                                            color: rgba(255, 255, 255, 255);
                                            background-color: rgba(0, 0, 0, 255);
                                        }
                                      """)
        
        self.threadpool = QThreadPool()


    def selected_ssid(self):
            selected_items = self.result.list.selectedItems()
            if len(selected_items) > 0:
                self.select_button.setDisabled(False)
            else:
                self.select_button.setDisabled(True)

    def scan_wifi(self):
        self.scan_button.setDisabled(True)
        checker = WiFiChecker()
        checker.signals.result[dict].connect(self.update_list)
        self.threadpool.start(checker)

    def update_list(self, wifi: dict):
        self.result.list.clear()
        self.result.clear_indicators()

        for ssid, signal in wifi.items():
            wifi_item = WifiListItem(ssid, signal)
            item = QListWidgetItem()
            item.setSizeHint(wifi_item.sizeHint())
            self.result.list.addItem(item)
            self.result.list.setItemWidget(item, wifi_item)
            self.result.list.addItem(item)
            self.result.update_indicators()
            del item, wifi_item

        self.scan_button.setEnabled(True)

    def show(self, reset: bool):
        if reset:
            self.result.list.clear()
            self.result.clear_indicators()
            self.scan_wifi()
        
        super().show()
