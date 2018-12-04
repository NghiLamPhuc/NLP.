from datetime import datetime
import json
from collections import defaultdict
import re
start=datetime.now()
from nltk.tokenize import word_tokenize
import os
#import nltk
#nltk.download('punkt')

link_raw_text = '\\Users\\NghiLam\\Documents\\NLP\\RAW_TEXT\\van ban tho\\'
#link_raw_text = '\\Users\\NghiLam\\Documents\\NLP\\IR\\txt\\'

link_folder = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\'
link_input = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\input\\'
link_sauKhiRemoveSome = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\sauKhiRemoveSome\\'
link_sauKhiTokenize = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\sauKhiTokenize\\'

#global
wlist = []
def remove_last_line_from_string(s):
    return s[:s.rfind('\n')]
#============================================================================== Loại bỏ một số dấu trng văn bản input.
def remove_some(s):
    new_s = re.sub('<<\w\s','',s)
    new_s = re.sub('\/\w>>','',new_s)
    new_s = re.sub('>>\s', '', new_s)
    new_s = re.sub('C. Ronaldo', 'C.Ronaldo', new_s)
    new_s = re.sub('\s\.\.\.', '...', new_s)
    new_s = re.sub('\n+','\n',new_s)

#    new_s = re.sub("[a-z][A-Z]\'\'",'"',new_s)                                 # 2 nháy đơn thành nháy kép.
#    new_s = re.sub('\[\[','[',new_s)
#    new_s = re.sub('\]\]',']',new_s)
    return new_s
#============================================================================== Loai bo ky tu trong file text.
def sauKhiRemoveSome():
    all_files = os.listdir(link_raw_text)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)
    for index, file in enumerate(txt_files):
        inputFile = open(link_raw_text+file,'r',encoding='utf-8-sig').read()
        inputFile = remove_some(inputFile)
        with open(link_sauKhiRemoveSome+'removed ' + str(index) + '.txt','w',encoding='utf-8-sig') as f:
            f.write('%s\n' % inputFile)
#============================================================================== Tach tu, moi phan tu la 1 cau sau khi tach.            
def sauKhiTokenize():
    all_files = os.listdir(link_sauKhiRemoveSome)
    print (all_files)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)
    for index,file in enumerate(txt_files):
        word_seg(file)
        with open(link_sauKhiTokenize+'tokenize file ' + str(index) + '.txt','w',encoding='utf-8-sig') as f:
#            for index,item in enumerate(wlist):
            for item in wlist:
                f.write('%s\n' % item)
#        print ('Xong file thứ %s.' % (index+1))
        print ('Xong file %s' % file)
#        f.close()
        wlist.clear()
#============================================================================== .Xu ly 1 removed
def word_seg(file_name):
    input_file = open(link_sauKhiRemoveSome+file_name,'r',encoding='utf-8-sig')
    for line in input_file:
        wlist.append(word_tokenize(line))
    del wlist[-1]
#==============================================================================Print removed file
def printRemovedFile(file_name):
    f = open(link_sauKhiRemoveSome+file_name,'r',encoding='utf-8-sig')
    for index, i in enumerate(f):
        print (index,i)
    
#==============================================================================Print
        
#==============================================================================Count word 1 doc
def InvertedIndex(doc_name,doc_id):
    inverted = dict()
    doc = open(link_sauKhiRemoveSome+doc_name,'r',encoding='utf-8-sig')
    s = ''
    for line in doc:
        line = line.lower()
        line = line.replace('\n','')
        list_word = line.split()
            
        
            
def main():
    
    global wlist
#    sauKhiRemoveSome()
    
#    sauKhiTokenize()
    
#    printRemovedFile('removed 0.txt')
        
#    InvertedIndex('removed 0.txt',0)
    f = open (link_folder+'InvertedIndex.txt','r',encoding='utf-8-sig')
    wlist = json.load(f)
    print (wlist['rau'])
    
    print ()
    print (datetime.now()-start)    
if __name__ == "__main__":main()

