# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lab_07.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_colour_segment = QtWidgets.QLabel(self.centralwidget)
        self.label_colour_segment.setStyleSheet("background-color: #ffa500")
        self.label_colour_segment.setText("")
        self.label_colour_segment.setObjectName("label_colour_segment")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_colour_segment)
        self.label_colour_cut_off = QtWidgets.QLabel(self.centralwidget)
        self.label_colour_cut_off.setStyleSheet("background-color: #56de47")
        self.label_colour_cut_off.setText("")
        self.label_colour_cut_off.setObjectName("label_colour_cut_off")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_colour_cut_off)
        self.label_colour_result = QtWidgets.QLabel(self.centralwidget)
        self.label_colour_result.setStyleSheet("background-color: #0079db")
        self.label_colour_result.setText("")
        self.label_colour_result.setObjectName("label_colour_result")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_colour_result)
        self.but_input_cut_off = QtWidgets.QPushButton(self.centralwidget)
        self.but_input_cut_off.setObjectName("but_input_cut_off")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.but_input_cut_off)
        self.but_cut_off = QtWidgets.QPushButton(self.centralwidget)
        self.but_cut_off.setObjectName("but_cut_off")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.but_cut_off)
        spacerItem = QtWidgets.QSpacerItem(50, 209, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.formLayout.setItem(6, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.verticalLayout.addLayout(self.formLayout)
        self.but_clean_all = QtWidgets.QPushButton(self.centralwidget)
        self.but_clean_all.setObjectName("but_clean_all")
        self.verticalLayout.addWidget(self.but_clean_all)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Цвет"))
        self.label_2.setText(_translate("MainWindow", "Линии"))
        self.label_3.setText(_translate("MainWindow", "Отсекатель"))
        self.label_4.setText(_translate("MainWindow", "Результат"))
        self.but_input_cut_off.setText(_translate("MainWindow", "Ввод отсекателя"))
        self.but_cut_off.setText(_translate("MainWindow", "Отсечь"))
        self.but_clean_all.setText(_translate("MainWindow", "Очистить всё"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
