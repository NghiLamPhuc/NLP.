import json
import pprint

link_folder_ = '\\Users\\NghiLam\\Documents\\GATSOP\\LanguageModel\\'
link_out_file = link_folder_ + 'outfile\\'
link_input_file = link_folder_ + 'output\\'
link_result_file = link_folder_

def display_out_file(lst,filename):
    file = link_out_file + filename
    with open(file, 'w', encoding='utf-8') as fout:
        pprint.pprint(lst,fout)

def main():
    
    with open(link_input_file + 'model.txt',encoding='utf-8') as model_file:    
        Lmodel = json.load(model_file)
        probability = Lmodel['Language model']
        word_count = Lmodel['Word count']
        totalWord = len(word_count)

    s = 'Tôi đi học .'
    lst_word = s.lower().split()
    
    prev = 'None'
    curr = lst_word[0]
    prob = 1
    for word in lst_word:    
        if prev is 'None':                                           #Neu chua duyet tiep word thư 2.
            prev = ''
            pass
        else:
            prev = curr
            curr = word
            #TU da co
            if prev in probability:
                if curr in probability[prev]:
                    prob *= probability[prev][curr]
                elif curr in word_count:
                    probability[prev][curr] = round(2/(word_count[curr]+totalWord),6)
                    prob *= probability[prev][curr]
                else:
                    word_count[curr] = 1
                    probability[prev][curr] = round(2/(1+totalWord),6)
                    prob *= probability[prev][curr]
            #Tu chua co
            else:
                word_count[prev] = 1
                if curr in word_count:    
                    probability[prev][curr] = round(2/(word_count[curr]+totalWord),6)
                    prob *= probability[prev][curr]
                else:
                    word_count[curr] = 1
                    probability[prev][curr] = round(2/(1+totalWord),6)
                    prob *= probability[prev][curr]
            
    print (prob)
        
if __name__ == "__main__":main()