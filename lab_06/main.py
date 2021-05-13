from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QPolygon, QPainterPath, QMouseEvent, QColor, QImage
from PyQt5.QtCore import QCoreApplication, QEventLoop, QPoint, QPointF, Qt
from PyQt5.QtWidgets import QGraphicsItem, QMessageBox, QLineEdit, QPushButton, QLabel, QGraphicsScene,\
                            QGraphicsView, QWidget, QMenu, QMainWindow, QAction, QColorDialog, QApplication
import matplotlib.colors as colors
from PIL import ImageColor
from copy import copy, deepcopy
from time import time

import sys
import lab_06_ui
from stack import stack_class

ZERO_COLOUR = Qt.white
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080

class GraphicsScene(QGraphicsScene, lab_06_ui.Ui_MainWindow):
    def __init__(self, polygons, choose_colour):
        '''
        Конструктор
        '''
        super().__init__()
        self.cursor_x = 0; self.cursor_y = 0
        self.flag_pressed_shift = False
        self.flag_fill_outline = False
        self.flag_choose_seed_point = False
        self.seed_point = [0, 0]
        self.count_points = 0
        self.count_polygons = 0
        self.radius_point_click = 1
        self.polygons = polygons
        self.choose_colour_graph = choose_colour
        self.pen_graph = QPen(QColor(self.choose_colour_graph), 1, Qt.SolidLine)
        self.clean_pen = QPen(Qt.white, 1, Qt.SolidLine)

        self.count_locked_polygons = 0

    
    def getPixelColor(self, x: int, y:int):
        '''
        Получить цвет пикселя
        '''
        return QColor(self.image.pixel(x,y)).name()

    def mousePressEvent(self, event):
        '''
        Нажатие мыши
        '''
        self.pen_graph.setColor(QColor(self.choose_colour_graph))
        if event.button() == Qt.LeftButton:
            self.cursor_x = int(event.scenePos().x())
            self.cursor_y = int(event.scenePos().y())
            if self.flag_pressed_shift == False:
                if self.flag_choose_seed_point == False:
                    self.addLine(self.cursor_x, self.cursor_y, self.cursor_x, self.cursor_y,
                                    self.pen_graph)
                    self.count_points += 1
                    if self.count_polygons == len(self.polygons):
                        self.polygons.append([])

                    self.polygons[self.count_polygons].append([self.cursor_x, self.cursor_y])
                    
                    if self.count_points > 1:
                        self.addLine(self.polygons[self.count_polygons][-2][0], self.polygons[self.count_polygons][-2][1],
                                    self.polygons[self.count_polygons][-1][0], self.polygons[self.count_polygons][-1][1],
                                    self.pen_graph)
                else:
                    self.seed_point[0] = self.cursor_x; self.seed_point[1] = self.cursor_y
                    self.addLine(self.seed_point[0], self.seed_point[1],
                                self.seed_point[0], self.seed_point[1], 
                                self.pen_graph)
                    self.flag_choose_seed_point = False
                                 
            else:
                #анализ горизонтальной и вертикальной линии             
                if self.count_points >= 1:
                    dx = abs(self.cursor_x - self.polygons[self.count_polygons][-1][0])
                    dy = abs(self.cursor_y - self.polygons[self.count_polygons][-1][1])
                    if dx < dy:
                        #рисуем горизонтальную линию
                        self.polygons[self.count_polygons].append([self.polygons[self.count_polygons][-1][0], self.cursor_y])
                        self.addLine(self.polygons[self.count_polygons][-2][0], self.polygons[self.count_polygons][-2][1],
                                     self.polygons[self.count_polygons][-1][0], self.polygons[self.count_polygons][-1][1],
                                     self.pen_graph)
                        
                    else:
                        #рисуем вертикальную линию
                        self.polygons[self.count_polygons].append([self.cursor_x, self.polygons[self.count_polygons][-1][1]])
                        self.addLine(self.polygons[self.count_polygons][-2][0], self.polygons[self.count_polygons][-2][1],
                                     self.polygons[self.count_polygons][-1][0], self.polygons[self.count_polygons][-1][1], 
                                     self.pen_graph)
                    self.count_points += 1
                    self.flag_pressed_shift = False
                

        elif event.button() == Qt.RightButton:
            if self.count_points > 2:
                self.addLine(self.polygons[self.count_polygons][0][0], self.polygons[self.count_polygons][0][1],
                             self.polygons[self.count_polygons][-1][0], self.polygons[self.count_polygons][-1][1],
                             self.pen_graph)
                self.flag_fill_outline = True
                self.count_points = 0
                self.count_polygons += 1
                self.count_locked_polygons += 1

    def keyPressEvent(self, event):
        '''
        Обработка нажатия Shift
        '''
        if event.key() == QtCore.Qt.Key_Shift:
            self.flag_pressed_shift = True
        pass

class Main_window(QMainWindow, lab_06_ui.Ui_MainWindow):
    def __init__(self):
        '''
        Конструктор
        '''
        super().__init__()
        self.setupUi(self)
        #список многоугольников с [x,y]
        self.polygons = []
        self.select_sleep = 0
        self.choose_colour = '#000000'
        self.background_colour = '#ffffff'
        self.graph = GraphicsScene(self.polygons, self.choose_colour)
        self.show()
        self.add_to_ui()
        self.add_functions()
        print(f"size_height, size_width = {self.width(), self.height()}")
        print(f"size_height, size_width = {self.graphview.width(), self.graphview.height()}")
        #список координат x и у пересечения активной строки и ребра

    def add_to_ui(self):
        '''
        Добавление функционала к интерфейсу
        '''
        self.graphview.setSceneRect(0, 0, self.graphview.width(), self.graphview.height())

        self.image = QImage(SCREEN_WIDTH, SCREEN_HEIGHT, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(ZERO_COLOUR)
        #self.graph.addItem(self.image)
        self.graphview.setScene(self.graph)

        self.but_clean_all.clicked.connect(lambda: self.delete_figure())
        self.but_choose_colour.clicked.connect(self.choose_colour_fill)

    def add_functions(self):
        '''
        Добавление функционала к выполняемым задачам
        '''
        self.but_fill.clicked.connect(self.fill_area)
        self.but_choose_seed_point.clicked.connect(self.choose_seed_point)

    def move_to_left_bottom_corner(window):
        '''
        Перемещение компактной формы окна в левый верхний угол
        '''
        screen_geometry = QApplication.desktop().availableGeometry()
        screen_size = (screen_geometry.width(), screen_geometry.height())
        window_size = (window.frameSize().width(), window.frameSize().height())
        x = screen_size[0] - window_size[0]
        y = screen_size[1] - window_size[1]
        window.move(-x, -y)

    def choose_seed_point(self):
        '''
        Выбор затравочной точки
        '''
        #очистка предыдущей затравочной точки (если имеется)
        if self.graph.seed_point[0] != 0 and self.graph.seed_point[1] != 0:
            if self.is_pixel_in_fill_area(self.graph.seed_point[0], self.graph.seed_point[1]) == False:
                self.graph.addLine(self.graph.seed_point[0], self.graph.seed_point[1],
                            self.graph.seed_point[0], self.graph.seed_point[1], 
                            self.graph.clean_pen)
            self.graph.seed_point[0] = 0; self.graph.seed_point[1] = 0
        self.graph.flag_choose_seed_point = True

    def is_pixel_in_fill_area(self, x, y):
        '''
        Находится ли затравочная точка в заполненной области
        '''
        flag_is_in = False
        if (QColor(self.image.pixelColor(x + 1, y)).name() == self.graph.choose_colour_graph and
           QColor(self.image.pixelColor(x - 1, y)).name() == self.graph.choose_colour_graph and
           QColor(self.image.pixelColor(x, y + 1)).name() == self.graph.choose_colour_graph and
           QColor(self.image.pixelColor(x, y - 1)).name() == self.graph.choose_colour_graph):
            flag_is_in = True
        return flag_is_in

    def delete_figure(self):
        '''
        Удалить фигуру
        '''
        self.graph.clear()
        self.polygons.clear()
        self.graph.count_polygons = 0
        self.graph.count_points = 0
        self.graph.count_locked_polygons = 0
        self.graph.flag_fill_outline = False
        self.graph.flag_choose_seed_point = False
        self.flag_choose_seed_point = False
        self.graph.cursor_x = 0; self.graph.cursor_y = 0
        self.graph.seed_point[0] = 0; self.graph.seed_point[1] = 0

        #self.image = QImage(SCREEN_WIDTH, SCREEN_HEIGHT, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(ZERO_COLOUR)

    def choose_colour_fill(self):
        '''
        Выбор цвета заполнения
        '''
        choose_colour = QColorDialog.getColor()
        if choose_colour.isValid():
            self.graph.choose_colour_graph = choose_colour.name()
            self.graph.pen_graph = QPen(QColor(self.graph.choose_colour_graph), 1, Qt.SolidLine)
            self.label_colour.setStyleSheet("background-color: " + self.graph.choose_colour_graph)

    def fill_area(self):
        text = ''
        flag_error = False
        if len(self.polygons) == 0 or (self.graph.count_locked_polygons != len(self.polygons) or not self.graph.flag_fill_outline):
            flag_error = True
            text = "Область заполнения не задана."
        elif self.graph.seed_point[0] == 0 and self.graph.seed_point[1] == 0:
            flag_error = True          
            text = "Не выбрана затравочная точка."
            

        if flag_error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(text)
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            self.graph.flag_choose_seed_point = False
            self.graph.pen_graph = QPen(QColor(self.graph.choose_colour_graph), 1, Qt.SolidLine)
            if self.radiobut_is_sleep.isChecked():
                sleep = 1
                self.fill(sleep)
            elif self.radiobut_no_sleep.isChecked():
                sleep = 0
                start_time = time()
                self.fill(sleep)
                end_time = time()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Общее время заполнения: "+ str(round(end_time - start_time, 6)) + "c.")
                msg.setWindowTitle("Сведения")
                msg.exec_()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Не выбран режим работы программы.")
                msg.setWindowTitle("Ошибка")
                msg.exec_()

    def fill(self, sleep):
        '''
        Заполнение (с задержкой / без задержки)
        ''' 
        pixmap = QPixmap()
        painter = QPainter()
        painter.begin(self.image)
        painter.setPen(self.graph.pen_graph)
        painter.drawImage(0, 0, self.image)

        self.draw_edges(painter)
        stack = stack_class(self.graph.seed_point)
        while not stack.is_empty():
            x, y = stack.pop()
            painter.drawPoint(x, y)

            x_left = self.fill_left(x - 1, y, painter)
            x_right = self.fill_right(x + 1, y, painter)

            self.find_pixel(stack, x_right, x_left, y + 1, painter)
            self.find_pixel(stack, x_right, x_left, y - 1, painter)
            if sleep:
                pixmap.convertFromImage(self.image)
                self.graph.addPixmap(pixmap)
                QCoreApplication.processEvents()
            
        pixmap.convertFromImage(self.image)
        self.graph.addPixmap(pixmap)
        self.draw_edges(painter)
        painter.end()

    def draw_edges(self, painter):
        '''
        Отрисовка границ на Image для корректного считывания пикселей
        '''
        for i in range(len(self.graph.polygons)):
            for j in range(len(self.graph.polygons[i]) - 1):
                painter.drawLine(self.graph.polygons[i][j][0], self.graph.polygons[i][j][1],
                                 self.graph.polygons[i][j+1][0], self.graph.polygons[i][j+1][1])
            painter.drawLine(self.graph.polygons[i][0][0], self.graph.polygons[i][0][1],
                             self.graph.polygons[i][-1][0], self.graph.polygons[i][-1][1])
    
    def fill_left(self, x, y, painter):
        '''
        Заполнить строку слева
        '''
        while QColor(self.image.pixelColor(x, y)).name() != self.graph.choose_colour_graph:
            painter.drawPoint(x, y)
            x -= 1
        return x + 1

    def fill_right(self, x, y, painter):
        '''
        Заполнить строку справа
        '''
        while QColor(self.image.pixelColor(x, y)).name() != self.graph.choose_colour_graph:
            painter.drawPoint(x, y)
            x += 1
        return x - 1

    def find_pixel(self, stack, x_right, x_left, y, painter):
        '''
        Поиск нового затравочного пикселя
        '''
        while x_left <= x_right:
            flag_find_new_seed_pixel = False

            while QColor(self.image.pixelColor(x_left, y)).name() != self.graph.choose_colour_graph and x_left <= x_right:
                flag_find_new_seed_pixel = True
                x_left += 1
            
            if flag_find_new_seed_pixel == True:
                if x_left == x_right and QColor(self.image.pixelColor(x_left, y)).name() != self.graph.choose_colour_graph:
                    stack.push([x_left, y])
                else:
                    stack.push([x_left - 1, y])
                flag_find_new_seed_pixel == False
            
            x_temp = x_left
            while QColor(self.image.pixelColor(x_left, y)).name() == self.graph.choose_colour_graph and x_left < x_right:
                x_left += 1
            
            if x_left == x_temp:
                x_left += 1
                


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    main_window.move(main_window.width() * -3, 0)
    Main_window.move_to_left_bottom_corner(main_window)
    sys.exit(app.exec_())