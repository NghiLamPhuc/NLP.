from nltk.stem import PorterStemmer
ps = PorterStemmer()
import os
from functools import reduce
import json
from datetime import datetime
start=datetime.now()

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

#http://xltiengviet.wikia.com/wiki/Danh_s%C3%A1ch_stop_word     stopwords

#https://github.com/stopwords/vietnamese-stopwords              stopwords2

#https://www.ranks.nl/stopwords                           stop word in English
file = open('stopwords.txt','r',encoding = 'utf-8-sig')
#file = open('stopwords2.txt','r',encoding = 'utf-8-sig')
#file = open('stopwords_Eng.txt','r',encoding = 'utf-8-sig')
stopwords = set()
for line in file:
    line = line.replace('\n','')
    stopwords.add(line)

def word_split(text):

    word_list = []  #(vị trí chữ cái bắt đầu, từ)
    wcurrent = []
    windex = None

    for i, c in enumerate(text):
        if c.isalnum():
            wcurrent.append(c)
            windex = i
#        elif (c.isalnum() == False):
#            windex = windex+1
        elif wcurrent:
            word = ''.join(wcurrent)
            word_list.append((windex - len(word) + 1, word))
            wcurrent = []

    if wcurrent:
        word = ''.join(wcurrent)
        word_list.append((windex - len(word) + 1, word))

#    f = open(link_outfile + 'wordlist.txt','w',encoding='utf-8-sig')
#    f.write('\n'.join('%s %s' % x for x in word_list))
    
    
    print ()

    return word_list

#Lấy ra các từ không có trong stop words.
def words_not_stop(words):
    not_stop_words = []
    is_stop_words = []
    for index, word in words:
        if word in stopwords:
#            continue
            is_stop_words.append((index, word))
        else: 
            not_stop_words.append((index, word))
    
#    Ghi file stop word
    
    return not_stop_words

    
def words_normalize(words): 
#                                             Trong tiếng Anh phải thêm STEMMING
    normalized_words = []
    for index, word in words:
        wnormalized = word.lower()
#        wnormalized = ps.stem(wnormalized)                       # stemming
        normalized_words.append((index, wnormalized))
    return normalized_words

def word_index(text):
    words = word_split(text)
    words = words_normalize(words)
    words = words_not_stop(words)
    return words


def get_max_count(invert):        
    _max=max(invert, key=lambda k: len(invert[k]))
    return _max

# Liệt kê từ xuất hiện vị trí nào trong 1 documents.
def inverted_index(text):
    inverted = {}

    for index, word in word_index(text):
        locations = inverted.setdefault(word, [])
        locations.append(index)
    
    # Dem so lan xuat hien max
    print ('Tiếng nhiều nhất.')
    print (get_max_count(inverted))
    
#    print (inverted)
    return inverted

#doc_index là 1 inverted_index.
def inverted_index_add(inverted, doc_id, doc_index):
    for word, locations in doc_index.items():
        temp = inverted.setdefault(word, {})
        temp[doc_id] = locations

#    print (inverted)
    return inverted

#   Duyệt trong query, nếu có từ trong stop words thì bỏ đi.
#    Thịt vịt có tính hàn => Thịt vịt tính hàn
#    results đầu tiên lưu danh sách document có từng từ thịt, vịt, tính, hàn.
#    Sau đó lấy giao theo : ((thịt-vịt)-tính)-hàn)
def search(inverted, query):
    words = []
    results = []
    
#    Lấy ra các từ (not in stop words).
    for _,word in word_index(query):
        if word in inverted:
            words.append(word)
    print (words)

    for word in words:
        results.append(set(inverted[word].keys()))
#    print (results)
    if results:
        return reduce(lambda x, y: x & y, results)
    return []

def extract_text(doc, index):
    first = index-20
    last = index+20
    if first < 0:
        first = 1
    if last > len(documents[doc]):
        last = index
        
    return documents[doc][first:last].replace('\n', '  ')

#link_text = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\sauKhiRemoveSome\\'
link_text = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\input\\'
link_Eng_text = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\input\\English\\'
link_folder = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\'
link_model = link_folder + 'model\\'
link_outfile = link_folder + 'outfile\\'


if __name__ == '__main__':
    
    createFolder('./model')

    
    f1 = open(link_text+'removed 0.txt','r',encoding='utf-8-sig')
    doc1 = f1.read()
    f2 = open(link_text+'removed 1.txt','r',encoding='utf-8-sig')
    doc2 = f2.read()
    f3 = open(link_text+'removed 2.txt','r',encoding='utf-8-sig')
    doc3 = f3.read()
    
    f4 = open(link_text+'removed 3.txt','r',encoding='utf-8-sig')
    doc4 = f4.read()
    f5 = open(link_text+'removed 4.txt','r',encoding='utf-8-sig')
    doc5 = f5.read()
    f6 = open(link_text+'removed 5.txt','r',encoding='utf-8-sig')
    doc6 = f6.read()
    
    f7 = open(link_text+'removed 6.txt','r',encoding='utf-8-sig')
    doc7 = f7.read()
    f8 = open(link_text+'removed 7.txt','r',encoding='utf-8-sig')
    doc8 = f8.read()
    f9 = open(link_text+'removed 8.txt','r',encoding='utf-8-sig')
    doc9 = f9.read()
    
    inverted = {}
    documents = {'doc1':doc1, 'doc2':doc2, 'doc3':doc3,'doc4':doc4,'doc5':doc5,'doc6':doc6,'doc7':doc7,'doc8':doc8,'doc9':doc9 }
    
    for doc_id, text in documents.items():
        print (doc_id)
        doc_index = inverted_index(text)
        print ('Đầu tiên liệt kê các từ - vị trí trong mỗi document ---------------------\n')
        inverted_index_add(inverted, doc_id, doc_index)
        print ('Sau đó liệt kê các từ - document - vị trí -------------------------------\n')
#        print (inverted)
#        print ()

    # Print Inverted-Index
    f = open(link_model + 'InvertedIndexDisplay.txt','w',encoding='utf-8-sig')
    f1 = open(link_model + 'InvertedIndex.txt','w',encoding='utf-8-sig')
#    json.dump(inverted, f1, ensure_ascii=False))
    f1.write(json.dumps(inverted, ensure_ascii=False))
    for key,value in inverted.items():
#        f.write('%s:%s\n' % (key, value))
        f.write('%s:\n' % key)
        for k,v in value.items():
            f.write('\t%s: %s\n' % (k,v))
#        pprint.pprint(inverted,f)
            
    print ()
    print (datetime.now()-start)
    
