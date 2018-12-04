from datetime import datetime
import json

link_folder = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\'

def main():
    start=datetime.now()
# Đọc file inverted index.====================================================
    f = open (link_folder+'InvertedIndex.txt','r',encoding='utf-8-sig')
    wlist = json.load(f)
    
#    print (wlist['hải'])
#    for doc_id,positions in wlist['hải'].items():
#        print (doc_id,positions)
    
    print ()
    print (datetime.now()-start)    
if __name__ == "__main__":main()