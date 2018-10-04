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
                             QListView, QLineEdit, QLabel, QPushButton,
                             QComboBox, QCheckBox)
from PyQt5.Qt import QStandardItemModel, QStandardItem
from MainFramDemo import Ui_MainWindow
import IOfunctions
from docutils.nodes import row

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
        self.Label2.setObjectName("Range_Vds")
        self.Label2.setText("Vds range :")
        self.LineEdit1 = QLineEdit(self.ui.groupBox)
        self.LineEdit1.setGeometry(QtCore.QRect(80, yVds, 40, 20))
        self.LineEdit1.setObjectName("Range_Vds[")
        self.Label1 = QLabel(self.ui.groupBox)
        self.Label1.setGeometry(QtCore.QRect(125, yVds, 10, 20))
        self.Label1.setText("to")
        self.LineEdit2 = QLineEdit(self.ui.groupBox)
        self.LineEdit2.setGeometry(QtCore.QRect(140, yVds, 40, 20))
        self.LineEdit2.setObjectName("Range_Vds]")
        self.Label3 = QLabel(self.ui.groupBox)
        self.Label3.setGeometry(QtCore.QRect(185, yVds, 50, 20))
        self.Label3.setText(", interval")        
        self.LineEdit3 = QLineEdit(self.ui.groupBox)
        self.LineEdit3.setGeometry(QtCore.QRect(235, yVds, 40, 20))
        self.LineEdit3.setObjectName("Interval_Vds")
        
        self.coor_yVgs = 65
        yVgs = self.coor_yVgs
        self.Label4 = QLabel(self.ui.groupBox)
        self.Label4.setGeometry(QtCore.QRect(20, yVgs, 60, 20))
        self.Label4.setObjectName("Range_Vgs")
        self.Label4.setText("Vgs range :")
        self.LineEdit4 = QLineEdit(self.ui.groupBox)
        self.LineEdit4.setGeometry(QtCore.QRect(80, yVgs, 40, 20))
        self.LineEdit4.setObjectName("Range_Vgs[")
        self.Label5 = QLabel(self.ui.groupBox)
        self.Label5.setGeometry(QtCore.QRect(125, yVgs, 10, 20))
        self.Label5.setText("to")
        self.LineEdit5 = QLineEdit(self.ui.groupBox)
        self.LineEdit5.setGeometry(QtCore.QRect(140, yVgs, 40, 20))
        self.LineEdit5.setObjectName("Range_Vgs]")
        self.Label6 = QLabel(self.ui.groupBox)
        self.Label6.setGeometry(QtCore.QRect(185, yVgs, 50, 20))
        self.Label6.setText(", interval")        
        self.LineEdit6 = QLineEdit(self.ui.groupBox)
        self.LineEdit6.setGeometry(QtCore.QRect(235, yVgs, 40, 20))
        self.LineEdit6.setObjectName("Interval_Vgs")
        
        self.PushButtom1 = QPushButton(self.ui.groupBox)
        self.PushButtom1.setGeometry(QtCore.QRect(180, 180, 120, 20))
        self.PushButtom1.setObjectName("doDraw")
        self.PushButtom1.setText("show the Data Figure")
        self.PushButtom1.clicked.connect(self.doDrawFigure)
    def doDrawFigure(self):
        Vds_u = self.ui.groupBox.findChild(QLineEdit, "Range_Vds]").text()
        Vds_l = self.ui.groupBox.findChild(QLineEdit, "Range_Vds[").text()
        Vgs_l = self.ui.groupBox.findChild(QLineEdit, "Range_Vgs[").text()
        Vgs_u = self.ui.groupBox.findChild(QLineEdit, "Range_Vgs]").text()
        Vgs_in = self.ui.groupBox.findChild(QLineEdit, "Interval_Vgs").text()
        Vds_in = self.ui.groupBox.findChild(QLineEdit, "Interval_Vds").text()
        iflog = self.ui.groupBox.findChild(QCheckBox, "log(y-axis)").isChecked()
        ftable = self.ui.DataFileTable.model()
        selectedFile = doCollectFile(ftable)
#         print(selectedFile)
        
        parameter = {"directory" : self.dir,
                     "experiment" : self.mode,
                     "dataFile" : selectedFile,
                     "Vds_range" : (float(Vds_l), float(Vds_u)),
                     "Vds_Interval" : float(Vds_in),
                     "Vgs_range" : (float(Vgs_l), float(Vgs_u)),
                     "Vgs_Interval" : float(Vgs_in),
                     "iflog" : iflog}
#         print(parameter)
        
    def onChangePlotMode(self):
        self.mode = self.ui.comboBox.currentText()
        mode = self.mode
        if mode == "transfer":
            self.ui.groupBox.findChild(QLineEdit, "Range_Vds[").setText("-1")
            self.ui.groupBox.findChild(QLineEdit, "Range_Vds]").setText("1")
            self.ui.groupBox.findChild(QLineEdit, "Interval_Vds").setText("0.5")
            self.ui.groupBox.findChild(QLineEdit, "Range_Vgs[").setText("-60")
            self.ui.groupBox.findChild(QLineEdit, "Range_Vgs]").setText("60")
            self.ui.groupBox.findChild(QLineEdit, "Interval_Vgs").setText("0.25")
        elif mode == "Output":
            self.ui.groupBox.findChild(QLineEdit, "Range_Vds[").setText("-1")
            self.ui.groupBox.findChild(QLineEdit, "Range_Vds]").setText("1")
            self.ui.groupBox.findChild(QLineEdit, "Interval_Vds").setText("0.05")
            self.ui.groupBox.findChild(QLineEdit, "Range_Vgs[").setText("-60")
            self.ui.groupBox.findChild(QLineEdit, "Range_Vgs]").setText("60")
            self.ui.groupBox.findChild(QLineEdit, "Interval_Vgs").setText("10")
            
     
    def onEventClickBtn(self):
        onClicked = self.sender().objectName()
        if onClicked == "Btn_directory":
            self.dir = QFileDialog.getExistingDirectory(self, 'choose directory', 'C:\\workspace\\Data\\180927', options = QFileDialog.ShowDirsOnly)
            dir = self.dir
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