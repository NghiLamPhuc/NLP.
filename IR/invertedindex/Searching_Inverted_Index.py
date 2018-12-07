from datetime import datetime
import re
import json
import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

link_folder = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\'
link_output = link_folder + 'output\\'
link_model = link_folder + 'model\\'
link_document = '\\Users\\NghiLam\\Documents\\NLP\\IR\\invertedindex\\input\\'

def get_stop_words():
    f = open(link_folder+'stopwords.txt','r',encoding='utf-8-sig')
    stopwords = set()
    for line in f:
        line = line.replace('\n','')
        stopwords.add(line)
    return stopwords

def run(index,find_word):#=========================================================   main
# =========================== Đọc file inverted index.=========================
    f = open (link_model+'InvertedIndex.txt','r',encoding='utf-8-sig')
    inverted = json.load(f)    
# ================================ stop words.=================================
    stop_words = get_stop_words()
# ============================ Xử lý câu cần tìm ==============================    
    regex1 = re.compile('(?<=[^\w+])(?=\w)')
    regex2 = re.compile('(?<=\w)(?=[^\w+])')
    
    query = find_word.lower()
#    query = re.sub('[^\w\s]','',query)
    query = re.sub(regex1, ' ', query)
    query = re.sub(regex2, ' ', query)
    words = query.split()
# ============================================================================= Bắt đầu tìm ==
    found_at_first_word = [] # Luu vi tri cua tu.
    doc_id = 'doc' + str(index)
    
    doc_name = 'removed '+ str(index-1) +'.txt'
# =============================== Bắt đầu tìm =============== nếu query có 1 từ
    if len(words) == 1:
        if words[0] in stop_words:
#            print ('Từ %s là stop word.' % words[0])
            return -1
        else:
            if doc_id not in inverted[words[0]]:
                return 0
            else:
                for pos in inverted[words[0]][doc_id]:
                   found_at_first_word.append(pos)
# =============================== Bắt đầu tìm =============== nếu query có 2 từ
    if len(words) == 2:
#        Nếu cả là stop word.
        if words[0] in stop_words:
            if words[1] in stop_words:
#                print ('"%s %s" là stop word.' % (words[0],words[1]))
                return -1
            else:
#                Tìm vị trí từ thứ 2, trừ đi len(từ thứ 1) - 1
#                Dò lại trong document vị trí mới đó.
                temp = open(link_document+doc_name,'r',encoding='utf-8-sig')
                document_1 = temp.read()
                if doc_id not in inverted[words[1]]:
                    return 0
                else:
                    for pos in inverted[words[1]][doc_id]:
                        pos_of_stop_word = pos - len(words[0]) -1
                        end_of_stop_word = pos - 2
                        words_0 = ''
                        for character in range(pos_of_stop_word,end_of_stop_word+1):
                            words_0 = words_0 + document_1[character]
                        if words_0 == words[0]:
                            found_at_first_word.append(pos)
                    temp.close()
        elif words[1] in stop_words:
            temp = open(link_document+doc_name,'r',encoding='utf-8-sig')
            document_1 = temp.read()
            if doc_id not in inverted[words[0]]:
                return 0
            else:
                for pos in inverted[words[0]][doc_id]:
                    pos_of_stop_word = pos + len(words[0])
                    end_of_stop_word = pos_of_stop_word + len(words[1]) -1
                    words_1 = ''
                    for character in range(pos_of_stop_word,end_of_stop_word):
                        words_1 = words_1 + document_1[character]
                        if words_1 == words[1]:
                            found_at_first_word.append(pos)
                temp.close()
        else:
            if doc_id not in inverted[words[0]]:
                return 0
            else:
                for pos_0 in inverted[words[0]][doc_id]:
                    next_0 = pos_0 + len(words[0]) + 1
                    if next_0 in inverted[words[1]][doc_id]:
                        found_at_first_word.append(pos_0)
# =============================== Bắt đầu tìm ========================== nhiều hơn 2 từ
    if len(words) > 2:
#        Nếu từ đầu tiên là stop word
#        if words[0] in stop_words:
        for pos_0 in inverted[words[0]][doc_id]:
            next_0 = pos_0 + len(words[0]) + 1
            for i in range(1,len(words)):
#                Kieerm tra ky tu dac biet.
                if words[i].isalnum():
    #                Kiểm tra stop word
                    if words[i] in stop_words:
    #                while (words[i] in stop_words):
                        next_0 = next_0 + len(words[i]) + 1
                        continue
                    else:
                        if next_0 in inverted[words[i]][doc_id]:
                            next_0 = next_0 + len(words[i]) + 1
                        else: break
                        if words[i] == words[-1]:
                            found_at_first_word.append(pos_0)
                else:# Neu words[i] la ky tu dac biet.
                    next_0 = next_0 + 1
                    
# =============================== Ghi vi tri vao KET QUA CUOI CUNG =========================================
    if found_at_first_word:
        out_file = open(link_output + find_word + '\\' + doc_id+'.txt','w',encoding='utf-8-sig') # Luu KET QUA CUOI CUNG.
        out_file.write('Found at: ')
        for i in found_at_first_word:
            out_file.write(str(i)+' ')
        out_file.write('\n\n')
# =============================== In câu chứa từ cần tìm  =====================
        f1 = open(link_document+doc_name,'r',encoding='utf-8-sig')
        doc1 = f1.read()
        
        len_query = len(words)
        for w in words:
            len_query = len_query + len(w)
    
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
        return 1
    else:
#        print ('Không tìm thấy')
        return 0
    
def document_contain_query(num_of_doct):
    ket_qua = [] # Lưu các document có chứa query.
    for i in range(1,num_of_doct+1):
        if run(i,query):
            ket_qua.append(str(i))
    if ket_qua: return ket_qua,1
    else: return ket_qua,0
# ======================================================================== Câu cần tìm =================================
#query = 'rau an toàn'
#query = 'rau an toàn chật vật tìm chỗ đứng'
#query = 'Tôi từng thuộc danh sách những cầu thủ nòng cốt cho tới'
#query = 'Quốc, hội, châu, Âu.'
#query = 'Quốc hội châu Âu'
#query = 'Quốc hội châu'
#query = 'bệnh viện'
#query = 'bệnh'
#query = 'thức ăn'
#query = 'thức tỉnh'
#query = 'thức'
#query = 'các'
#query = 'các một'
#query = 'bệnh ăn'
#query = 'của bệnh'
#query = "xhcn"
#query = "667"
#query = 'văn hóa Việt Nam'
#query = 'khoa học kỹ thuật'
#query = 'tai nạn giao thông'
#query = 'lê nin về vấn đề dân tộc'
#query = 'lê nin'
#query = 'hối lộ'
#query = 'hành vi đáng lên án'
#query = 'bạo lực học đường'
#query = 'điện thoại di động'
#query = 'nghĩa vụ quân sự'
#query = 'an ninh nhân dân'
#query = 'cảnh sát cơ động'
#query = 'trật tự an toàn xã hội'
#query = 'xuống cấp'
#query = 'thoái hóa đạo đức'
#query = 'nhà giáo ưu tú'
#query = 'nhà nước'
#query = 'dân do dân vì dân'
#query = 'ấm no hạnh phúc'
#query = 'điện ảnh việt nam'
#query = 'an toàn vệ sinh thực phẩm'
#query = 'kế hoạch hóa gia đình'
#query = 'nông thôn mới'
#query = 'nước phát triển'
#query = 'triều tiên'
#query = 'nhật bản'
#query = 'hàn quốc'
#query = 'trung quốc'
#query = 'tiểu vương quốc ả rập thống nhất'
#query = 'bất công'
#query = 'nợ công'
#query = 'tăng lương'
    
def main():
    start=datetime.now()
    print ("Cần Tìm: '%s'" % query)
    createFolder('./output/%s' % query)
    a,b = document_contain_query(9)
    if b == 0:
        print ('Không tìm thấy.')
    elif b == 1:
        print ('Tìm thấy tại các document: ')
        print (a)
    elif b == -1:
        print ('Từ cần tìm thuộc stop words.')
    print (datetime.now()-start)
if __name__ == "__main__":main()
