from datetime import datetime
import re
import json

link_folder = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\'
link_document = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\input\\'

def get_stop_words():
    f = open(link_folder+'stopwords.txt','r',encoding='utf-8-sig')
    stopwords = set()
    for line in f:
        line = line.replace('\n','')
        stopwords.add(line)
    return stopwords

def add_pos(pos,word):
    return pos+len(word)+1

def main():
    start=datetime.now()
# =========================== Đọc file inverted index.=========================
    f = open (link_folder+'InvertedIndex.txt','r',encoding='utf-8-sig')
    inverted = json.load(f)
# ================================ stop words.=================================
    stop_words = get_stop_words()
#    print (stop_words)
# =============================== Câu cần tìm =================================
    query = 'rau an toàn'
#    query = 'rau an toàn chật vật tìm chỗ đứng'
#    query = 'Cụ thể, các quan chức liên quan sẽ không được phép vào EU.'
#    query = 'Quốc, hội, châu, Âu.'
    
    query = query.lower()
    query = re.sub('[^\w\s]','',query)
    words = query.split()
    print (words)
    
    print ("Cần Tìm: "+query)
    
    found_at_last_word = []

                
    for pos_0 in inverted[words[0]]['doc1']:
        next_0 = pos_0 + len(words[0]) + 1
        for i in range(1,len(words)):
            if next_0 in inverted[words[i]]['doc1']:
                next_0 = next_0 + len(words[i]) + 1
            else: break
        if words[i] == words[-1]:
            found_at_last_word.append(pos_0)
    
    print (found_at_last_word)
    f1 = open(link_document+'removed 0.txt','r',encoding='utf-8-sig')
    doc1 = f1.read()
    
    len_query = len(words)
    for w in words:
        len_query = len_query + len(w)
        
    
    for pos in found_at_last_word:
        sentence_pos = ''
        if pos-30 <= 0:
            pos_show = pos
        else: pos_show = pos-30
        for i in range(pos_show,pos+len_query+20):
            sentence_pos = sentence_pos + doc1[i]
        sentence_pos = '...' + sentence_pos + '...'
        print (sentence_pos)
        print ()
        
        
    print ()
    print (datetime.now()-start)    
if __name__ == "__main__":main()
