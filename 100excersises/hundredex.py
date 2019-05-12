import re

fStr = "stressed stressed stressed"
fStr2 = "fresh fresh"
sentence = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."

def reverse_String(inStr): return inStr[::-1]

def create_even_position_string(inStr):
    newStr = ""
    for i in range(len(inStr)-1):
        if i%2==0:
            newStr += inStr[i+1]
    return newStr

def concat(inStr1,inStr2): return inStr1+inStr2

def tokenize(inSentence):
    listTokens = list()
    inSentence = re.sub("(?=[,.])(?<=\w)"," ",inSentence)
    listTokens.append(inSentence.split(" "))
    return listTokens

def count_alphabet_character(inSentence):
    listCount = list()
    count = 0
    for char in inSentence:
        if char.isalpha():
            count = count + 1
        if char == " ":
            listCount.append(count)
            count = 0
    return listCount
    
print ()