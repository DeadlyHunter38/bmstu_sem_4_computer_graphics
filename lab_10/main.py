from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QPalette, QColor, QImage
from PyQt5.QtCore import QCoreApplication, QEventLoop, Qt, QPointF, QRectF
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QGraphicsScene

import sys
import lab_10_ui
from screen_image import ScreenImage
from math import cos, sin, pi, fabs
from typing import List
from functions import *
from copy import deepcopy

FUNCTIONS = ['cos(x) * sin(z)', 'cos(x)', 'x + z']

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

        self.screen_image.setSceneRect(0, 0, self.width(), self.height())
        self.graphicsView.setScene(self.screen_image)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def add_choose_functions(self):
        """
        Выбор изображаемых функций
        """
        self.box_functions.addItem(FUNCTIONS[0])
        self.box_functions.addItem(FUNCTIONS[1])
        self.box_functions.addItem(FUNCTIONS[2])

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
        self.screen_image.clear()
        functions = [f1, f2, f3]
        self.get_data()
        index_function = self.get_index_function()
        self.draw_floating_horizon(functions[index_function], self.borders_x, self.borders_z,
                                   self.step_x, self.step_z, self.angles, int(self.screen_image.width()), int(self.screen_image.height()))
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

        self.angles[0] += self.spinbox_rotate_x.value()
        self.angles[1] += self.spinbox_rotate_y.value()
        self.angles[2] += self.spinbox_rotate_z.value()
        return 

    def get_index_function(self):
        index_function = -1
        for i in range(len(FUNCTIONS)):
            if FUNCTIONS[i] == self.function:
                index_function = i
                break
        return index_function

    def draw_floating_horizon(self, function: str, borders_x: List[int],
                                                   borders_z: List[int],
                                    step_x: int, step_z: int,
                                    angles: List[int],
                                    width_screen, height_screen):
        """
        Алгоритм плавающего горизонта
        """
        x_left, x_right = -1, -1
        y_left, y_right = -1, -1

        top = [0] * width_screen
        bottom = [height_screen] * width_screen

        z_max = borders_z[1]; z_min = borders_z[0]; z_step = step_z
        x_max = borders_x[1]; x_min = borders_x[0]; x_step = step_x

        z = z_max
        while z >= z_min - z_step / 2:
            x_previous = x_min
            y_previous = function(x_min, z)
            x_previous, y_previous = self.tranform_to_2d(x_previous, y_previous, z, angles)
            x_left, y_left = self.process_side_edge(x_previous, y_previous,
                                                    x_left, y_left, top, bottom)
            flag_visible_prev = self.visible(x_previous, y_previous, top, bottom)
            x = x_min
            while x <= x_max + x_step / 2:
                y_current = function(x, z)
                x_current, y_current = self.tranform_to_2d(x, y_current, z, angles)
                flag_visible_current = self.visible(x_current, y_current, top, bottom)
                if flag_visible_current == flag_visible_prev:
                    if flag_visible_current == 1 or flag_visible_current == -1:
                        self.screen_image.draw_line(x_previous, y_previous, x_current, y_current)
                        self.horizont(x_previous, y_previous, x_current, y_current,
                                      top, bottom)
                else:
                    if flag_visible_current == 0:
                        if flag_visible_prev == 1:
                            xi, yi = self.intersection(x_previous, y_previous,
                                                       x_current, y_current, top)
                        else:
                            xi, yi = self.intersection(x_previous, y_previous,
                                                       x_current, y_current, bottom)
                        self.screen_image.draw_line(x_previous, y_previous, xi, yi)
                        self.horizont(x_previous, y_previous, xi, yi, top, bottom)
                    else:
                        if flag_visible_current == 1:
                            if flag_visible_prev == 0:
                                xi, yi = self.intersection(x_previous, y_previous,
                                                            x_current, y_current,
                                                            top)
                                self.screen_image.draw_line(xi, yi, x_current, y_current)
                                self.horizont(xi, yi, x_current, y_current, top, bottom)
                            else:
                                xi, yi = self.intersection(x_previous, y_previous,
                                                            x_current, y_current,
                                                            bottom)
                                self.screen_image.draw_line(x_previous, y_previous, xi, yi)
                                self.horizont(x_previous, y_previous, xi, yi, top, bottom)
                                xi, yi = self.intersection(x_previous, y_previous,
                                                            x_current, y_current,
                                                            top)
                                self.screen_image.draw_line(xi, yi, x_current, y_current)
                                self.horizont(xi, yi, x_current, y_current, top, bottom)
                        else:
                            if flag_visible_prev == 0:
                                xi, yi = self.intersection(x_previous, y_previous,
                                                           x_current, y_current,
                                                           bottom)
                                self.screen_image.draw_line(xi, yi, x_current, y_current)
                                self.horizont(xi, yi, x_current, y_current, top, bottom)
                            else:
                                xi, yi = self.intersection(x_previous, y_previous, 
                                                           x_current, y_current,
                                                           top)
                                self.screen_image.draw_line(x_previous, y_previous, xi, yi)
                                self.horizont(x_previous, y_previous, xi, yi,
                                              top, bottom)
                                xi, yi = self.intersection(x_previous, y_previous,
                                                           x_current, y_current,
                                                           bottom)
                                self.screen_image.draw_line(xi, yi, x_current, y_current)
                                self.horizont(xi, yi, x_current, y_current, top, bottom)
                flag_visible_prev = flag_visible_current
                x_previous = x_current; y_previous = y_current
                x += x_step
            x_right, y_right = self.process_side_edge(x_previous, y_previous, x_right, 
                                                      y_right, top, bottom)
            z -= z_step
            QCoreApplication.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents, 0)
                                                       

    def process_side_edge(self, x_previous: int, y_previous: int,
                                x_edge: int, y_edge: int, top, bottom):
        """
        Обработка бокового ребра
        """
        if x_edge != -1:
            self.screen_image.draw_line(x_edge, y_edge, x_previous, y_previous)
            self.horizont(x_edge, y_edge, x_previous, y_previous, top, bottom)
        x_edge = x_previous; y_edge = y_previous
        return x_edge, y_edge

    def horizont(self, x1: int, y1: int,
                       x2: int, y2: int,
                       top: List[int], bottom: List[int]):
        """
        Заполнение массивов плавающего горизонта
        """
        if (x2 - x1) == 0:
            top[x2] = max(top[x2], y2)
            bottom[x2] = min(bottom[x2], y2)
        else:
            m = (y2 - y1) / (x2 - x1)
            for x in range(x1, x2 + 1):
                y = round(m * (x - x1) + y1)
                top[x] = max(top[x], y)
                bottom[x] = min(bottom[x], y)
        return      

    def visible(self, x: int, y: int, top: List[int], bottom: List[int]):
        """
        Определить видимость точки
        """    
        flag_visible_current_point = 0
        if y < top[x] and y > bottom[x]:
            flag_visible_current_point = 0
        elif y >= top[x]:
            flag_visible_current_point = 1
        elif y <= bottom[x]:
            flag_visible_current_point = -1

        return flag_visible_current_point

    def intersection(self, x1, y1, x2, y2, array):
        """
        Пересечение отрезков двух прямых
        """
        dx = x2 - x1
        if dx == 0:
            xi = x2
            yi = array[x2]
        elif y1 == array[x1] and y2 == array[x2]:
            xi = x2; yi = array[x2]
        else:
            dy_current = y2 - y1
            dy_previous = array[x2] - array[x1]
            m = dy_current / dx
            xi = x1 -int((dx * (y1 - array[x1]) / (dy_current - dy_previous)))
            yi = int(m * (xi - x1) + y1)

        return xi, yi

    def sign(self, x: int):
        flag_sign = 0
        if x < 0:
            flag_sign = -1
        elif x > 0:
            flag_sign = 1
        return flag_sign


    def tranform_to_2d(self, x: int, y: int, z: int,
                       angles: List[int]):
        """
        Проецирование координат
        """
        x, y = self.rotate_x(x, y, z, angles[0])
        x, y = self.rotate_y(x, y, z, angles[1])
        x, y = self.rotate_z(x, y, z, angles[2])
        return self.scale(x, y)

    def rotate_x(self, x: int, y: int, z: int, angle: int):
        angle_x = self.convert_degree_to_radian(angle)
        y = y * cos(angle_x) - z * sin(angle_x)
        return x, y

    def rotate_y(self, x: int, y: int, z: int, angle: int):
        angle_y = self.convert_degree_to_radian(angle)
        x = x * cos(angle_y) - z * sin(angle_y)
        return x, y

    def rotate_z(self, x: int, y: int, z: int, angle: int):
        angle_z = self.convert_degree_to_radian(angle)
        buffer_x = x

        x = cos(angle_z) * x - sin(angle_z) * y
        y = cos(angle_z) * y + sin(angle_z) * buffer_x
        return x, y

    def convert_degree_to_radian(self, angle):
        return pi / 180 * angle

    def scale(self, x, y):
        x *= 50; y *= 50
        x += self.screen_image.width() // 2; y += self.screen_image.height() // 2
        return int(x), int(y)



if __name__ == "__main__":  
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())