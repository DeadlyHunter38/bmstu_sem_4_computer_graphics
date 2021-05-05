# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lab_05.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(958, 637)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setToolTipDuration(0)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.graphview = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphview.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphview.sizePolicy().hasHeightForWidth())
        self.graphview.setSizePolicy(sizePolicy)
        self.graphview.setMinimumSize(QtCore.QSize(0, 0))
        self.graphview.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphview.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphview.setObjectName("graphview")
        self.horizontalLayout_2.addWidget(self.graphview)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(0, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.label)
        self.but_choose_colour = QtWidgets.QPushButton(self.centralwidget)
        self.but_choose_colour.setObjectName("but_choose_colour")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.but_choose_colour)
        self.label_colour = QtWidgets.QLabel(self.centralwidget)
        self.label_colour.setStyleSheet("background-color: #000000")
        self.label_colour.setText("")
        self.label_colour.setObjectName("label_colour")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_colour)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.SpanningRole, spacerItem1)
        self.label_sleep = QtWidgets.QLabel(self.centralwidget)
        self.label_sleep.setObjectName("label_sleep")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_sleep)
        self.radiobut_is_sleep = QtWidgets.QRadioButton(self.centralwidget)
        self.radiobut_is_sleep.setObjectName("radiobut_is_sleep")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.radiobut_is_sleep)
        self.radiobut_no_sleep = QtWidgets.QRadioButton(self.centralwidget)
        self.radiobut_no_sleep.setObjectName("radiobut_no_sleep")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.radiobut_no_sleep)
        self.but_fill = QtWidgets.QPushButton(self.centralwidget)
        self.but_fill.setObjectName("but_fill")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.but_fill)
        self.verticalLayout.addLayout(self.formLayout)
        self.but_clean_all = QtWidgets.QPushButton(self.centralwidget)
        self.but_clean_all.setObjectName("but_clean_all")
        self.verticalLayout.addWidget(self.but_clean_all)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Алгоритм заполнения с перегородкой"))
        self.but_choose_colour.setText(_translate("MainWindow", "Выбрать цвет"))
        self.label_sleep.setText(_translate("MainWindow", "Задержка отрисовки"))
        self.radiobut_is_sleep.setText(_translate("MainWindow", "С задержкой"))
        self.radiobut_no_sleep.setText(_translate("MainWindow", "Без задержки"))
        self.but_fill.setText(_translate("MainWindow", "Заполнить"))
        self.but_clean_all.setText(_translate("MainWindow", "Очистить всё"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
