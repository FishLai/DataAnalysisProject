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
    resized = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.resized.connect(self.reSizeHappen)
        self.ui.Btn_dir.clicked.connect(self.onEventClickBtn)
        self.ui.comboBox.activated.connect(self.onChangePlotMode)
        
        #objects in 'setup conditions' layout
        #實驗條件設定畫面實作
        self.Label4 = QLabel(self.ui.groupBox)
        self.Label4.setGeometry(QtCore.QRect(20, 15, 60, 20))
        self.Label4.setObjectName("SampleNameLabel")
        self.Label4.setText("Samples :")
        self.LineEdit4 = QLineEdit(self.ui.groupBox)
        self.LineEdit4.setGeometry(QtCore.QRect(85, 15, 225, 20))
        self.LineEdit4.setObjectName("Sample")
        self.LineEdit4.setPlaceholderText("ex:SnS2onMoTe2(source)")
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
        self.Label5 = QLabel(self.ui.groupBox)
        self.Label5.setGeometry(QtCore.QRect(20, 65, 80, 20))
        self.Label5.setObjectName("temperatureLabel")
        self.Label5.setText("temperature(K) :")
        self.LineEdit5 = QLineEdit(self.ui.groupBox)
        self.LineEdit5.setGeometry(QtCore.QRect(105, 65, 45, 20))
        self.LineEdit5.setObjectName("Kelvin")
        
        self.PushButtom1 = QPushButton(self.ui.groupBox)
        self.PushButtom1.setGeometry(QtCore.QRect(180, 180, 120, 20))
        self.PushButtom1.setObjectName("doTidy")
        self.PushButtom1.setText("Tidied Data for me")
        self.PushButtom1.clicked.connect(self.doTidyData)
    def doTidyData(self):
        V_u = self.ui.groupBox.findChild(QLineEdit, "Range_V]").text()
        V_l = self.ui.groupBox.findChild(QLineEdit, "Range_V[").text()
        V_in = self.ui.groupBox.findChild(QLineEdit, "Interval_V").text()
        sample = self.ui.groupBox.findChild(QLineEdit, "Sample").text()
        if sample =="":
            sample = "unknown"
        temperature = self.ui.groupBox.findChild(QLineEdit, "Kelvin").text()
        print(sample, temperature)
        ftable = self.ui.DataFileTable.model()
        selectedFile = doCollectFile(ftable)
#         print(selectedFile)
        
        parameter = {"directory" : self.dir,
                     "experiment" : self.mode,
                     "dataFile" : selectedFile,
                     "sample" : sample,
                     "V_range" : (float(V_l), float(V_u)),
                     "V_Interval" : float(V_in),
                     "temperature" : temperature
                    }
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
            #show the folder dialog
            #顯示選資料夾對話框
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
    
    def resizeEvent(self, event):
        #use emit() to make 'resized' as a signal
        #讓'resized' 可以當作連結方法的訊號
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)
    def reSizeHappen(self):
        width_window = self.width()
        height_window = self.height()
        newXPos_frame = width_window - 360
        y_frame = self.ui.frame.y()
        #As window resize change the position of the 'setting frame'
        #使'設定區塊'靠著右邊
        self.ui.frame.move(newXPos_frame, y_frame)
        #同時改變檔案顯示區塊的大小
        newHeight_scrollArea = (height_window - 48) - self.ui.scrollArea.y()
        newWidth_scrollArea = (width_window -368) - self.ui.scrollArea.x()
        self.ui.scrollArea.resize(newWidth_scrollArea, newHeight_scrollArea)
        self.ui.scrollAreaWidgetContents.resize(newWidth_scrollArea - 2, newHeight_scrollArea - 2)
        self.ui.DataFileTable.resize(newWidth_scrollArea -22, newHeight_scrollArea -22)

def showDataFile(dFileList, view):
    #將蒐集的資料檔名顯是在檔案區塊
    fs = dFileList
    model = QStandardItemModel(view)
    for df in fs:
        item = QStandardItem(df)
        item.setCheckable(True)
        model.appendRow(item)
    return model
  
def doCollectFile(model):
    #collect the data files which is selected 
    #蒐集被勾選的檔名
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