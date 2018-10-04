'''
Created on 2018/9/30

@author: quan_
'''
import os, fnmatch, csv


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
        dataHead = 0
        for row in dataReader:
            if dataHead == 1 or list(set(row).intersection(set([' Vd', ' Vg', ' Id']))) != []:
                dataHead = 1
                print(row)
if __name__ == "__main__":
    dir = "C:/workspace/Data_clone/180927/MoTe2_hBN_Vg60_output_Vd-11_200point.csv"
    loadData(dir)
