# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton,
    QSizePolicy, QSpinBox, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(859, 523)
        self.FindAdapter = QPushButton(Widget)
        self.FindAdapter.setObjectName(u"FindAdapter")
        self.FindAdapter.setGeometry(QRect(50, 50, 151, 51))
        self.Combo_Adapter = QComboBox(Widget)
        self.Combo_Adapter.setObjectName(u"Combo_Adapter")
        self.Combo_Adapter.setGeometry(QRect(240, 100, 181, 31))
        self.pushButton_open = QPushButton(Widget)
        self.pushButton_open.setObjectName(u"pushButton_open")
        self.pushButton_open.setGeometry(QRect(50, 130, 151, 41))
        self.Combo_Slaves = QComboBox(Widget)
        self.Combo_Slaves.setObjectName(u"Combo_Slaves")
        self.Combo_Slaves.setGeometry(QRect(250, 200, 181, 31))
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(70, 210, 141, 21))
        self.pushButton_move = QPushButton(Widget)
        self.pushButton_move.setObjectName(u"pushButton_move")
        self.pushButton_move.setGeometry(QRect(240, 380, 121, 41))
        self.pushButton_Close = QPushButton(Widget)
        self.pushButton_Close.setObjectName(u"pushButton_Close")
        self.pushButton_Close.setGeometry(QRect(440, 130, 151, 41))
        self.spinBox_TargetVelocity = QSpinBox(Widget)
        self.spinBox_TargetVelocity.setObjectName(u"spinBox_TargetVelocity")
        self.spinBox_TargetVelocity.setGeometry(QRect(130, 260, 111, 31))
        self.spinBox_TargetVelocity.setMaximum(100000)
        self.spinBox_TargetVelocity.setValue(5000)
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 260, 141, 31))
        self.pushButton_Stop = QPushButton(Widget)
        self.pushButton_Stop.setObjectName(u"pushButton_Stop")
        self.pushButton_Stop.setGeometry(QRect(470, 380, 121, 41))
        self.CloseB = QPushButton(Widget)
        self.CloseB.setObjectName(u"CloseB")
        self.CloseB.setGeometry(QRect(720, 0, 131, 51))
        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(260, 260, 101, 31))
        self.label_4 = QLabel(Widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(480, 268, 131, 20))
        self.ModeOfOperation = QComboBox(Widget)
        self.ModeOfOperation.setObjectName(u"ModeOfOperation")
        self.ModeOfOperation.setGeometry(QRect(610, 260, 191, 31))
        self.ApplySetB = QPushButton(Widget)
        self.ApplySetB.setObjectName(u"ApplySetB")
        self.ApplySetB.setGeometry(QRect(360, 310, 131, 41))
        self.spinBox_TargetTorque = QSpinBox(Widget)
        self.spinBox_TargetTorque.setObjectName(u"spinBox_TargetTorque")
        self.spinBox_TargetTorque.setGeometry(QRect(370, 260, 101, 31))
        self.spinBox_TargetTorque.setMaximum(1000)
        self.spinBox_TargetTorque.setValue(250)
        self.pushButton_move_2 = QPushButton(Widget)
        self.pushButton_move_2.setObjectName(u"pushButton_move_2")
        self.pushButton_move_2.setGeometry(QRect(240, 450, 121, 41))
        self.pushButton_Stop_2 = QPushButton(Widget)
        self.pushButton_Stop_2.setObjectName(u"pushButton_Stop_2")
        self.pushButton_Stop_2.setGeometry(QRect(470, 450, 121, 41))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.FindAdapter.setText(QCoreApplication.translate("Widget", u"Find Adapter", None))
        self.pushButton_open.setText(QCoreApplication.translate("Widget", u"Open EtherCat", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Servo drivers", None))
        self.pushButton_move.setText(QCoreApplication.translate("Widget", u"move", None))
        self.pushButton_Close.setText(QCoreApplication.translate("Widget", u"Close EtherCat", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"Target Velocity", None))
        self.pushButton_Stop.setText(QCoreApplication.translate("Widget", u"Stop", None))
        self.CloseB.setText(QCoreApplication.translate("Widget", u"Close", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Target Torque", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Mode of Operation", None))
        self.ApplySetB.setText(QCoreApplication.translate("Widget", u"Apply Settings", None))
        self.pushButton_move_2.setText(QCoreApplication.translate("Widget", u"move 2", None))
        self.pushButton_Stop_2.setText(QCoreApplication.translate("Widget", u"Stop 2", None))
    # retranslateUi

