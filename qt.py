#!/usr/bin/env python3


import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QMovie


class GifPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.resize(1024, 600)

    def init_ui(self):
        # Set up the layout
        layout = QVBoxLayout()

        # QLabel to display the GIF
        self.gif_label = QLabel(self)

        # Load and start the GIF
        self.movie = QMovie("face.gif")  # Replace with the path to your GIF
        self.gif_label.setMovie(self.movie)
        self.gif_label.resize(1024, 600)
        self.gif_label.move(0, 0)
        self.movie.start()

        # Set layout and window title
        self.setLayout(layout)
        self.setWindowTitle("GIF Player")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = GifPlayer()  # Set the window size
    player.show()
    sys.exit(app.exec_())
