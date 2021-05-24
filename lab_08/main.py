from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QPalette, QColor, QImage
from PyQt5.QtCore import QCoreApplication, QEventLoop, Qt, QPointF, QRectF
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QGraphicsScene

import sys
import lab_08_ui
from screen_image import ScreenImage, COLOUR_CUT_OFF

BG_COLOUR = Qt.white

class Main_window(QMainWindow, lab_08_ui.Ui_MainWindow):
    def __init__(self):
        '''
        Конструктор
        '''
        super().__init__()
        self.setupUi(self)
        self.segments = []
        self.cut_off_segments = []
        self.graph = ScreenImage(self.segments, self.cut_off_segments)

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
        self.but_input_segments.clicked.connect(self.input_segments)

    def input_segments(self):
        """
        Ввод отрезков
        """
        self.but_input_segments.setStyleSheet("background-color: #ffffff")
        self.but_input_cut_off.setStyleSheet("background-color: #cccccc")
        self.graph.flag_input_segments = True
        self.graph.flag_input_cut_off = False
        pass

    def input_cut_off(self):
        """
        Ввод отсекателя
        """
        self.but_input_segments.setStyleSheet("background-color: #cccccc")
        self.but_input_cut_off.setStyleSheet("background-color: #ffffff")
        self.graph.flag_input_cut_off = True
        self.graph.flag_input_segments = False
        pass

    def do_cut_off(self):
        """
        Выполнение отсечения
        """
        self.but_input_segments.setStyleSheet("background-color: #cccccc")
        self.but_input_cut_off.setStyleSheet("background-color: #cccccc")
        if self.check_correctness_input() == True:
            for i in range(len(self.graph.segments)):
                self.do_cut_off_segment(self.graph.segments[i])
            pass

    def check_correctness_input(self):
        """
        Проверка корректности исходных данных
        """
        flag_correctness = True
        flag_error = False
        text_error = ''
        if self.graph.segments == []:
            text_error = "Отрезки не были введены."
            flag_error = True
        elif self.graph.flag_locked_cut_off == False:
            text_error = 'Отсекатель не был задан.'
            self.but_input_cut_off.setStyleSheet("background-color: #ffffff")
            flag_error = True
        elif self.graph.is_polygon_convex() == False:
            text_error = "Отсекатель не явялется выпуклым."
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

    def do_cut_off_segment(self, segment):
        """
        Выполнить отсечение каждого отрезка (алгоритм Кируса-Бека)
        """
        count_cut_off_segments = len(self.cut_off_segments)
        t_down = 0; t_up = 1
        D = self.find_directrise(segment[0], segment[1])
        for i in range(count_cut_off_segments):
            if i < count_cut_off_segments - 2:
                inner_normal = self.find_inner_normal(self.graph.cut_off_segments[i], self.graph.cut_off_segments[i + 1],
                                        self.graph.cut_off_segments[i + 2])
            elif i == count_cut_off_segments - 2:
                inner_normal = self.find_inner_normal(self.graph.cut_off_segments[-2], self.graph.cut_off_segments[-1],
                                        self.graph.cut_off_segments[0])
            elif i == count_cut_off_segments - 1:
                inner_normal = self.find_inner_normal(self.graph.cut_off_segments[-1], self.graph.cut_off_segments[0],
                                        self.graph.cut_off_segments[1])
            W = self.find_w(segment[0], self.graph.cut_off_segments[i])
            D_scalar = self.find_scalar(D, inner_normal)
            W_scalar = self.find_scalar(W, inner_normal)

            if D_scalar == 0:
                if W_scalar <= 0:
                    #отрезок невидим
                    return

            t = -W_scalar / D_scalar

            if D_scalar > 0:
                if t > 1:
                    #отрезок невидим
                    return
                else:
                    t_down = max(t_down, t)
            elif D_scalar < 0:
                if t < 0:
                    #отрезок невидим
                    return
                else:
                    t_up = min(t_up, t)
        if t_down <= t_up:
            param_point_1 = self.convert_to_parametric(segment[0], segment[1], t_down)
            param_point_2 = self.convert_to_parametric(segment[0], segment[1], t_up)
            self.draw_part_segment([param_point_1, param_point_2])
        
        return

    def find_directrise(self, point_1, point_2):
        """
        Нахождение директрисы отрезка (задает его направление)
        """
        return [point_2[0] - point_1[0], point_2[1] - point_1[1]]

    def find_inner_normal(self, cut_off_point_1, cut_off_point_2, cut_off_point_3):
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

    def find_w(self, point_segment_1, cut_off_segment):
        """
        Вычисление W
        """
        w_i = [point_segment_1[0] - cut_off_segment[0], point_segment_1[1] - cut_off_segment[1]] 
        return w_i

    def find_scalar(self, vector_1, vector_2):
        """
        Вычисление скалярного произведения векторов
        """
        return vector_1[0] * vector_2[0] + vector_1[1] * vector_2[1]

    def convert_to_parametric(self, point_1, point_2, t):
        """
        Перевод уравнение отрезка в параметрическое
        """
        return list((point_1[0] + (point_2[0] - point_1[0]) * t, point_1[1] + (point_2[1] - point_1[1]) * t))

    def draw_part_segment(self, segment):
        """
        Нарисовать часть сегмента
        """
        self.graph.addLine(segment[0][0], segment[0][1], segment[1][0],
                            segment[1][1], self.graph.pen_result)

    def clean_screen(self):
        '''
        Очистка экрана
        '''
        self.graph.clear()
        self.graph.segments.clear()
        self.graph.cut_off_segments.clear()
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    sys.exit(app.exec_())