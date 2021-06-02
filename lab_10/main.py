from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QPalette, QColor, QImage
from PyQt5.QtCore import QCoreApplication, QEventLoop, Qt, QPointF, QRectF
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QGraphicsScene

import sys
import lab_10_ui
from screen_image import ScreenImage

from typing import List

class MainWindow(QMainWindow, lab_10_ui.Ui_MainWindow):
    def __init__(self):
        '''
        Конструктор
        '''
        super().__init__()
        self.screen_image = ScreenImage()
        self.function = ''
        self.borders_x = [0, 0] #начало и конец
        self.borders_z = [0, 0]
        self.step_x = 0; self.step_z = 0
        self.angles = [0, 0, 0] #x, y, z

        self.setupUi(self)

        self.add_choose_functions()
        self.add_to_ui()
        self.show()

    def add_to_ui(self):
        """
        Функции, добавленные к интерфейсу
        """
        self.but_draw_on_screen.clicked.connect(self.draw_3d_surface)
        self.but_clean_all.clicked.connect(self.clean_all)

    def add_choose_functions(self):
        """
        Выбор изображаемых функций
        """
        self.box_functions.addItem("1")
        self.box_functions.addItem("2")
        self.box_functions.addItem("3")
        self.box_functions.addItem("4")
        self.box_functions.addItem("5")

    def clean_all(self):
        """
        Очистить экран
        """
        self.screen_image.clear()
        pass

    def draw_3d_surface(self):
        """
        Отрисовка трехмерной поверхности
        """
        self.get_data()
        self.draw_floating_horizon(self.function, self.borders_x, self.borders_z,
                                   self.step_x, self.step_z, self.angles)
        pass

    def get_data(self):
        """
        Получить начальные значения
        """
        self.function = self.box_functions.currentText()
        self.borders_x[0] = self.spinbox_start_x.value()
        self.borders_x[1] = self.spinbox_end_x.value()

        self.borders_z[0] = self.spinbox_start_z.value()
        self.borders_z[1] = self.spinbox_end_z.value()

        self.step_x = self.spinbox_step_x.value()
        self.step_z = self.spinbox_step_z.value()

        self.angles[0] = self.spinbox_rotate_x.value()
        self.angles[1] = self.spinbox_rotate_y.value()
        self.angles[2] = self.spinbox_rotate_z.value()
        print(f"self.function = {self.function}")
        print(f"self.borders_x = {self.borders_x}")
        pass


    def draw_floating_horizon(self, function: str, borders_x: list(int, int),
                                                   borders_z: list(int, int),
                              step_x: int, step_z: int,
                              angles: list(int, int, int)):
        x_left, x_right = -1, -1
        y_left, y_right = -1, -1

        top = 0; bottom = screen_height


if __name__ == "__main__":  
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())