from datetime import datetime

class Node:
    def __init__(self, left, right, name, word):
        self.left = left
        self.right = right
        self.name = name
        self.word = word
        
    def add(self,node,side):
        if side == 'left':
            self.left = node
        if side == 'right':
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
    return "["+displayTree(node.left)+" "+displayTree(node.right)+"]_"+node.name
    
node = list()
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
            
        for i in range(0,len(words)):
            if words[i] == right and right not in terminal:
                terminal.append(right)
#    In kiểm tra có bao nhiêu quy tắc
#    print (size)
    return gram
#============================================================================= Hàm CYK.
#    Thiếu 1: Chưa phân biệt chữ hoa chữ thường.
#    Thiếu 2: Chưa xử lý giá trị của table, chỉ lưu đc 1 giá trị.
def CYK(words, grammar):
    numOfWord = len(words)
    
    w, h = numOfWord, numOfWord;
    table = [['|' for x in range(w)] for y in range(h)] 
    
    for j in range(0,numOfWord):
        for key,value in grammar.items():
            for v in value:
                if words[j] == v: # Kiểm tra nếu words[j] rỗng thì ra kết quả luôn.
#                    table[j][j] += key
                    table[j][j] = key
                    table[j][j] = table[j][j].lstrip()
#                    leaf.append(Node(None,None,key,words[j]))
                    node.append(Node(None,None,key,words[j]))
        
        for i in range(j-1,-1,-1):
            for k in range(i+1, j+1):
                temp = ''
                temp += table[i][k-1] + ' ' + table[k][j]
                for key, value in grammar.items():
                    for v in value:
                        if temp == v: # Kiểm tra nếu temp là rỗng hoặc thiếu thì ra kết quả.
#                            table[i][j] += key
                            table[i][j] = key
                            table[i][j] = table[i][j].lstrip()
#                            nl = Node()
                            node.append(Node(table[i][k-1],table[k][j],key,None))
        for m in range(0,numOfWord):
            print (table[m],end='\n')
        print ('\n')
        
        
    return table

#============================================================================= Hàm In Cây.
#def displayParseTree():
    
terminal = []

def main():
    start=datetime.now()
#             0    1     2     3      4     5         6
    words = ('I','saw','the','man','with','the','telescope')
#    words = ('Tôi','đã_nhìn','một','người_đàn_ông','với','một','ống_nhòm')
#    words = ('She','eats','a','fish','with','a','fork')
#    words = ('Tôi','ăn','một','con_cá','với','một','cái_nĩa')
#    
    grammar = getGrammar_1('grammar1.txt',words)
#    grammar = getGrammar('grammar1 - Copy.txt')
#    grammar = getGrammar('grammar2.txt')
#Đếm có bao nhiêu luật.
#    count = 0
#    for k,v in grammar.items():
#        print (k)
#        print (v)
#        count += len(v)
#    print (count)
#In bảng table được trả về bởi hàm CYK    
#    for i in CYK(words, grammar):
#        print (i)
    w, h = len(words), len(words)
    table = [['|' for x in range(w)] for y in range(h)] 
    table = CYK(words, grammar)
    
#    for i in leaf:
#        print (i.displayNode())
    
#    for i in range(len(words)-1, -1, -1):
#        for j in range(0, len(words)):
#            if table[i][j] != '|':
                
    
    
    for i in node:
        print (i.displayNode())
    print ('\n')
    
#    for j in node:
#        if j.name == 'S':
#            print (displayTree(j))
#            pass
    

    print (datetime.now()-start)
    
if __name__ == "__main__":main()
