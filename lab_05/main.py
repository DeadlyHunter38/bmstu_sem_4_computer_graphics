from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QPolygon, QPainterPath, QMouseEvent, QColor, QImage, qRgb
from PyQt5.QtCore import QCoreApplication, QEventLoop, QPoint, QPointF, Qt
from PyQt5.QtWidgets import QGraphicsItem, QMessageBox, QLineEdit, QPushButton, QLabel, QGraphicsScene,\
                            QGraphicsView, QWidget, QMenu, QMainWindow, QAction, QColorDialog
import matplotlib.colors as colors
from PIL import ImageColor
from copy import copy, deepcopy
from time import time

import sys, ui

ZERO_COLOUR = Qt.white

class GraphicsScene(QGraphicsScene, ui.Ui_MainWindow):
    def __init__(self, polygons, choose_colour):
        super().__init__()
        self.setSceneRect(0, 0, 743, 944)
        self.cursor_x = 0; self.cursor_y = 0
        self.flag_pressed_shift = False
        self.flag_fill_outline = False
        self.count_points = 0
        self.count_polygons = 0
        self.radius_point_click = 1
        self.polygons = polygons
        self.choose_colour_graph = choose_colour
        self.image = QImage(1000, 1500, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(ZERO_COLOUR)
        self.pen_graph = QPen(QColor(self.choose_colour_graph), 1, Qt.SolidLine)
        self.brush_graph = QBrush(QColor(self.choose_colour_graph))
        self.count_locked_polygons = 0
    
    def addLine(self, x1, y1, x2, y2, pen):
        # return QGraphicsScene.addLine(self, x1, y1, x2, y2, pen=pen)
        def draw_point(x,y):
            QGraphicsScene.addLine(self, x, y, x, y, pen=pen)
            pass
        
        if (y1 > y2):
            y1, y2, x1, x2 = y2, y1, x2, x1

        def create_line_by_digital_differential_analyzer(x_start, y_start, x_end, y_end, flag_table):
            #Цифровой дифференциальный анализатор
            if (x_start == x_end) and (y_start == y_end):
                if flag_table == 0: draw_point(x_start, y_start)
            else:
                l = 0; dx = 0; dy = 0
                if abs(x_end - x_start) >= abs(y_end - y_start):
                    l = abs(x_start - x_end)
                else:
                    l = abs(y_start - y_end)
                dx = (x_end - x_start) / l; dy = (y_end - y_start) / l
                x = x_start; y = y_start
                i = 0
                while i <= l:
                    x_draw = round(x); y_draw = round(y)
                    if flag_table == 0: draw_point(x_draw, y_draw)
                    x += dx; y += dy
                    i += 1
        create_line_by_digital_differential_analyzer(x1, y1, x2, y2, 0)
  
    def updateImage(self):
        '''
        Перевести в QImage
        '''
        painter = QPainter()
        paintDevice = QPixmap(int(self.width()), int(self.height()))
        paintDevice.fill(Qt.white)

        painter.begin(paintDevice)
        self.render(painter)
        painter.end()

        self.image = paintDevice.toImage()
    
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
                self.addLine(self.cursor_x, self.cursor_y, self.cursor_x, self.cursor_y,
                                self.pen_graph)
                self.count_points += 1
                if self.count_polygons == len(self.polygons):
                    self.polygons.append([])
                #print(f"self.count_polygons = {self.count_polygons}")
                self.polygons[self.count_polygons].append([self.cursor_x, self.cursor_y])
                
                if self.count_points > 1:
                    self.addLine(self.polygons[self.count_polygons][-2][0], self.polygons[self.count_polygons][-2][1],
                                 self.polygons[self.count_polygons][-1][0], self.polygons[self.count_polygons][-1][1],
                                 self.pen_graph)
                                 
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
        if event.key() == QtCore.Qt.Key_Shift:
            self.flag_pressed_shift = True
        pass

class Main_window(QMainWindow, ui.Ui_MainWindow):
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
        #список координат x и у пересечения активной строки и ребра

    def add_to_ui(self):
        '''
        Добавление функционала к интерфейсу
        '''
        self.graphview.setScene(self.graph)
        self.but_clean_all.clicked.connect(lambda: self.delete_figure())
        self.but_choose_colour.clicked.connect(self.choose_colour_fill)

    def add_functions(self):
        '''
        Добавление функционала к выполняемым задачам
        '''
        self.but_fill.clicked.connect(self.fill_area)
        pass

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
        self.graph.cursor_x = 0; self.graph.cursor_y = 0

    def choose_colour_fill(self):
        '''
        Выбор цвета заполнения
        '''
        choose_colour = QColorDialog.getColor()
        if choose_colour.isValid():
            self.graph.choose_colour_graph = choose_colour.name()
            self.graph.pen_graph = QPen(QColor(self.graph.choose_colour_graph), 1, Qt.SolidLine)
            #print(f"self.graph.choose_colour_graph = {self.graph.choose_colour_graph}")
            self.label_colour.setStyleSheet("background-color: " + self.graph.choose_colour_graph)

    def fill_area(self):
        if len(self.polygons) == 0 or (self.graph.count_locked_polygons != len(self.polygons) or not self.graph.flag_fill_outline):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Область заполнения не задана.")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            #print(f"self.graph.choose_colour_graph = {self.graph.choose_colour_graph}")
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
                msg.setText("Общее время заполнения: "+ str(end_time - start_time) + "c.")
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
        #self.graph.clear()
        for i in range(self.graph.count_polygons):
            partition_wall_x = self.find_partition_wall(self.polygons[i])
            self.fill_polygon(self.polygons[i], partition_wall_x, sleep)                                                        

    def fill_polygon(self, current_polygon, partition_wall_x, sleep):
        '''
        Заполнение многоугольника
        '''
        len_polygon = len(current_polygon)
        for i in range(len_polygon - 1):
            self.fill_area_polygon(current_polygon[i], current_polygon[i + 1], partition_wall_x, sleep)
        self.fill_area_polygon(current_polygon[-1], current_polygon[0], partition_wall_x, sleep)


    def fill_area_polygon(self, start_link_point, end_link_point, partition_wall_x, sleep):
        '''
        Обработка каждого отрезка многоугольника на заполнение
        '''
        self.graph.updateImage()
        start_point = copy(start_link_point)
        end_point = copy(end_link_point)
        #пропускаем горизонтальную линию
        if start_point[1] == end_point[1]:
            return

        #меняем значения для того, чтобы идти снизу-вверх по отрезку
        if start_point[1] > end_point[1]:
            start_point, end_point = end_point, start_point

        dx = (end_point[0] - start_point[0]) / (end_point[1] - start_point[1])
        dy = 1

        current_x = start_point[0]; current_y = start_point[1]
        if sleep == 0:
            self.process_fill_area_with_no_sleep(current_x, current_y, end_point, partition_wall_x, dx, dy)
        else:
            self.process_fill_area_with_sleep(current_x, current_y, end_point, partition_wall_x, dx, dy)

    def process_fill_area_with_no_sleep(self, current_x, current_y, end_point, partition_wall_x, dx, dy):
        '''
        Заполнение без задержки
        '''
        while current_y < end_point[1]:
            if current_x < partition_wall_x:
                #если пересечение находится левее перегородки
                for j in range(round(current_x) + 1, partition_wall_x):
                    self.reverse_pixel(j, round(current_y))
            elif current_x >= partition_wall_x:
                #если пересечение находится правее перегородки
                for j in range(partition_wall_x, round(current_x) + 1):
                    self.reverse_pixel(j, round(current_y))
            current_x += dx; current_y += dy

    def process_fill_area_with_sleep(self, current_x, current_y, end_point, partition_wall_x, dx, dy):
        '''
        Заполнение с задержкой
        '''
        while current_y < end_point[1]:
            if current_x < partition_wall_x:
                #если пересечение находится левее перегородки
                for j in range(round(current_x) + 1, partition_wall_x):
                    self.reverse_pixel(j, round(current_y))
            elif current_x >= partition_wall_x:
                #если пересечение находится правее перегородки
                for j in range(partition_wall_x, round(current_x) + 1):
                    self.reverse_pixel(j, round(current_y))
            current_x += dx; current_y += dy
            QCoreApplication.processEvents(QEventLoop.AllEvents, 0)

    def reverse_pixel(self, x, y):
        '''
        Инвертирование цвета пикселя
        '''
        pixel_colour = self.graph.getPixelColor(x, y)
        self.graph.choose_colour_graph
        if pixel_colour == self.graph.choose_colour_graph:
            self.graph.pen_graph.setColor(QColor(self.background_colour))
            self.graph.brush_graph = QBrush(QColor(self.background_colour))
        elif pixel_colour == self.background_colour:
            self.graph.pen_graph.setColor(QColor(self.graph.choose_colour_graph))
            self.graph.brush_graph = QBrush(QColor(self.graph.choose_colour_graph))
        self.graph.addLine(x, y, x, y, pen=self.graph.pen_graph)

    def find_partition_wall(self, current_polygon):
        '''
        Поиск перегородки
        '''
        x_max, x_min = self.find_x_max_x_min(current_polygon)
        middle = (x_max + x_min) / 2
        return round(middle)

    def find_x_max_x_min(self, current_polygon):
        '''
        Поиск x_max, x_min
        '''
        #print(f"current_polygon = {current_polygon}")
        x_max = x_min = current_polygon[0][0]
        len_current_polygon = len(current_polygon)
        for i in range(1, len_current_polygon):
            if current_polygon[i][0] > x_max:
                x_max = current_polygon[i][0]
            elif current_polygon[i][0] < x_min:
                x_min = current_polygon[i][0]
        return x_max, x_min

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    sys.exit(app.exec_())