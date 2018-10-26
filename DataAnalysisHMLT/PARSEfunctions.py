'''
FishLai created 18/10/06
'''
import IOfunctions
#from docutils.nodes import row

def tidyData(parameters):
    para = parameters
    fdir = para['directory']
    files = para['dataFile']
    if 'untidyData' in globals():
        untidyData = globals()['untidyData']
            
    if ('markPosition' in globals()
            and parameters['experiment'] == 'Output'):
        dataHead = globals()['untidyData'][0]
#     print(dataHead)
        for head in dataHead:
            if set(list('Vd')) <= set(list(head)):
                index_Vd = dataHead.index(head)
            elif set(list('Vg')) <= set(list(head)):
                index_Vg = dataHead.index(head)
            elif set(list('Id')) <= set(list(head)):
                index_Id = dataHead.index(head)        
        
        doMarkDataBegin(untidyData, para, index_Vd = index_Vd, index_Vg = index_Vg)
        tidiedData = doTidyForOutput(untidyData, index_Id = index_Id)
        IOfunctions.saveCSV(para, globals()['tidiedData'])
        return tidiedData
    elif ('markPosition' in globals()
            and parameters['experiment'] == 'transfer'):
        dataHead = globals()['untidyData'][0]
#     print(dataHead)
        for head in dataHead:
            if set(list('Vd')) <= set(list(head)):
                index_Vd = dataHead.index(head)
            elif set(list('Vg')) <= set(list(head)):
                index_Vg = dataHead.index(head)
            elif set(list('Id')) <= set(list(head)):
                index_Id = dataHead.index(head)        
        doMarkDataBegin(untidyData, para, index_Vd = index_Vd, index_Vg = index_Vg)
        tidiedData = doTidyForTransfer(index_Id = index_Id)
        IOfunctions.saveCSV(para, globals()['tidiedData'])
        return 'tidy data success'
    else:
        globals()['untidyData'] = IOfunctions.loadData(fdir, files)
        untidyData = globals()['untidyData']
        dataHead = globals()['untidyData'][0]
#     print(dataHead)
        for head in dataHead:
            if set(list('Vd')) <= set(list(head)):
                index_Vd = dataHead.index(head)
            elif set(list('Vg')) <= set(list(head)):
                index_Vg = dataHead.index(head)
            elif set(list('Id')) <= set(list(head)):
                index_Id = dataHead.index(head)        
#     print('markPosition' in globals())
    
    if parameters['experiment'] == 'Output':
        doMarkForOutput(untidyData, para = parameters, 
                            index_Vd = index_Vd)
    if parameters['experiment'] == 'transfer':
        doMarkForTransfer(untidyData, para, index_Vg) #Not complete

def doTidyForOutput(data, **kws):
    index_Id = kws['index_Id']
    mark_dataBegins = globals()['markPosition'][1]
    mark_inOne = globals()['markPosition'][0]
    i_vd_begin = mark_inOne[0]
    tidiedData = globals()['tidiedData']
    for i_vg, vg in mark_dataBegins:
        i_vd = i_vd_begin
        tidiedData[0].append('Id(Vg' + vg +')')
        for row in tidiedData[1:len(tidiedData)]:
            row.append(data[i_vd][index_Id])
            i_vd += 1
        rowIndex = mark_dataBegins.index([i_vg, vg])
        if rowIndex == len(mark_dataBegins)-1:
            globals()['tidiedData'] = tidiedData
            break
        i_vd_begin = mark_dataBegins[rowIndex+1][0] + (i_vd_begin - i_vg)
    return True

def doTidyForTransfer(**kwgs):
    data = globals()['untidyData']
    i_Id = kwgs['index_Id']
    mark_dataBegins = globals()['markPosition'][1]
    mark_inOne = globals()['markPosition'][0]
    tidiedData = globals()['tidiedData']
    i_vg_begin = mark_inOne[0]
    i_vg_mid = mark_inOne[2]
    for i_vd, vd in mark_dataBegins:
        i_vgF = i_vg_begin
        tidiedData['forward'][0].append('Id(Vd' + vd +')')
        for row in tidiedData['forward'][1:len(tidiedData['forward'])]:
            row.append(data[i_vgF][i_Id])
            i_vgF += 1
        i_vgB = i_vg_mid
        tidiedData['backward'][0].append('Id(Vd' + vd +')')
        for row in tidiedData['backward'][1:len(tidiedData['backward'])]:
            row.append(data[i_vgB][i_Id])
            i_vgB += 1
        rowIndex = mark_dataBegins.index([i_vd, vd])
        if rowIndex == len(mark_dataBegins)-1:
            globals()['tidiedData'] = tidiedData
            break
        i_vg_begin = mark_dataBegins[rowIndex+1][0] + (i_vg_begin - i_vd)        
        i_vg_mid = mark_dataBegins[rowIndex+1][0] + (i_vg_mid - i_vd)
    conbineData = []
    for i in range(len(tidiedData['forward'])):
        row = tidiedData['forward'][i] + tidiedData['backward'][i]
        conbineData += [row]
    globals()['tidiedData'] = conbineData
    return True
'''
    mark the begin, middle and end index
'''
def doMarkForOutput(data, **kwargs):
    para = kwargs['para']
    index_Vd = kwargs['index_Vd']
    r_Vd = para['Vds_range']
    in_Vd = para['Vds_Interval']
#     print(r_Vd[0])
    col_Vd = None
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
        upSubstraction = round(abs(upSubstraction), 5)
        downSubstraction = round(abs(downSubstraction), 5)
        '''
            construct Vd values
        '''
        if col_Vd != None:
            col_Vd.append([data[i][index_Vd]])
        
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
            col_Vd = [['Vd']]
            col_Vd.append([data[i][index_Vd]])
        elif (VdValue == r_Vd[0]
                and upSubstraction != in_Vd
                and downSubstraction == in_Vd
                ):
            part_act = 'upstair'
            begin_row = i            
            globals()['markPosition'] = [[begin_row, part_act]]
            col_Vd = [['Vd']]
            col_Vd.append([data[i][index_Vd]])
        elif ((VdValue == r_Vd[0] or VdValue == r_Vd[1])
                and upSubstraction == in_Vd
                and downSubstraction == in_Vd):
            middle_row = i
            globals()['markPosition'][0].append(middle_row)
        elif upSubstraction == in_Vd and downSubstraction != in_Vd:
            end_row = i
            globals()['markPosition'][0].append(end_row)
            globals()['tidiedData'] = col_Vd
            break
    tidyData(para)
    
def doMarkForTransfer(data, parameter, index_Vg):
    para = parameter
    r_Vg = para['Vgs_range']
    in_Vg = para['Vgs_Interval']
#     print(r_Vd[0])
    col_Vg_forward = None
    col_Vg_backward = None
    for i in range(1, len(data)):
        '''
            calculate the interval between adjacent data
            set up some value
        '''
        VgValue = data[i][index_Vg]
        VgValue = float(VgValue)
#         print(VdValue)
        if i == 1 : 
            upSubstraction = 0
            downSubstraction = float(data[i+1][index_Vg]) - float(data[i][index_Vg])
        elif i == len(data)- 1:
            upSubstraction = float(data[i][index_Vg]) - float(data[i-1][index_Vg])
            downSubstraction = 0
        else:
            upSubstraction = float(data[i][index_Vg]) - float(data[i-1][index_Vg])
            downSubstraction = float(data[i+1][index_Vg]) - float(data[i][index_Vg])            
#         print(round(abs(upSubstraction), 4), round(abs(downSubstraction), 4))
        upSubstraction = round(abs(upSubstraction), 5)
        downSubstraction = round(abs(downSubstraction), 5)
        '''
            construct Vg values, forward and backward
        '''
        if col_Vg_forward != None and col_Vg_backward == None:
            col_Vg_forward.append([data[i][index_Vg]])
        if col_Vg_backward != None:
            col_Vg_backward.append([data[i][index_Vg]])
        
        '''
            figure out the position row about beginning, middle and end
        '''
        if (VgValue == r_Vg[1]
                and upSubstraction != in_Vg
                and downSubstraction == in_Vg
                ):
            part_act = 'downstair'
            begin_row = i
            globals()['markPosition'] = [[begin_row, part_act]]            #mark the special row index in Data
            col_Vg_forward = [['Vg_downstair']]
            col_Vg_forward.append([data[i][index_Vg]])
        elif (VgValue == r_Vg[0]
                and upSubstraction != in_Vg
                and downSubstraction == in_Vg
                ):
            part_act = 'upstair'
            begin_row = i            
            globals()['markPosition'] = [[begin_row, part_act]]
            col_Vg_forward = [['Vg_upstair']]
            col_Vg_forward.append([data[i][index_Vg]])
        elif ((VgValue == r_Vg[0] or VgValue == r_Vg[1])
                and upSubstraction == in_Vg
                and downSubstraction == in_Vg):
            middle_row = i
            col_Vg_backward = [['Vg_backScan']]
            col_Vg_backward.append([data[i][index_Vg]])
            globals()['markPosition'][0].append(middle_row)
        elif upSubstraction == in_Vg and downSubstraction != in_Vg:
            end_row = i
            globals()['markPosition'][0].append(end_row)
            globals()['tidiedData'] = {'forward':col_Vg_forward,
                                       'backward':col_Vg_backward}
            break
    tidyData(para)
'''
    list out the stick values about Vg or Vd in output or transfer experiment
    mark the experiment start point
'''
def doMarkDataBegin(data, parameters, **kws):
    para = parameters
    markedDataBegin = []
    if para['experiment'] == 'Output':
        index_Vg = kws['index_Vg']
        Vg_value = None
        for row in data[1:len(data)]:
            if row[index_Vg] != Vg_value:
                rowIndex = data.index(row)
                Vg_value = row[index_Vg]
                markedDataBegin += [[rowIndex, Vg_value]]
    elif para['experiment'] == 'transfer':
        index_Vd = kws['index_Vd']
        Vd_value = None
        for row in data[1:len(data)]:
            if row[index_Vd] != Vd_value:
                rowIndex = data.index(row)
                Vd_value = row[index_Vd]
                markedDataBegin += [[rowIndex, Vd_value]]
    globals()['markPosition'].append(markedDataBegin)
            
    
if __name__ == "__main__":
    #output [(1) ; 9_27_2018 1_42_00 PM]
    #MoTe2_hBN_Vg60_output_Vd-11_200point
#     dir = "C:/workspace/Data/180927/output [(1) ; 9_27_2018 1_42_00 PM].csv"
    parameters = {'directory': 'C:/workspace/Data/180927',
                  'experiment': 'transfer', 
                  'dataFile': ['transfer [(2) ; 9_27_2018 3_12_06 PM].csv'],
                  'Vds_range': (-1.0, 1.0),
                  'Vds_Interval': 0.5,
                  'Vgs_range': (-60.0, 60.0), 
                  'Vgs_Interval': 0.25, 
                  'iflog': True}

    tidyData(parameters)