from collections import defaultdict
import pprint
import json

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
    word_word_freq = defaultdict(dict)
    
    with open(link_train_file+'input.pos','r',encoding='utf-8') as inputfile:
        for line in inputfile:                                                  #Duyet tung dong.
            line1 = line.lower()                                                #Bo? viet hoa.
            
            line_lowcase = line1.split()                                        #Cat ca^u thanh list word.
            
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
                    if preWord not in word_word_freq:
                        word_word_freq[preWord][curWord] = 1
                    elif curWord not in word_word_freq[preWord]:
                        word_word_freq[preWord][curWord] = 1
                    else: word_word_freq[preWord][curWord] += 1

    with open(link_out_file+'wordCount.txt','w',encoding='utf8') as outfile:
        json.dump(word_freq,outfile,ensure_ascii=False)
    display_out_file(word_word_freq,'word_to_word.txt')
    
if __name__ == "__main__":main()