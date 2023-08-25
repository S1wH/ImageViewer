from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, pyqtSignal


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.click_position = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.click_position = event.pos()
            self.clicked.emit()
        return QLabel.mousePressEvent(self, event)
