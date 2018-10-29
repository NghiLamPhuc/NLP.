from datetime import datetime
from collections import defaultdict

class Node:
    def __init__(self, left, right, name, word):
        self.left = left
        self.right = right
        self.name = name
        self.word = word
            
    def addLeft(self,node):
        self.left = node
    def addRight(self,node):
        self.right = node
            
    def displayNode(self):
        if self.left is None and self.right is None:
            x = self.name + '{' + self.word + '}'
        else:
            x = self.name + '(' + self.left + ' ' + self.right + ')'
        return x

def displayTree(node):
    if node.left == None and node.right == None:
        return node.word + '_' + node.name
    else:
        return '['+displayTree(node.left)+' '+displayTree(node.right)+']_'+node.name
    
preTree = list()
tree = list()
leaf = list()

link_folder = '\\Users\\NghiLam\\Documents\\GATSOP\\CYK\\'

#============================================================================= read file textIOwrapper.
def read_file_TextIOWrappertype(url, filename):                                #Dùng for để duyệt qua từng phần tử.
    return open(url + filename, 'r', encoding='utf-8-sig')
#============================================================================= Hàm xử lý để lấy grammar.
#def getGrammar(filename):
#    getGrammar_1(filename)
#============================================================================= Hàm xử lý để lấy grammar.
def getGrammar_1(filename, words):
    grammarFile = read_file_TextIOWrappertype(link_folder,filename)
#    Đếm có bao nhiêu quy tắc.
    size = 0
    gram = dict()
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
        
        list_right = right.split()
        if len(list_right) > 1:
            preTree.append(Node(list_right[0],list_right[1],left,None))
        else:
            leaf.append(Node(None,None,left,right))
            
        for i in range(0,len(words)):
            if words[i] == right and right not in terminal:
                terminal.append(right)
            
#    In kiểm tra có bao nhiêu quy tắc
#    print (size)
    return gram

#============================================================================= Hàm CYK.
#    Thiếu 1: Chưa phân biệt chữ hoa chữ thường.
def CYK(words, grammar):
    numOfWord = len(words)
    
    table = [[' ' for x in range(numOfWord)] for y in range(numOfWord)]
    
    for j in range(0,numOfWord):
#        Kiểm tra 
#        for key,value in grammar.items():
#            for v in value:
#                if words[j] == v:
#                    table[j][j] = key
        for l in leaf:
            if words[j] == l.word:
                table[j][j] = l.name
                preTree.append(l)
                                        
        for i in range(j-1,-1,-1):
            for k in range(i+1, j+1):
                if table[i][k-1] != ' ' and table[k][j] != ' ':
                    left = table[i][k-1].split()
                    right = table[k][j].split()
                    for l in left:
                        for r in right:
                            temp = ''
#                            temp += table[i][k-1] + ' ' + table[k][j]
                            temp += l + ' ' + r
                            for key,value in grammar.items():
                                for v in value:
                                    if temp == v: #Bổ sung Kiểm tra nếu temp là rỗng hoặc thiếu thì ra kết quả.
                                        if key not in table[i][j]:
                                            table[i][j] += ' ' + key
                                            table[i][j] = table[i][j].lstrip()

                                    


#        for m in range(0,numOfWord):
#            print (table[m],end='\n')
#        print ('\n')
        
    return tree, table

#============================================================================= Hàm In Cây.
#def displayParseTree():
    
terminal = []

def main():
    start=datetime.now()
    
#             0    1     2     3      4     5         6      7     8     9
    words = ('I','saw','the','man','with','the','telescope','in','the','man')
#    words = ('Tôi','đã_nhìn','một','người_đàn_ông','với','một','ống_nhòm')
#    words = ('She','eats','a','fish','with','a','fork')
#    words = ('Tôi','ăn','một','con_cá','với','một','cái_nĩa')
#    
    grammar = getGrammar_1('grammar1.txt',words)
#    grammar = getGrammar_1('grammar1 - Copy.txt',words)
#    grammar = getGrammar_1('grammar2.txt',words)
    
#    table = [[' ' for x in range(len(words))] for y in range(len(words))]

#In ra các luật và Đếm có bao nhiêu luật.
#    count = 0
#    for k,v in grammar.items():
#        print (k)
#        print (v)
#        count += len(v)
#    print (count)
    
    tree, table = CYK(words, grammar)
#In bảng table được trả về bởi hàm CYK   
#    for i in table:
#        print (i)

    for i in table:
        print (i)
    

#        if i.name == 'S':
#            displayTree(i)
#            break
    
    
    print (datetime.now()-start)
    
if __name__ == "__main__":main()
