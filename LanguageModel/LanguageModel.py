from collections import defaultdict
import pprint
import json
from collections import OrderedDict
from datetime import datetime
import os


def create_Folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

link_folder_ = '\\Users\\NghiLam\\Documents\\NLP\\LanguageModel\\'
link_out_file = link_folder_ + 'outfile\\'
link_train_file = link_folder_ + 'input\\'
link_result_file = link_folder_ + 'output\\'
link_model = link_folder_ + 'model\\'

word_freq = dict() #count word.
word_word_freq = defaultdict(dict)  #count word=>word
word_word_prob = defaultdict(dict)  #calculate probability.
word_prob_test = dict()             #sum of probability of one word.
bi_for_tri_freq = dict

def write_count_one_word(objet,filename,link):
    with open(link + filename, 'w', encoding='utf-8') as fout:
        json.dump(objet,'count_one_word.txt',)

def write_word_frequency_to_see(lst,filename,link):
    with open(link + filename, 'w', encoding='utf-8') as fout:
        pprint.pprint(lst,fout)

#def output_Model()

# Đoán từ tiếp theo.
def guess_next_word(word):
    for item in word_word_prob[word]:
        sorted_by_value = OrderedDict(sorted(word_word_prob[word].items(), key=lambda x: x[1], reverse=True))

    for index,item in enumerate(sorted_by_value.items()):
        print (index+1, item)

    return sorted_by_value
    
# Tính xác suất câu.
def calculate_sentence_probability(s):
    lst_word = s.lower().split()
    prev = 'None'
    curr = lst_word[0]
    prob = defaultdict(dict)
    sentence_prob = 1
    totalWord = len(word_freq)
    
    for word in lst_word:
        if prev is 'None':                                           #Neu chua duyet tiep word thư 2.
            prev = ''
            pass
        else:
            prev = curr
            curr = word
            #TU da co
            if prev in word_word_prob:
                if curr in word_word_prob[prev]:
                    prob[prev][curr] = word_word_prob[prev][curr]
                    sentence_prob *= prob[prev][curr]
                else:
#                    prob[prev][curr] = 1/(word_count[prev]+totalWord)
                    prob[prev][curr] = 1/word_freq[prev]
                    sentence_prob *= prob[prev][curr]
            #Tu chua co
            else:
                prob[prev][curr] = 1/(1+totalWord)
                sentence_prob *= prob[prev][curr]
                
    return sentence_prob,prob

# bi-gram
def training_bigram(filename):
    with open(link_train_file + filename,'r',encoding='utf-8') as inputfile:
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
            #Duyet tu word thu 2.
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
    del word_freq['$end.']
    
    create_Folder('./outfile/')
    write_word_frequency_to_see(word_word_freq,'bigram_freq_display.txt',link_out_file)  #Ghi file tan suat word=>word
    with open(link_out_file+ 'bigram_frequency.txt','w',encoding='utf-8') as biFreq:
        json.dump(word_word_freq,biFreq,ensure_ascii=False)
    
    for eachWord in word_freq:
        word_prob_test[eachWord] = 0
        for followWord in word_word_freq[eachWord]:
            word_word_prob[eachWord][followWord] = word_word_freq[eachWord][followWord]/word_freq[eachWord]
            word_prob_test[eachWord] += word_word_prob[eachWord][followWord]
    
    write_word_frequency_to_see(word_prob_test,'test_bi_probability.txt',link_out_file)
    
    create_Folder('./model/')
    Lmodel = {}
    Lmodel['Language model'] = word_word_prob
    Lmodel['Word count'] = word_freq
    with open(link_model + 'bi_model.txt', 'w',encoding='utf8') as outfile:
        json.dump(Lmodel, outfile, ensure_ascii=False)
    # GHI LAI CHO DE NHIN.
    with open(link_model + 'display_bi_model.txt', 'w',encoding='utf8') as outfile:
        outfile.write('Language model:\n')
        for key,value in Lmodel['Language model'].items():
            outfile.write('%s:%s\n' % (key, value))
        outfile.write('\nWord count:\n')    
        for key,value in Lmodel['Word count'].items():
            outfile.write('%s:%s\n' % (key, value))
# tri gram #########################################################################
def training_trigram(textFileName):
    bi,tri = counting_trigram(textFileName)
    prob = tri_prob(bi,tri)
    Lmodel = {}
    Lmodel['Language model'] = prob
    Lmodel['Word count'] = bi
    with open(link_model + 'tri_model.txt', 'w',encoding='utf8') as outfile:
        json.dump(Lmodel,outfile,ensure_ascii=False)
    # GHI LAI CHO DE NHIN.
    with open(link_model + 'display_tri_model.txt', 'w',encoding='utf8') as outfile:
        outfile.write('Language model:\n')
        for key,value in Lmodel['Language model'].items():
            outfile.write('%s:%s\n' % (key, value))
        outfile.write('\nWord count:\n')    
        for key,value in Lmodel['Word count'].items():
            outfile.write('%s:%s\n' % (key, value))
    return prob
    
def counting_trigram(textFileName):
    bi_count = dict()
    trigram_frequency = defaultdict(dict)
    with open(link_train_file + textFileName,'r',encoding='utf-8') as inputfile:
        for line in inputfile:                                                  #Duyet tung dong.
            line1 = line.lower()                                                #Bo? viet hoa.
            
            line_lowcase = line1.split()
            
            for i in range(0,len(line_lowcase)-2):

                first_word = line_lowcase[i]
                second_word = line_lowcase[i+1]
                third_word = line_lowcase[i+2]
#                bigram = (first_word, second_word)
                bigram = first_word+' '+second_word
                
                if bigram not in bi_count:
                    bi_count[bigram] = 1
                else:
                    bi_count[bigram] += 1

#                word_word_word frequency.
                if bigram not in trigram_frequency:
                    trigram_frequency[bigram][third_word] = 1
                else:
                    if third_word not in trigram_frequency[bigram]:
                        trigram_frequency[bigram][third_word] = 1
                    else:
                        trigram_frequency[bigram][third_word] += 1
                        
#                        In word_word_word frequency.
    write_word_frequency_to_see(trigram_frequency,'trigram_freq_display.txt',link_out_file)  #Ghi file tan suat word=>word
    write_word_frequency_to_see(bi_count,'bigram_count.txt',link_out_file)
    
    return bi_count,trigram_frequency
######################################### Probability
def tri_prob(bigram_count, trigram_count):
    probability = defaultdict(dict)
    
    for bigram in bigram_count:
        word_prob_test[bigram] = 0
        for third_word in trigram_count[bigram]:
            probability[bigram][third_word] = trigram_count[bigram][third_word]/bigram_count[bigram]
            word_prob_test[bigram] += probability[bigram][third_word]
    
    write_word_frequency_to_see(word_prob_test,'test_tri_probability.txt',link_out_file)
    
    return probability

def main():
    
    
#    word_freq = dict() #count word.
#    word_word_freq = defaultdict(dict)  #count word=>word
#    word_word_prob = defaultdict(dict)  #calculate probability.
#    word_prob_test = dict()             #sum of probability of one word.
    
    start=datetime.now()
# ==========================   Tính mô hình ngôn ngữ =====================================
#    training_bigram('input.pos')
    training_trigram('input.pos')
# ==========================   Đoán từ tiếp theo  ========================================
#    guess_next_word('kinh_tế')
#    guess_next_word('có_thể')
    
# ==========================   Tính xác suất một câu  ====================================    
#    s = 'Dịch_vụ đang trở_thành lĩnh_vực xuất_khẩu mới đóng_góp đáng_kể vào kim_ngạch xuất_khẩu của Việt_Nam .'
#    s = 'Hỏi sao gọi “ bù_kẹp ” , anh cười : “ Dân miền Tây gọi con bò_cạp là bù_kẹp .'
#    s = 'Nhưng đó là quyết_định của anh .'
#    s = 'Kỹ_thuật điêu_luyện , lối chơi thông_minh của Vinh “ sói ” đã làm điên_đảo hầu_hết những đối_thủ từ Á đến Âu mà tuyển miền Nam đã gặp thời ấy như Hàn_Quốc , Hong_Kong , Nhật , các đội Djugaden , Helsinborg ( Thụy_Điển ) , Lask ( Áo ) ...'
#    s = 'Giờ_đây nhiều nông_dân cố_cựu vùng Đồng_Tháp_Mười này như bác Võ_Văn_Ni ( ấp Bàu_Môn , xã Thạnh_Hưng , huyện Mộc_Hóa ) vẫn còn nhớ như in những ngày đầu khi Trung_tâm Nghiên_cứu thực_nghiệm nông_nghiệp Đồng_Tháp_Mười vừa thành_lập : “ Tôi là người ở Đồng_Tháp_Mười từ thời ông cố đến giờ , tôi hiểu cục đất nơi này còn hơn cả con mình , vậy_mà hồi mấy chú vô tôi cứ cười bảo : để rồi coi , ở không được một vụ đâu , đất này làm chơi thôi chứ cao_sản cao_siếc cái gì ...'
#    write_word_frequency_to_see(calculate_sentence_probability(s),'SentenceProb.txt',link_result_file)
    
    print (datetime.now()-start)
if __name__ == "__main__":main()
