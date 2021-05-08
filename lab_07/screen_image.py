from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QPalette, QColor
from PyQt5.QtCore import QCoreApplication, QEventLoop, Qt, QRectF, QPointF, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QGraphicsScene

import lab_07_ui
#from main import MainWindow

COLOUR_SEGMENT = '#ffa500'
COLOUR_CUT_OFF = '#56de47'
COLOUR_RESULT = '#0079db'
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

class ScreenImage(QGraphicsScene, QMainWindow, lab_07_ui.Ui_MainWindow):
    '''
    Класс для отрисовки
    '''
    #сигналы для плавной отрисовки прямоугольника
    clicked = pyqtSignal(QPointF)
    released = pyqtSignal(QPointF)
    moved = pyqtSignal(QPointF)

    def __init__(self, segments):
        super().__init__()
        self.cursor_x = 0; self.cursor_y = 0

        self.segments = segments
        self.count_segments = -1
        self.count_points = 0
        self.flag_input_cut_off = False
        self.rectangle = None
        self.rectangle_points = [0, 0, 0, 0]

        self.pen_graph = QPen(QColor(COLOUR_SEGMENT), 1, Qt.SolidLine)
        self.pen_cut_off = QPen(QColor(COLOUR_CUT_OFF))
        self.pen_result = QPen(QColor(COLOUR_RESULT))

    def mousePressEvent(self, event):
        '''
        Нажатие мыши
        '''
        if event.button() == Qt.LeftButton:
            if self.flag_input_cut_off == False:
                #ввод линий
                self.cursor_x = int(event.scenePos().x())
                self.cursor_y = int(event.scenePos().y())

                if self.segments == [] or len(self.segments[self.count_segments]) % 2 == 0:
                    self.segments.append([])
                    self.count_segments += 1
                    self.count_points = 0

                self.segments[self.count_segments].append([self.cursor_x, self.cursor_y])
                self.addLine(self.segments[self.count_segments][self.count_points][0], self.segments[self.count_segments][self.count_points][1],
                            self.segments[self.count_segments][self.count_points][0], self.segments[self.count_segments][self.count_points][1],
                            self.pen_graph)

                if self.count_points == 1:
                    self.addLine(self.segments[self.count_segments][0][0], self.segments[self.count_segments][0][1],
                                self.segments[self.count_segments][1][0], self.segments[self.count_segments][1][1],
                                self.pen_graph)
                self.count_points += 1
            else:
                #ввод отсекателя
                self.clicked.connect(self.point1)
                self.released.connect(self.point2)
                self.moved.connect(self.point2)

                if self.rectangle is not None:
                    self.removeItem(self.rectangle)

                cursor_position = event.scenePos()
                self.clicked.emit(cursor_position)
                super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        '''
        '''
        if self.flag_input_cut_off == True:
            cursor_position = event.scenePos()
            self.released.emit(cursor_position)
            super().mouseReleaseEvent(event)
            print(f"self.rectangle_points = {self.rectangle_points}")
            self.flag_input_cut_off = False
 
    def mouseMoveEvent(self, event):
        '''
        Отслеживание перемещения мыши
        '''
        if self.flag_input_cut_off == True:
            if event.buttons() == Qt.LeftButton:
                cursor_position = event.scenePos()
                self.moved.emit(cursor_position)
            super().mouseMoveEvent(event)

    def point1(self, p):
        '''
        Начало отслеживания первой вершины прямоугольника
        '''
        self.x = p.x()
        self.y = p.y()
        self.rectangle = self.addRect(QRectF(QPointF(self.x, self.y), 
                                             QPointF(self.x, self.y)),
                                             self.pen_cut_off)
 
    def point2(self, p):
        '''
        Отрисовка текущего прямоугольника
        '''
        self.rectangle_points[0] = min(self.x, p.x())
        self.rectangle_points[1] = min(self.y, p.y())
        self.rectangle_points[2] = max(self.x, p.x())
        self.rectangle_points[3] = max(self.y, p.y())
        self.rectangle.setRect(QRectF(QPointF(self.rectangle_points[0], self.rectangle_points[1]), 
                                      QPointF(self.rectangle_points[2], self.rectangle_points[3])))
