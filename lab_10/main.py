from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QPalette, QColor, QImage
from PyQt5.QtCore import QCoreApplication, QEventLoop, Qt, QPointF, QRectF
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QGraphicsScene

import sys
import lab_10_ui
from screen_image import ScreenImage

class MainWindow(QMainWindow, lab_10_ui.Ui_MainWindow):
    def __init__(self):
        '''
        Конструктор
        '''
        super().__init__()
        self.screen_image = ScreenImage()

        self.setupUi(self)
        self.show()

    def FloatingHorizon(self, screen_height):
        x_left, x_right = -1, -1
        y_left, y_right = -1, -1

        top = 0; bottom = screen_height


if __name__ == "__main__":  
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())