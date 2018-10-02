import re
import pprint

def display_out_file(List,filename,link_out_file):
    file = link_out_file + filename
    with open(file, 'w', encoding='utf-8') as fout:
        pprint.pprint(List,fout)

link_folder = '\\Users\\NghiLam\\Documents\\GATSOP\\Tokenize\\'
link_input_file = link_folder + 'input\\'
link_output_file = link_folder + 'output\\'

f = open(link_input_file+'12000-13000.txt','r',encoding='utf8')
input_file = f.read()
f.close()

def remove_some(s):
    new_s = re.sub('<<\w','',s)
    new_s = re.sub('\/\w>>','',new_s)
    new_s = re.sub('\n+','\n',new_s)
    return new_s

# The^m space va`o giua chu cai va ky tu dac biet
def add_space_after_word_matecharacter(s):
    return re.sub('(?<=\w)(?=[.,\-\)\}\]?!%\":;])', ' ', s)
    
def add_space_before_word_metacharacter(s):
    return re.sub('(?<=[.,\(\{\[?!%\":;])(?=\w)', ' ', s)

# BEGIN.########################### Tach cau #############################
def split_sentences(st):
    lst = list()
# Sau cùng là dấu '!', '?', '.'. Trước nó là bất cứ ký tự gì khác '!', '?', '.'.
    regex = re.compile('[^!?\.]+[!?\.]')
    sentences = regex.findall(st)
     
    for s in sentences:
        lst.append(s.strip())
    
    return lst
# Tách câu.################################################################ END
 
#kiểm tra có phải kết thúc 1 câu hay ko
def isBoudary(i,text):
	#kiểm tra hết text
	if i == len(text)-1: return 1

	#nếu i+1 là ký tự trắng thì trả về 1
	if re.match(r'\s',text[i+1]): return 1

	#nếu i-1 là số và i+1 là số thì trả về 0
	if re.match(r'[0-9]',text[i-1]) and re.match(r'[0-9]',text[i+1]): return 0

	#nếu i-1 là số và i+1 không phải là số thì trả về 1
	if re.match(r'[0-9]',text[i-1]) and re.match(r'[^0-9]',text[i+1]): return 1

	#nếu i-1 là ký tự thường và i+1 là ký tự hoa thì trả về 1
	if (re.match(r'[a-z\)\"\”]',text[i-1]) or isUniLower(text[i-1])) and (re.match(r'[A-Z\(\"\“)]',text[i+1]) or isUniUpper(text[i+1])): return 1

	#nếu i-1 là ký tự hoa và i+1 là ký tự hoa thì trả về 0
	if (re.match(r'[A-Z]',text[i-1]) or isUniUpper(text[i-1])) and (re.match(r'[A-Z]',text[i+1]) or isUniUpper(text[i+1])): return 0
	
	return 0    

def SplitSentence(text):
	sents = []
	#ký tự i bắt đầu =0
	i = 0
	#ký tự bắt đầu câu =0
	begin = 0

	#lặp từng ký tự trong text
	while i < len(text):
		#nếu gặp ký tự kết thúc
		if (text[i]=='.' or text[i]=='!' or text[i]=='...' or text[i]=='?'):
			#kiểm tra đó có phải vị trí kết thúc câu hay ko
			if isBoudary(i,text):
				#nếu là kết thúc câu thì cắt câu đó ra và tiếp tục
				sents.append(text[begin:i].strip())
				begin=i+1
		i+=1
	return sents    

# BEGIN.########################### Tach tu to #############################


def tokenize(the_list):
    lst = list()
    
    regex = re.compile('[^\s]+')
    
    for i in the_list:
#        i1 = add_space_after_word_matecharacter(i)
        i2 = add_space_before_word_metacharacter(i)
        token = regex.findall(i2)
        lst.append(token)
        
    return lst
# Tách từ tố.########################################################### END
    
input_file_2 = remove_some(input_file)
f = open(link_output_file+'removeog.txt','w',encoding='utf8')
f.write(input_file_2)
#display_out_file(input_file_2,'remove.txt',link_output_file)
# ############# In kết quả tách câu ###########################################
#lst_sntncs = split_sentences(input_file_2)
lst_sntncs = SplitSentence(input_file_2)
display_out_file(lst_sntncs,'sentences.txt',link_output_file)
#print(lst_sntncs)
#print(lst_tkns)
# ############# In kết quả tách tu to #######################################
#tokens = tokenize(lst_sntncs)
#display_out_file(tokens,'tokens.txt',link_output_file)
#print(tokens)
