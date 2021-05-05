#Большая подстава в питоне с округленем - округление до ближайшего четного
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPolygon, QPainterPath, QMouseEvent, QColor
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QPushButton, QLabel, QGraphicsScene,\
                            QGraphicsView, QWidget, QMenu, QMainWindow, QAction, QColorDialog
import sys, lab_03_ui, step
from math import trunc, fabs, radians, cos, sin
from time import monotonic
import matplotlib.pyplot as plt
import numpy as np

class Second_window(QWidget):
    FONT = "Times New Roman"
    SIZE = 14
    LAB_TEXT = ("РЕАЛИЗАЦИЯ И ИССЛЕДОВАНИЕ АЛГОРИТМОВ ПОСТРОЕНИЯ ОТРЕЗКОВ.\n" +
                "1. Реализовать следующие алгоритмы построения отрезков \n"+
                "(предоставить пользователю возможность выбора алгоритма, \n"+
                "задания координат начала и конца отрезка, выбора цвета рисования)\n"+
                "-Алгоритм, использующий библиотечную функцию;\n"+
                "-Алгоритм цифрового дифференциального анализатора;\n"+ 
                "-Алгоритм Брезенхема с действительными данными;\n" +
                "-Алгоритм Брезенхема с целочисленными данными;\n" +
                "-Алгоритм Брезенхема с устранением ступенчатости;\n" +
                "-Алгоритм Ву.\n"+
                "2. Исследование визуальных характеристик при выводе отрезков заданной длины в заданном\n"+
                "спектре углов с помощью одного из алгоритмов и наложения на полученный результат отрезков,\n"+
                "построенных с помощью другого алгоритма (цветом фона).\n"+
                "3. Исследование временных характеристик алгоритмов (результат вывести в виде гистограммы).\n"+
                "4. Исследование ступенчатости отрезков. (результат визуализировать в виде графика зависимости\n"+
                "длины ступеньки или количества ступенек в зависимости от угла наклона отрезка, вывести для\n"+
                "справки длину отрезка).")
    def __init__(self):
        super(Second_window, self).__init__()
        self.setWindowTitle('Справка')
        self.resize(800, 600)

        #установка шрифта, его размера 
        font = QtGui.QFont()
        font.setFamily(Second_window.FONT); font.setPointSize(Second_window.SIZE)
        self.setFont(font)

        self.create_UI_second()

    def create_UI_second(self):
        self.label_info = QLabel(self)
        self.label_info.setGeometry(QtCore.QRect(5, 10, 800, 600))
        self.label_info.setText(Second_window.LAB_TEXT)

class MyFrame():
    def __init__(self, parent):
        super().__init__()

        self.start_x = 0; self.start_y = 0
        self.end_x = 0; self.end_y = 0
        self.vu_start_x = 0; self.vu_start_y = 0
        self.vu_end_x = 0; self.vu_end_y = 0

class Main_window(QMainWindow, lab_03_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.number_action = 0
        self.setupUi(self)
        self.lb = MyFrame(self)
        self.create_menu()
        self.add_to_ui()
        self.add_functions()
        self.show()
        self.add_items_to_algorithm()
        self.add_items_to_colour()
        self.set_values_to_edit()

    def add_to_ui(self):
        scene = QGraphicsScene(self)
        self.graphicsView.setScene(scene)
        scene.setSceneRect(10, 10, 1500, 920)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene = scene
        self.pen = QPen(Qt.black, 1)
        

    def create_menu(self):
        '''
            Создание меню
        '''
        #создание панели меню
        window_menu = self.menuBar()
        file = window_menu.addMenu('Файл')
        analyse = window_menu.addMenu('Анализ')
      
        #создание подменю
        info = QAction("Справка", self)
        analyse_time = QAction("Времени", self)
        analyse_step = QAction("Ступенчатости", self)

        info.triggered.connect(self.create_info_window)
        analyse_time.triggered.connect(self.output_analyse_time)
        analyse_step.triggered.connect(self.output_analyse_step)

        file.addAction(info)
        analyse.addAction(analyse_time)
        analyse.addAction(analyse_step)

    def create_info_window(self):
        '''
        Создание окна со справкой
        '''
        self.info_window = Second_window()
        self.info_window.show()

    def add_items_to_algorithm(self):
        '''
        Добавление выбора алгоритма
        '''
        self.combo_algorithm.addItem("Библиотечная функция")
        self.combo_algorithm.addItem("Цифровой дифференциальный анализатор")
        self.combo_algorithm.addItem("Брезенхема с действительными данными")
        self.combo_algorithm.addItem("Брезенхема с целочисленными данными")
        self.combo_algorithm.addItem("Брезенхема с устранением ступенчатости")
        self.combo_algorithm.addItem("Ву")

    def set_values_to_edit(self):
        '''
        Установить значения в поля ввода
        '''
        self.edit_start_x.setText("0")
        self.edit_start_y.setText("0")
        self.edit_end_x.setText("0")
        self.edit_end_y.setText("0")

    def add_items_to_colour(self):
        '''
        Добавление выбора цвета
        '''
        self.combo_colour.addItem("Красный")
        self.combo_colour.addItem("Оранжевый")
        self.combo_colour.addItem("Синий")
        self.combo_colour.addItem("Фиолетовый")
        self.combo_colour.addItem("Черный")
        self.combo_colour.addItem("Желтый")
        self.combo_colour.addItem("Белый")

    def add_functions(self):
        '''
        Функции, выполняемые при нажатии кнопок
        '''
        self.button_process.clicked.connect(lambda: self.build_line())
        self.button_clean.clicked.connect(self.scene.clear)
        self.button_build_spectrum.clicked.connect(lambda: self.build_spectrum_lines())

    def draw_point(self, x, y):
        '''
        Отрисовка точки
        '''
        self.scene.addLine(x, y, x, y, self.pen)

    def draw_line_library(self, x_start, y_start, x_end, y_end):
        '''
        Отрисовка линии
        '''
        self.scene.addLine(x_start, y_start, x_end, y_end, self.pen)

    def set_brightness(self, brightness):
        '''
        Установить яркость цвета
        '''
        colour = self.pen.color()
        colour.setAlpha(int(brightness))
        self.pen.setColor(colour)

    def choose_colour_pen(self, colour):
        '''
        Выбор цвета отрисовки
        '''
        if colour == 'Красный':
            self.pen.setColor(Qt.red)
        elif colour == 'Оранжевый':
            self.pen.setColor(QColor(255,140,0))
        elif colour == 'Синий':
            self.pen.setColor(Qt.darkBlue)
        elif colour == 'Фиолетовый':
            self.pen.setColor(Qt.darkMagenta)
        elif colour == 'Черный':
            self.pen.setColor(Qt.black)
        elif colour == 'Желтый':
            self.pen.setColor(Qt.yellow)
        elif colour == 'Зеленый':
            self.pen.setColor(Qt.green)
        elif colour == 'Белый':
            self.pen.setColor(Qt.white)


    def build_line(self):
        '''
        Определение метода построения отрезка
        '''
        select_algorithm = self.combo_algorithm.currentText()
        select_colour = self.combo_colour.currentText()
        try:
            self.lb.start_x = float(self.edit_start_x.text())
            self.lb.start_y = float(self.edit_start_y.text())
            self.lb.end_x = float(self.edit_end_x.text()) 
            self.lb.end_y = float(self.edit_end_y.text())     
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неверные входные данные")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            flag_table = 0
            self.choose_method(self.lb.start_x, self.lb.start_y, self.lb.end_x, self.lb.end_y,
                                select_algorithm, select_colour, flag_table)

    def choose_method(self, x_start, y_start, x_end, y_end, select_algorithm, select_colour, flag_table):
        '''
        Выбор метода построения
        '''
        self.choose_colour_pen(select_colour)
        if (select_algorithm == 'Библиотечная функция'):
            self.draw_line_library(x_start, y_start, x_end, y_end)
        elif (select_algorithm == 'Цифровой дифференциальный анализатор'):
            self.create_line_by_digital_differential_analyzer(x_start, y_start,
                                                                x_end, y_end, flag_table)
        elif (select_algorithm == 'Брезенхема с действительными данными'):
            self.create_line_by_brezenham_with_float_data(x_start, y_start,
                                                            x_end, y_end, flag_table)
        elif (select_algorithm == 'Брезенхема с целочисленными данными'):
            self.create_line_by_brezenham_with_int_data(x_start, y_start,
                                                        x_end, y_end, flag_table)
        elif select_algorithm == 'Брезенхема с устранением ступенчатости':
            self.create_line_by_brezenham_with_step_removal(x_start, y_start,
                                                            x_end, y_end, flag_table)
        elif select_algorithm == 'Ву':
            self.create_line_by_vu(x_start, y_start, x_end, y_end, flag_table)

    def create_line_by_digital_differential_analyzer(self, x_start, y_start, x_end, y_end, flag_table):
        '''
        Цифровой дифференциальный анализатор
        '''
        if (x_start == x_end) and (y_start == y_end):
            if flag_table == 0: self.draw_point(x_start, y_start)
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
                if flag_table == 0: self.draw_point(x_draw, y_draw)
                x += dx; y += dy
                i += 1

    def create_line_by_brezenham_with_float_data(self, x_start, y_start, x_end, y_end, flag_table):
        '''
        Алгоритм Брезенхема с действительными данными
        '''
        if (x_start == x_end) and (y_start == y_end):
            if flag_table == 0: self.draw_point(x_start, y_start)
        else:
            dx = x_end - x_start; dy = y_end - y_start
            sx = self.sign(dx); sy = self.sign(dy)
            dx = abs(dx); dy = abs(dy)
            if dx > dy:
                flag_exchange = 0
            else:
                dx, dy = dy, dx
                flag_exchange = 1
            m = dy / dx
            f = m - 0.5

            x_temp = x_start; y_temp = y_start
            i = 0
            while i <= dx:
                if flag_table == 0: self.draw_point(x_temp, y_temp)
                if f > 0:
                    if flag_exchange == 1:
                        x_temp += sx
                    else:
                        y_temp += sy
                    f -= 1
                if f <= 0:
                    if flag_exchange == 1:
                        y_temp += sy
                    else:
                        x_temp += sx
                f += m
                i += 1


    def create_line_by_brezenham_with_int_data(self, x_start, y_start, x_end, y_end, flag_table):
        '''
        Алгоритм Брезенхема с целочисленными данными
        '''
        if (x_start == x_end) and (y_start == y_end):
            if flag_table == 0: self.draw_point(x_start, y_start)
        else:
            dx = x_end - x_start; dy = y_end - y_start
            sx = self.sign(dx); sy = self.sign(dy)
            dx = abs(dx); dy = abs(dy)
            if dx > dy:
                flag_exchange = 0
            else:
                dx, dy = dy, dx
                flag_exchange = 1
            m = dy/dx
            f = 2 * dy - dx

            x_temp = x_start; y_temp = y_start
            i = 0
            while i <= dx:
                if flag_table == 0: self.draw_point(x_temp, y_temp)
                if f >= 0:
                    if flag_exchange == 1:
                        x_temp += sx
                    else:
                        y_temp += sy
                    f -= 2 * dx
                if f < 0:
                    if flag_exchange == 1:
                        y_temp += sy
                    else:
                        x_temp += sx
                f += 2 * dy
                i += 1

    def create_line_by_brezenham_with_step_removal(self, x_start, y_start, x_end, y_end, flag_table):
        '''
        Алгоритм Брезенхема с устранением ступенчатости
        '''
        if x_start == x_end and y_start == y_end:
            if flag_table == 0: self.draw_point(x_start, y_start)
        else:
            # Количество уровней интенсивности
            I = 255
            dx = x_end - x_start; dy = y_end - y_start
            sx = self.sign(dx); sy = self.sign(dy)
            dx = abs(dx); dy = abs(dy)
            if dx != 0:
                m = dy/dx
            else:
                m = 0
            
            if dx > dy:
                flag_exchange = 0
            else:
                dx, dy = dy, dx
                flag_exchange = 1
                if m != 0:
                    m = 1 / m
            f = I / 2
            x_temp = x_start; y_temp = y_start
            m *= I
            w = I - m

            i = 0
            while i <= dx:
                if flag_table == 0:
                    self.set_brightness(255 - f)
                    self.draw_point(x_temp, y_temp)
                if f <= w:
                    if flag_exchange == 0:
                        x_temp += sx
                    if flag_exchange == 1:
                        y_temp += sy
                    f += m
                else:
                    x_temp += sx; y_temp += sy; f-= w
                i += 1
            if flag_table == 0: self.set_brightness(I)

    def create_line_by_vu(self, x_start, y_start, x_end, y_end, flag_table):
        '''
        Алгоритм Ву
        '''
        if (x_start == x_end) and (y_start == y_end):
            if flag_table == 0: self.draw_point(x_start, y_start)
        else:
            dx = x_end - x_start; dy = y_end - y_start

            flag_exchange = 0
            if abs(dx) < abs(dy):
                flag_exchange = 1
                x_start, y_start = y_start, x_start
                x_end, y_end = y_end, x_end
                dx, dy = dy, dx
            
            if x_end < x_start:
                x_start, x_end = x_end, x_start
                y_start, y_end = y_end, y_start
            
            m = 0
            if dx != 0:
                m = dy / dx
            
            y = y_start; x = x_start
            I = 255
            while x <= x_end:
                if flag_exchange == 1:
                    sign_y = self.sign(y)
                    if flag_table == 0:
                        brightness = I - I * (fabs(y - int(y)))
                        self.set_brightness(brightness)
                        self.draw_point(y, x)

                    if dy != 0 and dx != 0:
                        if flag_table == 0:
                            brightness = I - I * (fabs(y - int(y)))
                            self.set_brightness(brightness)
                            self.draw_point(y, x)
                    
                    if flag_table == 0: self.draw_point(y + sign_y, x)
                else:    
                    sign_y = self.sign(y)
                    if flag_table == 0:
                        brightness = I - I * (fabs(y - int(y)))
                        self.set_brightness(brightness)
                        self.draw_point(x, y)

                    if dy != 0 and dx != 0:
                        if flag_table == 0:
                            brightness = I - I * (fabs(y - int(y)))
                            self.set_brightness(brightness)
                            self.draw_point(x, y)
                    if flag_table == 0: self.draw_point(x, y + sign_y)
                y += m; x += 1
            
            self.set_brightness(I)     

    def sign(self, x):
        value = 0
        if x > 0:
            value = 1
        elif x == 0:
            value = 0
        else:
            value = -1
        return value

    def build_spectrum_lines(self):
        select_algorithm = self.combo_algorithm.currentText()
        select_colour = self.combo_colour.currentText()
        try:
            length = int(self.edit_length.text())
            angle = int(self.edit_angle.text())
            if length == 0:
                raise ZeroError
            elif angle <= 0 or angle > 360:
                raise AngleError
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неверные входные данные. Значение должно быть целочисленным.")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        except ZeroError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неверные входные данные. Значение должно быть положительным.")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        except AngleError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неверный угол.")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Что-то пошло не так...")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            x_start = 750; y_start = 410; flag_table = 0
            for i in range(0, 360+1, angle):
                rotate_x = cos(radians(i)) * length + x_start
                rotate_y = sin(radians(i)) * length + y_start

                self.choose_method(x_start, y_start, rotate_x, rotate_y, select_algorithm,
                                    select_colour, flag_table)

    def output_analyse_time(self):
        try:
            self.lb.start_x = float(self.edit_start_x.text())
            self.lb.start_y = float(self.edit_start_y.text())
            self.lb.end_x = float(self.edit_end_x.text()) 
            self.lb.end_y = float(self.edit_end_y.text())     
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неверные входные данные")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            x_start = self.lb.start_x; y_start = self.lb.start_y
            x_end = self.lb.end_x; y_end = self.lb.end_y
            flag_table = 1
            times = []

            start_time = monotonic()
            self.create_line_by_digital_differential_analyzer(x_start, y_start, x_end, y_end, flag_table)
            end_time = monotonic()
            times.append(end_time - start_time)

            start_time = monotonic()
            self.create_line_by_brezenham_with_float_data(x_start, y_start, x_end, y_end, flag_table)
            end_time = monotonic()
            times.append(end_time - start_time)

            start_time = monotonic()
            self.create_line_by_brezenham_with_int_data(x_start, y_start, x_end, y_end, flag_table)
            end_time = monotonic()
            times.append(end_time - start_time)

            start_time = monotonic()
            self.create_line_by_brezenham_with_step_removal(x_start, y_start, x_end, y_end, flag_table)
            end_time = monotonic()
            times.append(end_time - start_time)

            start_time = monotonic()
            self.create_line_by_vu(x_start, y_start, x_end, y_end, flag_table)
            end_time = monotonic()
            times.append(end_time - start_time)

            names = ['Цифровой\nдифф.анализатор', 'Брезенхем с\nдействительными',
                     'Брезенхем с\nцелочисленными', 'Брезенхем с\nустранением\nступенчатости', 'Ву']
            print(times)
            plt.subplots(figsize=(15,9))
            plt.title('Сравнение скорости алгоритмов')
            plt.bar(names, times, align='center')
            plt.xlabel('Алгоритм')
            plt.ylabel('Время, мс', labelpad = 30)
            plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
            plt.show()
    
    def output_analyse_step(self):
        length = 200; angle = 15
        count_steps = []; len_stairs = []
        x_start = 750; y_start = 410; flag_table = 0
        temp_count = 0; temp_len = 0
        i = 0
        for j in range(angle, 45+1, angle):
            count_steps.append([]); len_stairs.append([])
            rotate_x = cos(radians(j)) * length + x_start
            rotate_y = sin(radians(j)) * length + y_start

            temp_count, temp_len = step.analyze_step_digital_differential_analyzer(x_start, y_start, rotate_x, rotate_y, flag_table)
            count_steps[i].append(temp_count); len_stairs[i].append(temp_len)

            temp_count, temp_len = step.analyze_step_by_brezenham_with_float_data(x_start, y_start, rotate_x, rotate_y, flag_table)
            count_steps[i].append(temp_count); len_stairs[i].append(temp_len)

            temp_count, temp_len = step.analyze_step_by_brezenham_with_int_data(x_start, y_start, rotate_x, rotate_y, flag_table)
            count_steps[i].append(temp_count); len_stairs[i].append(temp_len)

            temp_count, temp_len = step.analyze_step_by_brezenham_with_step_removal(x_start, y_start, rotate_x, rotate_y, flag_table)
            count_steps[i].append(temp_count); len_stairs[i].append(temp_len)

            temp_count, temp_len = step.analyze_step_by_vu(x_start, y_start, rotate_x, rotate_y, flag_table)
            count_steps[i].append(temp_count); len_stairs[i].append(temp_len)
        
            i += 1
        
        fig, ax = plt.subplots(2, 1,figsize=(15,9))
        width = 0.1
        data_count = np.asarray(count_steps); data_len = np.asarray(len_stairs)
        angles = np.arange(len(data_count))
        
        x_labels = ['15', '30', '45']
        names = ['Цифровой\nдифф.анализатор', 'Брезенхем с\nдействительными',
                     'Брезенхем с\nцелочисленными', 'Брезенхем с\nустранением\nступенчатости', 'Ву']
        
        ax[0].bar(angles, data_count[:,0], width=0.1, color = '#003385')
        ax[0].bar(angles + (1 * width), data_count[:,1], width=0.1, color = '#0046b8')
        ax[0].bar(angles + (2 * width), data_count[:,2], width=0.1, color = '#005aeb')
        ax[0].bar(angles + (3 * width), data_count[:,3], width=0.1, color = '#1f75ff')
        ax[0].bar(angles + (4 * width), data_count[:,4], width=0.1, color = '#5294ff')

        ax[1].bar(angles, data_len[:,0], width=0.1, color = '#003385')
        ax[1].bar(angles + (1 * width), data_len[:,1], width=0.1, color = '#0046b8')
        ax[1].bar(angles + (2 * width), data_len[:,2], width=0.1, color = '#005aeb')
        ax[1].bar(angles + (3 * width), data_len[:,3], width=0.1, color = '#1f75ff')
        ax[1].bar(angles + (4 * width), data_len[:,4], width=0.1, color = '#5294ff')
        
        ax[0].set_xticklabels(x_labels)
        ax[1].set_xticklabels(x_labels)

        ax[0].set_title('Зависимость количества ступенек от угла наклона')
        ax[0].set_title('Зависимость максимальной длины ступеньки от угла наклона')

        ax[0].legend(names, bbox_to_anchor=(1, 0.6))
        ax[1].legend(names, bbox_to_anchor=(1, 0.6))

        ax[0].set_xticks(angles + 2 * width)
        ax[1].set_xticks(angles + 2 * width)

        ax[0].set_xticklabels(x_labels)
        ax[1].set_xticklabels(x_labels)

        ax[0].set_ylabel('Количество ступенек', labelpad = 30)
        ax[1].set_ylabel('Максимальная длина ступеньки', labelpad = 30)

        ax[0].grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
        ax[1].grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

        fig.tight_layout()
        plt.show()

if __name__ == "__main__":
    #создание окна"
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()

    #показ и нормальное завершение окна
    sys.exit(app.exec_())