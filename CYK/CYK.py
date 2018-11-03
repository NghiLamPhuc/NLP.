from datetime import datetime

class Node:
	def __init__(self, root, left, right, end):
		self._root = root
		self._left = left
		self._right = right
		self._terminal = end
		self._status = True
		if end == None:
			self._status = False

	def root(self):
		return self._root

	def left(self):
		return self._left

	def right(self):
		return self._right

	def status(self):
		return self._status

	def terminal(self):
		return self._terminal
    
def printBack(node):
    s = ''
    if node.terminal != None:
        s += node._root + '_' + node._terminal
    else:
        s += '(' + printBack(node.left) + ' ' + printBack(node.right) + ')_' + node.root
    return s

link_folder = '\\Users\\NghiLam\\Documents\\GATSOP\\CYK\\'
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
                    nodes_back[j][j].append(Node(key, None, None, words[j]))
                                        
        for i in range(j-1,-1,-1):
            for k in range(i+1, j+1):
                for l in table[i][k-1]:#left:
                    for r in table[k][j]:#right:
                        temp = ''
                        temp += l + ' ' + r
                        for key,value in grammar.items():
                            for v in value:
                                if temp == v: #Bổ sung Kiểm tra nếu temp là rỗng hoặc thiếu thì ra kết quả.
                                    table[i][j].append(key)
#                                    table[i][j] = [key]
                                    nodes_back[i][j].append(Node(key, l, r, None))
                                        
#                                    for b in nodes_back[i][k-1]:
#                                        for c in nodes_back[k][j]:
#                                            if b.root == l and c.root == r:
#                                                nodes_back[i][j].append(Node(key, b, c, None))

#    return tree, table
    return table,nodes_back[0][numOfWord-1]

#============================================================================= Hàm In Cây.
def printParseTrees(nodes_back):
    check = False
    for node in nodes_back:
        if node.root == 'S':
            print(getParseTree(node, 3))
            print()
            check = True
        break
    if check == False:
        print('The given sentence is not valid according to the grammar.')
#============================================================================= Hàm.    
def getParseTree(root, indent):
	if root.status:
		return '(' + root.root + ' ' + root.terminal + ')'

	# Calculates the new indent factors that we need to pass forward.
	new1 = indent + 2 + len(root.left.root) #len(tree[1][0])
	new2 = indent + 2 + len(root.right.root) #len(tree[2][0])
	left = getParseTree(root.left, new1)
	right = getParseTree(root.right, new2)
	return '(' + root.root + ' ' + left + '\n' \
			+ ' '*indent + right + ')'
#============================================================================= Main.
def main():
    start=datetime.now()
    
#             0    1     2     3      4     5         6      7     8     9
    words = ('I','saw','the','man','with','the','telescope','in','the','man')
#    words = ('Tôi','đã_nhìn','một','người_đàn_ông','với','một','ống_nhòm')
#    words = ('She','eats','a','fish','with','a','fork')
#    words = ('Tôi','ăn','một','con_cá','với','một','cái_nĩa')
#    
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
    printParseTrees(back)
#    print (back[0]._root+' '+back[0]._left+' '+back[0]._right)
    
    

    print (datetime.now()-start)
    
if __name__ == "__main__":main()
