from collections import defaultdict
import pprint
import json
from collections import OrderedDict
from datetime import datetime

link_folder_ = '\\Users\\NghiLam\\Documents\\NLP\\LanguageModel\\'
link_out_file = link_folder_ + 'outfile\\'
link_train_file = link_folder_ + 'input\\'
link_result_file = link_folder_ + 'output\\'

word_freq = dict() #count word.
word_word_freq = defaultdict(dict)  #count word=>word
word_word_prob = defaultdict(dict)  #calculate probability.
word_prob_test = dict()             #sum of probability of one word.

def display_file(lst,filename,link):
    with open(link + filename, 'w', encoding='utf-8') as fout:
        pprint.pprint(lst,fout)

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

def training(filename):
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
    del word_freq['$end.']
        
    display_file(word_word_freq,'word_to_word_freq.txt',link_out_file)  #Ghi file tan suat word=>word
    
    for eachWord in word_freq:
        word_prob_test[eachWord] = 0
        for followWord in word_word_freq[eachWord]:
            word_word_prob[eachWord][followWord] = word_word_freq[eachWord][followWord]/word_freq[eachWord]
            word_prob_test[eachWord] += word_word_prob[eachWord][followWord]
    
    display_file(word_prob_test,'test_probability.txt',link_out_file)
    
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

    

def main():
    
    
#    word_freq = dict() #count word.
#    word_word_freq = defaultdict(dict)  #count word=>word
#    word_word_prob = defaultdict(dict)  #calculate probability.
#    word_prob_test = dict()             #sum of probability of one word.
    
    start=datetime.now()
# ==========================   Tính mô hình ngôn ngữ =====================================
    training('input.pos')
# ==========================   Đoán từ tiếp theo  ========================================
    guess_next_word('kinh_tế')
    
# ==========================   Tính xác suất một câu  ====================================    
#    s = 'Dịch_vụ đang trở_thành lĩnh_vực xuất_khẩu mới đóng_góp đáng_kể vào kim_ngạch xuất_khẩu của Việt_Nam .'
#    s = 'Hỏi sao gọi “ bù_kẹp ” , anh cười : “ Dân miền Tây gọi con bò_cạp là bù_kẹp .'
#    s = 'Nhưng đó là quyết_định của anh .'
#    s = 'Kỹ_thuật điêu_luyện , lối chơi thông_minh của Vinh “ sói ” đã làm điên_đảo hầu_hết những đối_thủ từ Á đến Âu mà tuyển miền Nam đã gặp thời ấy như Hàn_Quốc , Hong_Kong , Nhật , các đội Djugaden , Helsinborg ( Thụy_Điển ) , Lask ( Áo ) ...'
#    s = 'Giờ_đây nhiều nông_dân cố_cựu vùng Đồng_Tháp_Mười này như bác Võ_Văn_Ni ( ấp Bàu_Môn , xã Thạnh_Hưng , huyện Mộc_Hóa ) vẫn còn nhớ như in những ngày đầu khi Trung_tâm Nghiên_cứu thực_nghiệm nông_nghiệp Đồng_Tháp_Mười vừa thành_lập : “ Tôi là người ở Đồng_Tháp_Mười từ thời ông cố đến giờ , tôi hiểu cục đất nơi này còn hơn cả con mình , vậy_mà hồi mấy chú vô tôi cứ cười bảo : để rồi coi , ở không được một vụ đâu , đất này làm chơi thôi chứ cao_sản cao_siếc cái gì ...'
#    display_file(calculate_sentence_probability(s),'SentenceProb.txt',link_result_file)
    
    print (datetime.now()-start)
if __name__ == "__main__":main()
