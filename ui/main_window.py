# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowYcnIsU.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(917, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.plotWidget = PlotWidget(self.centralwidget)
        self.plotWidget.setObjectName(u"plotWidget")

        self.gridLayout_2.addWidget(self.plotWidget, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButtonConnect = QPushButton(self.centralwidget)
        self.pushButtonConnect.setObjectName(u"pushButtonConnect")

        self.verticalLayout.addWidget(self.pushButtonConnect)

        self.pushButtonStart = QPushButton(self.centralwidget)
        self.pushButtonStart.setObjectName(u"pushButtonStart")
        self.pushButtonStart.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButtonStart)

        self.pushButtonStop = QPushButton(self.centralwidget)
        self.pushButtonStop.setObjectName(u"pushButtonStop")
        self.pushButtonStop.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButtonStop)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelDevice = QLabel(self.centralwidget)
        self.labelDevice.setObjectName(u"labelDevice")

        self.horizontalLayout.addWidget(self.labelDevice)

        self.labelDeviceName = QLabel(self.centralwidget)
        self.labelDeviceName.setObjectName(u"labelDeviceName")

        self.horizontalLayout.addWidget(self.labelDeviceName)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBoxAccelerometerScale = QComboBox(self.centralwidget)
        self.comboBoxAccelerometerScale.setObjectName(u"comboBoxAccelerometerScale")
        self.comboBoxAccelerometerScale.setEnabled(False)

        self.gridLayout.addWidget(self.comboBoxAccelerometerScale, 0, 1, 1, 1)

        self.labelGyroscopeScale = QLabel(self.centralwidget)
        self.labelGyroscopeScale.setObjectName(u"labelGyroscopeScale")

        self.gridLayout.addWidget(self.labelGyroscopeScale, 1, 0, 1, 1)

        self.comboBoxGyroscopeScale = QComboBox(self.centralwidget)
        self.comboBoxGyroscopeScale.setObjectName(u"comboBoxGyroscopeScale")
        self.comboBoxGyroscopeScale.setEnabled(False)

        self.gridLayout.addWidget(self.comboBoxGyroscopeScale, 1, 1, 1, 1)

        self.labelAccelerometerScale = QLabel(self.centralwidget)
        self.labelAccelerometerScale.setObjectName(u"labelAccelerometerScale")

        self.gridLayout.addWidget(self.labelAccelerometerScale, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 917, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButtonConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.pushButtonStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButtonStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.labelDevice.setText(QCoreApplication.translate("MainWindow", u"Device:", None))
        self.labelDeviceName.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.labelGyroscopeScale.setText(QCoreApplication.translate("MainWindow", u"Gyroscope scale, dps", None))
        self.labelAccelerometerScale.setText(QCoreApplication.translate("MainWindow", u"Accelerometer, g", None))
    # retranslateUi

