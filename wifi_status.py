from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QRect, QThread, QPoint, QObject, QProcess, pyqtSignal, pyqtSlot
from time import sleep

class Worker(QObject):
    wifi = pyqtSignal(int)
    
    def __init__(self):
        super(Worker, self).__init__()
        self.checking = True

    def current_wifi_signal(self):
        while self.checking:
            process = QProcess()
            process.start("wpa_cli signal_poll")
            process.waitForFinished(-1)
            output = process.readAllStandardOutput().data().decode()
            process.close()

            if "FAIL" in output:
                self.wifi.emit(0)
            else:
                for line in output.splitlines():
                    if 'RSSI' in line:
                        strength = int(line.split('=')[1])
                        if strength >= -60:
                            self.wifi.emit(3)
                        elif -60 > strength >= -80:
                            self.wifi.emit(2)
                        elif -80 > strength:
                            self.wifi.emit(1)
                        break

            sleep(5)


class WifiStatusWidget(QWidget):
    def __init__(self, parent=None, continuous=False):
        super(WifiStatusWidget, self).__init__(parent)
        self.signal_strength = 1
        self.setFixedSize(50, 40)
        self.vals = {1: QRect(12, 25, 26, 26), 2: QRect(2, 14, 46, 46), 3: QRect(-10, 3, 70, 70)}

        if continuous:
            self.worker = Worker()
            self.worker_thread = QThread()

            self.worker.moveToThread(self.worker_thread)
            self.worker_thread.started.connect(self.worker.current_wifi_signal)
            self.worker.wifi[int].connect(self.set_signal_strength)
            self.worker_thread.finished.connect(self.worker_thread.deleteLater)
            self.worker_thread.start()

    @pyqtSlot(int)
    def set_signal_strength(self, strength: int):
        self.signal_strength = strength
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.signal_strength == 0:
            painter.setPen(QPen(QColor(255, 0, 0, 255), 2))
            painter.drawPie(self.vals[3], 55 * 16, 70 * 16)
        
        else:
            painter.setPen(QPen(QColor(255, 255, 255, 255), 2))
            painter.drawPie(self.vals[3], 55 * 16, 70 * 16)
            painter.setBrush(QColor(255, 255, 255))
            painter.drawPie(self.vals[self.signal_strength], 55 * 16, 70 * 16)
