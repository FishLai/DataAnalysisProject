'''
Created on 2018/9/30

@author: quan_

181003, I think I will implement a function for tidy data
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
        data = []
        dataHead = 0
        for row in dataReader:
            if dataHead == 1 or list(set(row).intersection(set([' Vd', ' Vg', ' Id']))) != []:
                dataHead = 1
#                 print(row)
                data.append(row)
    return data

def tidiedData(path, parameters):
    untidyData = loadData(path)
    dataHead = untidyData[0]
#     print(dataHead)
    for head in dataHead:
        if list('Vd') <= list(head):
            index_Vd = dataHead.index(head)
        elif list('Vg') <= list(head):
            index_Vg = dataHead.index(head)
        elif list('Id') <= list(head):
            index_Id = dataHead.index(head)
    para = parameters
    r_Vd = para['Vds_range']
    in_Vd = para['Vds_Interval']
    for i in range(1, len(untidyData)):
        '''
                calculate the interval between adjacent data
                set up some value
        '''
        VdValue = untidyData[i][index_Vd]
        if i == 1 : 
            upSubstraction = 0
            downSubstraction = untidyData[i+1][index_Vd] - untidyData[i][index_Vd]
        elif i == len(untidyData):
            upSubstraction = untidyData[i][index_Vd] - untidyData[i-1][index_Vd]
            downSubstraction = 0
        else:
            upSubstraction = untidyData[i][index_Vd] - untidyData[i-1][index_Vd]
            downSubstraction = untidyData[i+1][index_Vd] - untidyData[i][index_Vd]
            
        '''
            figure out the position row about beginning, middle and end
        '''
        if (VdValue == r_Vd[1]
                and abs(upSubstraction) != in_Vd
                and abs(downSubstraction) == in_Vd
                ):
            part_act = 'downstair'
            begin_row = i
            markPosition = [begin_row, part_act]            #mark the special row index in Data
        elif (VdValue == r_Vd[0]
                and abs(upSubstraction) != in_Vd
                and abs(downSubstraction) == in_Vd
                ):
            part_act = 'upstair'
            begin_row = i
            markPosition = [begin_row, part_act]
        elif ((VdValue == r_Vd[0] or VdValue == r_Vd[1])
                and abs(upSubstraction) == in_Vd
                and abs(downSubstraction) == in_Vd):
            middle_row = i
            markPosition.append(middle_row)
        elif abs(upSubstraction) == in_Vd and abs(downSubstraction) != in_Vd:
            end_row = i
            markPosition.append(end_row)
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
    tidiedData(dir, parameters)
