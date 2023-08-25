from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem
from PyQt5.QtGui import QPixmap, QCursor, QStandardItem
from generated_file import Ui_MainWindow

import sys
import os


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.pixmap = None
        self.screen_width = QtWidgets.QDesktopWidget().screenGeometry(-1).width()
        self.screen_height = QtWidgets.QDesktopWidget().screenGeometry(-1).height()
        self.click_positions = []
        self.scale = 1
        self.ui.setupUi(self)
        self.ui.image_chooser_button.clicked.connect(self.image_chooser_handler)
        self.ui.image.clicked.connect(self.image_handler)
        self.ui.zoom_in_button.clicked.connect(self.zoom_in)
        self.ui.zoom_out_button.clicked.connect(self.zoom_out)
        self.showMaximized()

    def image_chooser_handler(self):
        filename = QFileDialog.getOpenFileName(self,
                                               directory=os.getcwd(),
                                               filter='Images (*.png *.jpg *.jpeg)'
                                               )[0]
        self.place_image(filename)

    def image_handler(self):
        if self.ui.image.pixmap():
            self.click_positions.append(
                [str(len(self.click_positions) + 1),
                 str(round(self.ui.image.click_position.x() / self.scale, 1)),
                 str(round(self.ui.image.click_position.y() / self.scale, 1))]
            )
            last_click = self.click_positions[-1]
            self.ui.point_list.addItem(' '.join(last_click))

    def place_image(self, filename):
        self.pixmap = QPixmap(filename)
        self.resize_ui(self.pixmap.width(), self.pixmap.height())
        self.ui.image.setPixmap(self.pixmap)
        self.scale = 1

    def zoom_in(self):
        self.scale *= 2
        self.resize_image()

    def zoom_out(self):
        if self.scale > 1:
            self.scale /= 2
            self.resize_image()

    def resize_image(self):
        if self.pixmap:
            size = self.pixmap.size()
            new_pixmap = self.pixmap.scaled(self.scale * size)
            self.ui.image.setPixmap(new_pixmap)
            print(self.scale)

    def resize_ui(self, image_width, image_height):
        btn_width = self.ui.image_chooser_button.width()
        btn_height = self.ui.image_chooser_button.height()
        point_list_height = self.ui.point_list.height()
        total_width = image_width + btn_width
        total_height = image_height
        if total_width > self.screen_width:
            total_width = self.screen_width
        elif total_width <= btn_width:
            total_width = btn_width
        if total_height > self.screen_height:
            total_height = self.screen_height
        elif total_height <= btn_height:
            total_height = btn_height
        self.ui.image.setGeometry(
            0,
            0,
            total_width - btn_width,
            total_height
        )
        self.ui.image_chooser_button.setGeometry(
            total_width - btn_width,
            0,
            btn_width,
            btn_height
        )
        self.ui.point_list.setGeometry(
            total_width - btn_width,
            btn_height,
            self.ui.point_list.width(),
            self.ui.point_list.height()
        )
        self.ui.zoom_in_button.setGeometry(
            total_width - btn_width,
            btn_height + point_list_height,
            self.ui.zoom_in_button.width(),
            self.ui.zoom_in_button.height()
        )
        self.ui.zoom_out_button.setGeometry(
            total_width - btn_width + self.ui.zoom_in_button.width(),
            btn_height + point_list_height,
            self.ui.zoom_out_button.width(),
            self.ui.zoom_out_button.height()
        )


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()
    sys.exit(app.exec())
