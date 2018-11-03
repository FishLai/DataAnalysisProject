"""
Fish Lai created 2018/09/29
Btn_dir -> button for select the directory
IBx_dir -> show the string of path which is selected
dFileList -> list of data files
Range_Vds[ -> floor of Vds 
"""

import MainFramDemo2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, 
                             QListView, QLineEdit, QLabel, QPushButton,
                             QComboBox, QCheckBox)
from PyQt5.Qt import QStandardItemModel, QStandardItem
from MainFramDemo2 import Ui_MainWindow
import IOfunctions, PLOTfunctions, PARSEfunctions2

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.Btn_dir.clicked.connect(self.onEventClickBtn)
        self.ui.comboBox.activated.connect(self.onChangePlotMode)
        self.ui.checkBox.setChecked(True)
        
        self.coor_yVds = 40
        yVds = self.coor_yVds
        self.Label2 = QLabel(self.ui.groupBox)
        self.Label2.setGeometry(QtCore.QRect(20, yVds, 60, 20))
        self.Label2.setObjectName("Range_V")
        self.Label2.setText("V range :")
        self.LineEdit1 = QLineEdit(self.ui.groupBox)
        self.LineEdit1.setGeometry(QtCore.QRect(80, yVds, 40, 20))
        self.LineEdit1.setObjectName("Range_V[")
        self.Label1 = QLabel(self.ui.groupBox)
        self.Label1.setGeometry(QtCore.QRect(125, yVds, 10, 20))
        self.Label1.setText("to")
        self.LineEdit2 = QLineEdit(self.ui.groupBox)
        self.LineEdit2.setGeometry(QtCore.QRect(140, yVds, 40, 20))
        self.LineEdit2.setObjectName("Range_V]")
        self.Label3 = QLabel(self.ui.groupBox)
        self.Label3.setGeometry(QtCore.QRect(185, yVds, 50, 20))
        self.Label3.setText(", interval")        
        self.LineEdit3 = QLineEdit(self.ui.groupBox)
        self.LineEdit3.setGeometry(QtCore.QRect(235, yVds, 40, 20))
        self.LineEdit3.setObjectName("Interval_V")
        
        self.PushButtom1 = QPushButton(self.ui.groupBox)
        self.PushButtom1.setGeometry(QtCore.QRect(180, 180, 120, 20))
        self.PushButtom1.setObjectName("doDraw")
        self.PushButtom1.setText("show the Data Figure")
        self.PushButtom1.clicked.connect(self.doDrawFigure)
    def doDrawFigure(self):
        V_u = self.ui.groupBox.findChild(QLineEdit, "Range_V]").text()
        V_l = self.ui.groupBox.findChild(QLineEdit, "Range_V[").text()
        V_in = self.ui.groupBox.findChild(QLineEdit, "Interval_V").text()
        iflog = self.ui.groupBox.findChild(QCheckBox, "log(y-axis)").isChecked()
        ftable = self.ui.DataFileTable.model()
        selectedFile = doCollectFile(ftable)
#         print(selectedFile)
        
        parameter = {"directory" : self.dir,
                     "experiment" : self.mode,
                     "dataFile" : selectedFile,
                     "V_range" : (float(V_l), float(V_u)),
                     "V_Interval" : float(V_in),
                     "iflog" : iflog}
        print(parameter)
        PARSEfunctions2.tidyData(parameter)
        
    def onChangePlotMode(self):
        self.mode = self.ui.comboBox.currentText()
        mode = self.mode
        if mode == "transfer":
            self.ui.groupBox.findChild(QLineEdit, "Range_V[").setText("-60")
            self.ui.groupBox.findChild(QLineEdit, "Range_V]").setText("60")
            self.ui.groupBox.findChild(QLineEdit, "Interval_V").setText("0.25")
        elif mode == "Output":
            self.ui.groupBox.findChild(QLineEdit, "Range_V[").setText("-1")
            self.ui.groupBox.findChild(QLineEdit, "Range_V]").setText("1")
            self.ui.groupBox.findChild(QLineEdit, "Interval_V").setText("0.005")
     
    def onEventClickBtn(self):
        onClicked = self.sender().objectName()
        if onClicked == "Btn_directory":
            def_dir = 'C:\\'
            self.dir = QFileDialog.getExistingDirectory(self, 'choose directory', def_dir, options = QFileDialog.ShowDirsOnly)
            def_dir = self.dir
            dir = def_dir
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
  
def doCollectFile(model):
    fileList = []
    for row in range(model.rowCount()):
        isChecked = model.item(row, 0).checkState() == QtCore.Qt.Checked
#         print(isChecked, row)
        if isChecked :
            fn = model.item(row, 0).text()
            fileList.append(fn)
    return fileList    
if __name__ == '__main__':
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.setWindowTitle("break away duplicating copy hell")
    ui.show()
    sys.exit(app.exec_())