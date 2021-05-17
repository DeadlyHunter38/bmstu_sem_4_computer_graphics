from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QPalette, QColor
from PyQt5.QtCore import QCoreApplication, QEventLoop, Qt, QRectF, QPointF, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QGraphicsScene

import lab_08_ui
#from main import MainWindow

COLOUR_SEGMENT = '#ffa500'
COLOUR_CUT_OFF = '#56de47'
COLOUR_RESULT = '#0079db'
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

class ScreenImage(QGraphicsScene, QMainWindow, lab_08_ui.Ui_MainWindow):
    '''
    Класс для отрисовки
    '''
    #сигналы для плавной отрисовки прямоугольника
    clicked = pyqtSignal(QPointF)
    released = pyqtSignal(QPointF)
    moved = pyqtSignal(QPointF)

    def __init__(self, segments, cut_off_segments):
        '''
        Конструктор
        '''
        super().__init__()
        print(f"here_constructor")
        self.cursor_x = 0; self.cursor_y = 0

        self.segments = segments
        self.cut_off_segments = cut_off_segments

        self.count_segments = -1
        self.count_segments_cut_off = -1

        self.count_points = 0
        self.count_points_cut_off = 0

        self.flag_input_cut_off = False
        self.flag_input_segments = False
        self.flag_pressed_shift = False
        self.rectangle = None
        self.rectangle_points = [0, 0, 0, 0]

        self.pen_graph = QPen(QColor(COLOUR_SEGMENT), 1, Qt.SolidLine)
        self.pen_cut_off = QPen(QColor(COLOUR_CUT_OFF))
        self.pen_result = QPen(QColor(COLOUR_RESULT))
        self.clear_pen = QPen(Qt.white, 1, Qt.SolidLine)
        self.clear_brush = QBrush(Qt.white)

    def mousePressEvent(self, event):
        '''
        Обработка нажатия мыши
        '''
        print(f"self.flag_input_cut_off = {self.flag_input_cut_off}")
        print(f"self.flag_input_segments = {self.flag_input_segments}")
        if event.button() == Qt.LeftButton:
            if self.flag_input_cut_off == False:
                if self.flag_input_segments == True:
                    self.count_segments, self.count_points = self.input_segments_on_screen(event, self.pen_graph, 
                                                    self.segments, self.count_segments, self.count_points)
            elif self.flag_input_cut_off == True:
                self.input_cut_off_on_screen(event)
        if event.button() == Qt.RightButton:
            self.lock_cut_off()

    def input_segments_on_screen(self, event, screen_pen, segments, count_segments, count_points):
        """
        Ввод отрезков на экране
        """
        #ввод линий
        print(f"segments = {segments}")
        self.cursor_x = int(event.scenePos().x())
        self.cursor_y = int(event.scenePos().y())

        if self.flag_input_segments == True and (segments == [] or len(segments[count_segments]) % 2 == 0):
            segments.append([])
            count_segments += 1
            count_points = 0
        elif self.flag_input_cut_off:
            count_segments += 1
        print(f"count_segments = {count_segments}")
        print(f"count_points = {count_points}")
        print(f"segments = {segments}")

        if self.flag_pressed_shift == False:
            if self.flag_input_segments == True:
                segments[count_segments].append([self.cursor_x, self.cursor_y])
                self.addLine(segments[count_segments][count_points][0], segments[count_segments][count_points][1],
                        segments[count_segments][count_points][0], segments[count_segments][count_points][1],
                        screen_pen)
            else:
                segments.append([self.cursor_x, self.cursor_y])
        print(f"segments = {segments}")

        if count_points >= 1:
            if self.flag_pressed_shift == True:
                #анализ горизонтальной и вертикальной линии
                dx = abs(self.cursor_x - segments[count_segments][-1][0])
                dy = abs(self.cursor_y - segments[count_segments][-1][1])
                if dx < dy:
                    #рисуем горизонтальную линию
                    segments[count_segments].append([segments[count_segments][-1][0], self.cursor_y])
                    self.addLine(segments[count_segments][-2][0], segments[count_segments][-2][1],
                                segments[count_segments][-1][0], segments[count_segments][-1][1],
                                screen_pen)
                    
                else:
                    #рисуем вертикальную линию
                    segments[count_segments].append([self.cursor_x, segments[count_segments][-1][1]])
                    self.addLine(segments[count_segments][-2][0], segments[count_segments][-2][1],
                                segments[count_segments][-1][0], segments[count_segments][-1][1], 
                                screen_pen)
                self.flag_pressed_shift = False  
            else:
                if self.flag_input_cut_off == False:
                    self.addLine(segments[count_segments][0][0], segments[count_segments][0][1],
                                segments[count_segments][1][0], segments[count_segments][1][1],
                                screen_pen)
                else:
                    print(f"count_points = {count_points}")
                    print(f"segments = {segments}")
                    self.addLine(segments[count_points - 1][0], segments[count_points - 1][1],
                                segments[count_points][0], segments[count_points][1],
                                screen_pen)
        count_points += 1
        return count_segments, count_points

    def input_cut_off_on_screen(self, event):
        """
        Ввод отсекателя на экран
        """
        self.count_segments_cut_off, self.count_points_cut_off = self.input_segments_on_screen(event, 
                                        self.pen_cut_off, self.cut_off_segments, self.count_segments_cut_off,
                                        self.count_points_cut_off)

    def lock_cut_off(self):
        """
        Замкнуть фигуру-отсекатель
        """
        if self.count_points_cut_off >= 2:
            self.addLine(self.cut_off_segments[-1][0], self.cut_off_segments[-1][1],
                         self.cut_off_segments[0][0], self.cut_off_segments[0][1],
                         self.pen_cut_off)

    def keyPressEvent(self, event):
        '''
        Обработка событий нажатия клавиш
        '''
        if event.key() == QtCore.Qt.Key_Shift:
            if not (self.segments == [] or len(self.segments[self.count_segments]) % 2 == 0):
                self.flag_pressed_shift = True