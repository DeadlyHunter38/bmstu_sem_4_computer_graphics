from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QPalette, QColor, QImage
from PyQt5.QtCore import QCoreApplication, QEventLoop, Qt, QPointF, QRectF
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QGraphicsScene

import sys
import lab_07_ui
import screen_image
from screen_image import ScreenImage, COLOUR_CUT_OFF

BG_COLOUR = Qt.white
MASK_LEFT = 0b0001
MASK_RIGHT = 0b0010
MASK_DOWN = 0b0100
MASK_UP = 0b1000

class Main_window(QMainWindow, lab_07_ui.Ui_MainWindow):
    def __init__(self):
        '''
        Конструктор
        '''
        super().__init__()
        self.setupUi(self)
        self.segments = []
        self.graph = ScreenImage(self.segments)

        self.add_to_ui()
        self.add_functions()
        self.show()

    def add_to_ui(self):
        '''
        Добавление функционала к интерфейсу
        '''
        self.graph.setSceneRect(-self.width(), -self.height(), self.width(), self.height())
        self.graphicsView.setScene(self.graph)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.image = QImage(self.graph.width(), self.graph.height(), QImage.Format_ARGB32_Premultiplied)
        self.bg_colour = BG_COLOUR
        self.image.fill(self.bg_colour)

    def add_functions(self):
        '''
        Добавление функционала к выполняемым задачам
        '''
        self.but_clean_all.clicked.connect(self.clean_screen)
        self.but_input_cut_off.clicked.connect(self.input_cut_off)
        self.but_cut_off.clicked.connect(self.do_cut_off)

    def clean_screen(self):
        '''
        Очистка экрана
        '''
        self.graph.clear()
        self.graph.segments.clear()
        self.graph.count_segments = -1
        self.graph.count_points = 0
        self.graph.cursor_x = 0; self.graph.cursor_y = 0
        self.graph.rectangle = None
        self.graph.flag_input_cut_off = False

        self.image = QImage(self.graph.width(), self.graph.height(), QImage.Format_ARGB32_Premultiplied)
        self.image.fill(self.bg_colour)

    def input_cut_off(self):
        '''
        Ввод отсекателя (прямоугольная область)
        '''
        self.graph.flag_input_cut_off = True

    def do_cut_off(self):
        '''
        Выполнение отсечения
        '''
        correctness = self.check_input_data()
        if correctness == True:
            rectangle = self.graph.addRect(QRectF(QPointF(self.graph.x - 1, self.graph.y - 1), 
                                             QPointF(self.graph.x - 1, self.graph.y - 1)),
                                             self.graph.clear_pen, self.graph.clear_brush)
            rectangle.setRect(QRectF(QPointF(self.graph.rectangle_points[0] + 1, self.graph.rectangle_points[1] + 1), 
                                      QPointF(self.graph.rectangle_points[2] - 1, self.graph.rectangle_points[3] - 1)))
            for i in range(len(self.graph.segments)):
                print(f"I = {i}")
                self.do_cut_off_segment(self.graph.segments[i], self.graph.rectangle_points)

    def check_input_data(self):
        '''
        Проверка корректности исходных данных
        '''
        flag_correctness = True
        flag_error = False
        text_error = ''
        if self.graph.segments == []:
            text_error = 'Отрезки не были введены.'
            flag_error = True
        elif self.graph.rectangle == None:
            text_error = 'Отсекатель не был введен.'
            flag_error = True
        
        if flag_error == True:
            flag_correctness = False
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(text_error)
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        
        return flag_correctness

    def do_cut_off_segment(self, segment, rectangle):
        '''
        Выполнение отсечения для каждого отрезка
        '''
        print(f"segment = {segment}")
        print(f"rectangle = {rectangle}")
        segment_bits_points = []
        segment_bits_points.append(self.create_segment_bits(segment[0]))
        segment_bits_points.append(self.create_segment_bits(segment[1]))
        print(bin(segment_bits_points[0])[2:].zfill(8))
        print(bin(segment_bits_points[1])[2:].zfill(8))
        #print(f"segment_bits[0] = {format(int(bin(segment_bits_points[0])), '04b')}")
        #print(f"segment_bits[1] = {bin(segment_bits_points[1])}")
        
        #отрезок полностью невидим
        print(f"segment_bits_points[0] & segment_bits_points[1] = {bin(segment_bits_points[0] & segment_bits_points[1])[2:].zfill(8)}")
        if segment_bits_points[0] & segment_bits_points[1]:
            print(f"here")
            return

        #отрезок полностью видим
        if segment_bits_points[0] == 0 and segment_bits_points[1] == 0:
            self.draw_part_segment(segment, screen_image.COLOUR_RESULT)
            return

        current_index_point = 0
        result_points = []
        #проверка видимости первой вершины
        if segment_bits_points[0] == 0:
            print(f"first is visible")
            current_index_point = 1
            result_points.append(segment[0])

        #проверка видимости второй вершины
        elif segment_bits_points[1] == 0:
            print(f"second is visible")
            current_index_point = 1
            result_points.append(segment[1])
            segment_bits_points.reverse()
            segment.reverse()

        print(f"current_index = {current_index_point}")
        while current_index_point < 2:
            if segment[0][0] == segment[1][0]:
                result_points.append(self.find_vertical(segment, current_index_point, rectangle))
                current_index_point += 1
                continue
            m = (segment[1][1] - segment[0][1]) / (segment[1][0] - segment[0][0])

            if segment_bits_points[current_index_point] & MASK_LEFT:
                print(f"MASK_LEFT")
                y = round(m * (rectangle[screen_image.LEFT] - segment[current_index_point][0]) + segment[current_index_point][1])
                if y >= rectangle[screen_image.DOWN] and y <= rectangle[screen_image.UP]:
                    result_points.append([rectangle[screen_image.LEFT], y])
                    current_index_point += 1
                    continue
            elif segment_bits_points[current_index_point] & MASK_RIGHT:
                print(f"MASK_RIGHT")
                y = round(m * (rectangle[screen_image.RIGHT]  - segment[current_index_point][0]) + segment[current_index_point][1])
                if y >= rectangle[screen_image.DOWN] and y <= rectangle[screen_image.UP]:
                    result_points.append([rectangle[screen_image.RIGHT], y])
                    current_index_point += 1
                    continue

            if m == 0:
                current_index_point += 1
                continue

            if segment_bits_points[current_index_point] & MASK_UP:
                print(f"MASK_UP")
                x = round((rectangle[screen_image.UP] - segment[current_index_point][1]) / m + segment[current_index_point][0])
                if x >= rectangle[screen_image.LEFT] and x <= rectangle[screen_image.RIGHT]:
                    result_points.append([x, rectangle[screen_image.UP]])
                    current_index_point += 1
                    continue
            elif segment_bits_points[current_index_point] & MASK_DOWN:
                print(f"MASK_DOWN")
                x = round((rectangle[screen_image.DOWN]  - segment[current_index_point][1]) / m + segment[current_index_point][0])
                if x >= rectangle[screen_image.LEFT] and x <= rectangle[screen_image.RIGHT]:
                    result_points.append([x, rectangle[screen_image.DOWN]])
                    current_index_point += 1
                    continue

            current_index_point += 1
        if result_points != []:
            self.draw_part_segment(result_points, screen_image.COLOUR_RESULT)
        
    def create_segment_bits(self, segment_point):
        '''
        Создать четырехразрядный код концов отрезка
        '''
        print(f"segment_point = {segment_point}")

        segment_bits = 0b0000
        print(f"bin(segment_bits) = {bin(segment_bits)}")
        if segment_point[0] < self.graph.rectangle_points[screen_image.LEFT]:
            print(f"LEFT")
            segment_bits |= MASK_LEFT
            print(f"bin(segment_bits) = {bin(segment_bits)}")
        if segment_point[0] > self.graph.rectangle_points[screen_image.RIGHT]:
            print(f"RIGHT")
            segment_bits |= MASK_RIGHT
            print(f"bin(segment_bits) = {bin(segment_bits)}")
        if segment_point[1] > self.graph.rectangle_points[screen_image.UP]:
            print(f"UP")
            segment_bits |= MASK_UP
            print(f"bin(segment_bits) = {bin(segment_bits)}")
        if segment_point[1] < self.graph.rectangle_points[screen_image.DOWN]:
            print(f"DOWN")
            segment_bits |= MASK_DOWN
            print(f"bin(segment_bits) = {bin(segment_bits)}")
        print(f"RESULT_bin(segment_bits) = {bin(segment_bits)}")
        print()
        return segment_bits

    def find_vertical(self, segment, current_index, rectangle):
        '''
        Поиск вертикальных линий
        '''
        if segment[current_index][1] > rectangle[screen_image.UP]:
            return [segment[current_index][0], rectangle[screen_image.UP]]
        elif segment[current_index][1] < rectangle[screen_image.DOWN]:
            return [segment[current_index][0], rectangle[screen_image.DOWN]]
        else:
            return segment[current_index]

    def draw_part_segment(self, result_points, colour_result):
        '''
        Отрисовка части отрезка
        '''
        print(f"result_points = {result_points}")
        print(f"colour_result = {colour_result}")
        print(f"len_result_points = {len(result_points)}")
        if len(result_points) > 1:
            self.graph.addLine(result_points[0][0], result_points[0][1], result_points[1][0],
                                result_points[1][1], self.graph.pen_result)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    sys.exit(app.exec_())