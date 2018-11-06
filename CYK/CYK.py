from datetime import datetime
from Node import Node

link_folder = '\\Users\\NghiLam\\Documents\\NLP\\CYK\\'

#============================================================================= read file textIOwrapper.
def read_file_TextIOWrappertype(url, filename):                                #Dùng for để duyệt qua từng phần tử.
    return open(url + filename, 'r', encoding='utf-8-sig')
#============================================================================= Hàm xử lý để lấy grammar.
def getGrammar_1(filename):
    grammarFile = read_file_TextIOWrappertype(link_folder,filename)
#    Đếm có bao nhiêu quy tắc.
#    size = 0
    gram = dict()
    for item in grammarFile:
#        size += 1
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

#============================================================================= Hàm CYK.
#    Thiếu 1: Chưa phân biệt chữ hoa chữ thường.
def CYK(words, grammar):
    numOfWord = len(words)
    table = [[[] for i in range(numOfWord)] for j in range(numOfWord)]
    nodes_back = [[[] for i in range(numOfWord)] for j in range(numOfWord)]
    
    for j in range(0,numOfWord):
#        Kiểm tra 
        for key,value in grammar.items():
            for v in value:
                if words[j] == v:
                    table[j][j].append(key)
                    nodes_back[j][j].append(Node(key,-1,-1,-1,-1,-1,-1,words[j]))
                    
                                        
        for i in range(j-1,-1,-1):
            for k in range(i+1, j+1):
#                for l in table[i][k-1]:#left:
                for l in range(0,len(table[i][k-1])):
#                    for r in table[k][j]:#right:
                    for r in range(0,len(table[k][j])):
                        temp = ''
#                        temp += l + ' ' + r
                        temp += table[i][k-1][l] + ' ' + table[k][j][r]
                        for key,value in grammar.items():
                            for v in value:
                                if temp == v: #Bổ sung Kiểm tra nếu temp là rỗng hoặc thiếu thì ra kết quả.
                                    table[i][j].append(key)
#                                    nodes_back[i][j].append(Node(key, l, r, None))
                                    nodes_back[i][j].append(Node(key,i,k-1,l,k,j,r,None))
                       
    return table,nodes_back#[0][numOfWord-1]

#============================================================================= Hàm In Cây 1 dòng.
table = []
back = []

def printTreeByLine(node):
#   Tai 1 node, neu gia tri left row: lrow bang -1, tuc la node do la terminal.
    if node.lrow is -1:
        return node.terminal + '.' + node.name
    return '[' + printTreeByLine(back[node.lrow][node.lcol][node.lorder]) + ' ' \
    + printTreeByLine(back[node.rrow][node.rcol][node.rorder]) + ']-' + node.name
#============================================================================= Hàm In Cây.
#def printTree(s):
    
#============================================================================= Hàm.    

#============================================================================= Main.
def main():
    start=datetime.now()
    
#             0    1     2     3      4     5         6      7     8     9
    words = ('I','saw','the','man','with','the','telescope','in','the','man')
#    words = ('Tôi','đã_nhìn','một','người_đàn_ông','với','một','ống_nhòm')
#    words = ('She','eats','a','fish','with','a','fork')
#    words = ('Tôi','ăn','một','con_cá','với','một','cái_nĩa')
    numOfWord = len(words)
    grammar = getGrammar_1('grammar1.txt')
#    grammar = getGrammar_1('grammar1 - Copy.txt')
#    grammar = getGrammar_1('grammar2.txt')
    
#In ra các luật và Đếm có bao nhiêu luật.
#    count = 0
#    for k,v in grammar.items():
#        print (k)
#        print (v)
#        count += len(v)
#    print (count)
    global table
    global back
    table,back = CYK(words, grammar)
#In bảng table được trả về bởi hàm CYK   
    for i in table:
        print (i)
    print ()
#                                                                              đóng băng đoạn này         
#    for i in back[0][numOfWord-1]:
#        print (i.name)
#        left = table[i.lrow][i.lcol][i.lorder]
#        right = table[i.rrow][i.rcol][i.rorder]
#        s = left + ' ' + right
#        print (s)
#        while (i1.lrow is not -1):
#                                                                    print left
#        j = back[i.lrow][i.lcol][i.lorder]
#            i1 = back[i.lrow][i.lcol][i.lorder]
#            if i1.lrow is not -1:
#                leftL = table[i1.lrow][i1.lcol][i1.lorder]
#                leftR = table[i1.rrow][i1.rcol][i1.rorder]
#                sL = leftL + ' ' + leftR
#            else:
#                sL = i1.terminal
##                                                                   print right
#            i2 = back[i.rrow][i.rcol][i.rorder]
#            if i.lrow is not -1:
#                leftR = table[i2.lrow][i2.lcol][i2.lorder]
#                rightR = table[i2.rrow][i2.rcol][i2.rorder]
#                sR = leftR + ' ' + rightR
#            else:
#                sR = i2.terminal            
#            print (sL + ' ' + sR)
#                                                                              đóng băng đoạn này
    for i in back[0][numOfWord-1]:
        print (printTreeByLine(i))
        print ()
#        printTree(printTreeByLine(i))
    printTree(printTreeByLine(back[0][numOfWord-1][0]))
    
    print (datetime.now()-start)
    
if __name__ == "__main__":main()
