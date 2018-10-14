import re
from datetime import datetime

start=datetime.now()

link_folder = '\\Users\\NghiLam\\Documents\\GATSOP\\Tokenize\\'
link_input_file = link_folder + 'input\\'
link_output_file = link_folder + 'output\\'
link_out_file = link_folder + 'outfile\\'

#============================================================================== Một số hàm đọc ghi.
#============================================================================== Ghi file ra từng dòng.
def write_listline_file(List, filename, url):
    f = open(url + filename,'w',encoding='utf8')
    for t in List:
        f.write("%s\n" % t)
    f.close()
#============================================================================== Ghi 1 list.
def write_file(file, filename, url):
    f = open(url + filename,'w',encoding='utf8')
    f.write(file)
    f.close()
#============================================================================== Đọc file kiểu string.
def read_file_stringtype(url,filename):
    f = open(url + filename,'r',encoding='utf8')
    input_file = f.read()
    f.close()
    return input_file
#============================================================================== Đọc file kiểu Text Wrapper.
def read_file_TextIOWrappertype(url, filename):                                 # Dùng for để duyệt qua từng phần tử.
    return open(url + filename, 'r', encoding='utf8')
    
#============================================================================== Loại bỏ một số dấu trng văn bản input.
def remove_some(s):
    new_s = re.sub('<<\w\s','',s)
    new_s = re.sub('\/\w>>','',new_s)
    new_s = re.sub('>>\s', '', new_s)
    new_s = re.sub('\n+','\n',new_s)
    new_s = re.sub('C. Ronaldo', 'C.Ronaldo', new_s)
    new_s = re.sub('\s\.\.\.', '...', new_s)

#    new_s = re.sub("[a-z][A-Z]\'\'",'"',new_s)                                 # 2 nháy đơn thành nháy kép.
#    new_s = re.sub('\[\[','[',new_s)
#    new_s = re.sub('\]\]',']',new_s)
    return new_s
#============================================================================== Thêm khoảng trắng vào ký tự.
def add_space_word_matecharacter(s):
    return re.sub('(?<=\w)(?=[\/\_\-\(\)\{\}\[\]?!%\":;]\s)', ' ', s)
    
def add_space_metacharacter_word(s):
    return re.sub('(?<=\s[,\/\_\-\(\)\{\}\[\]?!%\":;])(?=\w)', ' ', s)
    
def add_space_1(s):
    return re.sub('(?<=[,\/\_\-\(\)\{\}\[\]?!%\":;])(?=[,\/\_\-\(\)\{\}\[\]?!%\":;]\s)', ' ', s)

#https://vi.wikipedia.org/wiki/D%E1%BA%A5u_c%C3%A2u
def add_space(s):
    regex1 = re.compile('(?<=[\'\"])(?=\w) | (?<=\w)(?=[\'\"])')                #Nháy đơn, nháy kép.
    regex2 = re.compile('(?<=[\(\[\{])(?=\w) | (?<=\w)(?=[\)\]\}])')            #Ngoặc [ ( {
    regex3 = re.compile('(?<=[])(?=) | (?<=)(?=[])')                            #Hai chấm :
#    regex4 = re.compile('(?<=[])(?=) | (?<=)(?=[])')                            #Dấu phẩy , ` '
#    regex5 = re.compile('(?<=[])(?=) | (?<=)(?=[])')                            #Dấu - _
#    regex6 = re.compile('(?<=[])(?=) | (?<=)(?=[])')                            #Dấu chấm lửng ...
#    regex7 = re.compile('(?<=[])(?=) | (?<=)(?=[])')                            #Dấu chấm than !
#    regex8 = re.compile('(?<=[])(?=) | (?<=)(?=[])')                            #Dấu chấm .
#    regex9 = re.compile('(?<=[])(?=) | (?<=)(?=[])')                            #Dấu chấm hỏi ?
#    regex10 = re.compile('(?<=[])(?=) | (?<=)(?=[])')                           #Dấu chấm phẩy ;
#    regex11 = re.compile('(?<=[])(?=) | (?<=)(?=[])')                           #Dấu gạch / \ |
#    regex12 = re.compile('(?<=[])(?=) | (?<=)(?=[])')                           #Dấu xấp xỉ ~
#    regex13 = re.compile('(?<=[])(?=) | (?<=)(?=[])')                           #Dấu &

#============================================================================== Tách câu.
def split_sentences(url, filename):
    s = read_file_stringtype(url, filename)
    regex = re.compile('(?<=[\.\?!])[\s\n]|\n|\.+s')
    sentences = re.split(regex,s)
    del sentences[-1]
    return sentences

#============================================================================== Tách từ tố.
def tokenize(the_list):
    lst = list()
    
    regex = re.compile('[^\s]+')
#    prev = ''
#    curr = ''
    for i in the_list:
        
#        i = add_space_word_matecharacter(i)
#        i = add_space_metacharacter_word(i)
#        i = add_space_1(i)
#        
#        token = regex.findall(i)
        i.split()
        lst.append(i)
        
    return lst


def tokenizez(url,filename):
    s = list()
    regex1 = re.compile('(?<=[^\w+])(?=\w)')
    regex2 = re.compile('(?<=\w)(?=[^\w+])')
    sentences = read_file_TextIOWrappertype(link_output_file,filename)
    for sentence in sentences:
        sentence = re.sub(regex1, ' ', sentence)
        sentence = re.sub(regex2, ' ', sentence)
        sentence = sentence.split()

        
        s.append(sentence)
    return s
#============================================================================== Tách từ.
def word_seagment(the_list):
    
        
    return 0

#============================================================================== Main.
input_file = read_file_stringtype(link_input_file,'12000-13000.txt')
input_file = remove_some(input_file)
write_file(input_file,'removed.txt',link_out_file)
#============================================================================== In kết quả tách câu.
list_sentences = split_sentences(link_out_file,'removed.txt')
write_listline_file(list_sentences,'sentences.txt',link_output_file)
print ('So cau: %d' % len(list_sentences))
#============================================================================== In kết quả tách từ tố.
tokens = tokenizez(link_output_file,'sentences.txt')
print (tokens[1][-2])

write_listline_file(tokens,'tokens.txt',link_output_file)

print (datetime.now()-start)