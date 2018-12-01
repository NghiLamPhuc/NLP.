from functools import reduce

#http://xltiengviet.wikia.com/wiki/Danh_s%C3%A1ch_stop_word

file = open('stopwords.txt','r',encoding = 'utf-8-sig')
stopwords = set()
for line in file:
    line = line.replace('\n','')
    line = line.strip()
    stopwords.add(line)

#print (stopwords)

# Hàm này lấy ra danh sách từ, vị trí.
# Vị trí là vị trí chữ cái đầu tiên trong từ.
def word_split(text):

    word_list = []  #(vị trí chữ cái bắt đầu, từ)
    wcurrent = []
    windex = None

    for i, c in enumerate(text):
        if c.isalnum():
            wcurrent.append(c)
            windex = i
        elif len(wcurrent)>0:
            word = ''.join(wcurrent)
            word_list.append((windex - len(word) + 1, word))
            wcurrent = []

    if wcurrent:
        word = ''.join(wcurrent)
        word_list.append((windex - len(word) + 1, word))

#    f = open('wordlist.txt','w',encoding='utf-8-sig')
#    f.write('\n'.join('%s %s' % x for x in word_list))
#    print (word_list)
    
    print ()

    return word_list

#Lấy ra các từ không có trong stop words.
def words_not_stop(words):
    not_stop_words = []
    for index, word in words:
        if word in stopwords:
            continue
        not_stop_words.append((index, word))
    return not_stop_words

def words_normalize(words):
#                                           Trong tiếng Anh phải thêm STEMMING
    normalized_words = []
    for index, word in words:
        wnormalized = word.lower()
        normalized_words.append((index, wnormalized))
    return normalized_words

def word_index(text):
    words = word_split(text)            #Tách từ, vị trí.
    words = words_normalize(words)      #Viết hoa -> thường.
    words = words_not_stop(words)       #Lấy những từ không có trong stop word.
    return words

# Liệt kê từ xuất hiện vị trí nào trong 1 documents.
def inverted_index(text):
    inverted = {}
    
    word_pos = word_index(text)
#    for index, word in word_index(text):
    for index, word in word_pos:
        locations = inverted.setdefault(word, [])
        locations.append(index)
    
#    print ('This is inverted of one text')
#    print (inverted)
    return inverted

#doc_index là 1 inverted_index.
# Hàm này kết hợp các inverted riêng rẻ, gán thêm vị trí document.
# Đầu tiên duyệt các từ trong 1 inverted, để lấy từ và location.
# Sau đó thêm vào một dict có cấu trúc key1: từ key2 document id: value là bộ các vị trí
#                                                                   ứng trong từng document.
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
    stop_words = {}
    result = dict()
    results = []
    
#    Lấy ra các từ (not in stop words)
#    for _,word in word_index(query):
#        if word in inverted:
#            words.append(word)
    t1 = word_split(query)
    t1 = words_normalize(t1)
    for index,w in t1:
        if w not in stopwords:
            words.append(w)
            print (w)
        else:
            stop_words.setdefault(index,w)
    print (stop_words)
    for word in words:
        print ('\t'+word)
#        for k,v in inverted[word].items():
#            print (k,v)
#            temp = result.setdefault(word,{})
#            temp[k] = v
#    for word in words:
#        print ('\t'+word)
        print (set(inverted[word].keys()))
        results.append(set(inverted[word].keys()))
        
    
    if results:
        return reduce(lambda x, y: x & y, results)
    return []

def search2(inverted, query):
    words = []
    results = []
    result = dict()
    
#    Lấy ra các từ (not in stop words).
    for _,word in word_index(query):
        if word in inverted:
            words.append(word)

    for word in words:
        print ('\t'+word)
        for k,v in inverted[word].items():
#            print (k,v)
            temp = result.setdefault(word,{})
            temp[k] = v
#    print (result)
    for key,value in result.items():
        for k,v in value.items():
            for i in v:
                print (i)
    if result:
        return result
    return []

def extract_text(doc, index):
    first = index-20
    last = index+20
    if first < 0:
        first = 1
    if last > len(documents[doc]):
        last = index
        
    return documents[doc][first:last].replace('\n', '  ')

if __name__ == '__main__':
#    document string
#    https://suckhoe.vnexpress.net/tin-tuc/dinh-duong/an-thit-ga-hay-thit-vit-tot-hon-3845985.html
    doc1 = """
Thịt gà dồi dài protein. Theo Bảng thành phần dinh dưỡng Việt Nam, trong 100 g thịt gà chứa 199 kcalo, 20,3 g protein, 4,3 g chất béo và nhiều vitamin, khoáng chất có lợi cho sức khỏe. Có khoảng 75 mg cholesterol trong 100 g thịt gà. 

Thịt vịt không phổ biến như thịt gà nhưng hàm lượng dinh dưỡng cao hơn. Trong Đông y, thịt vịt được coi là loại thuốc bổ điều hòa ngũ tạng, lợi thủy, trừ nhiệt, bổ hư. Trong 100 g thịt vịt có 267 kcalo, 7,3 g chất béo, 17,8 g protein, 76 mg cholesterol, vitamin và chất béo. """

    doc2 = """
"Thịt gà mềm, dễ tiêu hóa hơn thịt vịt", bác sĩ Linh nhấn mạnh. Thịt gà là món ăn rất có ích cho những người bệnh, cần bổ sung năng lượng cho cơ thể để thúc đẩy quá trình trao đổi chất. Ức gà cũng phù hợp với những người đang ăn kiêng, nhiều phốt pho có lợi cho răng và xương.

Thịt vịt có tính hàn nên được dùng để giải nhiệt, giải độc. Trong thịt vịt nhiều protein, sắt, canxi, vitamin A, B1, D... có lợi cho những người gầy muốn tăng cân. Tuy nhiên, thịt vịt dai và khó tiêu nên người già và trẻ em hạn chế ăn.

Cấm kỵ:

- Những người dương hư tỳ nhược, ngoại cảm chưa khỏi hẳn không nên ăn thịt vịt.

- Da gà và lòng trắng trứng gà nhiều mỡ cùng cholesterol, do đó không phù hợp với người huyết áp cao, tim mạch.

- Không ăn thịt bảo quản kém và không rõ nguồn gốc rõ ràng."""
    
    doc3 = """ddaay la documetn so 3.Thịt gà"""

#    d1 = open('doc1.txt','r',encoding='utf-8-sig')
#    d2 = open('doc2.txt','r',encoding='utf-8-sig')
#    d3 = open('doc3.txt','r',encoding='utf-8-sig')
##    document1 = d1.read()
#    document2 = d2.read()
#    document3 = d3.read()
#    
#    for line in d1:
#        line = line.replace('\n','')
#        line = line.split()
#        print (line)
    
    inverted = {}
    documents = {'doc1':doc1, 'doc2':doc2, 'doc3':doc3}
    
    for doc_id, text in documents.items():
        doc_index = inverted_index(text)
        print ('Đầu tiên liệt kê các từ - vị trí trong mỗi document ----------------\n')
#        print (doc_index)
        print ()
        inverted_index_add(inverted, doc_id, doc_index)
        print ('Sau đó liệt kê các từ - document - vị trí --------------------------\n')
#        print (inverted)
        print ()

    # Print Inverted-Index
    for word, doc_locations in inverted.items():
        print (word, doc_locations)
    qQuery = []
    positionFirst = []
    
    queries = ('thịt gà','thịt vịt') #,'thịt vịt có tính hàn','theo Bảng thành phần dinh dưỡng Việt Nam','Thịt gà dồi dài protein.')
    for query in queries:
        print ('\nquery muon tim: '+query)
        # tach word trong query
        print ('Tach word trong query')
        temp1 = word_split(query)
        temp1 = words_normalize(temp1)
        for _,word in temp1:
            print (word)
            for doc_id,location in inverted[word].items():
                print (doc_id)
                print (location)
#        result_docs = search(inverted, query)
#        print ()
#        print ("Từ '%s' xuất hiện trong: %r" % (query, result_docs))
        
#        for _, word in word_index(query):
#            qQuery.append(word)
#        
##        for i in qQuery:
#        for i in range(0,len(qQuery)):
#            for doc in result_docs:
#                positionFirst.append(doc)
#                for index1 in inverted[qQuery[i]][doc]:
##                    print (index1)
#                    tmp = index1+len(qQuery[i])+1
##                    print (tmp)
#                    if i < len(qQuery)-1:
#                        for index2 in inverted[qQuery[i+1]][doc]:
#                            if tmp == index2:
#                                positionFirst.append(index1)
#                    elif i is (len(qQuery)-1):
#                        index2 = inverted[qQuery[i]][doc]
#                        if tmp == index2:
#                                positionFirst.append(index1)
#        print (positionFirst)
#        positionFirst = []
#        qQuery = []
        
