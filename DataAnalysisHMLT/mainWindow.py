"""
Fish Lai created 2018/09/29
Btn_dir -> button for select the directory
IBx_dir -> show the string of path which is selected
dFileList -> list of data files
Range_Vds[ -> floor of Vds 
"""

import MainFramDemo
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, 
                             QListView, QLineEdit, QLabel, QPushButton)
from PyQt5.Qt import QStandardItemModel, QStandardItem
from MainFramDemo import Ui_MainWindow
import IOfunctions

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Btn_dir.clicked.connect(self.onEventClickBtn)
        
        self.Label2 = QLabel(self.ui.groupBox)
        self.Label2.setGeometry(QtCore.QRect(20, 40, 60, 20))
        self.Label2.setObjectName("Range_Vds")
        self.Label2.setText("Vds range :")
        self.LineEdit1 = QLineEdit(self.ui.groupBox)
        self.LineEdit1.setGeometry(QtCore.QRect(80, 40, 40, 20))
        self.LineEdit1.setObjectName("Range_Vds[")
        self.Label1 = QLabel(self.ui.groupBox)
        self.Label1.setGeometry(QtCore.QRect(125, 40, 10, 20))
        self.Label1.setText("to")
        self.LineEdit2 = QLineEdit(self.ui.groupBox)
        self.LineEdit2.setGeometry(QtCore.QRect(140, 40, 40, 20))
        self.LineEdit2.setObjectName("Range_Vds]")
        self.Label3 = QLabel(self.ui.groupBox)
        self.Label3.setGeometry(QtCore.QRect(185, 40, 50, 20))
        self.Label3.setText(", interval")        
        self.LineEdit3 = QLineEdit(self.ui.groupBox)
        self.LineEdit3.setGeometry(QtCore.QRect(235, 40, 40, 20))
        self.LineEdit3.setObjectName("Interval_Vds")
        
        self.Label4 = QLabel(self.ui.groupBox)
        self.Label4.setGeometry(QtCore.QRect(20, 65, 60, 20))
        self.Label4.setObjectName("Range_Vgs")
        self.Label4.setText("Vgs range :")
        self.LineEdit4 = QLineEdit(self.ui.groupBox)
        self.LineEdit4.setGeometry(QtCore.QRect(80, 65, 40, 20))
        self.LineEdit4.setObjectName("Range_Vgs[")
        self.Label5 = QLabel(self.ui.groupBox)
        self.Label5.setGeometry(QtCore.QRect(125, 65, 10, 20))
        self.Label5.setText("to")
        self.LineEdit5 = QLineEdit(self.ui.groupBox)
        self.LineEdit5.setGeometry(QtCore.QRect(140, 65, 40, 20))
        self.LineEdit5.setObjectName("Range_Vgs]")
        self.Label6 = QLabel(self.ui.groupBox)
        self.Label6.setGeometry(QtCore.QRect(185, 65, 50, 20))
        self.Label6.setText(", interval")        
        self.LineEdit6 = QLineEdit(self.ui.groupBox)
        self.LineEdit6.setGeometry(QtCore.QRect(235, 65, 40, 20))
        self.LineEdit6.setObjectName("Interval_Vgs")
        
        self.PushButtom1 = QPushButton(self.ui.groupBox)
        self.PushButtom1.setGeometry(QtCore.QRect(180, 180, 120, 20))
        self.PushButtom1.setObjectName("doDraw")
        self.PushButtom1.setText("show the Data Figure")
    def onEventClickBtn(self):
        onClicked = self.sender().objectName()
        if onClicked == "Btn_directory":
            dir = QFileDialog.getExistingDirectory(self, 'choose directory', './', options = QFileDialog.ShowDirsOnly)
#             print(dir == "")
            if dir != "":
                self.ui.IBx_dir.setText(dir)
                self.dfiles = IOfunctions.showDataFiles(dir)            
#             print(self.dfiles)
            #need a function to show data files
                model = showDataFile(self.dfiles, self.ui.DataFileTable)
                self.ui.DataFileTable.setModel(model)

def showDataFile(dFileList, view):
    fs = dFileList
    model = QStandardItemModel(view)
    for df in fs:
        item = QStandardItem(df)
        item.setCheckable(True)
        model.appendRow(item)
    return model    
    
        
if __name__ == '__main__':
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())