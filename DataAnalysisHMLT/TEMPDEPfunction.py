'''
Created on Nov 4, 2018

@author: quan_
'''
import IOfunctions, fnmatch, re

def tidyForTempDepend(directory):
    fns = IOfunctions.showDataFiles(directory)
    pat = re.compile('(transfer|Output)\S*_(\d+\.*\d*K)')
    for fn in fns:
        part = re.search(pat, fn)
        exp = part.group(1)
        temp = part.group(2)
        doConvertListToDictData(directory = directory, 
                                file = fn,
                                experiment = exp,
                                temperature = temp
                               )
    for row in globals()['dictData']['transfer']['(Vd1.5)']['forward']:
        print(row['Vg_downstair']+', '+row['Id(300K)'])
def doConvertListToDictData(**kwgs):
    dir = kwgs['directory']
    fn = kwgs['file']
    exp = kwgs['experiment']
    temp = kwgs['temperature']
    if 'dictData' not in globals():
        globals()['dictData'] = {}
    dictData = globals()['dictData']
    if exp not in dictData:
        dictData[exp] = {}
    listData = IOfunctions.loadTidiedData(directory = dir,file = fn)
    heads = listData[0]
    i_backScan = heads.index(([head 
                               for head in heads 
                               if 'back' in head][0]))
    pat = re.compile('\(\S*\)')
    if dictData[exp] != {}:
        for i, head in enumerate(heads):
            if i < i_backScan:
                const_V = re.search(pat, head)
                if 'I' in head:
                    const_V = const_V.group()
                    if const_V not in dictData[exp]:
                        dictData[exp][const_V] = {}
                    if 'forward' not in dictData[exp][const_V]:
                        dictData[exp][const_V]['forward'] = []
                        dictData[exp][const_V]['backward'] = []
            else:
                break
        for j, row in enumerate(listData[1:len(listData)]):
            row_f = {}
            row_b = {}
            for i, val in enumerate(row):
                const_V = re.search(pat, heads[i])
                row_f_in = {}
                row_b_in = {}
                if i < i_backScan:
                    if const_V is not None:
                        const_V = const_V.group()
                        data_f = dictData[exp][const_V]['forward']
                        base_V = len(data_f)
                        base = len(listData) - 1
                        if data_f != [] and base_V == base:
                            head = 'Id(' + temp + ')'
                            data_f[j][head] = val
                        elif len(data_f) - j == 0:
                            head = 'Id(' + temp + ')'
                            row_f_in.update(row_f)
                            row_f_in[head] = val
                            data_f.append(row_f_in)
                        else:
                            print("your data has different voltage base")
                    else:
                        head = heads[i]                    
                        row_f[head] = val
                else:
                    if const_V is not None:
                        const_V = const_V.group()
                        data_b = dictData[exp][const_V]['backward']
                        base_V = len(data_b)
                        base = len(listData) - 1
                        if data_b != [] and base_V == base:
                            head = 'Id(' + temp + ')'
                            data_b[j][head] = val
                        elif len(data_b) - j == 0 :
                            head = 'Id(' + temp + ')'
                            row_b_in.update(row_b)
                            row_b_in[head] = val
                            data_b.append(row_b_in)
                    else:
                        head = heads[i]                    
                        row_b[head] = val
    else:
        for i, head in enumerate(heads):
            if i < i_backScan:
                const_V = re.search(pat, head)
                if 'I' in head:
                    const_V = const_V.group()
                    dictData[exp][const_V] = {}
                    dictData[exp][const_V]['forward'] = []
                    dictData[exp][const_V]['backward'] = []
        for row in listData[1:len(listData)]:
            row_f = {}
            row_b = {}
            for i, val in enumerate(row):
                row_f_in = {}
                row_b_in = {}
                const_V = re.search(pat, heads[i])
                if i < i_backScan:
                    if const_V is not None:
                        const_V = const_V.group()
                        data_f = dictData[exp][const_V]['forward']
                        head = 'Id(' + temp + ')'
                        row_f_in.update(row_f)
                        row_f_in[head] = val
                        data_f.append(row_f_in)
                    else:
                        head = heads[i]                    
                        row_f[head] = val
                else:
                    if const_V is not None:
                        const_V = const_V.group()
                        data_b = dictData[exp][const_V]['backward']
                        head = 'Id(' + temp + ')'
                        row_b_in.update(row_b)
                        row_b_in[head] = val
                        data_b.append(row_b_in)
                    else:
                        head = heads[i]              
                        row_b[head] = val
    globals()['dictData'] = dictData
    return True

if __name__ == '__main__':
    dir = "C:\\workspace\\Data\\181104\\Temperature-depend\\transfer"
    tidyForTempDepend(dir)
    pass