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

def write_for_display_out_file(lst, fileName):
    file = link_out_file + fileName
    with open(file, 'w', encoding = 'utf-8') as fout:
        pprint.pprint(lst, fout)

def write_dict(dct, fileName):
    with open(link_out_file + fileName,'w', encoding = 'utf-8') as outfile:
        outfile.write(json.dumps(dct, ensure_ascii = False))

def write_Listline_File(List, filename, url):
    f = open(url + filename, 'w', encoding = 'utf8')
    for t in List:
        f.write("%s\n" % t)
    f.close()

def write_dict_two_type(dictionary, fileName):
    write_for_display_out_file(dictionary, 'display ' + fileName)
    write_dict(dictionary, fileName)

def convert_string_file_to_sentences(stringFile):
    listSentences = stringFile.split('\n')
    del listSentences[-1]
    print ('sentences: %d' % len(listSentences))
    return listSentences

def convert_list_sentences_to_list_tokenized_sentences(listSentences):
    listTokens = list()
    count = 0
    countWithoutLast = 0
    for sentence in listSentences:
        tokens = sentence.split()
        count += len(tokens)
        countWithoutLast += len(tokens) - 1
        listTokens.append(tokens)
    print ('tokens: %d' % count)
    print ('tokens without last: %d' % countWithoutLast)
    return listTokens
    
def get_some_from_list_tokens(listTokenizedSentences):
    listTagWord = defaultdict(dict)
    listTagTag = defaultdict(dict)
    listUniqeTags = list()
    listTagCount = dict()
    countTagWord = 0
    countTagTag = 0
    countTag = 0    
    for sentence in listTokenizedSentences:
        for tokenIndex in range(len(sentence)):
            wordTag = sentence[tokenIndex].split('/')
            word = wordTag[0]
            tag = wordTag[1]
#            add tag_word
            if tag not in listTagWord:
                listTagWord[tag][word] = 1
            elif word not in listTagWord[tag]:
                listTagWord[tag][word] = 1
            else:
                listTagWord[tag][word] += 1
#            add tag_tag
            if tokenIndex < len(sentence) - 1:
                nextWordTag = sentence[tokenIndex + 1].split('/')
                nextTag = nextWordTag[1]
                if tag not in listTagTag:
                    listTagTag[tag][nextTag] = 1
                elif nextTag not in listTagTag[tag]:
                    listTagTag[tag][nextTag] = 1
                else:
                    listTagTag[tag][nextTag] += 1
#            add tag_count
            if tag not in listTagCount:
                listTagCount[tag] = 1
            else:
                listTagCount[tag] += 1
                
    for _, word in listTagWord.items():
        for _, i in word.items():
            countTagWord += i
    for tag, nextTag in listTagTag.items():
        listUniqeTags.append(tag)
        for _, i in nextTag.items():
            countTagTag += i
    
    for tag, count in listTagCount.items():
        countTag += count
    listUniqeTags.append('P_s')
    write_Listline_File(listUniqeTags, 'uniqe_tag.txt', link_out_file)
    write_dict_two_type(listTagWord, 'list_Tag_Word.txt')
    write_dict_two_type(listTagTag, 'list_Tag_Tag.txt')
    write_for_display_out_file(listTagCount, 'list_Tag_Count.txt')
#    self check count
#    print ('tag_word: %d' % countTagWord)
#    print ('tag_tag: %d' % countTagTag)
    
    print ('tag_count %d' % countTag)
    return listTagWord, listTagTag, listUniqeTags

def step_one():
    trainFile = read_train_file('train_da2.pos')
    listSentences = convert_string_file_to_sentences(trainFile)
    listTokenziedSentences = convert_list_sentences_to_list_tokenized_sentences(listSentences)
    tagWord, tagTag, totalTags = get_some_from_list_tokens(listTokenziedSentences)

def main():
    step_one()
    
    
    
    
    
if __name__ == "__main__":main()