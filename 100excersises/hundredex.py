import re

fStr = "stressed stressed stressed"
fStr2 = "fresh fresh"
fStr3 = "MPyaktQrBoilk RCSahr"
sentence = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
sentence2 = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
#1
def reverse_string(inStr): return inStr[::-1]
#2
def create_even_position_string(inStr):
    newStr = ""
    for i in range(len(inStr)-1):
        if i%2==0:
            newStr += inStr[i+1]
    return newStr
#3
def concat(inStr1,inStr2): return inStr1+inStr2
#4
def tokenize(inSentence):
    tokens = re.sub("(?=[,.])(?<=\w)"," ",inSentence).split(" ")
#                 tra ve string                           tra ve list 
    return tokens

def count_alphabet(listToken):
    return map(lambda n:len(n),listToken)
    
#def func_map(listChar):
    

def get_char_requier(listToken):
    listChar = list()
    a = list(range(20))
    b = [1,5,6,7,8,9,15,16,19]
    c = list(set(a)-set(b))
    listToken = remove_nonAlphabet_token(listToken)
    for i in a:
        if i in b:
            listChar.append(get_char_from_word(listToken[i],0,1))
        if i in c:
            listChar.append(get_char_from_word(listToken[i],0,2))
#    listMap = map(lambda l: l+"->")
    return listChar

def get_char_from_word(inWord,begin,end):
    return inWord[begin:end]

def remove_nonAlphabet_token(listToken):
    for i in listToken:
        if any(char.isalpha() for char in i)==False:
            listToken.remove(i)
    return listToken
#5
#   1 ham lay danh sach n-gram.
#   1 ham, vong lap lay n danh sach cua n tokens.
def get_any_gram_from_token(listToken,n):
    if len(listToken)<n: return "Error: n-gram > lenght of String!"
    listNgram=list()
    n_gram = ""
#    Lenght list - n-gram + first position of gram.
    for i in range(len(listToken)+1-n):
        n_gram = listToken[i]
        for j in range(i+1,i+n):
            n_gram += " " + listToken[j]
        listNgram.append(n_gram)
        n_gram = ""
    return listNgram
#get n-gram from String
def get_any_gram_from_string(inString,n):
    listToken = tokenize(inString)
    if len(listToken)<n: return "Error: n-gram > lenght of String!"
    listNgram=list()
    n_gram = ""
#    Lenght list - n-gram + first position of gram.
    for i in range(len(listToken)+1-n):
        n_gram = listToken[i]
        for j in range(i+1,i+n):
            n_gram += " " + listToken[j]
        listNgram.append(n_gram)
        n_gram = ""
    return listNgram
#get ngram character
def get_any_gram_char_from_string(inString,n):
    if len(inString)<n: return "Error: n-gram > lenght of String!"
    listNgram=list()
    n_gram = ""
#    Lenght list - n-gram + first position of gram.
    for i in range(len(inString)+1-n):
        n_gram = inString[i]
        for j in range(i+1,i+n):
            n_gram += " " + inString[j]
        listNgram.append(n_gram)
        n_gram = ""
    return listNgram
#get all n-gram
def get_all_n_gram_from_token(listToken):
    ngram = dict()
    for i in range(1,len(listToken)+1):
        ngram[i]=get_any_gram_from_token(listToken,i)
    return ngram

def get_all_n_gram_from_string(inString):
    ngram = dict()
    listToken = tokenize(inString)
    for i in range(1,len(listToken)+1):
        ngram[i]=get_any_gram_from_token(listToken,i)
    return ngram

def display_all_ngram(dictNgram):
    for key,value in dictNgram.items():
        print ("%s-gram:"%key)
        print (value)
        print ()
#5
print (get_any_gram_from_string("I am an NLPer",2))
print (get_any_gram_char_from_string("I am an NLPer",2))

#6
