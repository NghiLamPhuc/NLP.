from collections import defaultdict
import pprint
import json
import os
cwd = os.getcwd()


link_folder_train = cwd
link_out_file = link_folder_train + '\\outfile\\'
link_train_file = link_folder_train + '\\trainfile\\'
link_result_file = link_folder_train + '\\model\\'

def display_out_file(lst,filename):
    file = link_out_file + filename
    with open(file, 'w', encoding='utf-8') as fout:
        pprint.pprint(lst,fout)
        
def main():
    uniquetags = list()
#    list_word_tag = defaultdict(dict)   #tan so xuat hien word->tag
    list_tag_word = defaultdict(dict)   #tan so xuat hien tag->word
    list_tag_tag = defaultdict(dict)    #tan so xuat hien tag->tag
    tagCount = dict()
    
    uniquetags.append('s0')
    
    with open(link_train_file+'train_da2.pos','r',encoding='utf-8') as inputfile:
        for line1 in inputfile:
            currentTag = 's0'
            prevTag = ''
            if 's0' not in tagCount:
                tagCount['s0'] = 1
            else:
                tagCount['s0'] += 1
                
            line = line1.lower() #-------------------------------------------------------luu y
            lst_word_tag = line.split()
#            print (lst_word_tag)
            for word_tag in lst_word_tag:
                t = 0
                for count in word_tag:
                    if count != '/':
                        t = t + 1
                    else:break    
                    
                    word = word_tag[:t]
                    tag = word_tag[t+1:]
                    
#                print (tag)
#                print (word)
                
				#count word_to_tag[word][tag]
                #list_word_tag add value
#                if word not in list_word_tag:     
#                    list_word_tag[word][tag] = 1
#                elif tag in list_word_tag[word]:
#                    list_word_tag[word][tag] += 1
#                else:
#                    list_word_tag[word][tag] = 1
                    
                if tag not in list_tag_word:     
                    list_tag_word[tag][word] = 1
                elif word in list_tag_word[tag]:
                    list_tag_word[tag][word] += 1
                else:
                    list_tag_word[tag][word] = 1
                
                #tan so tag transittion
                prevTag = currentTag
                currentTag = tag
                
				#Count tag_to_tag[prev][cur]
                if prevTag not in list_tag_tag:
                    list_tag_tag[prevTag][currentTag] = 1
                elif currentTag in list_tag_tag[prevTag]:
                    list_tag_tag[prevTag][currentTag] += 1
                else:
                    list_tag_tag[prevTag][currentTag] = 1
                    
#                print (list_tag_tag)
                
                #Update tags counter   
                if tag not in tagCount:
                    tagCount[tag] = 1
                else:
                    tagCount[tag] += 1
                
                #add to uniquetags list
                if tag not in uniquetags:       
                    uniquetags.append(tag)
#            del list_tag_tag['s0']
            
        with open(link_out_file+'uniquetags.txt','w',encoding='utf8') as outfile:
            json.dump(uniquetags,outfile)
        display_out_file(list_tag_word,'list_tag_word.txt')
        display_out_file(list_tag_tag,'list_tag_tag.txt')
        with open(link_out_file+'tagCount.txt','w',encoding='utf8') as outfile:
            json.dump(tagCount,outfile)
        
    ####### Transition Probability ####### P(T)
    
#  + P(T|W)= P(W|T)P(T) / P(W) ma W khong doi, can tim max( P(W|T)P(T) )
#  + P(T) = P(t1.t2.t3....tn) = P(t1)P(t2|t1)...P(t n|t n-1) = ...(count(tn-1|tn) + alpha ) / count(tn-1) + v.alpha...
#  + P(W|T) = P(w1.w2...wn | t1...tn) = P(w1|T)P(w2|T)... voi w1,w2 độc lập theo điều kiện T
#           = P(w i  | T) = P(w i | t1...tn) ~ P(wi|t1) voi gia su: ti chỉ tac dong len wi
#           = count(ti|wi) / count(ti)
    
    totalTags = len(uniquetags)-1 #la so v trong smoothing, chon alpha la 1
    
    for eachTag in uniquetags:
        for thisTag in uniquetags:
            if thisTag not in list_tag_tag[eachTag]:
                list_tag_tag[eachTag][thisTag] = 0
#                print (eachTag+' '+thisTag+'\n')
#                print (list_tag_tag[eachTag][thisTag])
    
    for eachTag in uniquetags:
        for transitionTag in list_tag_tag[eachTag]:
            list_tag_tag[eachTag][transitionTag] = round((list_tag_tag[eachTag][transitionTag] + 1) / (tagCount[eachTag] + totalTags),6)
#    print (list_tag_tag['m']['s0'])
    
    ######## Emission Probability ####### P(W|T) = ount(t | w)/ount(t)
    
#    for eachWord in list_word_tag:
#        for innerTag in list_word_tag[eachWord]:
#            list_word_tag[eachWord][innerTag] = round(list_word_tag[eachWord][innerTag] / tagCount[innerTag],6)
    check = dict()
    for eachTag in list_tag_word:
        for innerWord in list_tag_word[eachTag]:
            list_tag_word[eachTag][innerWord] = round(list_tag_word[eachTag][innerWord] / tagCount[eachTag],6)
    for tag,word in list_tag_word.items():
        c_heck = 0
        for wOrd,count in list_tag_word[tag].items():
            c_heck += count
        check[tag] = c_heck
    fIle = open(link_folder_train+'check_probability.txt','w',encoding='utf-8')
    for key,value in check.items():
        fIle.write('%s:%s\n' % (key, value))
        
        
    HMMmodel = {}
    HMMmodel['Transition Probability'] = list_tag_tag
    HMMmodel['Emission Probability'] = list_tag_word
    
    with open(link_result_file + 'model.txt', 'w',encoding='utf8') as outfile:
        json.dump(HMMmodel, outfile, ensure_ascii=False)

    with open(link_result_file + 'display_model.txt', 'w',encoding='utf8') as outfile:
        outfile.write('Transition Probability:\n')
        for key,value in HMMmodel['Transition Probability'].items():
            outfile.write('%s:%s\n' % (key, value))
        outfile.write('\nEmission Probability:\n')    
        for key,value in HMMmodel['Emission Probability'].items():
            outfile.write('%s:%s\n' % (key, value))

if __name__ == "__main__":main()