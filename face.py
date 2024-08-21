from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QSequentialAnimationGroup, QPauseAnimation, QTimer, QEvent, QSize, QThread
from PyQt5.QtGui import QPixmap, QMovie
from mouth import Speak, Connect, Listen

class Face(QWidget):
    def __init__(self):
        super().__init__()

        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 800

        self.EYES_HEIGHT = 420
        self.EYES_WIDTH = 900
        self.EYES_X = (self.WINDOW_WIDTH - self.EYES_WIDTH) // 2
        self.EYES_Y = ((self.WINDOW_HEIGHT - self.EYES_HEIGHT)) // 4

        self.EYE_LIDS_X = self.EYES_X
        self.EYE_LIDS_Y = self.EYES_Y
        self.EYE_LIDS_WIDTH = self.EYES_WIDTH
        self.EYE_LIDS_HEIGHT = 0
        self.EYE_LIDS_CLOSE_HEIGHT = self.EYES_HEIGHT // 2

        self.MOUTH_WIDTH = 435
        self.MOUTH_HEIGHT = 150
        self.MOUTH_X = (self.WINDOW_WIDTH - self.MOUTH_WIDTH) // 2
        self.MOUTH_Y = self.EYES_Y + 470

        self.setStyleSheet("""
                            QWidget {
                                background-color: rgba(0, 0, 0, 255);
                            }
                           """)
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
    
        self.init_face()

    def start_interacting(self):
        self.speak.run()
        self.speak_timer.start()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            self.long_press_timer.start()
        elif event.type() == QEvent.MouseButtonRelease:
            self.long_press_timer.stop()
        elif event.type() == QEvent.MouseButtonDblClick:
            self.start_interacting()
        return super().eventFilter(obj, event)

    def init_face(self):
        self.eyes = QLabel(self)
        self.eyes.resize(self.EYES_WIDTH, self.EYES_HEIGHT)
        self.eyes.setPixmap(QPixmap("/root/qt/eyes.jpg").scaled(self.EYES_WIDTH, self.EYES_HEIGHT))
        self.eyes.move(self.EYES_X, self.EYES_Y)

        self.eye_lids = QLabel(self)
        self.eye_lids.resize(self.EYE_LIDS_WIDTH, self.EYE_LIDS_HEIGHT)
        self.eye_lids.setStyleSheet("background-color: black;")
        self.eye_lids.move(self.EYE_LIDS_X, self.EYE_LIDS_Y)

        self.mouth = QLabel(self)
        self.mouth_gif = QMovie("/root/qt/mouth.gif")
        self.mouth_gif.setScaledSize(QSize(self.MOUTH_WIDTH, self.MOUTH_HEIGHT))
        self.mouth.resize(self.MOUTH_WIDTH, self.MOUTH_HEIGHT)
        self.mouth.setMovie(self.mouth_gif)
        self.mouth.move(self.MOUTH_X, self.MOUTH_Y)
        self.mouth_gif.setCacheMode(QMovie.CacheAll)
        self.mouth_gif.jumpToFrame(0)

        self.speak = Listen(self.mouth_gif)

        self.speak_timer = QTimer(self)
        self.speak_timer.setInterval(10000)
        self.speak_timer.setSingleShot(True)
        self.speak_timer.timeout.connect(self.speak.stop_running)

        self.look_animation = QSequentialAnimationGroup(self)
        self.blink_animation = QSequentialAnimationGroup(self)

        self.setup_look_animation()
        self.setup_blink_animation()

        self.installEventFilter(self)

        self.look_animation.start()

    def setup_look_animation(self):
        look_offset = 150
        duration = 200

        pause1 = QPauseAnimation(2000)
        move1 = QPropertyAnimation(self.eyes, b"geometry")
        move1.setDuration(duration)
        move1.setStartValue(QRect(self.EYES_X, self.EYES_Y, self.EYES_WIDTH, self.EYES_HEIGHT))
        move1.setEndValue(QRect(self.EYES_X - look_offset, self.EYES_Y, self.EYES_WIDTH, self.EYES_HEIGHT))
        
        move2 = QPropertyAnimation(self.eyes, b"geometry")
        move2.setDuration(duration)
        move2.setStartValue(QRect(self.EYES_X - look_offset, self.EYES_Y, self.EYES_WIDTH, self.EYES_HEIGHT))
        move2.setEndValue(QRect(self.EYES_X, self.EYES_Y, self.EYES_WIDTH, self.EYES_HEIGHT))
        
        pause2 = QPauseAnimation(800)
        
        move3 = QPropertyAnimation(self.eyes, b"geometry")
        move3.setDuration(duration)
        move3.setStartValue(QRect(self.EYES_X, self.EYES_Y, self.EYES_WIDTH, self.EYES_HEIGHT))
        move3.setEndValue(QRect(self.EYES_X + look_offset, self.EYES_Y, self.EYES_WIDTH, self.EYES_HEIGHT))
        
        move4 = QPropertyAnimation(self.eyes, b"geometry")
        move4.setDuration(duration)
        move4.setStartValue(QRect(self.EYES_X + look_offset, self.EYES_Y, self.EYES_WIDTH, self.EYES_HEIGHT))
        move4.setEndValue(QRect(self.EYES_X, self.EYES_Y, self.EYES_WIDTH, self.EYES_HEIGHT))
        
        self.look_animation.addAnimation(pause1)
        self.look_animation.addAnimation(move1)
        self.look_animation.addAnimation(move2)
        self.look_animation.addAnimation(pause2)
        self.look_animation.addAnimation(move3)
        self.look_animation.addAnimation(move4)

        self.look_animation.finished.connect(self.blink_animation.start)

    def setup_blink_animation(self):
        duration = 200

        pause1 = QPauseAnimation(2000)
        blink1 = QPropertyAnimation(self.eye_lids, b"geometry")
        blink1.setDuration(duration)
        blink1.setStartValue(QRect(self.EYE_LIDS_X, self.EYE_LIDS_Y, self.EYE_LIDS_WIDTH, self.EYE_LIDS_HEIGHT))
        blink1.setEndValue(QRect(self.EYE_LIDS_X, self.EYE_LIDS_Y, self.EYE_LIDS_WIDTH, self.EYE_LIDS_CLOSE_HEIGHT))
        
        blink2 = QPropertyAnimation(self.eye_lids, b"geometry")
        blink2.setDuration(duration)
        blink2.setStartValue(QRect(self.EYE_LIDS_X, self.EYE_LIDS_Y, self.EYE_LIDS_WIDTH, self.EYE_LIDS_CLOSE_HEIGHT))
        blink2.setEndValue(QRect(self.EYE_LIDS_X, self.EYE_LIDS_Y, self.EYE_LIDS_WIDTH, self.EYE_LIDS_HEIGHT))
        
        pause2 = QPauseAnimation(800)

        blink3 = QPropertyAnimation(self.eye_lids, b"geometry")
        blink3.setDuration(duration)
        blink3.setStartValue(QRect(self.EYE_LIDS_X, self.EYE_LIDS_Y, self.EYE_LIDS_WIDTH, self.EYE_LIDS_HEIGHT))
        blink3.setEndValue(QRect(self.EYE_LIDS_X, self.EYE_LIDS_Y, self.EYE_LIDS_WIDTH, self.EYE_LIDS_CLOSE_HEIGHT))
        
        blink4 = QPropertyAnimation(self.eye_lids, b"geometry")
        blink4.setDuration(duration)
        blink4.setStartValue(QRect(self.EYE_LIDS_X, self.EYE_LIDS_Y, self.EYE_LIDS_WIDTH, self.EYE_LIDS_CLOSE_HEIGHT))
        blink4.setEndValue(QRect(self.EYE_LIDS_X, self.EYE_LIDS_Y, self.EYE_LIDS_WIDTH, self.EYE_LIDS_HEIGHT))
        
        self.blink_animation.addAnimation(pause1)
        self.blink_animation.addAnimation(blink1)
        self.blink_animation.addAnimation(blink2)
        self.blink_animation.addAnimation(pause2)
        self.blink_animation.addAnimation(blink3)
        self.blink_animation.addAnimation(blink4)
        
        self.blink_animation.finished.connect(self.look_animation.start)

    def hide(self):
        self.speak.stop_running()
        self.blink_animation.stop()
        self.look_animation.stop()
        self.eyes.move(self.EYES_X, self.EYES_Y)
        self.eye_lids.move(self.EYE_LIDS_X, self.EYE_LIDS_Y)
        self.mouth_gif.jumpToFrame(0)
        super().hide()

    def show(self):
        self.look_animation.start()
        super().show()