from datetime import datetime


link_folder = '\\Users\\NghiLam\\Documents\\GATSOP\\CYK\\'


#============================================================================= read file textIOwrapper.
def read_file_TextIOWrappertype(url, filename):                                 # Dùng for để duyệt qua từng phần tử.
    return open(url + filename, 'r', encoding='utf8')
#============================================================================= Hàm xử lý để lấy grammar.
def getGrammar():
    grammarFile = read_file_TextIOWrappertype(link_folder,'grammar.txt')
#    Đếm có bao nhiêu quy tắc.
    gram = dict()
    size = 0
    for item in grammarFile:
        size += 1
        item = item.replace('\n','')
        item = item.replace(' -> ', '-')
    
        t = 0
        for count in item:
            if count != '-':
                t += 1
            else:break
    
        left = item[:t]
        right = item[t+1:]
        
        if left not in gram:
            gram[left] = [right]
        elif right not in gram[left]:
            gram[left].append(right)
#    In kiểm tra có bao nhiêu quy tắc
#    print (size)
    return gram

def CYK(words, grammar):
    numOfWord = len(words)
    
    w, h = numOfWord, numOfWord;
    table = [[' ' for x in range(w)] for y in range(h)] 
    
    for j in range(0,numOfWord):
        for key,value in grammar.items():
            for v in value:
                if words[j] == v:
                    table[j][j] += key
                    table[j][j] = table[j][j].lstrip()
        for i in range(j-1,-1,-1):
            for k in range(i+1, j+1):
                temp = ''
                temp += table[i][k-1] + ' ' + table[k][j]
                for key, value in grammar.items():
                    for v in value:
                        if temp == v:
#                            table[i][j] += key
                            table[i][j] = key
                            table[i][j] = table[i][j].lstrip()
    

    return table

def main():
    start=datetime.now()
#             0    1     2     3      4     5         6
    words = ('I','saw','the','man','with','the','telescope')
#    print (type(words[3]))
    grammar = getGrammar()
#    count = 0
#    for k,v in grammar.items():
#        print (k)
#        print (v)
#        count += len(v)
#    print (count)
    for i in CYK(words, grammar):
        print (i)
    

    print (datetime.now()-start)
    
if __name__ == "__main__":main()