# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 16:45:25 2018

@author: NghiLam
"""
import os
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
