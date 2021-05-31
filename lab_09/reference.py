from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import reference_ui
import sys

class DialogMenu(QMainWindow, reference_ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        

    def open_reference_window(self):
        self.show()
        sys.exit(self.exec_())
        #self.exec_()
