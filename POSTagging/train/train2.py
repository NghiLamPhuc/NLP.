from collections import defaultdict
import pprint
import json
import os
cwd = os.getcwd()

link_folder_train = cwd
link_out_file = link_folder_train + '\\outfile\\'
link_train_file = link_folder_train + '\\trainfile\\'
link_result_file = link_folder_train + '\\model\\'

def read_train_file(fileName):
    f = open(link_train_file + fileName, 'r', encoding = 'utf-8')
    file = f.read()
    f.close()
    return file

def write_for_display_out_file(lst,fileName):
    file = link_out_file + fileName
    with open(file, 'w', encoding = 'utf-8') as fout:
        pprint.pprint(lst,fout)

def write_dict(dct,fileName):
    with open(link_out_file + fileName,'w', encoding = 'utf-8') as outfile:
        outfile.write(json.dumps(dct, ensure_ascii = False))

def convert_string_file_to_sentences(stringFile):
    listSentences = stringFile.split('\n')
    del listSentences[-1]
    return listSentences

def convert_sentence_to_tokens_by_space(sentence):
    return sentence.split()

def convert_list_sentences_to_list_tokened_sentences(listSentences):
    listTokens = list()
    for sentence in listSentences:
        listTokens.append(convert_sentence_to_tokens_by_space(sentence))
    return listTokens
    
def get_dict_tag_word_from_list_tokens(listTokenizedSentences):
    listTagWord = defaultdict(dict)
    for sentence in listTokenizedSentences:
#        for token in sentence:
#            if len(token) > 2:
#                token = token.split('/')
#                word = token[0]
#                tag = token[1]
#                if tag not in listTagWord:
#                    listTagWord[tag][word] = 1
#                elif word not in listTagWord[tag]:
#                    listTagWord[tag][word] = 1
#                else:
#                    listTagWord[tag][word] += 1
        for tokenIndex in range(len(sentence)-1):
            wordTag = sentence[tokenIndex].split('/')
            word = wordTag[0]
            tag = wordTag[1]
            if tag not in listTagWord:
                listTagWord[tag][word] = 1
            elif word not in listTagWord[tag]:
                listTagWord[tag][word] = 1
            else:
                listTagWord[tag][word] += 1
    return listTagWord

def get_dict_tag_tag_from_list_tokens(listTokenizedSentences):
    return 0

def main():
    a = read_train_file('train_da2.pos')
    b = convert_string_file_to_sentences(a)
    c = convert_list_sentences_to_list_tokened_sentences(b)
    d = get_dict_tag_word_from_list_tokens(c)
    write_for_display_out_file(d,'display_tag_word.txt')
    write_dict(d,'tag_word.txt')
    
if __name__ == "__main__":main()