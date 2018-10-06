'''
FishLai created 18/10/06
'''
import IOfunctions

def tidyData(path, parameters):
    untidyData = IOfunctions.loadData(path)
    dataHead = untidyData[0]
#     print(dataHead)
    for head in dataHead:
        if set(list('Vd')) <= set(list(head)):
            index_Vd = dataHead.index(head)
        elif set(list('Vg')) <= set(list(head)):
            index_Vg = dataHead.index(head)
        elif set(list('Id')) <= set(list(head)):
            index_Id = dataHead.index(head)
            
    if ('markPosition' in globals()
            and parameters['experiment'] == 'Output'):
        markDataBegin = doMarkDataBegin(untidyData, parameters, 
                                        index_Vd = index_Vd, index_Vg = index_Vg)
        globals()['markPosition'].append(markDataBegin)
        print(globals()['markPosition'])
        tidiedData = doTidyForOutput(untidyData, index_Vd = index_Vd, 
                                     index_Vg = index_Vg, index_Id = index_Id)
        return tidiedData
    print('markPosition' in globals())    
    if parameters['experiment'] == 'Output':
        doMarkForOutput(untidyData,path = path, para = parameters, 
                            index_Vd = index_Vd)
    if parameters['experiment'] == 'transfer':
        doMarkForTransfer() #Not implement

def doTidyForOutput(data, **kws):
    index_Vd = kws['index_Vd']
    index_Vg = kws['index_Vg']
    indes_Id = kws['index_Id']
    mark_dataBegins = globals()['markPosition'][1]
    mark_inOne = globals()['markPosition'][0]
    pass

'''
    mark the begin, middle and end index
'''
def doMarkForOutput(data, **kwargs):
    path = kwargs['path']
    para = kwargs['para']
    index_Vd = kwargs['index_Vd']
#     index_Vg = kwargs['index_Vg']
#     indes_Id = kwargs['index_Id']
    r_Vd = para['Vds_range']
    in_Vd = para['Vds_Interval']
#     print(r_Vd[0])
    for i in range(1, len(data)):
        '''
                calculate the interval between adjacent data
                set up some value
        '''
        VdValue = data[i][index_Vd]
        VdValue = float(VdValue)
#         print(VdValue)
        if i == 1 : 
            upSubstraction = 0
            downSubstraction = float(data[i+1][index_Vd]) - float(data[i][index_Vd])
        elif i == len(data)- 1:
            upSubstraction = float(data[i][index_Vd]) - float(data[i-1][index_Vd])
            downSubstraction = 0
        else:
            upSubstraction = float(data[i][index_Vd]) - float(data[i-1][index_Vd])
            downSubstraction = float(data[i+1][index_Vd]) - float(data[i][index_Vd])            
#         print(round(abs(upSubstraction), 4), round(abs(downSubstraction), 4))
        upSubstraction = round(abs(upSubstraction), 4)
        downSubstraction = round(abs(downSubstraction), 4)
        '''
            figure out the position row about beginning, middle and end
        '''
        if (VdValue == r_Vd[1]
                and upSubstraction != in_Vd
                and downSubstraction == in_Vd
                ):
            part_act = 'downstair'
            begin_row = i
            globals()['markPosition'] = [[begin_row, part_act]]            #mark the special row index in Data
        elif (VdValue == r_Vd[0]
                and upSubstraction != in_Vd
                and downSubstraction == in_Vd
                ):
            part_act = 'upstair'
            begin_row = i
            globals()['markPosition'] = [[begin_row, part_act]]
        elif ((VdValue == r_Vd[0] or VdValue == r_Vd[1])
                and upSubstraction == in_Vd
                and downSubstraction == in_Vd):
            middle_row = i
            globals()['markPosition'][0].append(middle_row)
        elif upSubstraction == in_Vd and downSubstraction != in_Vd:
            end_row = i
            globals()['markPosition'][0].append(end_row)
            break
    tidyData(path, para)
def doMarkForTransfer():
    pass
'''
    list out the stick values about Vg or Vd in output or transfer experiment
    mark the experiment start point
'''
def doMarkDataBegin(data, parameters, **kws):
    index_Vd = kws['index_Vd']
    index_Vg = kws['index_Vg']
    para = parameters
    markedDataBegin = []
    if para['experiment'] == 'Output':
        Vg_value = None
        Vg_values = []
        for row in data[1:len(data)]:
            if row[index_Vg] != Vg_value:
                rowIndex = data.index(row)
                Vg_value = row[index_Vg]
                markedDataBegin += [[rowIndex, Vg_value]]
        return markedDataBegin
    elif para['experiment'] == 'transfer':
        pass
            
    
if __name__ == "__main__":
    #output [(1) ; 9_27_2018 1_42_00 PM]
    #MoTe2_hBN_Vg60_output_Vd-11_200point
    dir = "C:/workspace/Data/180927/output [(1) ; 9_27_2018 1_42_00 PM].csv"
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
    tidyData(dir, parameters)