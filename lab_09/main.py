from typing import List
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QPalette, QColor, QImage
from PyQt5.QtCore import QCoreApplication, QEventLoop, Qt, QPointF, QRectF
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QGraphicsScene

from typing import List

import sys
import lab_09_ui
from screen_image import ScreenImage, COLOUR_CUT_OFF

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

        self.add_to_ui()
        self.add_functions()
        self.show()

    def add_to_ui(self):
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

    def add_functions(self):
        '''
        Добавление функционала к выполняемым задачам
        '''
        self.but_clean_all.clicked.connect(self.clean_screen)
        self.but_input_cut_off.clicked.connect(self.input_cut_off)
        self.but_cut_off.clicked.connect(self.do_cut_off)
        self.but_input_segments.clicked.connect(self.input_segments)

    def input_segments(self):
        """
        Ввод отрезков
        """
        self.but_input_segments.setStyleSheet("background-color: #ffffff")
        self.but_input_cut_off.setStyleSheet("background-color: #cccccc")
        self.graph.flag_input_segments = True
        self.graph.flag_input_cut_off = False

    def input_cut_off(self):
        """
        Ввод отсекателя
        """
        self.but_input_segments.setStyleSheet("background-color: #cccccc")
        self.but_input_cut_off.setStyleSheet("background-color: #ffffff")
        self.graph.flag_input_cut_off = True
        self.graph.flag_input_segments = False

    def clean_screen(self):
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
            result_polygon = self.do_cut_off_sutherland_hodgman()
    '''
    def do_cut_off_sutherland_hodgman(self):
        
        """
        Алгоритм Сазерленда-Ходжмана
        """
        result_polygon = []
        for i in range(len(self.graph.cut_off_segment)):
            polygon_point = self.graph.segment[0]
            if self.is_visible(polygon_point, self.graph.cut_off_segment[i], 
                            self.graph.cut_off_segment[i + 1], self.graph.cut_off_segment[i + 2]) == True:
                result_polygon.append(polygon_point)
            s = []
            for j in range(1, len()):


        return result_polygon
    '''

    def is_visible(self, polygon_point, cut_off_point_1, cut_off_point_2, cut_off_point_3) -> bool:
        """
        Определить видимость точки
        """
        flag_visible = True
        inner_normal = self.find_inner_normal(cut_off_point_1, cut_off_point_2, cut_off_point_3)
        vector = self.graph.get_coordinates_vector(cut_off_point_2, polygon_point)
        if self.find_scalar(inner_normal, vector) < 0:
            flag_visible = False
        return flag_visible
        

    def find_inner_normal(self, cut_off_point_1, cut_off_point_2, cut_off_point_3) -> list([int, int]):
        """
        Вычисление внутренней нормали вектора многоугольника (пропорционален текущему вектору отсекателя)
        """
        # нормаль > 0 - находится точка внутри отсекателя
        # нормаль < 0 - находится точка вне отсекателя
        inner_normal = [cut_off_point_2[1] - cut_off_point_1[1], cut_off_point_1[0] - cut_off_point_2[0]]
        vector_cut_off = self.graph.get_coordinates_vector(cut_off_point_2, cut_off_point_3)
        if self.find_scalar(inner_normal, vector_cut_off) < 0:
            inner_normal = [-inner_normal[0], -inner_normal[1]]
        return inner_normal

    def find_scalar(self, vector_1, vector_2):
        """
        Вычисление скалярного произведения векторов
        """
        return vector_1[0] * vector_2[0] + vector_1[1] * vector_2[1]



if __name__ == "__main__":  
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    sys.exit(app.exec_())