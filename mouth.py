from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QMovie

class Speak():
    def __init__(self, mouth_gif: QMovie):
        self.running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.mouth_gif = mouth_gif

    def stop_running(self):
        self.running = False

    def run(self):
        self.i = 98
        self.inc = 1
        self.running = True
        self.timer.start(20)

    def update_frame(self):
        if not self.running:
            return

        self.mouth_gif.jumpToFrame(self.i)
        self.i += self.inc

        if self.i == 140:
            self.i = 98

class Connect():
    def __init__(self, mouth_gif: QMovie):
        self.running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.mouth_gif = mouth_gif

    def stop_running(self):
        self.running = False

    def run(self):
        self.i = 0
        self.inc = 1
        self.running = True
        self.timer.start(20)

    def update_frame(self):
        if not self.running:
            return

        self.mouth_gif.jumpToFrame(self.i)
        self.i += self.inc

        if self.i == 79:
            self.i -= self.inc

class Listen():
    def __init__(self, mouth_gif: QMovie):
        self.running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.mouth_gif = mouth_gif

    def stop_running(self):
        self.running = False

    def run(self):
        self.i = 159
        self.inc = 1
        self.running = True
        self.timer.start(20)

    def update_frame(self):
        if not self.running:
            return

        self.mouth_gif.jumpToFrame(self.i)
        self.i += self.inc

        if self.i == 188:
            self.i = 159
