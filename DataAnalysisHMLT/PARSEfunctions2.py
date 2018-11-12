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
            
    if 'markPosition' in globals():
        dataHead = globals()['untidyData'][0]
#     print(dataHead)
        for head in dataHead:
            if 'Vd' in head:
                index_Vd = dataHead.index(head)
            elif 'Vg' in head:
                index_Vg = dataHead.index(head)
            elif 'Id' in head:
                index_Id = dataHead.index(head)        
        doMarkDataBegin(untidyData, para, index_Vd = index_Vd, index_Vg = index_Vg)
        tidiedData = doTidyData(experiment = para['experiment'], index_Id = index_Id)
        IOfunctions.saveCSV(para, globals()['tidiedData'])
        print("tidy data success")
        globals().pop('untidyData')
        globals().pop('tidiedData')
        globals().pop('markPosition')
        return 'tidy data success'
    else:
        globals()['untidyData'] = IOfunctions.loadData(fdir, files)
        untidyData = globals()['untidyData']
        dataHead = globals()['untidyData'][0]
        for head in dataHead:
            if 'Vd' in head:
                index_Vd = dataHead.index(head)
            elif 'Vg' in head:
                index_Vg = dataHead.index(head)
            elif 'Id' in head:
                index_Id = dataHead.index(head)        
#     print('markPosition' in globals())
    
    if parameters['experiment'] == 'Output':
        doMarkInSingle(untidyData, para, index_Vd)
    if parameters['experiment'] == 'transfer':
        doMarkInSingle(untidyData, para, index_Vg) #Not complete

def doTidyData(**kwgs):
    data = globals()['untidyData']
    i_Id = kwgs['index_Id']
    exp = kwgs['experiment']
    mark_dataBegins = globals()['markPosition'][1]
    mark_inOne = globals()['markPosition'][0]
    tidiedData = globals()['tidiedData']
    i_v_begin = mark_inOne[0]
    i_v_mid = mark_inOne[2]
    
    for i_v, v in mark_dataBegins:
        i_vF = i_v_begin
        if exp == 'Output':
            Idhead = 'Id(Vg' + v +')'
        elif exp == 'transfer':
            Idhead = 'Id(Vd' + v +')'
        tidiedData['forward'][0].append(Idhead)
        for row in tidiedData['forward'][1:len(tidiedData['forward'])]:
            row.append(data[i_vF][i_Id])
            i_vF += 1
        i_vB = i_v_mid
        tidiedData['backward'][0].append(Idhead)
        for row in tidiedData['backward'][1:len(tidiedData['backward'])]:
            row.append(data[i_vB][i_Id])
            i_vB += 1
        rowIndex = mark_dataBegins.index([i_v, v])
        if rowIndex == len(mark_dataBegins)-1:
            globals()['tidiedData'] = tidiedData
            break
        i_v_begin = mark_dataBegins[rowIndex+1][0] + (i_v_begin - i_v)        
        i_v_mid = mark_dataBegins[rowIndex+1][0] + (i_v_mid - i_v)
    conbineData = []
    for i in range(len(tidiedData['forward'])):
        row = tidiedData['forward'][i] + tidiedData['backward'][i]
        conbineData += [row]
    globals()['tidiedData'] = conbineData
    return True
'''
    mark the begin, middle and end index
'''
    
def doMarkInSingle(data, parameter, index_Vot):
    para = parameter
    r_V = para['V_range']
    in_V = para['V_Interval']
#     print(r_Vd[0])
    col_Vot_forward = None
    col_Vot_backward = None
    for i in range(1, len(data)):
        '''
            calculate the interval between adjacent data
            set up some value
        '''
        VotValue = data[i][index_Vot]
        VotValue = float(VotValue)
#         print(VdValue)
        if i == 1 : 
            upSubstraction = 0
            downSubstraction = float(data[i+1][index_Vot]) - float(data[i][index_Vot])
        elif i == len(data)- 1:
            upSubstraction = float(data[i][index_Vot]) - float(data[i-1][index_Vot])
            downSubstraction = 0
        else:
            upSubstraction = float(data[i][index_Vot]) - float(data[i-1][index_Vot])
            downSubstraction = float(data[i+1][index_Vot]) - float(data[i][index_Vot])            
        upSubstraction = round(abs(upSubstraction), 5)
        downSubstraction = round(abs(downSubstraction), 5)
        '''
            construct Vg values, forward and backward
        '''
        if col_Vot_forward != None and col_Vot_backward == None:
            col_Vot_forward.append([data[i][index_Vot]])
        if col_Vot_backward != None:
            col_Vot_backward.append([data[i][index_Vot]])
        
        '''
            figure out the position row about beginning, middle and end
        '''
        if (VotValue == r_V[1]
                and upSubstraction != in_V
                and downSubstraction == in_V
                ):
            part_act = 'downstair'
            begin_row = i
            globals()['markPosition'] = [[begin_row, part_act]]            #mark the special row index in Data
            col_Vot_forward = [['V_downstair']]
            col_Vot_forward.append([data[i][index_Vot]])
        elif (VotValue == r_V[0]
                and upSubstraction != in_V
                and downSubstraction == in_V
                ):
            part_act = 'upstair'
            begin_row = i            
            globals()['markPosition'] = [[begin_row, part_act]]
            col_Vot_forward = [['V_upstair']]
            col_Vot_forward.append([data[i][index_Vot]])
        elif ((VotValue == r_V[0] or VotValue == r_V[1])
                and upSubstraction == in_V
                and downSubstraction == in_V):
            middle_row = i
            col_Vot_backward = [['V_backScan']]
            col_Vot_backward.append([data[i][index_Vot]])
            globals()['markPosition'][0].append(middle_row)
        elif upSubstraction == in_V and downSubstraction != in_V:
            end_row = i
            globals()['markPosition'][0].append(end_row)
            globals()['tidiedData'] = {'forward':col_Vot_forward,
                                       'backward':col_Vot_backward}
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
    parameters = {'directory': 'C:/workspace/Data/test data/YYY', 
                  'experiment': 'transfer', 
                  'dataFile': ['S1DB transfer.csv'], 
                  'V_range': (-60.0, 60.0), 
                  'V_Interval': 0.5, 
                  'iflog': True
                  }


    tidyData(parameters)