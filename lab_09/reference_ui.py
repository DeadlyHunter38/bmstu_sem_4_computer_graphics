# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reference.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 412)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(9, 9, 421, 19))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 621, 91))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 611, 91))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 270, 391, 71))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Справка"))
        self.label_2.setText(_translate("Form", "Справка по работе с приложением"))
        self.label_3.setText(_translate("Form", "Ввод исходного многоугольника:\n"
"     1. Нажать на кнопку \"Многоугольник\". \n"
"     2. Щелнуть мышкой по экрану ввода (постепенно будут появляться отрезки). \n"
"     3. Нажать на ПКМ - замкнуть фигуру."))
        self.label_4.setText(_translate("Form", "Ввод отсекателя (многоугольник):\n"
"      1. Нажать на кнопку \"Отсекатель\". \n"
"     2. Щелнуть мышкой по экрану ввода (постепенно будут появляться отрезки). \n"
"     3. Нажать на ПКМ - замкнуть фигуру."))
        self.label_5.setText(_translate("Form", "Отсечение:\n"
"     1.Ввести произвольный многоугольник\n"
"     2.Ввести отсекатель (выпуклый многоугольник)\n"
"     3.Нажать на кнопку \"Отсечь\""))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
