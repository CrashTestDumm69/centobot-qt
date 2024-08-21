from PyQt5.QtWidgets import QStatusBar, QLabel 
from wifi_status import WifiStatusWidget

class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(50)
        self.setFixedWidth(parent.width())
        self.move(0, parent.height() - 50)

        self.setStyleSheet("""
                            QStatusBar::item {
                                border: 0px;
                                background-color: rgba(0, 0, 0, 255);
                            }
                           """)
        
        self.wifi_icon = WifiStatusWidget(continuous=True)
        self.addPermanentWidget(self.wifi_icon)
