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
        MainWindow.resize(768, 501)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(12, -1, 9, -1)
        self.formLayout.setHorizontalSpacing(33)
        self.formLayout.setVerticalSpacing(7)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setStyleSheet("background-color: #ffa500")
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_colour_segment = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_colour_segment.sizePolicy().hasHeightForWidth())
        self.label_colour_segment.setSizePolicy(sizePolicy)
        self.label_colour_segment.setStyleSheet("background-color: #ffa500")
        self.label_colour_segment.setText("")
        self.label_colour_segment.setObjectName("label_colour_segment")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_colour_segment)
        self.label_colour_cut_off = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_colour_cut_off.sizePolicy().hasHeightForWidth())
        self.label_colour_cut_off.setSizePolicy(sizePolicy)
        self.label_colour_cut_off.setStyleSheet("background-color: #56de47")
        self.label_colour_cut_off.setText("")
        self.label_colour_cut_off.setObjectName("label_colour_cut_off")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_colour_cut_off)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_colour_result = QtWidgets.QLabel(self.centralwidget)
        self.label_colour_result.setStyleSheet("background-color: #0079db")
        self.label_colour_result.setText("")
        self.label_colour_result.setObjectName("label_colour_result")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.label_colour_result)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.but_clean_all = QtWidgets.QPushButton(self.centralwidget)
        self.but_clean_all.setObjectName("but_clean_all")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.but_clean_all)
        spacerItem = QtWidgets.QSpacerItem(20, 278, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(7, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.but_cut_off = QtWidgets.QPushButton(self.centralwidget)
        self.but_cut_off.setObjectName("but_cut_off")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.but_cut_off)
        self.but_input_cut_off = QtWidgets.QPushButton(self.centralwidget)
        self.but_input_cut_off.setObjectName("but_input_cut_off")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.but_input_cut_off)
        self.horizontalLayout.addLayout(self.formLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 768, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "Линии"))
        self.label_4.setText(_translate("MainWindow", "Отсекатель"))
        self.label_7.setText(_translate("MainWindow", "Результат"))
        self.label_2.setText(_translate("MainWindow", "Цвет"))
        self.but_clean_all.setText(_translate("MainWindow", "Очистить всё"))
        self.but_cut_off.setText(_translate("MainWindow", "Отсечь"))
        self.but_input_cut_off.setText(_translate("MainWindow", "Ввод отсекателя"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
