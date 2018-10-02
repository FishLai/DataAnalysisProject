'''
Created on 2018年9月30日

@author: quan_
'''
import os, fnmatch

def showDataFiles(directory):
    d = directory
#     print(d)
    files = os.listdir(d)
    dfiles = fnmatch.filter(files, '*.csv')
#     print(dfiles)
    return dfiles

if __name__ == "__main__":
    dir = "C:/workspace/Data/180927"
    showDataFiles(dir)
