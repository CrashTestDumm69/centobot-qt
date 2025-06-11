#!/usr/bin/env python3
import sys
import socket
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
import roslibpy


class GifPlayer(QWidget):
    animation_change_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Create fullscreen label with no margins
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        # Remove window decorations and make fullscreen
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        # Make label fill the entire window
        self.label.setGeometry(0, 10, self.width(), self.height())

        self.setStyleSheet("background-color: black;")

        # Load GIFs
        self.movies = {}
        for state in ['idle', 'speech']:
            movie = QMovie(f"/root/qt/{state}.gif")
            if movie.isValid():
                movie.setCacheMode(QMovie.CacheAll)
                movie.setSpeed(100)
                self.movies[state] = movie

        print(self.movies)

        # Start with idle animation immediately
        self.state = None
        if 'idle' in self.movies:
            self.set_movie('idle')

        # ROS Setup with hostname namespace
        namespace = socket.gethostname()
        self.ros = roslibpy.Ros(host='localhost', port=9090)
        self.ros.run()

        topic_name = f'/{namespace}/speech_control'
        self.sub = roslibpy.Topic(self.ros, topic_name, 'std_msgs/String')
        self.sub.subscribe(self.on_ros_message)

        self.animation_change_signal.connect(self.set_movie)

    def resizeEvent(self, event):
        """Ensure label always fills the entire window when resized"""
        self.label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    @pyqtSlot(str)
    def set_movie(self, state):
        """Set and play the animation for the given state"""
        if self.state == state:
            return

        if state in self.movies:
            self.state = state
            movie = self.movies[state]
            self.label.setMovie(movie)
            movie.start()

    def on_ros_message(self, message):
        """Handle incoming ROS messages"""
        try:
            msg = message['data'].lower()
            if msg == 'remote_start':
                self.animation_change_signal.emit("speech")
            elif msg == 'remote_stop':
                self.animation_change_signal.emit("idle")
        except Exception:
            pass

    def closeEvent(self, event):
        """Clean up when closing the window"""
        try:
            if hasattr(self, 'sub') and self.sub:
                self.sub.unsubscribe()
            if hasattr(self, 'ros') and self.ros:
                self.ros.terminate()
        except Exception:
            pass
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = GifPlayer()
    sys.exit(app.exec_())
