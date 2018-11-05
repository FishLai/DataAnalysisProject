'''
Created on Nov 4, 2018

@author: quan_
'''
import IOfunctions, fnmatch, re

def tidyForTempDepend(directory):
    fns = IOfunctions.showDataFiles(directory)
    pat = re.compile('(transfer|Output)\S*_(\d+\.*\d*K)')
    pool = {}
    for fn in fns:
        dictData = doConvertListToDictData(directory = directory, file = fn)
        part = re.search(pat, fn)
        exp = part.group(1)
        temp = part.group(2)
        if exp not in pool:
            pool[exp] = {}
        pool[exp][temp] = dictData
    temps = list(pool['transfer'].keys())
    exps = list(pool.keys())
    createTempDepData(pool)

def doConvertListToDictData(**kwgs):
    dir = kwgs['directory']
    fn = kwgs['file']
    listData = IOfunctions.loadTidiedData(directory = dir,file = fn)
    heads = listData[0]
    i_backScan = heads.index([head for head in heads if 'back' in head][0])
    dictData = {}
    dictData['forward'] = []
    dictData['backward'] = []
    for row in listData[1:len(listData)]:
        forwardDict = {}
        backDict = {}
        for i, item in enumerate(row):
            if i < i_backScan:
                forwardDict[heads[i]] = item
            else:
                backDict[heads[i]] = item    
        dictData['forward'].append(forwardDict)
        dictData['backward'].append(backDict)
    return dictData

def createTempDepData(dictData):
    exps = list(dictData.keys())
    for exp in exps:
        temps = list(dictData[exp].keys())
        for temp in temps:
            scanDirection = list(dictData[exp][temp].keys())
            for direction in scanDirection:
                heads = list
    pass
if __name__ == '__main__':
    dir = "C:\\workspace\\Data\\181104\\Temperature-depend\\transfer"
    tidyForTempDepend(dir)
    pass