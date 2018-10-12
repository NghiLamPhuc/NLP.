import re
from datetime import datetime

start=datetime.now()

link_folder = '\\Users\\NghiLam\\Documents\\GATSOP\\Tokenize\\'
link_input_file = link_folder + 'input\\'
link_output_file = link_folder + 'output\\'
link_out_file = link_folder + 'outfile\\'

#-----------------------------------------------------------------------------# Cac ham co ban.START
def write_listline_file(List, filename, url):
    f = open(link_folder + url + filename,'w',encoding='utf8')
    for t in List:
        f.write("%s\n" % t)
    f.close()
    
def write_file(file, filename, url):
    f = open(link_folder + url + filename,'w',encoding='utf8')
    f.write(file)
    f.close()

def read_file(filename):
    f = open(link_input_file + filename,'r',encoding='utf8')
    input_file = f.read()
    f.close()
    return input_file
#-----------------------------------------------------------------------------# Cac ham co ban.END
    
#-----------------------------------------------------------------------------# Cac ham xu ly input.BEGIN
def remove_some(s):
    new_s = re.sub('<<\w','',s)
    new_s = re.sub('\/\w>>','',new_s)
    new_s = re.sub('\n+','\n',new_s)
    return new_s
# The^m space va`o giua chu cai va ky tu dac biet
def add_space_word_matecharacter(s):
    return re.sub('(?<=\w)(?=[,\/\_\-\(\)\{\}\[\]?!%\":;]\s)', ' ', s)
    
      
def add_space_metacharacter_word(s):
    return re.sub('(?<=\s[,\/\_\-\(\)\{\}\[\]?!%\":;])(?=\w)', ' ', s)
    
    
def add_space_1(s):
    return re.sub('(?<=[,\/\_\-\(\)\{\}\[\]?!%\":;])(?=[,\/\_\-\(\)\{\}\[\]?!%\":;]\s)', ' ', s)

############################ Tach cau ######################################### BEGIN
def split_sentences(s):
    regex = re.compile('(?<=[\.\?!])[\s\n]|\n')
    sentences = re.split(regex,s)
    del sentences[0]
    del sentences[-1]
   
    return sentences
# Tách câu.#################################################################### END

#################################### Tach tu to ################################ BEGIN
def tokenize(the_list):
    lst = list()
    
    regex = re.compile('[^\s]+')
#    prev = ''
#    curr = ''
    for i in the_list:
        
        i = add_space_word_matecharacter(i)
        i = add_space_metacharacter_word(i)
        i = add_space_1(i)
        
        token = regex.findall(i)
        lst.append(token)
        
    return lst
# Tách từ tố.################################################################## END

#################################### Tach tu ################################# BEGIN
def word_seagment(the_list):
    
        
    return 0
# Tách từ .#################################################################### END

input_file = read_file('12000-13000.txt')
input_file = remove_some(input_file)
write_file(input_file,'removed.txt','outfile\\')
# ############# In kết quả tách câu ###########################################
list_sentences = split_sentences(input_file)
write_listline_file(list_sentences,'sentences.txt','output\\')
# ############# In kết quả tách tu to #########################################
tokens = tokenize(list_sentences)
write_listline_file(tokens,'tokens.txt','output\\')


print (datetime.now()-start)
