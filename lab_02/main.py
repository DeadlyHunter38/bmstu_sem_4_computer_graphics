from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPolygon, QPainterPath, QMouseEvent
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QPushButton, QLabel, QGraphicsScene,\
                            QGraphicsView, QWidget, QMenu, QMainWindow, QAction
from copy import deepcopy
from math import cos, sin, radians, pi
import sys
import ui

#НАЧАЛЬНЫЕ КООРДИНАТЫ
#list_x = [170, 120, 170, 220, 270, 320, 370, 315]
#list_y = [420, 420, 50, 130, 130, 50, 420, 420]

FONT_1 = "Times New Roman"
SIZE_1 = 14
SHIFT_WIDGETS_X = 1600         #сдвиг виджетов по оси х

class Second_window(QWidget):
    def __init__(self):
        super(Second_window, self).__init__()
        self.setWindowTitle('Справка')
        self.resize(800, 600)

        #установка шрифта, его размера 
        font = QtGui.QFont()
        font.setFamily(FONT_1); font.setPointSize(SIZE_1)
        self.setFont(font)

        self.create_UI_second()

    def create_UI_second(self):
        self.label_info = QLabel(self)
        self.label_info.setGeometry(QtCore.QRect(5, 10, 800, 100))
        self.label_info.setText("Задание на лабораторную работу:\n"+
                                "Нарисовать исходный рисунок, затем его переместить,"+
                                "промасштабировать, повернуть.")
        self.label_image = QtWidgets.QLabel(self)
        self.pix = QtGui.QPixmap('cat.png')
        self.label_image.setPixmap(self.pix)
        self.label_image.move(200, 200)

class MyFrame(QLabel):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setStyleSheet('QFrame {background-colorwhite;}')
        self.resize(1500, 920)
        self.flag = False
        self.flag_click = False
        self.x = 0
        self.y = 0
        #создание координат для изображения туловища
        self.list_x = [170, 120, 170, 220, 270, 320, 370, 315]
        self.list_y = [420, 420, 50, 130, 130, 50, 420, 420]

        self.extra_x = [ [220+450+25], #верхушка головы
                         [120+450-30.0, 120+450-53.28, 120+450-53.28, 120+450-36.6, 120+450+5.28], #левая лапа
                         [120+450-39.96, 120+450-39.96, 120+450-30, 120+450-26.64, 120+450-23.28],  #полоски этой лапки
                         [450+370+44.955, 450+370+53.28, 450+370+53.28, 450+370+36.6, 450+370-5.28], #правая лапка
                         [450+370+39.96, 450+370+39.96, 450+370+30, 450+370+26.64, 450+370+23.28], #полоски этой лапки
                         [120+450+49.992, 120+450+49.992, 120+450+86.64, 120+450+123.324, 120+450+49.992, 120+450+49.992, 120+450+86.64, 120+450+123.324], #левая нижняя лапка
                         [120+450+49.992, 120+450+66.6, 120+450+69.996, 120+450+73.32, 120+450+76.656], #полоски этой лапки
                         [120+450+123.324, 120+450+123.324, 120+450+159.96, 120+450+196.656, 120+450+123.324, 120+450+123.324, 120+450+159.96, 120+450+196.656], #правая нижняя лапка
                         [120+450+196.656, 120+450+180, 120+450+176.664, 120+450+173.28, 120+450+169.992], #полоски этой лапки
                         [693-35], #левый глаз
                         [693+35], #правый глаз
                         [693], #носик
                         [170+450+26.656, 170+450+26.656, 170+450+73.321, 170+450+119.986], #улыбка
                         [170+450+63.325, 170+450-56.78, 170+450+63.325, 170+450-56.78, 170+450+63.325, 170+450-56.78, 170+450+83.317, 170+450+196.656, 170+450+83.317, 170+450+196.656, 170+450+83.317, 170+450+196.656], #усы
                         [666.665, 719.335], #зрачок
                         [170 + 450 + 73.321, 170 + 450 +73.321]] #линия, выше рта

        self.extra_y = [ [130+170-13],
                         [420+170+6.636, 420+170-0.096, 420+170-0.096, 420+170-53.34, 420+170-49.98],
                         [420+170+1.3314, 420+170+1.3314, 420+170-19.992, 420+170+1.3314, 420+170-19.74],
                         [420+170+9.954, 420+170-4.3845, 420+170-4.3845, 420+170-53.34, 420+170-49.98],
                         [420+170+1.3314, 420+170-1.3314, 420+170-19.992, 420+170-1.3314, 420+170-19.74],
                         [420+170+0, 420+170+0, 420+170-69.972, 420+170+0, 420+170+0, 420+170+0, 420+170+16.632, 420+170+0], 
                         [420+170+0, 420+170+3.318, 420+170-10.038, 420+170+6.636, 420+170-10.038],
                         [420+170+0, 420+170+0, 420+170-70.14, 420+170+0, 420+170+0, 420+170+0, 420+170+16.632, 420+170+0],
                         [420+170+0, 420+170+3.318, 420+170-10.038, 420+170+6.636, 420+170-10.038],
                         [420+170-227.022],
                         [420+170-227.022],
                         [420+170-195.682],
                         [420 + 170 -153.342, 420 + 170 -153.342, 420 + 170 -120.036, 420 + 170 -153.342],
                         [420+170-200.004, 420+170-160.02, 420+170-200.004, 420+170-146.706, 420+170-200.004, 420+170-133.35, 420+170-200.004, 420+170-160.02, 420+170-200.004, 420+170-146.706, 420+170-200.004, 420+170-133.35],
                         [420+170-227.022, 420+170-227.022],
                         [406.998, 450.972]]
        self.left_eye_x = []; self.left_eye_y = []
        self.right_eye_x = []; self.right_eye_y = []
        self.nose_x = []; self.nose_y = []
        self.left_pupil_x = []; self.left_pupil_y = []
        self.right_pupil_x = []; self.right_pupil_y = []
        
        self.koeff_zoom_x = 1               #коэффициент масштабирования фигуры по х
        self.koeff_zoom_y = 1               #коэффициент масштабирования фигуры по y
        self.shift_image_x = 0              #сдвиг фигуры по оси х
        self.shift_image_y = 0              #сдвиг фигуры по оси у
        self.START_X = 450                  #начальный сдвиг по оси х
        self.START_Y = 170                   #начальный сдвиг по оси у
        self.nose_radius_width = 12               #радиус носа
        self.nose_radius_height = 12
        self.eye_radius_width = 35             #радиус глаза
        self.eye_radius_height = 35
        self.eyeball_radius_width = 8       #радиус зрачка
        self.eyeball_radius_height = 8

        #глаза и нос
        center_left_eye_x = 657; center_left_eye_y = 363; r = 35
        center_right_eye_x = 727; center_right_eye_y = 363; r = 35
        center_nose_x = 692; center_nose_y = 393; r_nose = 12
        center_left_pupil_x = 667; center_left_pupil_y = 363
        center_right_pupil_x = 717; center_right_pupil_y = 363
        dn = 1/r
        n = 0
        while n < 2*pi:
            self.left_eye_x.append(round(center_left_eye_x + r * cos(n)))
            self.left_eye_y.append(round(center_left_eye_y + r * sin(n)))
            self.right_eye_x.append(round(center_right_eye_x + r * cos(n)))
            self.right_eye_y.append(round(center_right_eye_y + r * sin(n)))
            self.nose_x.append(round(center_nose_x + r_nose * cos(n)))
            self.nose_y.append(round(center_nose_y + r_nose * sin(n)))
            self.left_pupil_x.append(round(center_left_pupil_x + 8 * sin(n)))
            self.left_pupil_y.append(round(center_left_pupil_y + 8 * cos(n)))
            self.right_pupil_x.append(round(center_right_pupil_x + 8 * sin(n)))
            self.right_pupil_y.append(round(center_right_pupil_y + 8 * cos(n)))
            n += dn

        #предыдущие значения
        self.old_nose_radius_width = deepcopy(self.nose_radius_width)
        self.old_nose_radius_height = deepcopy(self.nose_radius_height)
        self.old_eye_radius_width = deepcopy(self.eye_radius_width)
        self.old_eye_radius_height = deepcopy(self.eye_radius_height)
        self.old_eyeball_radius_width = deepcopy(self.eyeball_radius_width)
        self.old_eyeball_radius_height = deepcopy(self.eyeball_radius_height)
        self.old_koeff_zoom_x = deepcopy(self.koeff_zoom_x)
        self.old_koeff_zoom_y = deepcopy(self.koeff_zoom_y)
        self.old_extra_x = deepcopy(self.extra_x)
        self.old_extra_y = deepcopy(self.extra_y)

        #первоначальные значения
        self.first_nose_radius_width = deepcopy(self.nose_radius_width)
        self.first_nose_radius_height = deepcopy(self.nose_radius_height)
        self.first_eye_radius_width = deepcopy(self.eye_radius_width)
        self.first_eye_radius_height = deepcopy(self.eye_radius_height)
        self.first_eyeball_radius_width = deepcopy(self.eyeball_radius_width)
        self.first_eyeball_radius_height = deepcopy(self.eyeball_radius_height)
        self.first_koeff_zoom_x = deepcopy(self.koeff_zoom_x)
        self.first_koeff_zoom_y = deepcopy(self.koeff_zoom_y)
        self.first_extra_x = deepcopy(self.extra_x)
        self.first_extra_y = deepcopy(self.extra_y)
        self.first_left_eye_x = deepcopy(self.left_eye_x)
        self.first_left_eye_y = deepcopy(self.left_eye_y)
        self.first_right_eye_x = deepcopy(self.right_eye_x)
        self.first_right_eye_y = deepcopy(self.right_eye_y)
        self.first_nose_x = deepcopy(self.nose_x)
        self.first_nose_y = deepcopy(self.nose_y)
        self.first_left_pupil_x = deepcopy(self.left_pupil_x)
        self.first_left_pupil_y = deepcopy(self.left_pupil_y)
        self.first_right_pupil_x = deepcopy(self.right_pupil_x)    
        self.first_right_pupil_y = deepcopy(self.right_pupil_y)             

        for i in range(len(self.list_x)):
            self.list_x[i] += self.START_X
            self.list_y[i] += self.START_Y
            self.list_x[i] *= self.koeff_zoom_x
            self.list_y[i] *= self.koeff_zoom_y

        #сохранение состояния предыдущего значения
        self.old_list_x = deepcopy(self.list_x)
        self.old_list_y = deepcopy(self.list_y)

        #сохранение первоначального состояния
        self.first_list_x = deepcopy(self.list_x)
        self.first_list_y = deepcopy(self.list_y)


    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        if self.flag and self.x < 1490:
            painter = QPainter()
            painter.begin(self)
            pen = QPen(Qt.black, 2, Qt.SolidLine)
            painter.setPen(pen)
            self.flag = False
            painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
            painter.drawEllipse(QtCore.QPoint(self.x, self.y),5,5)
            painter.end()

        #отрисовка тела котика
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        path = QPainterPath()

        path.moveTo(self.list_x[3],self.list_y[3])
        path.cubicTo(self.list_x[3],self.list_y[3], 
                    self.extra_x[0][0], self.extra_y[0][0], 
                    self.list_x[4], self.list_y[4])
        painter.drawPath(path)

        size_list = len(self.list_x)
        for i in range(size_list - 1):
            if i != 3:
                painter.drawLine(int(self.list_x[i]), int(self.list_y[i]), int(self.list_x[i + 1]), int(self.list_y[i + 1]))

        #отрисовка левой лапы котика
        path.moveTo(self.list_x[1],self.list_y[1])
        path.cubicTo(self.list_x[1], self.list_y[1],
                    self.extra_x[1][0], self.extra_y[1][0],
                    self.extra_x[1][1], self.extra_y[1][1])
        path.cubicTo(self.extra_x[1][2], self.extra_y[1][2],
                    self.extra_x[1][3], self.extra_y[1][3],
                    self.extra_x[1][4], self.extra_y[1][4])
        painter.drawPath(path)

        #отрисовка полосок этой лапки
        path.moveTo(self.extra_x[2][0], self.extra_y[2][0])
        painter.drawLine(int(self.extra_x[2][1]), int(self.extra_y[2][1]),
                        int(self.extra_x[2][2]), int(self.extra_y[2][2]))
        painter.drawLine(int(self.extra_x[2][3]), int(self.extra_y[2][3]),
                        int(self.extra_x[2][4]), int(self.extra_y[2][4]))      

        #отрисовка правой лапы котика
        path.moveTo(self.list_x[size_list - 2],self.list_y[size_list - 2])
        path.cubicTo(self.list_x[size_list - 2], self.list_y[size_list - 2],
                    self.extra_x[3][0], self.extra_y[3][0],
                    self.extra_x[3][1], self.extra_y[3][1])
        path.cubicTo(self.extra_x[3][2], self.extra_y[3][2],
                    self.extra_x[3][3], self.extra_y[3][3],
                    self.extra_x[3][4], self.extra_y[3][4])
        painter.drawPath(path)

        #отрисовка полосок этой лапки
        path.moveTo(self.extra_x[4][0], self.extra_y[4][0])
        painter.drawLine(int(self.extra_x[4][1]), int(self.extra_y[4][1]),
                        int(self.extra_x[4][2]), int(self.extra_y[4][2]))
        painter.drawLine(int(self.extra_x[4][3]), int(self.extra_y[4][3]),
                        int(self.extra_x[4][4]), int(self.extra_y[4][4]))   
        
        #отрисовка левой нижней лапки котика
        path.moveTo(self.extra_x[5][0], self.extra_y[5][0])
        path.cubicTo(self.extra_x[5][1], self.extra_y[5][1],
                    self.extra_x[5][2], self.extra_y[5][2],
                    self.extra_x[5][3], self.extra_y[5][3])
        path.moveTo(self.extra_x[5][4], self.extra_y[5][4])
        path.cubicTo(self.extra_x[5][5], self.extra_y[5][5],
                    self.extra_x[5][6], self.extra_y[5][6],
                    self.extra_x[5][7], self.extra_y[5][7])
        painter.drawPath(path)

        #отрисовка полосок этой лапки
        path.moveTo(self.extra_x[6][0], self.extra_y[6][0])
        painter.drawLine(int(self.extra_x[6][1]), int(self.extra_y[6][1]),
                        int(self.extra_x[6][2]), int(self.extra_y[6][2]))
        painter.drawLine(int(self.extra_x[6][3]), int(self.extra_y[6][3]),
                        int(self.extra_x[6][4]), int(self.extra_y[6][4]))  
        
        #отрисовка правой нижней лапки котика
        path.moveTo(self.extra_x[7][0], self.extra_y[7][0])
        path.cubicTo(self.extra_x[7][1], self.extra_y[7][1],
                    self.extra_x[7][2], self.extra_y[7][2],
                    self.extra_x[7][3], self.extra_y[7][3])
        path.moveTo(self.extra_x[7][4], self.extra_y[7][4])
        path.cubicTo(self.extra_x[7][5], self.extra_y[7][5],
                    self.extra_x[7][6], self.extra_y[7][6],
                    self.extra_x[7][7], self.extra_y[7][7])
        painter.drawPath(path)
        
        #отрисовка полосок этой лапки
        path.moveTo(self.extra_x[8][0], self.extra_y[8][0])
        painter.drawLine(int(self.extra_x[8][1]), int(self.extra_y[8][1]),
                        int(self.extra_x[8][2]), int(self.extra_y[8][2]))
        painter.drawLine(int(self.extra_x[8][3]), int(self.extra_y[8][3]),
                            int(self.extra_x[8][4]), int(self.extra_y[8][4]))
        
        #рисование левого и правого глаза
        for i in range(len(self.left_eye_x)):
            painter.drawPoint(int(self.left_eye_x[i]), int(self.left_eye_y[i]))
            painter.drawPoint(int(self.right_eye_x[i]), int(self.right_eye_y[i]))
            painter.drawPoint(int(self.nose_x[i]), int(self.nose_y[i]))
            painter.drawPoint(int(self.left_pupil_x[i]), int(self.left_pupil_y[i]))
            painter.drawPoint(int(self.right_pupil_x[i]), int(self.right_pupil_y[i]))


        #рисование улыбки

        path_smile = QPainterPath()
        path_smile.moveTo(int(self.extra_x[12][0]), int(self.extra_y[12][0]))
        path_smile.cubicTo(int(self.extra_x[12][1]), int(self.extra_y[12][1]),
                            int(self.extra_x[12][2]), int(self.extra_y[12][2]),
                            int(self.extra_x[12][3]), int(self.extra_y[12][3]))
        painter.drawPath(path_smile)

        #рисование усов
        painter.drawLine(int(self.extra_x[13][0]), int(self.extra_y[13][0]),
                            int(self.extra_x[13][1]), int(self.extra_y[13][1]))
        painter.drawLine(int(self.extra_x[13][2]), int(self.extra_y[13][2]),
                        int(self.extra_x[13][3]), int(self.extra_y[13][3]))
        painter.drawLine(int(self.extra_x[13][4]), int(self.extra_y[13][4]),
                        int(self.extra_x[13][5]), int(self.extra_y[13][5]))

        painter.drawLine(int(self.extra_x[13][6]), int(self.extra_y[13][6]),
                        int(self.extra_x[13][7]), int(self.extra_y[13][7]))
        painter.drawLine(int(self.extra_x[13][8]), int(self.extra_y[13][8]),
                        int(self.extra_x[13][9]), int(self.extra_y[13][9]))
        painter.drawLine(int(self.extra_x[13][10]), int(self.extra_y[13][10]),    
                        int(self.extra_x[13][11]), int(self.extra_y[13][11]))

        #рисование линии, выше рта
        painter.drawLine(int(self.extra_x[15][0]), int(self.extra_y[15][0]),
                        int(self.extra_x[15][1]), int(self.extra_y[15][1]))





        painter.end()


class Main_window(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.number_action = 0
        self.secondWin = None
        self.lb = MyFrame(self)
        self.setupUi(self)
        self.create_menu()
        self.show()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.lb.flag = True
            self.lb.flag_click = True
            self.lb.x=e.pos().x()
            self.lb.y=e.pos().y()

            if self.lb.x < 1490:
                self.entry_zoom_x.setText(str(self.lb.x))
                self.entry_zoom_y.setText(str(self.lb.y))
                self.entry_rotate_x.setText(str(self.lb.x))
                self.entry_rotate_y.setText(str(self.lb.y))
            self.update()

    def create_menu(self):
        '''
            Создание меню
        '''
        #создание панели меню
        window_menu = self.menuBar()
        file = window_menu.addMenu('Файл')
      
        #создание подменю
        cancel = QAction("Назад", self)
        info = QAction("Справка", self)
        cancel.triggered.connect(self.cancel_action)
        info.triggered.connect(self.create_info_window)

        file.addAction(cancel)
        file.addAction(info)

    def create_info_window(self):
        self.info_window = Second_window()
        self.info_window.show()
        

    def cancel_action(self):
        '''
            Отменить последнее действие
        '''
        if self.number_action == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Не было совершено ни одного действия.")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            if self.number_action == 1:
                self.lb.list_x = deepcopy(self.lb.old_list_x)
                self.lb.list_y = deepcopy(self.lb.old_list_y)
                self.lb.extra_x = deepcopy(self.lb.old_extra_x)
                self.lb.extra_y = deepcopy(self.lb.old_extra_y)
            elif self.number_action == 2:
                self.lb.list_x = deepcopy(self.lb.old_list_x)
                self.lb.list_y = deepcopy(self.lb.old_list_y)
                self.lb.extra_x = deepcopy(self.lb.old_extra_x)
                self.lb.extra_y = deepcopy(self.lb.old_extra_y)
                self.lb.koeff_zoom_x = deepcopy(self.lb.old_koeff_zoom_x)
                self.lb.koeff_zoom_y = deepcopy(self.lb.old_koeff_zoom_y)

                self.lb.eye_radius_width = self.lb.old_eye_radius_width / 1
                self.lb.eye_radius_height = self.lb.old_eye_radius_height / 1
                self.lb.eyeball_radius_width = self.lb.old_eyeball_radius_width / 1
                self.lb.eyeball_radius_height = self.lb.old_eyeball_radius_height / 1
                self.lb.nose_radius_width = self.lb.old_nose_radius_width / 1
                self.lb.nose_radius_height = self.lb.old_nose_radius_height / 1
            elif self.number_action == 3:
                self.lb.list_x = deepcopy(self.lb.old_list_x)
                self.lb.list_y = deepcopy(self.lb.old_list_y)
                self.lb.extra_x = deepcopy(self.lb.old_extra_x)
                self.lb.extra_y = deepcopy(self.lb.old_extra_y)

            self.number_action = 0
            self.update()

    def move_image(self):
        '''
            Перемещение изображения
        '''
        try:
            move_dx = self.entry_move_dx.text()  #возвращается класс <str>
            move_dy = self.entry_move_dy.text()
            move_dx = float(move_dx); move_dy = float(move_dy)
            move_dy *= -1
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неверные входные данные")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            self.number_action = 1
            self.lb.old_list_x = deepcopy(self.lb.list_x)
            self.lb.old_list_y = deepcopy(self.lb.list_y)
            self.lb.old_extra_x = deepcopy(self.lb.extra_x)
            self.lb.old_extra_y = deepcopy(self.lb.extra_y)
            for i in range(len(self.lb.list_x)):
                self.lb.list_x[i] += float(move_dx) * self.lb.koeff_zoom_x
                self.lb.list_y[i] += float(move_dy) * self.lb.koeff_zoom_y

            for i in range(0, len(self.lb.extra_x)):
                for j in range(0, len(self.lb.extra_x[i])):
                    self.lb.extra_x[i][j] += float(move_dx) * self.lb.koeff_zoom_x
                    self.lb.extra_y[i][j] += float(move_dy) * self.lb.koeff_zoom_y

            for i in range(len(self.lb.left_eye_x)):
                self.lb.left_eye_x[i] += float(move_dx) * self.lb.koeff_zoom_x
                self.lb.left_eye_y[i] += float(move_dy) * self.lb.koeff_zoom_y
                self.lb.right_eye_x[i] += float(move_dx) * self.lb.koeff_zoom_x
                self.lb.right_eye_y[i] += float(move_dy) * self.lb.koeff_zoom_y
                self.lb.nose_x[i] += float(move_dx) * self.lb.koeff_zoom_x
                self.lb.nose_y[i] += float(move_dy) * self.lb.koeff_zoom_y
                self.lb.left_pupil_x[i] += float(move_dx) * self.lb.koeff_zoom_x
                self.lb.left_pupil_y[i] += float(move_dy) * self.lb.koeff_zoom_y
                self.lb.right_pupil_x[i] += float(move_dx) * self.lb.koeff_zoom_x
                self.lb.right_pupil_y[i] += float(move_dy) * self.lb.koeff_zoom_y

            self.update()
        
    def zoom_image(self):
        '''
            Масштабирование изображения
        '''
        try:
            if (self.lb.flag_click == False):
                zoom_dx = float(self.entry_zoom_x.text())  #возвращается класс <str>
                zoom_dy = float(self.entry_zoom_y.text())
            else:
                zoom_dx = self.lb.x
                zoom_dy = self.lb.y 
                self.lb.flag_click = False    
            temp_zoom_kx = float(self.entry_kx.text())
            temp_zoom_ky = float(self.entry_ky.text())
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неверные входные данные")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            self.number_action = 2
            temp_x = 0; temp_y = 0
            
            self.lb.old_list_x = deepcopy(self.lb.list_x)
            self.lb.old_list_y = deepcopy(self.lb.list_y)
            self.lb.old_extra_x = deepcopy(self.lb.extra_x)
            self.lb.old_extra_y = deepcopy(self.lb.extra_y)
            self.lb.old_koeff_zoom_x = deepcopy(self.lb.koeff_zoom_x)
            self.lb.old_koeff_zoom_y = deepcopy(self.lb.koeff_zoom_y)

            self.lb.koeff_zoom_x = temp_zoom_kx
            self.lb.koeff_zoom_y = temp_zoom_ky

            for i in range(0, len(self.lb.extra_x)):
                for j in range(0, len(self.lb.extra_x[i])):
                    temp_extra_x = self.lb.extra_x[i][j]; temp_extra_y = self.lb.extra_y[i][j]
                    self.lb.extra_x[i][j] = self.lb.koeff_zoom_x * temp_extra_x + zoom_dx * (1 - self.lb.koeff_zoom_x)
                    self.lb.extra_y[i][j] = self.lb.koeff_zoom_y * temp_extra_y + zoom_dy * (1 - self.lb.koeff_zoom_y)

            for i in range(len(self.lb.list_x)):
                temp_x = self.lb.list_x[i]; temp_y = self.lb.list_y[i]
                self.lb.list_x[i] = self.lb.koeff_zoom_x * temp_x + zoom_dx * (1 - self.lb.koeff_zoom_x)
                self.lb.list_y[i] = self.lb.koeff_zoom_y * temp_y + zoom_dy * (1 - self.lb.koeff_zoom_y)

            for i in range(len(self.lb.left_eye_x)):
                temp_x_left = self.lb.left_eye_x[i]; temp_y_left = self.lb.left_eye_y[i]
                temp_x_right = self.lb.right_eye_x[i]; temp_y_right = self.lb.right_eye_y[i]
                temp_x_nose = self.lb.nose_x[i]; temp_y_nose = self.lb.nose_y[i]
                temp_x_left_pupil = self.lb.left_pupil_x[i]; temp_y_left_pupil = self.lb.left_pupil_y[i]
                temp_x_right_pupil = self.lb.right_pupil_x[i]; temp_y_right_pupil = self.lb.right_pupil_y[i]; 
                self.lb.left_eye_x[i] = self.lb.koeff_zoom_x * temp_x_left + zoom_dx * (1 - self.lb.koeff_zoom_x)
                self.lb.left_eye_y[i] = self.lb.koeff_zoom_y * temp_y_left + zoom_dy * (1 - self.lb.koeff_zoom_y)
                self.lb.right_eye_x[i] = self.lb.koeff_zoom_x * temp_x_right + zoom_dx * (1 - self.lb.koeff_zoom_x)
                self.lb.right_eye_y[i] = self.lb.koeff_zoom_y * temp_y_right + zoom_dy * (1 - self.lb.koeff_zoom_y)
                self.lb.nose_x[i] = self.lb.koeff_zoom_x * temp_x_nose + zoom_dx * (1 - self.lb.koeff_zoom_x)
                self.lb.nose_y[i] = self.lb.koeff_zoom_y * temp_y_nose + zoom_dy * (1 - self.lb.koeff_zoom_y)
                self.lb.left_pupil_x[i] = self.lb.koeff_zoom_x * temp_x_left_pupil + zoom_dx * (1 - self.lb.koeff_zoom_x)
                self.lb.left_pupil_y[i] = self.lb.koeff_zoom_y * temp_y_left_pupil + zoom_dy * (1 - self.lb.koeff_zoom_y)
                self.lb.right_pupil_x[i] = self.lb.koeff_zoom_x * temp_x_right_pupil + zoom_dx * (1 - self.lb.koeff_zoom_x)
                self.lb.right_pupil_y[i] = self.lb.koeff_zoom_y * temp_y_right_pupil + zoom_dy * (1 - self.lb.koeff_zoom_y)  

            self.update()
        pass

    def rotate_image(self):
        '''
            Поворот изображения
        '''
        try:
            if (self.lb.flag_click == False):
                rotate_x = float(self.entry_rotate_x.text())
                rotate_y = float(self.entry_rotate_y.text())
            else:
                rotate_x = self.lb.x
                rotate_y = self.lb.y
                self.lb.flag_click = False
            angle = float(self.entry_angle.text())
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неверные входные данные")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            self.number_action = 3
            self.lb.old_list_x = deepcopy(self.lb.list_x)
            self.lb.old_list_y = deepcopy(self.lb.list_y)
            self.lb.old_extra_x = deepcopy(self.lb.extra_x)
            self.lb.old_extra_y = deepcopy(self.lb.extra_y)
            sin_angle = sin(radians(angle)); cos_angle = cos(radians(angle))

            temp_extra_x = 0; temp_extra_y = 0 
            for i in range(0, len(self.lb.extra_x)):
                for j in range(0, len(self.lb.extra_x[i])):
                    temp_extra_x = self.lb.extra_x[i][j]; temp_extra_y = self.lb.extra_y[i][j]
                    self.lb.extra_x[i][j] = rotate_x + (temp_extra_x - rotate_x) * cos_angle + (temp_extra_y - rotate_y) * sin_angle
                    self.lb.extra_y[i][j] = rotate_y - (temp_extra_x - rotate_x) * sin_angle + (temp_extra_y - rotate_y) * cos_angle
            temp_x = 0; temp_y = 0
            for i in range(len(self.lb.list_x)):
                temp_x = self.lb.list_x[i]; temp_y = self.lb.list_y[i]
                self.lb.list_x[i] = rotate_x + (temp_x - rotate_x) * cos_angle + (temp_y - rotate_y) * sin_angle
                self.lb.list_y[i] = rotate_y - (temp_x - rotate_x) * sin_angle + (temp_y - rotate_y) * cos_angle
            temp_x_eye = self.lb.eye_radius_width; temp_y_eye = self.lb.eye_radius_height

            for i in range(len(self.lb.left_eye_x)):
                temp_x_left = self.lb.left_eye_x[i]; temp_y_left = self.lb.left_eye_y[i]
                temp_x_right = self.lb.right_eye_x[i]; temp_y_right = self.lb.right_eye_y[i]
                temp_x_nose = self.lb.nose_x[i]; temp_y_nose = self.lb.nose_y[i]
                temp_x_left_pupil = self.lb.left_pupil_x[i]; temp_y_left_pupil = self.lb.left_pupil_y[i]
                temp_x_right_pupil = self.lb.right_pupil_x[i]; temp_y_right_pupil = self.lb.right_pupil_y[i];
                self.lb.left_eye_x[i] = rotate_x + (temp_x_left - rotate_x) * cos_angle + (temp_y_left - rotate_y) * sin_angle
                self.lb.left_eye_y[i] = rotate_y - (temp_x_left - rotate_x) * sin_angle + (temp_y_left - rotate_y) * cos_angle
                self.lb.right_eye_x[i] = rotate_x + (temp_x_right - rotate_x) * cos_angle + (temp_y_right - rotate_y) * sin_angle
                self.lb.right_eye_y[i] = rotate_y - (temp_x_right - rotate_x) * sin_angle + (temp_y_right - rotate_y) * cos_angle
                self.lb.nose_x[i] = rotate_x + (temp_x_nose - rotate_x) * cos_angle + (temp_y_nose - rotate_y) * sin_angle
                self.lb.nose_y[i] = rotate_y - (temp_x_nose - rotate_x) * sin_angle + (temp_y_nose - rotate_y) * cos_angle
                self.lb.left_pupil_x[i] = rotate_x + (temp_x_left_pupil - rotate_x) * cos_angle + (temp_y_left_pupil - rotate_y) * sin_angle
                self.lb.left_pupil_y[i] = rotate_y - (temp_x_left_pupil - rotate_x) * sin_angle + (temp_y_left_pupil - rotate_y) * cos_angle
                self.lb.right_pupil_x[i] = rotate_x + (temp_x_right_pupil - rotate_x) * cos_angle + (temp_y_right_pupil - rotate_y) * sin_angle
                self.lb.right_pupil_y[i] = rotate_y - (temp_x_right_pupil - rotate_x) * sin_angle + (temp_y_right_pupil - rotate_y) * cos_angle
            self.update()

        pass

    def draw_first_image(self):
        '''
            Прорисовка изображения в первоначальном состоянии
        '''
        self.lb.list_x = deepcopy(self.lb.first_list_x)
        self.lb.list_y = deepcopy(self.lb.first_list_y)

        self.lb.koeff_zoom_x = deepcopy(self.lb.first_koeff_zoom_x)
        self.lb.koeff_zoom_y = deepcopy(self.lb.first_koeff_zoom_y)
        self.lb.list_x = deepcopy(self.lb.first_list_x)
        self.lb.list_y = deepcopy(self.lb.first_list_y)
        self.lb.extra_x = deepcopy(self.lb.first_extra_x)
        self.lb.extra_y = deepcopy(self.lb.first_extra_y)
        self.lb.left_eye_x = deepcopy(self.lb.first_left_eye_x)
        self.lb.left_eye_y = deepcopy(self.lb.first_left_eye_y)
        self.lb.right_eye_x = deepcopy(self.lb.first_right_eye_x)
        self.lb.right_eye_y = deepcopy(self.lb.first_right_eye_y)
        self.lb.nose_x = deepcopy(self.lb.first_nose_x)
        self.lb.nose_y = deepcopy(self.lb.first_nose_y)
        self.lb.left_pupil_x = deepcopy(self.lb.first_left_pupil_x)
        self.lb.left_pupil_y = deepcopy(self.lb.first_left_pupil_y)
        self.lb.right_pupil_x = deepcopy(self.lb.first_right_pupil_x)
        self.lb.right_pupil_y = deepcopy(self.lb.first_right_pupil_y)
        self.number_action = 0       
        self.update()

if __name__ == "__main__":
    #создание окна
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()

    #показ и нормальное завершение окна
    
    sys.exit(app.exec_())
