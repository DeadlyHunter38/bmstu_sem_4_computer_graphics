from copy import deepcopy
from typing import List
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QPalette, QColor, QImage
from PyQt5.QtCore import QCoreApplication, QEventLoop, Qt, QPointF, QRectF
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QGraphicsScene

from typing import List

import sys
import lab_09_ui
from screen_image import ScreenImage
from reference import DialogMenu

BG_COLOUR = Qt.white

class Main_window(QMainWindow, lab_09_ui.Ui_MainWindow):
    def __init__(self):
        '''
        Конструктор
        '''
        super().__init__()
        self.setupUi(self)
        self.segments = []
        self.cut_off_polygon = []
        self.graph = ScreenImage(self.segments, self.cut_off_polygon)
        self.menu = DialogMenu()

        self.add_to_ui()
        self.add_functions()
        self.show()

    def add_to_ui(self) -> None:
        '''
        Добавление функционала к интерфейсу
        '''
        self.graph.setSceneRect(0, 0, self.width(), self.height())
        self.graphicsView.setScene(self.graph)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.image = QImage(int(self.graph.width()), int(self.graph.height()), QImage.Format_ARGB32_Premultiplied)
        self.bg_colour = BG_COLOUR
        self.image.fill(self.bg_colour)

        self.menu_reference.triggered.connect(lambda: self.open_reference())

    def open_reference(self):
        reference_window = DialogMenu()
        reference_window.open_reference_window()

    def add_functions(self) -> None:
        '''
        Добавление функционала к выполняемым задачам
        '''
        self.but_clean_all.clicked.connect(self.clean_screen)
        self.but_input_cut_off.clicked.connect(self.input_cut_off)
        self.but_cut_off.clicked.connect(self.do_cut_off)
        self.but_input_segments.clicked.connect(self.input_segments)

    def input_segments(self) -> None:
        """
        Ввод отрезков
        """
        self.but_input_segments.setStyleSheet("background-color: #ffffff")
        self.but_input_cut_off.setStyleSheet("background-color: #cccccc")
        self.graph.flag_input_polygon = True
        self.graph.flag_input_cut_off = False

    def input_cut_off(self) -> None:
        """
        Ввод отсекателя
        """
        self.but_input_segments.setStyleSheet("background-color: #cccccc")
        self.but_input_cut_off.setStyleSheet("background-color: #ffffff")
        self.graph.flag_input_cut_off = True
        self.graph.flag_input_polygon = False

    def clean_screen(self) -> None:
        '''
        Очистка экрана
        '''
        self.graph.clear()
        self.graph.input_polygon.clear()
        self.graph.cut_off_polygon.clear()

        self.but_input_segments.setStyleSheet("background-color: #cccccc")
        self.but_input_cut_off.setStyleSheet("background-color: #cccccc")
        self.graph.count_segments = -1
        self.graph.count_points = 0

        self.graph.count_segments_cut_off = -1
        self.graph.count_points_cut_off = 0

        self.graph.cursor_x = 0; self.graph.cursor_y = 0
        self.graph.flag_input_cut_off = False
        self.graph.flag_locked_cut_off = False

        self.image = QImage(int(self.graph.width()), int(self.graph.height()), QImage.Format_ARGB32_Premultiplied)
        self.image.fill(self.bg_colour)

    def do_cut_off(self) -> None:
        """
        Отсечение выпуклым многоугольником
        """
        self.but_input_segments.setStyleSheet("background-color: #cccccc")
        self.but_input_cut_off.setStyleSheet("background-color: #cccccc")
        print(f"segments = {self.graph.input_polygon}")
        print(f"segments = {self.graph.cut_off_polygon}")
        pass
        if self.check_correctness_input() == True:
            polygon = self.graph.input_polygon
            cut_off_polygon = self.graph.cut_off_polygon
            result_polygon = self.do_cut_off_sutherland_hodgman(cut_off_polygon, polygon)
            self.draw_result_polygon(result_polygon, self.graph.pen_result)
            print(f"result_polygon = {result_polygon}")

    def check_correctness_input(self):
        """
        Проверка корректности исходных данных
        """
        flag_correctness = True
        flag_error = False
        text_error = ''
        print(f"self.graph.flag_locked_input_polygon = {self.graph.flag_locked_input_polygon}")
        print(f"self.graph.flag_locked_cut_off = {self.graph.flag_locked_cut_off}")
        if self.graph.input_polygon == [] or self.graph.flag_locked_input_polygon == False:
            text_error = "Исходный многоугольник не был введен."
            flag_error = True
        elif self.graph.flag_locked_cut_off == False:
            text_error = 'Отсекатель не был задан.'
            self.but_input_cut_off.setStyleSheet("background-color: #ffffff")
            flag_error = True
        elif self.graph.is_polygon_convex() == False:
            text_error = "Отсекатель не является выпуклым."
            self.but_input_cut_off.setStyleSheet("background-color: #ffffff")
            flag_error = True
        
        if flag_error == True:
            flag_correctness = False
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(text_error)
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        
        return flag_correctness
    
    def do_cut_off_sutherland_hodgman(self, cut_off_polygon, polygon):
        cut_off_polygon.append(cut_off_polygon[0])
        cut_off_polygon.append(cut_off_polygon[1])
        for i in range(len(cut_off_polygon) - 2):
            new = []
            first_point = polygon[0]
            if self.is_visible(first_point, cut_off_polygon[i], cut_off_polygon[i + 1], cut_off_polygon[i + 2]):
                new.append(first_point)
            s = polygon[0]
            for j in range(1, len(polygon)):
                t = self.is_intersection([s, polygon[j]], [cut_off_polygon[i],
                                                    cut_off_polygon[i + 1]], cut_off_polygon[i + 2])
                if t:
                    new.append(t)
                s = polygon[j]
                if self.is_visible(s, cut_off_polygon[i], cut_off_polygon[i + 1], cut_off_polygon[i + 2]):
                    new.append(s)

            if not len(new):
                return False
            t = self.is_intersection([s, first_point], [cut_off_polygon[i], cut_off_polygon[i + 1]], cut_off_polygon[i + 2])
            if t:
                new.append(t)
            polygon = deepcopy(new)
        return polygon

    def is_visible(self, point, cut_off_point_1, cut_off_point_2, cut_off_point_3):
        flag_visible = True
        inner_normal = self.find_inner_normal(cut_off_point_1, cut_off_point_2, cut_off_point_3)
        vector = self.graph.get_coordinates_vector(cut_off_point_2, point)
        if self.find_scalar(inner_normal, vector) < 0:
            flag_visible = False
        print(f"flag_visible = {flag_visible}")
        return flag_visible

    def find_inner_normal(self, cut_off_point_1, cut_off_point_2, point):
        """
        Вычисление внутренней нормали вектора многоугольника (пропорционален текущему вектору отсекателя)
        """
        # нормаль > 0 - находится точка внутри отсекателя
        # нормаль < 0 - находится точка вне отсекателя
        vector_cut_off = self.graph.get_coordinates_vector(cut_off_point_1, cut_off_point_2)
        inner_normal = [1, 0] if vector_cut_off[0] == 0 else [-vector_cut_off[1] / vector_cut_off[0], 1]
        vector_peak_point = self.graph.get_coordinates_vector(cut_off_point_2, point)
        if self.find_scalar(vector_peak_point, inner_normal) < 0:
            inner_normal = [-inner_normal[0], -inner_normal[1]]
        return inner_normal


    def find_directrise(self, point_1, point_2):
        """
        Нахождение директрисы отрезка (задает его направление)
        """
        return [point_2[0] - point_1[0], point_2[1] - point_1[1]]                            

    def find_w(self, point_segment_1, cut_off_segment):
        """
        Вычисление W
        """
        return [point_segment_1[0] - cut_off_segment[0], point_segment_1[1] - cut_off_segment[1]]

    def find_scalar(self, vector_1, vector_2):
        """
        Вычисление скалярного произведения векторов
        """
        return vector_1[0] * vector_2[0] + vector_1[1] * vector_2[1]

    def convert_to_parametric(self, point_1, point_2, t):
        """
        Перевод уравнение отрезка в параметрическое
        """
        def convert_axis(a,b,t):
            return a + (b - a) * t
        return list((
            convert_axis(point_1[0], point_2[0], t), 
            convert_axis(point_1[1], point_2[1], t)
        ))

    def is_intersection(self, edge_input, edge_cut_off, next_point_cut_off):
        visible_1 = self.is_visible(edge_input[0], edge_cut_off[0], edge_cut_off[1], next_point_cut_off)
        visible_2 = self.is_visible(edge_input[1], edge_cut_off[0], edge_cut_off[1], next_point_cut_off)
        if not (visible_1 ^ visible_2):
            return False
        inner_normal = self.find_inner_normal(edge_cut_off[0], edge_cut_off[1], next_point_cut_off)
        D = self.find_directrise(edge_input[0], edge_input[1])
        W = self.find_w(edge_input[0], edge_cut_off[0])
        D_scalar = self.find_scalar(D, inner_normal)
        W_scalar = self.find_scalar(W, inner_normal)
        t = -W_scalar / D_scalar

        param_point = self.convert_to_parametric(edge_input[0], edge_input[1], t)
        return param_point



    def draw_result_polygon(self, result_polygon, pen):
        """
        Отрисовка результата (многуогольник)
        """
        self.graph.addLine(result_polygon[-1][0], result_polygon[-1][1], result_polygon[0][0], result_polygon[0][1], pen)
        for i in range(len(result_polygon) - 1):
            self.graph.addLine(result_polygon[i][0], result_polygon[i][1],
                               result_polygon[i + 1][0], result_polygon[i + 1][1], pen)



if __name__ == "__main__":  
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    sys.exit(app.exec_())