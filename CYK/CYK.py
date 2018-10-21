from datetime import datetime


#T = [[11, 12, 5, 2], [15, 6,10], [10, 8, 12, 5], [12,15,8,6]]
#for r in T:
#    for c in r:
#        print(c,end = "end.")
#    print()

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
    table = []
    numOfWord = len(words)
    for j in range(0,numOfWord):
        print (words[j])
        for key,value in grammar.items():
            for v in value:
                if words[j] == v:
                    #table[j-1][j] = key
                    for ta in range(0,numOfWord):
                        new = []
                        for tanew in range(0,numOfWord):
                            new.append(key)
                        table.append(new)

        if j<2: pass
        for i in range(j-2,-1,-1):
            for k in range(i+1,j-1):
                temp = ''
                temp += table[i][k]
                temp += ' '
                temp += table[k][j]
                for key,value in grammar.items():
                    for v in value:
                        if temp == v:
#                           table[i][j] = k
                            for ta in range(0,numOfWord):
                                new = []
                                for tanew in range(0,numOfWord):
                                    new.append(key)
                                table.append(new)
                        
    print (type(table))
    return table

def main():
    start=datetime.now()

    words = ('I','saw','the','man','with','the','telescope')
#    print (type(words[3]))
    grammar = getGrammar()
#    count = 0
#    for k,v in grammar.items():
#        print (k)
#        print (v)
#        count += len(v)
#    print (count)
    CYK(words, grammar)
    

    print (datetime.now()-start)
    
if __name__ == "__main__":main()