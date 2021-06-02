from PyQt5.QtWidgets import QMainWindow, QGraphicsScene

import lab_10_ui

class ScreenImage(QGraphicsScene, QMainWindow, lab_10_ui.Ui_MainWindow):
    def __init__(self):
        '''
        Конструктор
        '''
        super().__init__()