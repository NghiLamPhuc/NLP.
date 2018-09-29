# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 23:21:30 2018

@author: NghiLam
"""

link_folder = '\\Users\\NghiLam\\Desktop\\NLP\\POSTagging\\compare\\'
file1 = link_folder + 'output.txt'
file2 = link_folder + 'test_da2.pos'
file3 = link_folder + 'test_da2_lower.txt'

w1 = set(open(file1,'r',encoding='utf-8'))

#w1 = (open(file1,'r',encoding='utf-8'))
w2 = open(file2,'r',encoding='utf-8')
w3 = set(open(file3,'r',encoding='utf-8'))
#w3 = open(file3,'w',encoding='utf-8')
#
#for lines in w2:
#    line = lines.lower()
#    w3.write(line)

#    
with open(link_folder + 'matches.txt','w',encoding='utf-8') as fout1, open(link_folder + 'differences.txt','w',encoding='utf-8') as fout2:
        fout1.writelines(w1 & w3)
        fout2.writelines(w3 - w1)
