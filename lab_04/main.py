from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPolygon, QPainterPath, QMouseEvent, QColor
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QPushButton, QLabel, QGraphicsScene,\
                            QGraphicsView, QWidget, QMenu, QMainWindow, QAction, QColorDialog

import sys
import lab_04_ui, analyze
from math import sqrt, fabs, radians, cos, sin, pi

class GraphicsScene(QGraphicsScene):
    def __init__(self, edit_center_x_circle, edit_center_y_circle, ):
        super().__init__()
        self.setSceneRect(1, 1, 1500, 855)
        self.cursor_x = -100; self.cursor_y = -100
        self.last_cursor_x = 0; self.last_cursor_y = 0
        self.edit_center_x_circle = edit_center_x_circle
        self.edit_center_y_circle = edit_center_y_circle
        self.radius_point_click = 2


    def mousePressEvent(self, event):
        '''
        Нажатие мыши
        '''
        pen_white = QPen(Qt.white, 1, Qt.SolidLine)
        brush_white = QBrush(QtCore.Qt.white)
        self.last_cursor_x = self.cursor_x
        self.last_cursor_y = self.cursor_y
        self.addEllipse(self.last_cursor_x - self.radius_point_click, self.last_cursor_y - self.radius_point_click,
                        self.radius_point_click * 2, self.radius_point_click * 2,
                        pen_white, brush_white)

        pen_black = QPen(Qt.black, 1, Qt.SolidLine)
        brush_black = QBrush(QtCore.Qt.black)
        self.cursor_x = event.scenePos().x()
        self.cursor_y = event.scenePos().y()
        self.addEllipse(self.cursor_x - self.radius_point_click, self.cursor_y - self.radius_point_click,
                        self.radius_point_click * 2, self.radius_point_click * 2,
                        pen_black, brush_black)

        self.edit_center_x_circle.setText(str(int(self.cursor_x)))      
        self.edit_center_y_circle.setText(str(int(self.cursor_y)))

class Main_window(QMainWindow, lab_04_ui.Ui_MainWindow):
    def __init__(self):
        '''
        Конструктор
        '''
        super().__init__()
        self.setupUi(self)
        self.gs_circle = GraphicsScene(self.edit_center_x_circle, self.edit_center_y_circle)
        self.gs_ellipse = GraphicsScene(self.edit_center_x_ellipse, self.edit_center_y_ellipse)
        self.show()
        self.add_names_algorithms_circle()
        self.add_names_algorithms_ellipse()
        self.add_items_to_colour_circle()
        self.add_items_to_colour_ellipse()
        self.add_to_ui()
        self.set_first_values_to_edit_circle()
        self.set_first_values_to_edit_ellipse()
        self.add_functions_circle()
        self.add_functions_ellipse()
        self.center_x_circle = 0; self.center_y_circle = 0
        self.center_x_ellipse = 0; self.center_y_ellipse = 0
        self.radius_circle = 0; self.radius_ellipse = 0


    def add_to_ui(self):
        '''
        Добавление функционала к интерфейсу
        '''
        #Установить стартовую вкладку при открытии окна
        self.tabWidget.setCurrentIndex(0)

        self.graphview_circle.setScene(self.gs_circle)
        self.graphview_circle.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphview_circle.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.graphview_ellipse.setScene(self.gs_ellipse)
        self.graphview_ellipse.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphview_ellipse.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.pen = QPen(Qt.black, 1)

    def add_names_algorithms_circle(self):
        '''
        Добавление выбора алгоритма (окружность)
        '''
        self.box_algorithm_circle.addItem("Библиотечная функция")
        self.box_algorithm_circle.addItem("Каноническое уравнение")
        self.box_algorithm_circle.addItem("Параметрическое уравнение")
        self.box_algorithm_circle.addItem("Алгоритм Брезенхема")
        self.box_algorithm_circle.addItem("Алгоритм средней точки")

    def add_names_algorithms_ellipse(self):
        '''
        Добавление выбора алгоритма (эллипс)
        '''
        self.box_algorithm_ellipse.addItem("Библиотечная функция")
        self.box_algorithm_ellipse.addItem("Каноническое уравнение")
        self.box_algorithm_ellipse.addItem("Параметрическое уравнение")
        self.box_algorithm_ellipse.addItem("Алгоритм Брезенхема")
        self.box_algorithm_ellipse.addItem("Алгоритм средней точки")

    def add_items_to_colour_circle(self):
        '''
        Добавление выбора цвета (окружность)
        '''
        self.box_colour_circle.addItem("Черный")
        self.box_colour_circle.addItem("Белый")
        self.box_colour_circle.addItem("Красный")
        self.box_colour_circle.addItem("Оранжевый")
        self.box_colour_circle.addItem("Желтый")
        self.box_colour_circle.addItem("Зеленый")
        self.box_colour_circle.addItem("Синий")
        self.box_colour_circle.addItem("Фиолетовый")

    def add_items_to_colour_ellipse(self):
        '''
        Добавление выбора цвета (эллипс)
        '''
        self.box_colour_ellipse.addItem("Черный")
        self.box_colour_ellipse.addItem("Белый")
        self.box_colour_ellipse.addItem("Красный")
        self.box_colour_ellipse.addItem("Оранжевый")
        self.box_colour_ellipse.addItem("Желтый")
        self.box_colour_ellipse.addItem("Зеленый")
        self.box_colour_ellipse.addItem("Синий")
        self.box_colour_ellipse.addItem("Фиолетовый")

    def draw_point_circle(self, x, y, pen):
        '''
        Отрисовка точки (окружность)
        '''
        self.gs_circle.addLine(x, y, x, y, pen)

    def draw_point_ellipse(self, x, y, pen):
        '''
        Отрисовка точки (эллипс)
        '''
        self.gs_ellipse.addLine(x, y, x, y, pen)

    def choose_colour_pen(self, colour):
        '''
        Выбор цвета отрисовки
        '''
        if colour == 'Черный':
            self.pen.setColor(Qt.black)
        elif colour == 'Белый':
            self.pen.setColor(Qt.white)
        elif colour == 'Красный':
            self.pen.setColor(Qt.red)
        elif colour == 'Оранжевый':
            self.pen.setColor(QColor(255,140,0))
        elif colour == 'Желтый':
            self.pen.setColor(Qt.darkYellow)
        elif colour == 'Синий':
            self.pen.setColor(Qt.darkBlue)
        elif colour == 'Зеленый':
            self.pen.setColor(Qt.darkGreen)
        elif colour == 'Фиолетовый':
            self.pen.setColor(Qt.darkMagenta)

    def set_first_values_to_edit_circle(self):
        '''
        Установить начальные значения в поля ввода (окружность)
        '''
        self.edit_center_x_circle.setText("0")
        self.edit_center_y_circle.setText("0")
        self.edit_radius_circle.setText("0")
        self.edit_start_radius_circle.setText("0")
        self.edit_end_radius_circle.setText("0")
        self.edit_step_change_circle.setText("0")
        self.edit_count_circle.setText("0")
    
    def set_first_values_to_edit_ellipse(self):
        '''
        Установить начальные значения в поля ввода (эллипс)
        '''
        self.edit_center_x_ellipse.setText("0")
        self.edit_center_y_ellipse.setText("0")
        self.edit_halfaxis_big_ellipse.setText("0")
        self.edit_halfaxis_low_ellipse.setText("0")
        self.edit_step_change_big_halfaxis.setText("0")
        self.edit_step_change_low_halfaxis.setText("0")
        self.edit_count_ellipses.setText("0")   

    def add_functions_circle(self):
        '''
        Функции, выполняемые при нажатии кнопок (окружность)
        '''
        self.but_create_circle.clicked.connect(lambda: self.build_circle())
        self.but_create_spectrum_circle.clicked.connect(lambda: self.build_spectrum_circle(0, None))
        self.analyze_circle_time.triggered.connect(lambda: self.analyze_time_spectrum_circle())
        self.but_clear_circle.clicked.connect(self.gs_circle.clear)

    def add_functions_ellipse(self):
        '''
        Функции, выполняемые при нажатии кнопок (эллипс)
        '''
        self.but_create_ellipse.clicked.connect(lambda: self.build_ellipse())
        self.but_create_spectrum_ellipse.clicked.connect(lambda: self.build_spectrum_ellipse(0, None))
        self.analyze_ellipse_time.triggered.connect(lambda: self.analyze_time_spectrum_ellipse())
        self.but_clear_ellipse.clicked.connect(self.gs_ellipse.clear)

    def build_circle(self):
        '''
        Определение метода построения окружности
        '''
        select_algorithm = self.box_algorithm_circle.currentText()
        select_colour = self.box_colour_circle.currentText()
        try:
            center_x_circle = int(self.edit_center_x_circle.text())
            center_y_circle = int(self.edit_center_y_circle.text())
            radius_circle = int(self.edit_radius_circle.text())
            if radius_circle <= 0:
                raise ValueError     
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неверные входные данные")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            self.choose_colour_pen(select_colour)
            self.choose_method_circle(center_x_circle, center_y_circle, radius_circle,
                                select_algorithm, select_colour)

    def build_ellipse(self):
        '''
        Определение метода построения окружности
        '''
        select_algorithm = self.box_algorithm_ellipse.currentText()
        select_colour = self.box_colour_ellipse.currentText()
        try:
            center_x_ellipse = int(self.edit_center_x_ellipse.text())
            center_y_ellipse = int(self.edit_center_y_ellipse.text())
            big_halfaxis_ellipse = int(self.edit_halfaxis_big_ellipse.text())
            low_halfaxis_ellipse = int(self.edit_halfaxis_low_ellipse.text())
            if big_halfaxis_ellipse <= 0 or low_halfaxis_ellipse <= 0:
                raise ValueError     
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неверные входные данные")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            self.choose_colour_pen(select_colour)
            self.choose_method_ellipse(center_x_ellipse, center_y_ellipse, big_halfaxis_ellipse,
                                low_halfaxis_ellipse, select_algorithm, select_colour)
    
    def choose_method_circle(self, center_x, center_y, radius, select_algorithm, select_colour):
        '''
        Выбор метода построения (окружность)
        '''
        if select_algorithm == 'Библиотечная функция':
            self.draw_circle_library(center_x, center_y, radius)
        elif select_algorithm == 'Каноническое уравнение':
            self.create_circle_by_canonical_equation(center_x, center_y, radius)                                                 
        elif select_algorithm == 'Параметрическое уравнение':
            self.create_circle_by_parametric_equation(center_x, center_y, radius)
        elif select_algorithm == 'Алгоритм Брезенхема':
            self.create_circle_by_brezenhem_algorithm(center_x, center_y, radius)
        elif select_algorithm == 'Алгоритм средней точки':
            self.create_circle_by_middle_point_method(center_x, center_y, radius)

    def choose_method_ellipse(self, center_x, center_y, big_halfaxis, low_halfaxis, select_algorithm, select_colour):
        '''
        Выбор метода построения (эллипс)
        '''
        if select_algorithm == 'Библиотечная функция':
            self.draw_ellipse_library(center_x, center_y, low_halfaxis, big_halfaxis)
        elif select_algorithm == 'Каноническое уравнение':
            self.create_ellipse_by_canonical_equation(center_x, center_y, low_halfaxis, big_halfaxis)                                                 
        elif select_algorithm == 'Параметрическое уравнение':
            self.create_ellipse_by_parametric_equation(center_x, center_y, low_halfaxis, big_halfaxis)
        elif select_algorithm == 'Алгоритм Брезенхема':
            self.create_ellipse_by_brezenhem_algorithm(center_x, center_y, low_halfaxis, big_halfaxis)
        elif select_algorithm == 'Алгоритм средней точки':
            self.create_ellipse_by_middle_point_method(center_x, center_y, low_halfaxis, big_halfaxis)

    def draw_circle_library(self, center_x, center_y, radius):
        '''
        Библиотечная функция (окружность)
        '''
        rect = QtCore.QRectF(center_x - radius, center_y - radius, radius * 2, radius * 2)
        self.gs_circle.addEllipse(rect, self.pen)

    def draw_ellipse_library(self, center_x, center_y, low_halfaxis, big_halfaxis):
        '''
        Библиотечная функция (эллипс)
        '''
        rect = QtCore.QRectF(center_x - big_halfaxis, center_y - low_halfaxis, big_halfaxis * 2, low_halfaxis * 2)
        self.gs_ellipse.addEllipse(rect, self.pen)

    def create_circle_by_canonical_equation(self, center_x, center_y, radius):
        '''
        Каноническое уравнение (окружность)
        '''
        x = 0; y = 0
        sqr_r = radius * radius
        limit = radius / sqrt(2)
        while x <= limit:
            y = sqrt(sqr_r - x * x)
            self.draw_point_circle(center_x + x, center_y + y, self.pen)
            self.draw_point_circle(center_x + x, center_y - y, self.pen)
            self.draw_point_circle(center_x - x, center_y + y, self.pen)
            self.draw_point_circle(center_x - x, center_y - y, self.pen)

            self.draw_point_circle(center_x + y, center_y - x, self.pen)
            self.draw_point_circle(center_x + y, center_y + x, self.pen)
            self.draw_point_circle(center_x - y, center_y - x, self.pen)
            self.draw_point_circle(center_x - y, center_y + x, self.pen)

            x += 1

    def create_ellipse_by_canonical_equation(self, center_x, center_y, low_halfaxis, big_halfaxis):
        '''
        Каноническое уравнение (эллипс)
        '''
        x = 0; y = 0
        a = big_halfaxis * big_halfaxis
        b = low_halfaxis * low_halfaxis
        limit_x = big_halfaxis
        limit_y = low_halfaxis
        while x <= limit_x:
            y = low_halfaxis * sqrt(1 - x * x / a)
            self.draw_point_ellipse(center_x + x, center_y + y, self.pen)
            self.draw_point_ellipse(center_x + x, center_y - y, self.pen)
            self.draw_point_ellipse(center_x - x, center_y + y, self.pen)
            self.draw_point_ellipse(center_x - x, center_y - y, self.pen)

            x += 1

        while y <= limit_y:
            x = big_halfaxis * sqrt(1 - y * y / b)
            self.draw_point_ellipse(center_x + x, center_y + y, self.pen)
            self.draw_point_ellipse(center_x + x, center_y - y, self.pen)
            self.draw_point_ellipse(center_x - x, center_y + y, self.pen)
            self.draw_point_ellipse(center_x - x, center_y - y, self.pen)

            y += 1

        

    def create_circle_by_parametric_equation(self, center_x, center_y, radius):
        '''
        Параметрическое уравнение (окружность)
        '''
        R = radius
        x = 0; y = 0
        t = 0
        limit = pi / 4
        step_t = 1 / R
        while t <= limit:
            x = R * cos(t)
            y = R * sin(t)
            self.draw_point_circle(center_x + x, center_y + y, self.pen)
            self.draw_point_circle(center_x + x, center_y - y, self.pen)
            self.draw_point_circle(center_x - x, center_y + y, self.pen)
            self.draw_point_circle(center_x - x, center_y - y, self.pen)

            self.draw_point_circle(center_x + y, center_y + x, self.pen)
            self.draw_point_circle(center_x + y, center_y - x, self.pen)
            self.draw_point_circle(center_x - y, center_y + x, self.pen)
            self.draw_point_circle(center_x - y, center_y - x, self.pen)

            t += step_t

    def create_ellipse_by_parametric_equation(self, center_x, center_y, low_halfaxis, big_halfaxis):
        '''
        Параметрическое уравнение (эллипс)
        '''
        a = big_halfaxis; b = low_halfaxis
        x = 0; y = 0
        t = 0
        limit = pi / 2
        step_t = 1 / big_halfaxis
        while t <= limit:
            x = a * cos(t)
            y = b * sin(t)
            self.draw_point_ellipse(center_x + x, center_y + y, self.pen)
            self.draw_point_ellipse(center_x + x, center_y - y, self.pen)
            self.draw_point_ellipse(center_x - x, center_y + y, self.pen)
            self.draw_point_ellipse(center_x - x, center_y - y, self.pen)

            t += step_t

    def create_ellipse_by_brezenhem_algorithm(self, center_x, center_y, low_halfaxis, big_halfaxis):
        '''
        Алгоритм Брезенхема построения эллипса
        '''
        x = 0; y = low_halfaxis
        b = big_halfaxis * big_halfaxis
        delta_i = round(low_halfaxis * low_halfaxis / 2 - big_halfaxis * low_halfaxis / 2 +
                        big_halfaxis * big_halfaxis / 2)
        a = low_halfaxis * low_halfaxis
        sum_a_b = a + b
        while y >= 0:
            self.draw_point_ellipse(center_x + x, center_y + y, self.pen)
            self.draw_point_ellipse(center_x + x, center_y - y, self.pen)

            self.draw_point_ellipse(center_x - x, center_y + y, self.pen)
            self.draw_point_ellipse(center_x - x, center_y - y, self.pen)
            if delta_i < 0:
                d1 = 2 * (delta_i + b * y) - b
                if d1 < 0:
                    #горизонтальный шаг
                    x += 1
                    delta_i += 2 * x * a + a
                else:
                    #диагональный шаг
                    x += 1
                    y -= 1
                    delta_i = delta_i + 2 * (x * a - y * b) + sum_a_b
            elif delta_i == 0:
                # диагональный шаг
                x += 1
                y -= 1
                delta_i = delta_i + 2 * (x * a - y * b) + sum_a_b
            elif delta_i > 0:
                d2 = 2 * (delta_i - a * x) - a
                if d2 <= 0:
                    #диагональный шаг
                    x += 1
                    y -= 1
                    delta_i = delta_i + 2 * (x * a - y * b) + sum_a_b
                else:
                    #вертикальный шаг
                    y -= 1
                    delta_i = delta_i - 2 * y * b + b

    def create_circle_by_brezenhem_algorithm(self, center_x, center_y, radius):
        '''
        Алгоритм Брезенхема построения окружности
        '''
        x = 0; y = radius
        delta_i = 2 * (1 - radius)
        limit = round(radius / sqrt(2))
        while y >= limit:
            self.draw_point_circle(center_x + x, center_y + y, self.pen)
            self.draw_point_circle(center_x - x, center_y + y, self.pen)
            self.draw_point_circle(center_x + x, center_y - y, self.pen)
            self.draw_point_circle(center_x - x, center_y - y, self.pen)

            self.draw_point_circle(center_x + y, center_y + x, self.pen)
            self.draw_point_circle(center_x - y, center_y + x, self.pen)
            self.draw_point_circle(center_x + y, center_y - x, self.pen)
            self.draw_point_circle(center_x - y, center_y - x, self.pen)

            if delta_i < 0:
                #точка лежит внутри окружности
                d1 = 2 * delta_i + 2 * y - 1
                if d1 <= 0:
                    #горизонтальный шаг
                    x += 1
                    delta_i += 2 * x + 1
                else:
                    #диагональный шаг
                    x += 1
                    y -= 1
                    delta_i += 2 * (x - y + 1)
            elif delta_i >= 0:
                # диагональный шаг
                x += 1
                y -= 1
                delta_i = delta_i + 2 * (x - y + 1)

    def create_circle_by_middle_point_method(self, center_x, center_y, radius):
        '''
        Метод серединной точки (окружность)
        '''
        x = 0; y = radius
        delta_i = 1 - radius
        while x <= y:
            self.draw_point_circle(center_x + x, center_y + y, self.pen)
            self.draw_point_circle(center_x + x, center_y - y, self.pen)
            self.draw_point_circle(center_x - x, center_y + y, self.pen)
            self.draw_point_circle(center_x - x, center_y - y, self.pen)

            self.draw_point_circle(center_x + y, center_y + x, self.pen)
            self.draw_point_circle(center_x + y, center_y - x, self.pen)
            self.draw_point_circle(center_x - y, center_y + x, self.pen)
            self.draw_point_circle(center_x - y, center_y - x, self.pen)
            
            x += 1

            if delta_i < 0:
                delta_i += 2 * x + 1
            else:
                y -= 1
                delta_i += 2 * (x - y) + 1

    def create_ellipse_by_middle_point_method(self, center_x, center_y, low_halfaxis, big_halfaxis):
        '''
        Построение серединной точки (эллипс)
        '''
        x = 0; y = low_halfaxis
        a_sqr = big_halfaxis * big_halfaxis
        b_sqr = low_halfaxis * low_halfaxis

        #tg < -1 начальное значение пробной функции
        f_prob = b_sqr - a_sqr * (low_halfaxis - 0.25)

        #тангенс угла наклона меньше -1
        while b_sqr * x <= a_sqr * y:
            self.draw_point_ellipse(center_x + x, center_y + y, self.pen)
            self.draw_point_ellipse(center_x + x, center_y - y, self.pen)
            self.draw_point_ellipse(center_x - x, center_y + y, self.pen)
            self.draw_point_ellipse(center_x - x, center_y - y, self.pen)

            x += 1
            #если средняя точка внутри эллипса (ближе верхний пиксел) - горизонтальный шаг
            if f_prob < 0:
                f_prob += b_sqr * (2 * x + 1)
            #если средняя точка вне эллипса (диагональный пиксель) - диагональный шаг
            else:
                y -= 1
                f_prob += b_sqr * (2 * x + 1) - 2 * a_sqr * y

        #tg > -1 начальное значение параметра в точке (x + 0.5, y - 1) последнего положения
        f_prob = b_sqr * ((x + 0.5) ** 2 - a_sqr) + a_sqr * ((y - 1) ** 2)

        while y >= 0:
            self.draw_point_ellipse(center_x + x, center_y + y, self.pen)
            self.draw_point_ellipse(center_x + x, center_y - y, self.pen)
            self.draw_point_ellipse(center_x - x, center_y + y, self.pen)
            self.draw_point_ellipse(center_x - x, center_y - y, self.pen)

            y -= 1
            if f_prob > 0:
                f_prob -= a_sqr * (2 * y + 1)
            else:
                x += 1
                f_prob += 2 * (b_sqr * x - a_sqr * y) + a_sqr

    def build_spectrum_circle(self, table_flag, analyze_time):
        '''
        Построение спектра окружностей
        '''
        select_algorithm = self.box_algorithm_circle.currentText()
        select_colour = self.box_colour_circle.currentText()
        r_start = 0; r_step = 0; r_end = 0
        try:
            center_x_circle = int(self.edit_center_x_circle.text())
            center_y_circle = int(self.edit_center_y_circle.text())
            radius_start = int(self.edit_start_radius_circle.text())
            step = int(self.edit_step_change_circle.text())
            if radius_start <= 0 or step <= 0:
                raise ValueError
            if self.radiobut_end_radius.isChecked():
                radius_end = int(self.edit_end_radius_circle.text())
                if radius_end <= 0 or radius_end <= radius_start:
                    raise ValueError
            elif self.radiobut_count_circles.isChecked():
                count_circles = int(self.edit_count_circle.text())
                if count_circles <= 0:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неверные входные данные")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            if table_flag == 0:
                #Заданы R0, Rk, шаг
                self.choose_colour_pen(select_colour)
                if self.radiobut_end_radius.isChecked():
                    #выбрали конечный радиус
                    for radius in range(radius_start, radius_end + 1, step):
                        self.choose_method_circle(center_x_circle, center_y_circle, radius, select_algorithm,
                                                    select_colour)
                elif self.radiobut_count_circles.isChecked():
                    #выбрали количество окружностей
                    radius = radius_start
                    for i in range(1, count_circles + 1):
                        self.choose_method_circle(center_x_circle, center_y_circle, radius, select_algorithm,
                                                    select_colour)
                        radius += step
            else:
                #Заданы R0, Rk, шаг
                if self.radiobut_end_radius.isChecked():
                    #для отрисовки графика
                    r_start = radius_start; r_step = step; r_end = radius_end
                    #выбрали конечный радиус
                    for radius in range(radius_start, radius_end + 1, step):
                        cur_analyze_time = []
                        cur_analyze_time = analyze.analyze_choose_method_circle(radius, cur_analyze_time)
                        analyze_time.append(cur_analyze_time)
                elif self.radiobut_count_circles.isChecked():
                    #выбрали количество окружностей
                    radius = radius_start
                    r_start = radius_start; r_step = step; r_end = radius_start + count_circles * step
                    for i in range(1, count_circles + 1):
                        cur_analyze_time = []
                        cur_analyze_time = analyze.analyze_choose_method_circle(radius, cur_analyze_time)
                        analyze_time.append(cur_analyze_time)
                        radius += step
        return analyze_time, r_start, r_step, r_end

    def build_spectrum_ellipse(self, table_flag, analyze_time):
        '''
        Построение спектра эллипсов
        '''
        select_algorithm = self.box_algorithm_ellipse.currentText()
        
        select_colour = self.box_colour_ellipse.currentText()
        try:
            center_x_ellipse = int(self.edit_center_x_ellipse.text())
            center_y_ellipse = int(self.edit_center_y_ellipse.text())
            count_ellipses = int(self.edit_count_ellipses.text())
            
            big_halfaxis_ellipse = int(self.edit_halfaxis_big_ellipse.text())
            low_halfaxis_ellipse = int(self.edit_halfaxis_low_ellipse.text())
            if big_halfaxis_ellipse <= 0 or low_halfaxis_ellipse <= 0 or count_ellipses <= 0:
                raise ValueError

            if self.radiobut_big_halfaxis.isChecked():
                step_big_halfaxis_ellipse = int(self.edit_step_change_big_halfaxis.text())
                if step_big_halfaxis_ellipse <= 0:
                    raise ValueError 
            elif self.radiobut_low_halfaxis.isChecked():
                step_low_halfaxis_ellipse = int(self.edit_step_change_low_halfaxis.text())
                if step_low_halfaxis_ellipse <= 0:
                    raise ValueError
            else:
                raise ValueError  
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неверные входные данные")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            r_start = 0; r_step = 0; r_end = 0
            if table_flag == 0:
                #Заданы центр, полуоси
                self.choose_colour_pen(select_colour)
                if self.radiobut_big_halfaxis.isChecked():
                    #выбрали шаг изменения большой полуоси
                    for i in range(1, count_ellipses + 1):
                        self.choose_method_ellipse(center_x_ellipse, center_y_ellipse, big_halfaxis_ellipse, low_halfaxis_ellipse,
                                                select_algorithm, select_colour)
                        big_halfaxis_ellipse += step_big_halfaxis_ellipse
                elif self.radiobut_low_halfaxis.isChecked():
                    #выбрали шаг изменения малой полуоси
                    for i in range(1, count_ellipses + 1):
                        self.choose_method_ellipse(center_x_ellipse, center_y_ellipse, big_halfaxis_ellipse, low_halfaxis_ellipse,
                                                    select_algorithm, select_colour)
                        low_halfaxis_ellipse += step_low_halfaxis_ellipse
            else:
                #Заданы центр, полуоси  
                if self.radiobut_big_halfaxis.isChecked():
                    r_start = big_halfaxis_ellipse; r_step = step_big_halfaxis_ellipse
                    r_end = r_start + count_ellipses * r_step
                    #выбрали шаг изменения большой полуоси
                    for i in range(1, count_ellipses + 1):
                        cur_analyze_time = []
                        cur_analyze_time = analyze.analyze_choose_method_ellipse(center_x_ellipse, center_y_ellipse,
                                                    big_halfaxis_ellipse, low_halfaxis_ellipse,
                                                    cur_analyze_time)
                        analyze_time.append(cur_analyze_time)
                        big_halfaxis_ellipse += step_big_halfaxis_ellipse
                elif self.radiobut_low_halfaxis.isChecked():
                    #выбрали шаг изменения малой полуоси
                    r_start = low_halfaxis_ellipse; r_step = step_low_halfaxis_ellipse
                    r_end = r_start + count_ellipses * r_step
                    for i in range(1, count_ellipses + 1):
                        cur_analyze_time = []
                        cur_analyze_time = analyze.analyze_choose_method_ellipse(center_x_ellipse, center_y_ellipse,
                                                    big_halfaxis_ellipse, low_halfaxis_ellipse,
                                                    cur_analyze_time)
                        analyze_time.append(cur_analyze_time)
                        low_halfaxis_ellipse += step_low_halfaxis_ellipse

        return analyze_time, r_start, r_step, r_end
            

    def analyze_time_spectrum_circle(self):
        analyze_time_circle = []
        analyze_time_circle, r_start, r_step, r_end = self.build_spectrum_circle(1, analyze_time_circle)  
        if analyze_time_circle != []:
            analyze.output_analyze_time(analyze_time_circle, r_start, r_step, r_end)
        

    def analyze_time_spectrum_ellipse(self):
        analyze_time_ellipse = []
        analyze_time_ellipse, r_start, r_step, r_end = self.build_spectrum_ellipse(1, analyze_time_ellipse)
        if analyze_time_ellipse != None:
            analyze.output_analyze_time(analyze_time_ellipse, r_start, r_step, r_end)


if __name__ == "__main__":
    #создание окна
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()

    #показ и нормальное завершение окна
    sys.exit(app.exec_())