from datetime import datetime
from Node import Node

link_folder = '\\Users\\NghiLam\\Documents\\NLP\\CYK\\'

#============================================================================= read file textIOwrapper.
def read_file_TextIOWrappertype(url, filename):                                #Dùng for để duyệt qua từng phần tử.
    return open(url + filename, 'r', encoding='utf-8-sig')
#============================================================================= Hàm xử lý để lấy grammar.
def getGrammar(filename):
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
        for key,value in grammar.items():
            for v in value:
#               Neu moi value la terminal thi khong can chay tiep 
                if words[j] == v:
                    table[j][j].append(key)
                    nodes_back[j][j].append(Node(key,-1,-1,-1,-1,-1,-1,words[j],j-j))
                    
                                        
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
                                    nodes_back[i][j].append(Node(key,i,k-1,l,k,j,r,None,j-i))
                       
    return table,nodes_back

#============================================================================= Hàm In Cây.
table = []
back = []
l_node = []
def printTreeByLine(node):
#   Tai 1 node, neu gia tri left row: lrow bang -1, tuc la node do la terminal.
    if node.lrow is -1:
        l_node.append(node.name + '.' + node.terminal)
#        l_node.append(node.terminal)
        return node.name + '.' + node.terminal
    else:
        l_node.append(node.name)
        return node.name + '[' + printTreeByLine(back[node.lrow][node.lcol][node.lorder]) + \
    ' ' + printTreeByLine(back[node.rrow][node.rcol][node.rorder]) + ']'
        
def printTreeByLine2(node):
    if node.lrow is -1:
        return node.name + '(' + node.terminal + ')'
    else:
        return node.name + '(' + printTreeByLine2(back[node.lrow][node.lcol][node.lorder]) + \
        printTreeByLine2(back[node.rrow][node.rcol][node.rorder]) + ')' 
        
def printTree1(node):
    if node.lrow is -1:
        return '\t'*node.level + node.name + '.' + node.terminal
    return ' '*node.level + node.name + '\n' + printTree1(back[node.lrow][node.lcol][node.lorder]) + \
    ' ' + printTree1(back[node.rrow][node.rcol][node.rorder])

#============================================================================= Hàm.    

#============================================================================= Main.
def main():
    start=datetime.now()
    
    sentence = read_file_TextIOWrappertype(link_folder,'sentence1.txt.')
#    sentence = read_file_TextIOWrappertype(link_folder,'sentence2.txt.')
#    sentence = read_file_TextIOWrappertype(link_folder,'sentence3.txt.')
    
    for i in sentence:
        print (i)
        words = i.split()
        
    
    numOfWord = len(words)
    grammar = getGrammar('grammar1.txt')
    
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


    for i in back[0][numOfWord-1]:
        print (printTreeByLine(i))
#        print (printTreeByLine2(i))
        print (printTree1(i))
        print ()

#    print (l_node)
        
    
    print (datetime.now()-start)
    
if __name__ == "__main__":main()
