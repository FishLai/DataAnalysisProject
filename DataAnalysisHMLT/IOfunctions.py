'''
Created on 2018/9/30

@author: quan_

181003, I think I will implement a function for tidy data
'''
import os, fnmatch, csv 
from datetime import datetime as dd


def showDataFiles(directory):
    d = directory
#     print(d)
    files = os.listdir(d)
    dfiles = fnmatch.filter(files, '*.csv')
#     print(dfiles)
    return dfiles
def loadData(path):
    with open(path, newline="") as dfile:
        dataReader = csv.reader(dfile)
        data = []
        dataHead = 0
        for row in dataReader:
            if dataHead == 1 or list(set(row).intersection(set(['Vd', 'Vg', 'Id']))) != []:
                dataHead = 1
#                 print(row)
                data.append(row)
    return data
def saveCSV(directory):
    if 'tidiedData' in globals():
        dir = directory
        today = dd.now().strftime("%y%m%d")
        mkpath = dir + '/' + today + 'tidied'
        os.mkdir(mkpath)
        dir = mkpath
        open()
        pass
    pass
if __name__ == "__main__":
    dir = "C:/workspace/Data/180927/MoTe2_hBN_Vg60_output_Vd-11_200point.csv"
    parameters = {'directory': 'C:/workspace/Data/180927',
                  'experiment': 'Output',
                  'dataFile': ['MoTe2_hBN_Vg60_output_Vd-11_200point.csv', 
                               'output [(4) ; 9_27_2018 12_13_01 PM].csv', 
                               'output [(5) ; 9_27_2018 12_16_33 PM].csv'], 
                  'Vds_range': (-1.0, 1.0), 
                  'Vds_Interval': 0.005, 
                  'Vgs_range': (-60.0, 60.0), 
                  'Vgs_Interval': 10.0, 
                  'iflog': True}