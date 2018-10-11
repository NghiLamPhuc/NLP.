import re
from datetime import datetime
start=datetime.now()

def display_out_file(List,filename,link_out_file):
    file = link_out_file + filename
    with open(file, 'w', encoding='utf-8') as fout:
        for i in range(len(List)):
            fout.write(List[i]+'\n')

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
    return re.sub('(?<=\w)(?=[.,\/\_\-\(\)\{\}\[\]?!%\":;])', ' ', s)
    
        
def add_space_before_word_metacharacter(s):
    return re.sub('(?<=[.,\/\_\-\(\)\{\}\[\]?!%\":;])(?=\w)', ' ', s)
    
      
def add_space_1(s):
    return re.sub('(?<=[.,\/\_\-\(\)\{\}\[\]?!%\":;])(?=[.,\/\_\-\(\)\{\}\[\]?!%\":;])', ' ', s)


# BEGIN.########################### Tach cau #############################
def split_sentences(st):
    lst = list()
# Sau cùng là dấu '!', '?', '.'. Trước nó là bất cứ ký tự gì khác '!', '?', '.'.
#    regex = re.compile('[^!?\.]+[!?\n\.]')
#    sentences = regex.findall(st)
    regex = re.compile('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z]\.)(?<=[\.\?!])[\s\n]')
    sentences = re.split(regex,st)
    lst = sentences
#    for s in sentences:
#        lst.append(s.strip())
    
    return lst
# Tách câu.################################################################ END

# BEGIN.########################### Tach tu to #############################
def tokenize(the_list):
    lst = list()
    
    regex = re.compile('[^\s]+')
    
    for i in the_list:
        i = add_space_before_word_metacharacter(i)
        i = add_space_after_word_matecharacter(i)
        i = add_space_1(i)
        token = regex.findall(i)
        lst.append(token)
        
    return lst
# Tách từ tố.########################################################### END
    
input_file = remove_some(input_file)
f = open(link_output_file+'removeog.txt','w',encoding='utf8')
f.write(input_file)
# ############# In kết quả tách câu ###########################################
list_sentences = split_sentences(input_file)
display_out_file(list_sentences,'sentences.txt',link_output_file)
print (list_sentences[0])
#print (input_file[3])
# ############# In kết quả tách tu to #######################################
tokens = tokenize(list_sentences)
#print (tokens)
f = open(link_output_file+'token.txt','w',encoding='utf8')
for t in tokens:
     f.write("%s\n" % t)

#display_out_file(tokens,'tokens.txt',link_output_file)

print (datetime.now()-start)
##################################################