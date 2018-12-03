'''
Created on 2018/9/30

@author: quan_

181003, I think I will implement a function for tidy data
'''
import os, fnmatch, csv 
from datetime import datetime as dd


def loadTidiedData(**kwgs):
    dir = kwgs['directory']
    fn = kwgs['file']
    path = os.path.join(dir, fn)
    with open(path, newline='') as csvfile:
        dictData = csv.reader(csvfile)
        dictData = list(dictData)    
    return dictData
def showDataFiles(directory):
    d = directory
#     print(d)
    files = os.listdir(d)
    dfiles = fnmatch.filter(files, '*.csv')
#     print(dfiles)
    return dfiles
def loadData(directory, files):
    allData = []
    for fn in files:
        path = os.path.join(directory, fn)
        with open(path, newline="") as dfile:
            dataReader = csv.reader(dfile)
            data = []
            dataHead = 0
            for row in dataReader:
                if 'DataName' in row:
                    data = []
                if (dataHead == 1 
                    or list(set(row).intersection(set(['Vd', 'Vg', 'Id']))) != []
                    or list(set(row).intersection(set([' Vd', ' Vg', ' Id']))) !=[]):
                    dataHead = 1
    #                 print(row)
                    data.append(row)
        dataHead = 0
        '''
            collect the dataes in one list
        '''
        if allData == []:
            allData += data            
        else:
            allData += data[1:len(data)]
    return allData
def saveCSV(parameters, *args):
    globals()['tidiedData']=args[0]
    if 'tidiedData' in globals():
        para = parameters
        dir = para['directory']
        today = dd.now().strftime("%y%m%d")
        mkpath = dir + '/' + today + 'Tidied'
        
        if os.path.isdir(mkpath) != True:
            os.mkdir(mkpath)
        time = dd.now().strftime("%H%M%S")
        fn = (time + '_' 
              + para['experiment'] + '_' 
              + para['sample'] + '_' 
              + para['temperature'] + '.csv'
            )
        newfile = mkpath + '/' + fn
        with open(newfile, 'w', newline='') as newfn:
            writer = csv.writer(newfn)
            writer.writerows(globals()['tidiedData'])
        
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
    loadData("C:/workspace/Data/test data/YYY", ['S1DB transfer.csv'])