import re

#f = open("chientranh_hoabinh.txt",'r',encoding="utf8")
f = open("12000-13000.txt",'r',encoding="utf8")
string1 = f.read()
f.close()

# The^m space va`o giua chu cai va ky tu dac biet
def add_space_after_word_matecharacter(s):
    return re.sub('(?<=\w)(?=[.,\-\)\}\]?!%\":;])', ' ', s)
    
def add_space_before_word_metacharacter(s):
    return re.sub('(?<=[.,\(\{\[?!%\":;])(?=\w)', ' ', s)

# BEGIN.########################### Tach cau #############################
# input la van ban
def split_sentences(st):
    lst = list()
# Sau cùng là dấu '!', '?', '.'. Trước nó là bất cứ ký tự gì khác '!', '?', '.'.
    regex = re.compile('[^!?\.]+[!?\.]')
#    regex = re.compile('')
    sentences = regex.findall(st)
     
    for s in sentences:
        lst.append(s.strip())
    
    return lst
# Tách câu.################################################################ END
 
# BEGIN.########################### Tach tu to #############################


def split_tokens_2(the_list):
    lst = list()
    
    regex = re.compile('[^\s]+')
    
    for i in the_list:
#        i1 = add_space_after_word_matecharacter(i)
        i2 = add_space_before_word_metacharacter(i1)
        token = regex.findall(i2)
        lst.append(token)
        
    return lst
# Tách từ tố 1.########################################################### END
    
# ############# In kết quả tách câu ###########################################
lst_sntncs = split_sentences(string1)
#print(lst_sntncs)
#print(lst_tkns)
# ############# In kết quả tách tu to #######################################
tokens = split_tokens_2(lst_sntncs)
print(tokens)
