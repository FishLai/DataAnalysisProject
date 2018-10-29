'''
Created on Oct 29, 2018

@author: quan_
'''

import sys
from cx_Freeze import setup, Executable

build_exe_options = {'build_exe':{
                          'includes':['atexit', 'IOfunctions', 'MainFramDemo',
                                      'PARSEfunctions'
                                      ],
                          'path' : sys.path
                            }
                }
base = None
if sys.platform =="win32":
    base = "Win32GUI"
setup( name = "AnalysisData",
       version = '1.0',
       description = "tidy transfer and output data only",
       options = build_exe_options,
       executables = [Executable("mainWindow.py", base=base)])