import os
import re
from datetime import datetime

def create_Folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

cwd = os.getcwd()

link_folder = cwd
link_input_file = '/Workspace/NLP/RAW_TEXT/van ban tho/'
link_out_file = link_folder + '/outfile/'
link_sentences = link_folder + '/sentences/'
link_token = link_folder + '/tokens/'

#============================================================================== Một số hàm đọc ghi.
#============================================================================== Ghi file ra từng dòng.
def write_Listline_File(List, filename, url):
    f = open(url + filename,'w',encoding='utf8')
    for t in List:
        f.write("%s\n" % t)
    f.close()
    
#============================================================================== Ghi 1 list.
def write_File(file, filename, url):
    f = open(url + filename,'w',encoding='utf8')
    f.write(file)
    f.close()
#============================================================================== Đọc file kiểu string.
def read_File_Stringtype(url,filename):
    f = open(url + filename,'r',encoding='utf8')
    input_file = f.read()
    f.close()
    return input_file
#============================================================================== Đọc file kiểu Text Wrapper.
def read_file_TextIOWrappertype(url, filename):                                 # Dùng for để duyệt qua từng phần tử.
    return open(url + filename, 'r', encoding='utf8')
    
#============================================================================== Loại bỏ một số dấu trong văn bản input.
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
def add_Space_Word_Matecharacter(s):
    return re.sub('(?<=\w)(?=[\/\_\-\(\)\{\}\[\]?!%\":;]\s)', ' ', s)          # abc{
    
def add_Space_Metacharacter_Word(s):
    return re.sub('(?<=\s[,\/\_\-\(\)\{\}\[\]?!%\":;])(?=\w)', ' ', s)         # }abc
    
def add_Space_1(s):
    return re.sub('(?<=[,\/\_\-\(\)\{\}\[\]?!%\":;])(?=[,\/\_\-\(\)\{\}\[\]?!%\":;]\s)', ' ', s)

#https://vi.wikipedia.org/wiki/D%E1%BA%A5u_c%C3%A2u
def add_Space(s):
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
alphabets = "(A-Za-z)"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](vn|com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

def split_Sentences(url, filename):
    s = read_File_Stringtype(url, filename)
    regex = re.compile('(?<!\w\.\w.)(?<![A-Z][a-z])(?<=\.|\?|\!)\s')
#    regex = re.compile('(?<=[\.\?!])[\s\n]')
    sentences = re.split(regex,s)
         
    del sentences[-1]
    return sentences

def sentencize(url, filename):
    s = read_File_Stringtype(url, filename)
    
#============================================================================== Tách từ tố.
def tokenize(the_list):
    lst = list()
    
    regex = re.compile('[^\s]+')
#    prev = ''
#    curr = ''
    for i in the_list:
        
        i = add_Space_Word_Matecharacter(i)
        i = add_Space_Metacharacter_Word(i)
        i = add_Space_1(i)
#        
        token = regex.findall(i)
        i.split()
        lst.append(i)
        
    return lst


def tokenizez(url,filename):
    s = list()
    regex1 = re.compile('(?<=[^\w+])(?=\w)')
#    regex1 = re.compile('(?<=[^\[A-Z][a-z]+])(?=\w)') // sai roi sao?
    regex2 = re.compile('(?<=\w)(?=[^\w+])')
#    regex2 = re.compile('(?<=\w)(?=[^[A-Z][a-z]+])')
    sentences = read_file_TextIOWrappertype(link_sentences,filename)
    for sentence in sentences:
        sentence = re.sub(regex1, ' ', sentence)
        sentence = re.sub(regex2, ' ', sentence)
        sentence = sentence.split()

        s.append(sentence)
    return s
#============================================================================== Tách từ.

# Lấy danh sách các file txt trong folder.
def get_Os_Dir_File(link):
    all_files = os.listdir(link)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files) # Co cung dc, khong co k sao.
    return txt_files
# Loại bỏ ký tự đặc biệt lưu vào file.
def text_Proccessing_Before():
    create_Folder('./outfile/')
    txt_files = get_Os_Dir_File(link_input_file)   # raw text
    text_proccessed = ''
    for index, file in enumerate(txt_files):
        input_file = read_File_Stringtype(link_input_file,file)
        input_file = remove_some(input_file)
        text_proccessed = text_proccessed + input_file
        write_File(input_file,file+'.txt',link_out_file)
#    write_File(text_proccessed,'all_text.txt',link_out_file)
    return text_proccessed

def tach_Cau():
    create_Folder('./sentences/')
    proccessed_file = get_Os_Dir_File(link_out_file)
    for index,file in enumerate(proccessed_file):
        list_sentences = split_Sentences(link_out_file,file)
#        write_Listline_File(list_sentences,file,link_sentences)
        print ('%d. Số câu: %d' % (index,len(list_sentences)))
    return list_sentences
        
def tach_Tu_To():
    create_Folder('./tokens/')
    proccessed_file = get_Os_Dir_File(link_sentences)
    for index,file in enumerate(proccessed_file):
        tokens = tokenizez(link_sentences,file)
#        write_Listline_File(tokens,file,link_token)
#        print ('%d. Số tokens: %d' % (index,len(tokens)))
        print ('Số tokens: %d' % len(tokens))
    return tokens

def main():
    start=datetime.now()

    #============================================================================== Main.
    # Đầu tiên đọc file text, loại bỏ ký tự đặc biệt, ghi lại file vào outfile.
#    text_proccessed = text_Proccessing_Before()
#    write_File(text_proccessed,'all_text.txt',link_out_file)
    #============================================================================ In kết quả tách câu.
    a = tach_Cau()
    write_Listline_File(a,'sentences.txt',link_sentences)
    #========================================================================== In kết quả tách từ tố.
    b = tach_Tu_To()
    write_Listline_File(b,'tokens.txt',link_token)
    
    print (datetime.now()-start)

if __name__ == "__main__":main()
