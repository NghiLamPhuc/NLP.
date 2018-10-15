import json
from collections import defaultdict

link_folder_ = '\\Users\\NghiLam\\Documents\\GATSOP\\LanguageModel\\'
link_out_file = link_folder_ + 'outfile\\'
link_input_file = link_folder_ + 'output\\'
link_result_file = link_folder_


def main():
    
    with open(link_input_file + 'model.txt',encoding='utf-8') as model_file:    
        Lmodel = json.load(model_file)
        
        probability = Lmodel['Language model']
        word_count = Lmodel['Word count']
        totalWord = len(word_count)

#    s = 'Dịch_vụ đang trở_thành lĩnh_vực xuất_khẩu mới đóng_góp đáng_kể vào kim_ngạch xuất_khẩu của Việt_Nam .'
#    s = 'Hỏi sao gọi “ bù_kẹp ” , anh cười : “ Dân miền Tây gọi con bò_cạp là bù_kẹp .'
    s = 'Nhưng đó là quyết_định của anh .'
#    s = 'Kỹ_thuật điêu_luyện , lối chơi thông_minh của Vinh “ sói ” đã làm điên_đảo hầu_hết những đối_thủ từ Á đến Âu mà tuyển miền Nam đã gặp thời ấy như Hàn_Quốc , Hong_Kong , Nhật , các đội Djugaden , Helsinborg ( Thụy_Điển ) , Lask ( Áo ) ...'
#    s = 'Giờ_đây nhiều nông_dân cố_cựu vùng Đồng_Tháp_Mười này như bác Võ_Văn_Ni ( ấp Bàu_Môn , xã Thạnh_Hưng , huyện Mộc_Hóa ) vẫn còn nhớ như in những ngày đầu khi Trung_tâm Nghiên_cứu thực_nghiệm nông_nghiệp Đồng_Tháp_Mười vừa thành_lập : “ Tôi là người ở Đồng_Tháp_Mười từ thời ông cố đến giờ , tôi hiểu cục đất nơi này còn hơn cả con mình , vậy_mà hồi mấy chú vô tôi cứ cười bảo : để rồi coi , ở không được một vụ đâu , đất này làm chơi thôi chứ cao_sản cao_siếc cái gì ...'    
    lst_word = s.lower().split()
    
    prev = 'None'
    curr = lst_word[0]
    prob = defaultdict(dict)
    sentence_prob = 1
    
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
                    prob[prev][curr] = 1/word_count[prev]
                    sentence_prob *= prob[prev][curr]
            #Tu chua co
            else:
                prob[prev][curr] = 1/(1+totalWord)
                sentence_prob *= prob[prev][curr]
    
    print (sentence_prob)
    for k,v in prob.items():
        print (k,v)
if __name__ == "__main__":main()