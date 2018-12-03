# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Programs\Qt\MyUI\dataAnalysisHMLT_sketch.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(980, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(20, 50, 592, 382))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 590, 380))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.DataFileTable = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.DataFileTable.setGeometry(QtCore.QRect(10, 10, 570, 360))
        self.DataFileTable.setObjectName("DataFileTable")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.IBx_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.IBx_dir.setGeometry(QtCore.QRect(100, 20, 151, 20))
        self.IBx_dir.setObjectName("IBx_dir")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(620, 50, 351, 381))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(20, 20, 91, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(20, 50, 311, 211))
        self.groupBox.setObjectName("groupBox")
        
        
        self.Btn_dir = QtWidgets.QPushButton(self.centralwidget)
        self.Btn_dir.setGeometry(QtCore.QRect(250, 20, 21, 23))
        self.Btn_dir.setObjectName("Btn_directory")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionData_Directory = QtWidgets.QAction(MainWindow)
        self.actionData_Directory.setObjectName("actionData_Directory")
        self.actionversion = QtWidgets.QAction(MainWindow)
        self.actionversion.setObjectName("actionversion")
        self.menu_File.addAction(self.actionData_Directory)
        self.menu_Help.addAction(self.actionversion)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Data"))
        self.IBx_dir.setText(_translate("MainWindow", "directory"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Output"))
        self.comboBox.setItemText(1, _translate("MainWindow", "transfer"))
        self.groupBox.setTitle(_translate("MainWindow", "Setup Conditions"))
        self.Btn_dir.setText(_translate("MainWindow", ".."))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.actionData_Directory.setText(_translate("MainWindow", "Data Directory"))
        self.actionversion.setText(_translate("MainWindow", "version"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())