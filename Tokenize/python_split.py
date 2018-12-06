import os
import re
from datetime import datetime

start=datetime.now()

link_folder = '\\Users\\NghiLam\\Documents\\NLP\\Tokenize\\'
link_input_file = '\\Users\\NghiLam\\Documents\\NLP\\RAW_TEXT\\van ban tho\\'
link_out_file = link_folder + 'outfile\\'
link_sentences = link_folder + 'sentences\\'
link_token = link_folder + 'token\\'

link_raw_text = '\\Users\\NghiLam\\Documents\\NLP\\RAW_TEXT\\van ban tho\\'

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
#    regex = re.compile('(?<=[\.\?!])\n|\.+s')
    regex = re.compile('(?<=[\.\?!])[\s\n]')
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
        
        i = add_space_word_matecharacter(i)
        i = add_space_metacharacter_word(i)
        i = add_space_1(i)
#        
        token = regex.findall(i)
        i.split()
        lst.append(i)
        
    return lst


def tokenizez(url,filename):
    s = list()
    regex1 = re.compile('(?<=[^\w+])(?=\w)')
    regex2 = re.compile('(?<=\w)(?=[^\w+])')
    sentences = read_file_TextIOWrappertype(link_sentences,filename)
    for sentence in sentences:
        sentence = re.sub(regex1, ' ', sentence)
        sentence = re.sub(regex2, ' ', sentence)
        sentence = sentence.split()

        
        s.append(sentence)
    return s
#============================================================================== Tách từ.

# Lấy danh sách các file txt trong folder.
def get_os_dir_file(link):
    all_files = os.listdir(link)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files) # Co cung dc, khong co k sao.
    return txt_files
# Loại bỏ ký tự đặc biệt lưu vào file.
def text_proccessing_before():
    txt_files = get_os_dir_file(link_raw_text)
    for index, file in enumerate(txt_files):
        input_file = read_file_stringtype(link_input_file,file)
        input_file = remove_some(input_file)
        write_file(input_file,file+'.txt',link_out_file)

def tach_cau():
    proccessed_file = get_os_dir_file(link_out_file)
    for index,file in enumerate(proccessed_file):
        list_sentences = split_sentences(link_out_file,file)
        write_listline_file(list_sentences,file,link_sentences)
        print ('Số câu: %d' % len(list_sentences))
        
def tach_tu_to():
    proccessed_file = get_os_dir_file(link_sentences)
    for index,file in enumerate(proccessed_file):
#        tokens = tokenizez(link_sentences,file)
        tokens = tokenizez(link_sentences,file)
        write_listline_file(tokens,file,link_token)
    
#============================================================================== Main.
# Đầu tiên đọc file text, loại bỏ ký tự đặc biệt, ghi lại file vào outfile.
text_proccessing_before()
#============================================================================ In kết quả tách câu.
tach_cau()
#========================================================================== In kết quả tách từ tố.
tach_tu_to()



print (datetime.now()-start)