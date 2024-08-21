from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor

class Delegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        
        # Draw the line
        painter.save()
        pen = painter.pen()
        pen.setColor(QColor("gray"))
        painter.setPen(pen)
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
        painter.restore()

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        return QSize(size.width(), size.height() + 20)