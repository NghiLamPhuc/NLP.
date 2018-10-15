from collections import defaultdict
import pprint
import json
from datetime import datetime

link_folder_ = '\\Users\\NghiLam\\Documents\\GATSOP\\LanguageModel\\'
link_out_file = link_folder_ + 'outfile\\'
link_train_file = link_folder_ + 'input\\'
link_result_file = link_folder_ + 'output\\'

def display_out_file(lst,filename):
    file = link_out_file + filename
    with open(file, 'w', encoding='utf-8') as fout:
        pprint.pprint(lst,fout)
        
def main():
    word_freq = dict() #count word.
    word_word_freq = defaultdict(dict)  #count word=>word
    word_word_prob = defaultdict(dict)  #calculate probability.
    word_prob_test = dict()             #sum of probability of one word.
    
    with open(link_train_file+'input.pos','r',encoding='utf-8') as inputfile:
        for line in inputfile:                                                  #Duyet tung dong.
            line1 = line.lower()                                                #Bo? viet hoa.
            
            line_lowcase = line1.split()                                        #Cat ca^u thanh list word.
            line_lowcase.append('$end.')
            
            curWord = line_lowcase[0]                                           #Xet word dau tien.
            preWord = 'None'
                                                                                #Dem word dau tien cua moi cau.
            if curWord not in word_freq:
                word_freq[curWord] = 1
            else:
                word_freq[curWord] += 1
                                                                                #Duyet tiep tuc.
            for word in line_lowcase:
                if preWord is 'None':                                           #Neu chua duyet tiep word thư 2.
                    preWord = ''
                    pass
                else:
                    preWord = curWord
                    curWord = word
                                                                                #Dem tan suat word.
                    if word not in word_freq:
                        word_freq[word] = 1
                    else:
                        word_freq[word] += 1
                                                                                #Dem tan suat word_to_word.
                    if preWord not in word_word_freq:                           # Thiếu word => $.
                        word_word_freq[preWord][curWord] = 1
                    elif curWord not in word_word_freq[preWord]:
                        word_word_freq[preWord][curWord] = 1
                    else: word_word_freq[preWord][curWord] += 1
        
    display_out_file(word_word_freq,'word_to_word_freq.txt')                    #Ghi file tan suat word=>word
# Tinh xác suất: những từ có trong train.
    v = len(word_freq)                                                          #Số các từ trong train.
    print (v)
    
    #P(w_i | w_i-1) = count(w_i-1, w_i) / count(w_i-1)
                
    for eachWord in word_freq:
        word_prob_test[eachWord] = 0
        for followWord in word_word_freq[eachWord]:
            word_word_prob[eachWord][followWord] = word_word_freq[eachWord][followWord]/word_freq[eachWord]
            word_prob_test[eachWord] += word_word_prob[eachWord][followWord]
    
    display_out_file(word_prob_test,'test_probability.txt')
    
    Lmodel = {}
    Lmodel['Language model'] = word_word_prob
    Lmodel['Word count'] = word_freq
    with open(link_result_file + 'model.txt', 'w',encoding='utf8') as outfile:
        json.dump(Lmodel, outfile, ensure_ascii=False)
    # GHI LAI CHO DE NHIN.
    with open(link_result_file + 'display_model.txt', 'w',encoding='utf8') as outfile:
        outfile.write('Language model:\n')
        for key,value in Lmodel['Language model'].items():
            outfile.write('%s:%s\n' % (key, value))
        outfile.write('\nWord count:\n')    
        for key,value in Lmodel['Word count'].items():
            outfile.write('%s:%s\n' % (key, value))

start=datetime.now()
if __name__ == "__main__":main()
print (datetime.now()-start)