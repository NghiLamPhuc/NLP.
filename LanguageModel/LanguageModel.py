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
        json.dump(objet,'count_one_word.txt',fout)

def write_word_frequency_to_see(lst,filename,link):
    with open(link + filename, 'w', encoding='utf-8') as fout:
        pprint.pprint(lst,fout)

#def output_Model()

# Đoán từ tiếp theo.
def guess_next_bi(word):
    with open(link_model + 'bi_model.txt',encoding='utf-8') as model_file:    
        Lmodel = json.load(model_file)
        probability = Lmodel['Language model']
#        emissionProb = Lmodel['Emission Probability']
    for item in probability[word]:
        sorted_by_value = OrderedDict(sorted(probability[word].items(), key=lambda x: x[1], reverse=True))

    for index,item in enumerate(sorted_by_value.items()):
        print (index+1, item)

    return sorted_by_value
# Doan tu tiep theo 1 bigram.
def guess_next_tri(word):
    with open(link_model + 'tri_model.txt',encoding='utf-8') as model_file:    
        Lmodel = json.load(model_file)
        probability = Lmodel['Language model']
    bigram = word
    for item in probability[bigram]:
        sorted_by_value = OrderedDict(sorted(probability[bigram].items(), key=lambda x: x[1], reverse=True))

    for index,item in enumerate(sorted_by_value.items()):
        print (index+1, item)

    return sorted_by_value
# Doan tu tiep theo 1 trigram.
def guess_next_four(word):
    with open(link_model + 'four_model.txt',encoding='utf-8') as model_file:    
        Lmodel = json.load(model_file)
        probability = Lmodel['Language model']
    trigram = word
    for item in probability[trigram]:
        sorted_by_value = OrderedDict(sorted(probability[trigram].items(), key=lambda x: x[1], reverse=True))

    for index,item in enumerate(sorted_by_value.items()):
        print (index+1, item)

    return sorted_by_value

# Tính xác suất câu.
def calculate_sentence_probability(s):
    with open(link_model + 'bi_model.txt',encoding='utf-8') as model_file:    
        Lmodel = json.load(model_file)
        probability = Lmodel['Language model']
        word_freq = Lmodel['Word count']
        
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
            if prev in probability:
                if curr in probability[prev]:
                    prob[prev][curr] = probability[prev][curr]
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


###############################################################################################################
# ----------------------------------------------------------------------------------------------------- BI GRAM.
###############################################################################################################
def training_bigram(textFileName):
    uni,bi = counting_bigram(textFileName)
    prob = bi_prob(uni,bi)
    Lmodel = {}
    Lmodel['Language model'] = prob
    Lmodel['Word count'] = bi
    with open(link_model + 'bi_model.txt', 'w',encoding='utf8') as outfile:
        json.dump(Lmodel,outfile,ensure_ascii=False)
    # GHI LAI CHO DE NHIN.
    with open(link_model + 'display_bi_model.txt', 'w',encoding='utf8') as outfile:
        outfile.write('Language model:\n')
        for key,value in Lmodel['Language model'].items():
            outfile.write('%s:%s\n' % (key, value))
        outfile.write('\nWord count:\n')    
        for key,value in Lmodel['Word count'].items():
            outfile.write('%s:%s\n' % (key, value))
    return prob
# Counting word frequency; word to word frequency.
def counting_bigram(textFileName):
#    word or uni
    word_count = dict()
    bigram_frequency = defaultdict(dict)
    with open(link_train_file + textFileName,'r',encoding='utf-8') as inputfile:
        for line in inputfile:                                                  #Duyet tung dong.
            line1 = line.lower()                                                #Bo? viet hoa.
            line_lowcase = line1.split()
            for i in range(0,len(line_lowcase)-1):

                first_word = line_lowcase[i]
                second_word = line_lowcase[i+1]
                
                if first_word not in word_count:
                    word_count[first_word] = 1
                else:
                    word_count[first_word] += 1

#                word_word frequency.
                if first_word not in bigram_frequency:
                    bigram_frequency[first_word][second_word] = 1
                else:
                    if second_word not in bigram_frequency[first_word]:
                        bigram_frequency[first_word][second_word] = 1
                    else:
                        bigram_frequency[first_word][second_word] += 1
                        
    create_Folder('./outfile/bigram/')
#                        In word_word_word frequency.
    write_word_frequency_to_see(bigram_frequency,'bigram_freq_display.txt',link_out_file+'\\bigram\\')  #Ghi file tan suat word=>word
    write_word_frequency_to_see(word_count,'uni_count.txt',link_out_file+'\\bigram\\')
    return word_count, bigram_frequency

# Probability bi gram p(w2|w1) = count(w1,w2) / count(w1)
def bi_prob(word_count, bigram_count):
    probability = defaultdict(dict)
    
    for word in word_count:
        word_prob_test[word] = 0
        for nd_word in bigram_count[word]:
            probability[word][nd_word] = bigram_count[word][nd_word]/word_count[word]
            word_prob_test[word] += probability[word][nd_word]
    
    write_word_frequency_to_see(word_prob_test,'test_bi_probability.txt',link_out_file+'\\bigram\\')
    
    return probability
###############################################################################################################
# ----------------------------------------------------------------------------------------------------- TRI GRAM.
###############################################################################################################
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
# Counting tri gram ################################################################
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
    create_Folder('./outfile/trigram/')
#                        In word_word_word frequency.
    write_word_frequency_to_see(trigram_frequency,'trigram_freq_display.txt',link_out_file+'\\trigram\\')
    write_word_frequency_to_see(bi_count,'bigram_count.txt',link_out_file+'//trigram//')
    
    return bi_count,trigram_frequency

# Probability tri gram
def tri_prob(bigram_count, trigram_count):
    probability = defaultdict(dict)
    
    for bigram in bigram_count:
        word_prob_test[bigram] = 0
        for third_word in trigram_count[bigram]:
            probability[bigram][third_word] = trigram_count[bigram][third_word]/bigram_count[bigram]
            word_prob_test[bigram] += probability[bigram][third_word]
    
    write_word_frequency_to_see(word_prob_test,'test_tri_probability.txt',link_out_file+'//trigram//')
    
    return probability
###############################################################################################################
# ----------------------------------------------------------------------------------------------------- 4 GRAM.
###############################################################################################################
def training_fourgram(textFileName):
    tri,four = counting_fourgram(textFileName)
    prob = four_prob(tri,four)
    Lmodel = {}
    Lmodel['Language model'] = prob
    Lmodel['Word count'] = tri
    with open(link_model + 'four_model.txt', 'w',encoding='utf8') as outfile:
        json.dump(Lmodel,outfile,ensure_ascii=False)
    # GHI LAI CHO DE NHIN.
    with open(link_model + 'display_four_model.txt', 'w',encoding='utf8') as outfile:
        outfile.write('Language model:\n')
        for key,value in Lmodel['Language model'].items():
            outfile.write('%s:%s\n' % (key, value))
        outfile.write('\nWord count:\n')    
        for key,value in Lmodel['Word count'].items():
            outfile.write('%s:%s\n' % (key, value))
    return prob
# Counting tri gram ################################################################
def counting_fourgram(textFileName):
    tri_count = dict()
    four_gram_frequency = defaultdict(dict)
    with open(link_train_file + textFileName,'r',encoding='utf-8') as inputfile:
        for line in inputfile:                                                  #Duyet tung dong.
            line1 = line.lower()                                                #Bo? viet hoa.
            
            line_lowcase = line1.split()
            
            for i in range(0,len(line_lowcase)-3):

                first_word = line_lowcase[i]
                second_word = line_lowcase[i+1]
                third_word = line_lowcase[i+2]
                fourth_word = line_lowcase[i+3]

                trigram = first_word+' '+second_word+' '+third_word
                
                if trigram not in tri_count:
                    tri_count[trigram] = 1
                else:
                    tri_count[trigram] += 1

#                word_word_word_word frequency.
                if trigram not in four_gram_frequency:
                    four_gram_frequency[trigram][fourth_word] = 1
                else:
                    if fourth_word not in four_gram_frequency[trigram]:
                        four_gram_frequency[trigram][fourth_word] = 1
                    else:
                        four_gram_frequency[trigram][fourth_word] += 1
    create_Folder('./outfile/fourgram/')
#                        In word_word_word frequency.
    write_word_frequency_to_see(four_gram_frequency,'four_gram_freq_display.txt',link_out_file+'//fourgram//')
    write_word_frequency_to_see(tri_count,'trigram_count.txt',link_out_file+'//fourgram//')
    
    return tri_count,four_gram_frequency

# Probability tri gram
def four_prob(trigram_count, four_gram_count):
    probability = defaultdict(dict)
    
    for trigram in four_gram_count:
        word_prob_test[trigram] = 0
        for fourth_word in four_gram_count[trigram]:
            probability[trigram][fourth_word] = four_gram_count[trigram][fourth_word]/trigram_count[trigram]
            word_prob_test[trigram] += probability[trigram][fourth_word]
    
    write_word_frequency_to_see(word_prob_test,'test_4_probability.txt',link_out_file+'//fourgram//')
    
    return probability

###############################################################################################################################
################################################################################################################     MAIN
###############################################################################################################################
def main():
    start=datetime.now()
    
#    word_freq = dict() #count word.
#    word_word_freq = defaultdict(dict)  #count word=>word
#    word_word_prob = defaultdict(dict)  #calculate probability.
#    word_prob_test = dict()             #sum of probability of one word.
    
    create_Folder('./outfile/')
    create_Folder('./model/')
# ==========================   Tính mô hình ngôn ngữ =====================================
#    bi_prob = training_bigram('input.pos')
#    tri_prob = training_trigram('input.pos')
#    four_prob = training_fourgram('input.pos')
# ==========================   Đoán từ tiếp theo  ========================================
#    guess_next_bi('kinh_tế')
#    guess_next_tri('kinh_tế và')
#    guess_next_four('kinh_tế và hội_nhập')
    
# ==========================   Tính xác suất một câu  ====================================    
#    s = 'Dịch_vụ đang trở_thành lĩnh_vực xuất_khẩu mới đóng_góp đáng_kể vào kim_ngạch xuất_khẩu của Việt_Nam .'
#    s = 'Hỏi sao gọi “ bù_kẹp ” , anh cười : “ Dân miền Tây gọi con bò_cạp là bù_kẹp .'
#    s = 'Nhưng đó là quyết_định của anh .'
#    s = 'Kỹ_thuật điêu_luyện , lối chơi thông_minh của Vinh “ sói ” đã làm điên_đảo hầu_hết những đối_thủ từ Á đến Âu mà tuyển miền Nam đã gặp thời ấy như Hàn_Quốc , Hong_Kong , Nhật , các đội Djugaden , Helsinborg ( Thụy_Điển ) , Lask ( Áo ) ...'
#    s = 'Giờ_đây nhiều nông_dân cố_cựu vùng Đồng_Tháp_Mười này như bác Võ_Văn_Ni ( ấp Bàu_Môn , xã Thạnh_Hưng , huyện Mộc_Hóa ) vẫn còn nhớ như in những ngày đầu khi Trung_tâm Nghiên_cứu thực_nghiệm nông_nghiệp Đồng_Tháp_Mười vừa thành_lập : “ Tôi là người ở Đồng_Tháp_Mười từ thời ông cố đến giờ , tôi hiểu cục đất nơi này còn hơn cả con mình , vậy_mà hồi mấy chú vô tôi cứ cười bảo : để rồi coi , ở không được một vụ đâu , đất này làm chơi thôi chứ cao_sản cao_siếc cái gì ...'
#    s = 'Hôm nay là ngày nắng'
#    create_Folder('./output/')
#    write_word_frequency_to_see(calculate_sentence_probability(s),'SentenceProbability.txt',link_result_file)
    
    print (datetime.now()-start)
if __name__ == "__main__":main()
