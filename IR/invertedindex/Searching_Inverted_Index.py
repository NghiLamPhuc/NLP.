from datetime import datetime
import re
import json

link_folder = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\'
link_output = link_folder + 'output\\'
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
    f = open (link_output+'InvertedIndex.txt','r',encoding='utf-8-sig')
    inverted = json.load(f)
    print ('Có ' + str(len(inverted)) + ' tiếng.')
# =========================== Đếm từ nào nhiều nhất ===========================
    
        
    
# ================================ stop words.=================================
    stop_words = get_stop_words()
#    print (stop_words)
# =============================== Câu cần tìm =================================
#    query = 'rau an toàn'
#    query = 'rau an toàn chật vật tìm chỗ đứng'
#    query = 'Cụ thể, các quan chức liên quan sẽ không được phép vào EU.'
#    query = 'Quốc, hội, châu, Âu.'
    query = 'Quốc hội châu'
#    query = 'bệnh viện'
#    query = 'bệnh'
#    query = 'thức ăn'
#    query = 'thức tỉnh'
#    query = 'thức'
#    query = 'các'
#    query = 'các một'
#    query = 'bệnh ăn'
#    query = 'của bệnh'
#    query = "kinh tế xhcn"
# ============================ Xử lý câu cần tìm ==============================    
    query = query.lower()
    query = re.sub('[^\w\s]','',query)
    words = query.split()
    
    print ("Cần Tìm: ")
    print (words)
    
# =============================== Bắt đầu tìm =================================
    found_at_first_word = [] # Luu vi tri cua tu.
    out_file = open(link_output+'output.txt','w',encoding='utf-8-sig') # Luu KET QUA CUOI CUNG.
# =============================== Bắt đầu tìm =============== nếu query có 1 từ
    if len(words) == 1:
        if words[0] in stop_words:
            print ('Từ %s là stop word.' % words[0])
        else:
            for pos in inverted[words[0]]['doc1']:
                found_at_first_word.append(pos)
            print ('Inverted index của từ "%s" có %d phần từ.' % (words[0],len(inverted[words[0]]['doc1'])))
               
# =============================== Bắt đầu tìm =============== nếu query có 2 từ
    if len(words) == 2:
#        Nếu cả là stop word.
        if words[0] in stop_words:
            if words[1] in stop_words:
                print ('"%s %s" là stop word.' % (words[0],words[1]))
            else:
#                Tìm vị trí từ thứ 2, trừ đi len(từ thứ 1) - 1
#                Dò lại trong document vị trí mới đó.
                temp = open(link_document+'removed 0.txt','r',encoding='utf-8-sig')
                document_1 = temp.read()
                for pos in inverted[words[1]]['doc1']:
                    pos_of_stop_word = pos - len(words[0]) -1
                    end_of_stop_word = pos - 2
#                    print (end_of_stop_word)
                    words_0 = ''
                    for character in range(pos_of_stop_word,end_of_stop_word+1):
                        words_0 = words_0 + document_1[character]
#                    print (words_0)
                    if words_0 == words[0]:
                        found_at_first_word.append(pos)
                temp.close()
        elif words[1] in stop_words:
            temp = open(link_document+'removed 0.txt','r',encoding='utf-8-sig')
            document_1 = temp.read()
            for pos in inverted[words[0]]['doc1']:
                pos_of_stop_word = pos + len(words[0])
                end_of_stop_word = pos_of_stop_word + len(words[1]) -1
                words_1 = ''
                for character in range(pos_of_stop_word,end_of_stop_word):
                    words_1 = words_1 + document_1[character]
                    if words_1 == words[1]:
                        found_at_first_word.append(pos)
            temp.close()
        else:
            for pos_0 in inverted[words[0]]['doc1']:
                next_0 = pos_0 + len(words[0]) + 1
                if next_0 in inverted[words[1]]['doc1']:
                    found_at_first_word.append(pos_0)
# =============================== Bắt đầu tìm =================================
    if len(words) > 2:
        for pos_0 in inverted[words[0]]['doc1']:
            next_0 = pos_0 + len(words[0]) + 1
            for i in range(1,len(words)):
                if next_0 in inverted[words[i]]['doc1']:
                    next_0 = next_0 + len(words[i]) + 1
                else: break
            if words[i] == words[-1]:
                found_at_first_word.append(pos_0)
# =============================== Ghi vi tri vao KET QUA CUOI CUNG ============
    out_file.write('Found at: ')
    for i in found_at_first_word:
        out_file.write(str(i)+' ')
    out_file.write('\n\n')
    
# =============================== In câu chứa từ cần tìm  =====================
    f1 = open(link_document+'removed 0.txt','r',encoding='utf-8-sig')
    doc1 = f1.read()
    
    len_query = len(words)
    for w in words:
        len_query = len_query + len(w)
        
#    out_file = open(link_folder+'output.txt','w',encoding='utf-8-sig')
        
    for index,pos in enumerate(found_at_first_word):
        sentence_pos = ''
        if pos-30 <= 0: pos_left_show = pos
        else: pos_left_show = pos-30
        
        if pos+len_query+20 > len(doc1): pos_right_show = pos+len_query
        else: pos_right_show = pos+len_query+20
        
        for i in range(pos_left_show,pos_right_show):
            sentence_pos = sentence_pos + doc1[i]
        sentence_pos = '...' + sentence_pos + '...'
        
        out_file.write(str(index+1)+' '+sentence_pos+'\n')
        
    print ()
    print (datetime.now()-start)    
if __name__ == "__main__":main()
