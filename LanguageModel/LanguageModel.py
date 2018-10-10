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
        for line in inputfile:
            line1 = line.lower()
            
            line_lowcase = line1.split()
            
            curWord = line_lowcase[0]
            preWord = 'None'
            
            if curWord not in word_freq:
                word_freq[curWord] = 1
            else:
                word_freq[curWord] += 1
            
            
            for word in line_lowcase:
                if preWord is 'None':
                    curWord = word
                    preWord = curWord
                    pass
                else:
                    preWord = curWord
                    curWord = word                
                
                    if word not in word_freq:
                        word_freq[word] = 1
                    else:
                        word_freq[word] += 1
            
                    if preWord not in word_word_freq:
                        word_word_freq[preWord][curWord] = 1
                    elif curWord not in word_word_freq[preWord]:
                        word_word_freq[preWord][curWord] = 1
                    else: word_word_freq[preWord][curWord] += 1
                
#            del word_word_freq[line_lowcase[0]]
    with open(link_out_file+'wordCount.txt','w',encoding='utf8') as outfile:
        json.dump(word_freq,outfile,ensure_ascii=False)
    display_out_file(word_word_freq,'word_to_word.txt')
    
if __name__ == "__main__":main()