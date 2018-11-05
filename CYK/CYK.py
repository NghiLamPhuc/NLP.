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
    
#    table = [[' ' for x in range(numOfWord)] for y in range(numOfWord)]
    
    for j in range(0,numOfWord):
#        Kiểm tra 
        for key,value in grammar.items():
            for v in value:
                if words[j] == v:
                    table[j][j].append(key)
#                    nodes_back[j][j].append(Node(key,None,None,words[j]))
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
                                        
#                                    for b in nodes_back[i][k-1]:
#                                        for c in nodes_back[k][j]:
#                                            if b.root == l and c.root == r:
#                                                nodes_back[i][j].append(Node(key, b, c, None))

#    return tree, table
    return table,nodes_back#[0][numOfWord-1]

#============================================================================= Hàm In Cây.
def printParseTrees(nodes_back):
    check = False
    for node in nodes_back:
        if node.root == 'S':
            print(getParseTree(node))
            print()
            check = True
        break
    if check == False:
        print('The given sentence is not valid according to the grammar.')
#============================================================================= Hàm.    
def getParseTree(root):
	if root.status:
		return '(' + root.root + ' ' + root.terminal + ')'

	# Calculates the new indent factors that we need to pass forward.
#	new1 = indent + 2 + len(root.left.root) #len(tree[1][0])
#	new2 = indent + 2 + len(root.right.root) #len(tree[2][0])
	left = getParseTree(root.left)
	right = getParseTree(root.right)
	return '(' + root.root + ' ' + left + '\n' + right + ')'
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
    
    table,back = CYK(words, grammar)
#In bảng table được trả về bởi hàm CYK   
    for i in table:
        print (i)
    
#    for i in range(numOfWord-1,-1,-1):
#        for j in range(numOfWord-1,-1,-1):
#            print (back[0][i])
    for i in back[0][numOfWord-1]:
        print (i.name)
        left = table[i.lrow][i.lcol][i.lorder]
        right = table[i.rrow][i.rcol][i.rorder]
        s = left + ' ' + right
        print (s)
#        print left
#        for j in back[i.lrow][i.lcol]:
#            if j.lrow is -1:
#                print (j.terminal)
        j = back[i.lrow][i.lcol][i.lorder]
        if j.lrow is not -1:
            leftL = table[j.lrow][j.lcol][j.lorder]
            leftR = table[j.rrow][j.rcol][j.rorder]
            sL = leftL + ' ' + leftR
        else:
            sL = j.terminal
#        print right
        k = back[i.rrow][i.rcol][i.rorder]
        leftR = table[k.lrow][k.lcol][k.lorder]
        rightR = table[k.rrow][k.rcol][k.rorder]
        sR = leftR + ' ' + rightR
        
        print (sL + ' ' + sR)
        
        
    
    
#    print (back[1][6][0].name)
            

    print (datetime.now()-start)
    
if __name__ == "__main__":main()
