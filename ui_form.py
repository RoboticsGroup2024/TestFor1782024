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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        self.SearchB = QPushButton(Widget)
        self.SearchB.setObjectName(u"SearchB")
        self.SearchB.setGeometry(QRect(390, 60, 161, 111))
        self.textE = QPlainTextEdit(Widget)
        self.textE.setObjectName(u"textE")
        self.textE.setGeometry(QRect(570, 60, 211, 341))
        self.CloseB = QPushButton(Widget)
        self.CloseB.setObjectName(u"CloseB")
        self.CloseB.setGeometry(QRect(320, 365, 101, 61))
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 30, 271, 21))
        self.masterLE = QLineEdit(Widget)
        self.masterLE.setObjectName(u"masterLE")
        self.masterLE.setGeometry(QRect(20, 50, 271, 31))
        self.OpenB = QPushButton(Widget)
        self.OpenB.setObjectName(u"OpenB")
        self.OpenB.setGeometry(QRect(70, 100, 141, 71))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.SearchB.setText(QCoreApplication.translate("Widget", u"Search", None))
        self.CloseB.setText(QCoreApplication.translate("Widget", u"Close", None))
        self.label.setText(QCoreApplication.translate("Widget", u"After Serch, Write the name of the slave", None))
        self.OpenB.setText(QCoreApplication.translate("Widget", u"Open", None))
    # retranslateUi

