from collections import defaultdict
import json
import os

#current folder this file

cwd = os.getcwd()

#get back folder of cwd 

chdir = os.path.normpath(cwd + os.sep + os.pardir)

#go to folder readwrite

os.chdir(chdir + '\\readwrite\\')
from readwrite import read_train_file, read_dictionary, write_dict \
    , write_dict_two_type, write_Listline_File
from create_Folder import createFolder

#back to folder this file

os.chdir(cwd)

LINK_INPUT_FILE = cwd + '\\input\\'
LINK_OUT_FILE = cwd + '\\outfile\\'
LINK_OUTPUT = cwd + '\\output\\'
LINK_MODEL = chdir + '\\train\\outfile\\'

def get_model(url, nameTransition, nameEmission):
    transition = read_dictionary(url, nameTransition)
    emission = read_dictionary(url, nameEmission)
    possibleTags = transition.keys()
    return transition, emission, possibleTags
    
    
def calculate_prob_start_to_first_word(wordFirst ,transition, emission, possibleTags):
    probabilities = defaultdict(dict)
    backTag = defaultdict(dict)
    
#    word is in training file.
  
    for tag in possibleTags:
        if tag != 'ps':
            if wordFirst in emission[tag]:
                probabilities[tag][0] = emission[tag][wordFirst] * transition['ps'][tag]
                
#    word is not in training file => new word.

            else:
                probabilities[tag][0] = transition['ps'][tag]
            backTag[tag][0] = 'ps'
    
    return probabilities, backTag

def calculate_prob_second_word_to_end(listWords, transition, emission, possibleTags, probabilities, backTag):
    
#    word is in training file.
    
    for i in range(1, len(listWords) - 1):
        max = -1
        probability = 1
        word = listWords[i + 1]
        backOfTag = ''
        for tag in possibleTags:
            if tag != 'ps':
                if word in emission[tag]:
                    for prevTag in possibleTags:
                        if prevTag != 'p_s':
                            probability = emission[tag][word] * transition[prevTag][tag] * probabilities[tag][i - 1]
                            if probability > max:
                                probability, max = max, probability
                                backOfTag = prevTag
#                            elif probability == max
                else:
                    for prevTag in possibleTags:
                        if prevTag != 'p_s':
                            probability = transition[prevTag][tag] * probabilities[tag][i - 1]
#                            probability = transition[prevTag][tag]
                            if probability > max:
                                probability, max = max, probability
                                backOfTag = prevTag
            
            probabilities[tag][i] = max
            backTag[tag][i] = backOfTag

    return probabilities, backTag

def get_best_list_tags(probabilities, backTag):
    max = -1
    target = 'error'
    lenWords = 0
    strListTags = list()
    for (tag, position) in probabilities.items():
        lenWords = len(position)
        for (pos, prob) in position.items():
            if pos == (lenWords - 1):
                if prob > max:
                    max, prob = prob, max
                    target = tag
    strListTags.append(target)
    for i in range(lenWords - 1, 0, -1):
        strListTags.append(backTag[target][i])
    strListTags.reverse()
    return strListTags
    

def main():
    (transition, emission, possibleTags) = \
        get_model(LINK_MODEL, 'transition_probability.txt', 'emission_probability.txt')
    
#    inputSentence = 'start Không ít học_viên đã phải bỏ_cuộc trong giai_đoạn này vì không_thể lết đi nổi với hai ống_quyển sưng_vù , thậm_chí nứt xương . end'
    inputSentence = 'start Những học_sinh nội_trú bắt_đầu một ngày làm_việc rất vất_vả . end'
#    inputSentence = 'start Em muốn trở_thành một võ_sĩ chuyên_nghiệp , nhưng giấc mơ xa hơn của em là được vào đại_học ” . end'
    inputSentence = inputSentence.lower()
    inputSentence = inputSentence.split()
    
    (probabilities, backTags) = calculate_prob_start_to_first_word(inputSentence[1], \
                                transition, emission, possibleTags)
    
    (a, b) = calculate_prob_second_word_to_end(inputSentence, transition, emission,\
                possibleTags, probabilities, backTags)
    
    
    write_dict_two_type(probabilities, LINK_OUT_FILE, 'prob.txt')
    write_dict_two_type(backTags, LINK_OUT_FILE, 'back.txt')
    print (get_best_list_tags(a, b))
#   kiem tra key của từ 
    
#    for key, value in emission.items():
#        for k, v in value.items():
#            if k == 'không':
#                print (key)
                
if __name__ == "__main__": main()
