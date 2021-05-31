from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QPalette, QColor
from PyQt5.QtCore import QCoreApplication, QEventLoop, Qt, QRectF, QPointF, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QGraphicsScene

import lab_09_ui
#from main import MainWindow

COLOUR_SEGMENT = '#ffa500'
COLOUR_CUT_OFF = '#56de47'
COLOUR_RESULT = '#0079db'
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

class ScreenImage(QGraphicsScene, QMainWindow, lab_09_ui.Ui_MainWindow):
    '''
    Класс для отрисовки
    '''
    #сигналы для плавной отрисовки прямоугольника
    clicked = pyqtSignal(QPointF)
    released = pyqtSignal(QPointF)
    moved = pyqtSignal(QPointF)

    def __init__(self, input_polygon, cut_off_polygon):
        '''
        Конструктор
        '''
        super().__init__()
        self.cursor_x = 0; self.cursor_y = 0

        self.input_polygon = input_polygon
        self.cut_off_polygon = cut_off_polygon

        self.count_segments = -1
        self.count_segments_cut_off = -1

        self.count_points = 0
        self.count_points_cut_off = 0

        self.flag_input_cut_off = False
        self.flag_input_polygon = False
        self.flag_pressed_shift = False

        self.flag_locked_cut_off = False
        self.flag_locked_input_polygon = False

        self.pen_graph = QPen(QColor(COLOUR_SEGMENT), 1, Qt.SolidLine)
        self.pen_cut_off = QPen(QColor(COLOUR_CUT_OFF))
        self.pen_result = QPen(QColor(COLOUR_RESULT))
        self.clear_pen = QPen(Qt.white, 1, Qt.SolidLine)
        self.clear_brush = QBrush(Qt.white)

    def mousePressEvent(self, event):
        '''
        Обработка нажатия мыши
        '''
        if event.button() == Qt.LeftButton:
            if self.flag_input_cut_off == False:
                if self.flag_input_polygon == True:
                    self.count_segments, self.count_points = self.input_segments_on_screen(event, self.input_polygon,
                                                            self.count_segments, self.count_points, self.pen_graph)                    
            elif self.flag_input_cut_off == True:
                self.input_cut_off_on_screen(event)
        if event.button() == Qt.RightButton:
            print(f"self.flag_input_polygon = {self.flag_input_polygon}")
            print(f"here")
            if self.flag_input_polygon == True:
                self.flag_locked_input_polygon = self.lock_cut_off(self.input_polygon, self.count_points, self.pen_graph)
            elif self.flag_input_cut_off == True:
                self.flag_locked_cut_off = self.lock_cut_off(self.cut_off_polygon,
                                                            self.count_points_cut_off, self.pen_cut_off)

    def input_segments_on_screen(self, event, input_polygon, count_segments, count_points, screen_pen):
        """
        Ввод отрезков на экране
        """
        #ввод линий
        self.cursor_x = int(event.scenePos().x())
        self.cursor_y = int(event.scenePos().y())

        '''if self.flag_input_segments == True and (segments == [] or len(segments[count_segments]) % 2 == 0):
            segments.append([])
            count_segments += 1
            count_points = 0
        elif''' 
        #self.flag_input_cut_off:
        count_segments += 1

        if self.flag_pressed_shift == False:
            input_polygon.append([self.cursor_x, self.cursor_y])

        if count_points >= 1:
            if self.flag_pressed_shift == True:
                #анализ горизонтальной и вертикальной линии
                dx = abs(self.cursor_x - input_polygon[count_segments][-1][0])
                dy = abs(self.cursor_y - input_polygon[count_segments][-1][1])
                if dx < dy:
                    #рисуем горизонтальную линию
                    input_polygon[count_segments].append([input_polygon[count_segments][-1][0], self.cursor_y])
                    self.addLine(input_polygon[count_segments][-2][0], input_polygon[count_segments][-2][1],
                                input_polygon[count_segments][-1][0], input_polygon[count_segments][-1][1],
                                screen_pen)
                    
                else:
                    #рисуем вертикальную линию
                    input_polygon[count_segments].append([self.cursor_x, input_polygon[count_segments][-1][1]])
                    self.addLine(input_polygon[count_segments][-2][0], input_polygon[count_segments][-2][1],
                                input_polygon[count_segments][-1][0], input_polygon[count_segments][-1][1], 
                                screen_pen)
                self.flag_pressed_shift = False  
            else:
                self.addLine(input_polygon[count_points - 1][0], input_polygon[count_points - 1][1],
                            input_polygon[count_points][0], input_polygon[count_points][1],
                            screen_pen)
        count_points += 1
        return count_segments, count_points

    def input_cut_off_on_screen(self, event) -> None:
        """
        Ввод отсекателя на экран
        """
        self.count_segments_cut_off, self.count_points_cut_off = self.input_segments_on_screen(event, 
                                                    self.cut_off_polygon, self.count_segments_cut_off,
                                                    self.count_points_cut_off, self.pen_cut_off)

    def lock_cut_off(self, polygon, count_points, pen_graph) -> bool:
        """
        Замкнуть многоугольник
        """
        flag_is_locked_polygon = False
        if count_points >= 2:
            self.addLine(polygon[-1][0], polygon[-1][1],
                         polygon[0][0], polygon[0][1], pen_graph)
            flag_is_locked_polygon = True
        return flag_is_locked_polygon

    def is_polygon_convex(self) -> bool:
        """
        Проверка многоугольника на выпуклость
        """
        flag_is_convex = True
        first_vector = self.get_coordinates_vector(self.cut_off_polygon[-1], self.cut_off_polygon[0])
        second_vector = self.get_coordinates_vector(self.cut_off_polygon[0], self.cut_off_polygon[1])
        sign_mul_vectors = self.compulate_sign_mul_vectors(first_vector, second_vector)

        if self.flag_locked_cut_off == True:
            for i in range(len(self.cut_off_polygon) - 2):
                first_vector = self.get_coordinates_vector(self.cut_off_polygon[i], self.cut_off_polygon[i + 1])
                second_vector = self.get_coordinates_vector(self.cut_off_polygon[i + 1], self.cut_off_polygon[i + 2])
                current_sign_mul_vectors = self.compulate_sign_mul_vectors(first_vector, second_vector)
                #если вект. произв. имеют разный знак или одно из них ноль
                if current_sign_mul_vectors * sign_mul_vectors <= 0:
                    flag_is_convex = False
                    break

        if flag_is_convex == True:
            first_vector = self.get_coordinates_vector(self.cut_off_polygon[i - 1], self.cut_off_polygon[i])
            second_vector = self.get_coordinates_vector(self.cut_off_polygon[i], self.cut_off_polygon[0])
            if current_sign_mul_vectors * sign_mul_vectors <= 0:
                flag_is_convex = False

        return flag_is_convex

    def get_coordinates_vector(self, point_1, point_2):
        """
        Получить координаты вектора
        """
        return [point_2[0] - point_1[0], point_2[1] - point_1[1]]

    def compulate_sign_mul_vectors(self, first_vector, second_vector):
        """
        Вычислить векторное произведение и вернуть его знак
        """
        angle = first_vector[0] * second_vector[1] - first_vector[1] * second_vector[0]
        return angle

    def keyPressEvent(self, event):
        '''
        Обработка событий нажатия клавиш
        '''
        if event.key() == QtCore.Qt.Key_Shift:
            if not (self.input_polygon == [] or len(self.input_polygon[self.count_segments]) % 2 == 0):
                self.flag_pressed_shift = True