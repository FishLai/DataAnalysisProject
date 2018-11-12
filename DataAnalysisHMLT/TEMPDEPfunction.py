'''
Created on Nov 4, 2018

@author: quan_
'''
import IOfunctions, re

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
    try:
        allData = globals()['dictData']
    except:
        print('there is no collected data')
    exps = list(allData.keys())
    for exp in exps:
        Vconsts = list(allData[exp].keys())
        for Vconst in Vconsts:
            datas = allData[exp][Vconst]
            data_f = datas['forward']
            data_b = datas['backward']
            data = doCombineFandB(data_f, data_b) ##Combine forward and backward in a file
            para = {'directory':directory,
                    'experiment':exp + '_' + Vconst + '_temperature-depend',
                    }
            IOfunctions.saveCSV(para, data)
    globals().pop('dictData', None)
    return "Down"

def doCombineFandB(fowardData, backwardData):
    f = fowardData
    fhs = list(f[0].keys())
    b = backwardData
    bhs = list(b[0].keys())
    V_fh = ([fh 
           for fh in fhs 
           if 'V' in fh][0]
           )
    V_bh = ([bh
           for bh in bhs
           if 'V' in bh][0])
    heads = [V_fh]
    pat = re.compile('\((\d+\.*\d*)K')
    I_heads = [h for h in fhs if 'V' not in h]
    for i, I_head in enumerate(I_heads[0:len(I_heads)-1]):
        for j, I_head2 in enumerate(I_heads[i+1:len(I_heads)]):
            temp = int(re.search(pat, I_head).group(1))
            temp2 = int(re.search(pat, I_head2).group(1))
            if temp > temp2:
                big = I_head
                I_heads[i] = I_head2
                I_head = I_head2
                I_heads[j] = big
    heads = heads + I_heads + [V_bh] + I_heads
    i_back = heads.index(V_bh)
    data = [heads]
    for i, row_f in enumerate(f):
        row_b = b[i]
        row = []
        for j, head in enumerate(heads):
            if j < i_back:
                row.append(row_f[head])
            else:
                row.append(row_b[head])
        data.append(row)
    return data
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
    dir = "C:\\workspace\\Data\\181007\\181111Tidied"
    tidyForTempDepend(dir)
    pass