from collections import defaultdict
import os
import urllib
#response = urllib.urlopen('https://github.com/NghiLamPhuc/NLP./blob/master/POSTagging/train/trainfile/train_da2.pos')
#urllib.urlretrieve ("https://github.com/NghiLamPhuc/NLP./blob/master/POSTagging/train/trainfile", "train_da2.pos")
# Tao ham download file train ve, create folder cho file train.
#
#current folder this file
cwd = os.getcwd()
#get back folder of cwd 
chdir = os.path.normpath(cwd + os.sep + os.pardir)
#go to folder readwrite
os.chdir(chdir + '\\readwrite\\')
from readwrite import read_train_file, read_dictionary, write_dict, write_dict_two_type, write_Listline_File
from create_Folder import createFolder
#back to folder this file
os.chdir(cwd)

LINK_FOLDER_TRAIN = cwd
LINK_OUT_FILE = LINK_FOLDER_TRAIN + '\\outfile\\'
LINK_TRAIN_FILE = LINK_FOLDER_TRAIN + '\\trainfile\\'
LINK_RESULT_FILE = LINK_FOLDER_TRAIN + '\\model\\'

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
    createFolder('./outfile/')
    write_Listline_File(listUniqueTags, LINK_OUT_FILE, 'unique_tag.txt')
    write_dict_two_type(listTagWord, LINK_OUT_FILE, 'list_Tag_Word.txt')
    write_dict_two_type(listTagTag, LINK_OUT_FILE, 'list_Tag_Tag.txt')
    write_dict(listTagCount, LINK_OUT_FILE, 'list_Tag_Count.txt')
#    self check count
    print ('tag_word: %d' % countTagWord)
    print ('tag_tag: %d' % countTagTag)
    print ('tag_count %d' % countTag)
    return listTagWord, listTagTag, listUniqueTags

def step_one():
    trainFile = read_train_file(LINK_TRAIN_FILE, 'train_da2.pos')
    listSentences = convert_string_file_to_sentences(trainFile)
    listTokenziedSentences = convert_list_sentences_to_list_tokenized_sentences(listSentences)
    tagWord, tagTag, uniqueTags = get_some_from_list_tokens(listTokenziedSentences)

#  + P(T|W)= P(W|T)P(T) / P(W) ma W khong doi, can tim max( P(W|T)P(T) )
#  + P(T) = P(t1.t2.t3....tn) = P(t1)P(t2|t1)...P(t n|t n-1) = ...(count(tn-1|tn) + alpha ) / count(tn-1) + v.alpha...
#  + P(W|T) = P(w1.w2...wn | t1...tn) = P(w1|T)P(w2|T)... voi w1,w2 độc lập theo điều kiện T
#           = P(w i  | T) = P(w i | t1...tn) ~ P(wi|t1) voi gia su: ti chỉ tac dong len wi
#           = count(ti|wi) / count(ti)

def transition_probability(nameListTagTag, nameListTagCount):
    listTagTag = read_dictionary(LINK_OUT_FILE, nameListTagTag)
    listTagCount = read_dictionary(LINK_OUT_FILE, nameListTagCount)
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
    write_dict_two_type(listTagTag, LINK_OUT_FILE, 'transition_probability.txt')
#    check total probability = 1 or not.
    check = 0
    checkProb = dict()
    for tag, nextTag in listTagTag.items():
        for _, count in nextTag.items():
            check += count
        checkProb[tag] = check
        check = 0
    write_dict(checkProb, LINK_OUT_FILE, 'Check_TagTag_Probability.txt')    
    return listTagTag

def emission_probability(nameListTagWord, nameListTagCount):
    listTagWord = read_dictionary(LINK_OUT_FILE, nameListTagWord)
    listTagCount = read_dictionary(LINK_OUT_FILE, nameListTagCount)
    for tag, wordCount in listTagWord.items():
        for word, count in wordCount.items():
            listTagWord[tag][word] = round(count / listTagCount[tag], 6)
    write_dict_two_type(listTagWord, LINK_OUT_FILE, 'emission_probability.txt')
    check = 0
    checkProb = dict()
    for tag, wordCount in listTagWord.items():
        for _, count in wordCount.items():
            check += count
        checkProb[tag] = check
        check = 0
    write_dict(checkProb, LINK_OUT_FILE, 'Check_TagWord_Probability.txt')    
    return listTagWord

def step_two():
    return 0

def main():
    step_one()
    transition_probability('list_Tag_Tag.txt', 'list_Tag_Count.txt')
    emission_probability('list_Tag_Word.txt', 'list_Tag_Count.txt')
    
    
    
if __name__ == "__main__":main()