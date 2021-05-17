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
        print(f"here_cut_off")
        self.but_input_segments.setStyleSheet("background-color: #cccccc")
        self.but_input_cut_off.setStyleSheet("background-color: #ffffff")
        self.graph.flag_input_cut_off = True
        self.graph.flag_input_segments = False
        print(f"self.graph.flag_input_cut_off = {self.graph.flag_input_cut_off}")
        print(f"self.graph.flag_input_segments = {self.graph.flag_input_segments}")
        pass

    def do_cut_off(self):
        """
        Выполнение отсечения
        """
        self.but_input_segments.setStyleSheet("background-color: #cccccc")
        self.but_input_cut_off.setStyleSheet("background-color: #cccccc")
        pass

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
        self.graph.rectangle = None
        self.graph.flag_input_cut_off = False

        self.image = QImage(int(self.graph.width()), int(self.graph.height()), QImage.Format_ARGB32_Premultiplied)
        self.image.fill(self.bg_colour)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    sys.exit(app.exec_())