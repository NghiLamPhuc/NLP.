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

def read_dictionary(url, fileName):
    dictionary = json.load(open(url + fileName, encoding = 'utf-8'))
    return dictionary

def write_for_display_out_file(lst, fileName, url):
    file = url + fileName
    with open(file, 'w', encoding = 'utf-8') as fout:
        pprint.pprint(lst, fout)

def write_dict(dct, fileName, url):
    with open(url + fileName,'w', encoding = 'utf-8') as outfile:
        outfile.write(json.dumps(dct, ensure_ascii = False))

def write_Listline_File(List, filename, url):
    f = open(url + filename, 'w', encoding = 'utf8')
    for t in List:
        f.write("%s\n" % t)
    f.close()

def write_dict_two_type(dictionary, fileName, url):
    write_for_display_out_file(dictionary, 'display ' + fileName, url)
    write_dict(dictionary, fileName, url)

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
    listUniqueTags = list()
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
        listUniqueTags.append(tag)
        for _, i in nextTag.items():
            countTagTag += i
    for tag, count in listTagCount.items():
        countTag += count
    listUniqueTags.append('P_s')
    write_Listline_File(listUniqueTags, 'unique_tag.txt', link_out_file)
    write_dict_two_type(listTagWord, 'list_Tag_Word.txt', link_out_file)
    write_dict_two_type(listTagTag, 'list_Tag_Tag.txt', link_out_file)
    write_dict(listTagCount, 'list_Tag_Count.txt', link_out_file)
#    self check count
    print ('tag_word: %d' % countTagWord)
    print ('tag_tag: %d' % countTagTag)
    print ('tag_count %d' % countTag)
    return listTagWord, listTagTag, listUniqueTags

def step_one():
    trainFile = read_train_file('train_da2.pos')
    listSentences = convert_string_file_to_sentences(trainFile)
    listTokenziedSentences = convert_list_sentences_to_list_tokenized_sentences(listSentences)
    tagWord, tagTag, uniqueTags = get_some_from_list_tokens(listTokenziedSentences)

#  + P(T|W)= P(W|T)P(T) / P(W) ma W khong doi, can tim max( P(W|T)P(T) )
#  + P(T) = P(t1.t2.t3....tn) = P(t1)P(t2|t1)...P(t n|t n-1) = ...(count(tn-1|tn) + alpha ) / count(tn-1) + v.alpha...
#  + P(W|T) = P(w1.w2...wn | t1...tn) = P(w1|T)P(w2|T)... voi w1,w2 độc lập theo điều kiện T
#           = P(w i  | T) = P(w i | t1...tn) ~ P(wi|t1) voi gia su: ti chỉ tac dong len wi
#           = count(ti|wi) / count(ti)

def transition_probability(nameListTagTag, nameListTagCount):
    listTagTag = read_dictionary(link_out_file, nameListTagTag)
    listTagCount = read_dictionary(link_out_file, nameListTagCount)
    alpha = 1
    totalTags = len(listTagCount)
#    add value for null item, using division equation.
    for tag, _ in listTagCount.items():
        if tag != 'P_s':
            for nextTag, _ in listTagCount.items():
                if nextTag not in listTagTag[tag]:
                    listTagTag[tag][nextTag] = 0
    for tag, count in listTagCount.items():
        if tag != 'P_s':
            for nextTag in listTagTag[tag]:
                listTagTag[tag][nextTag] = round((listTagTag[tag][nextTag] + alpha) / (count + totalTags), 6)
    write_dict_two_type(listTagTag, 'transition_probability.txt', link_out_file)
#    check total probability = 1 or not.
    check = 0
    checkProb = dict()
    for tag, nextTag in listTagTag.items():
        for _, count in nextTag.items():
            check += count
        checkProb[tag] = check
        check = 0
    write_dict(checkProb, 'Check_TagTag_Probability.txt', link_out_file)    
    return listTagTag

def emission_probability(nameListTagWord, nameListTagCount):
    listTagWord = read_dictionary(link_out_file, nameListTagWord)
    listTagCount = read_dictionary(link_out_file, nameListTagCount)
    for tag, wordCount in listTagWord.items():
        for word, count in wordCount.items():
            listTagWord[tag][word] = round(count / listTagCount[tag], 6)
    write_dict_two_type(listTagWord, 'emission_probability.txt', link_out_file)
    check = 0
    checkProb = dict()
    for tag, wordCount in listTagWord.items():
        for _, count in wordCount.items():
            check += count
        checkProb[tag] = check
        check = 0
    write_dict(checkProb, 'Check_TagWord_Probability.txt', link_out_file)    
    return listTagWord

def step_two():
    return 0

def main():
#    step_one()
#    transition_probability('list_Tag_Tag.txt', 'list_Tag_Count.txt')
    emission_probability('list_Tag_Word.txt', 'list_Tag_Count.txt')
    
    
    
if __name__ == "__main__":main()