import json
from collections import defaultdict
import pprint

link_folder = '\\Users\\NghiLam\\Documents\\NLP\\POSTagging\\decode\\'
link_input = link_folder + 'input\\'
link_model = link_folder + 'model\\'
link_output = link_folder + 'output\\'
link_out_file = link_folder + 'outfile\\'

def display_out_file(lst,filename):
    file = link_out_file + filename
    with open(file, 'w', encoding='utf-8') as fout:
        pprint.pprint(lst,fout)

def main():
    
    with open(link_model + 'model.txt',encoding='utf-8') as model_file:    
        HMMmodel = json.load(model_file)
        transitionProb = HMMmodel['Transition Probability'] #Prob(tj | ti)
        emissionProb = HMMmodel['Emission Probability'] #Prob(t | w)
        
        allPossibleTags = transitionProb.keys() #tag
        
    fout = open(link_output + 'output.txt','w',encoding='utf-8')    

    with open(link_input + 'test_da2.input','r',encoding='utf-8') as infile:
        for line1 in infile:
            line = line1.lower() #-----------------------------------------------------------------luu y
            probability = defaultdict(dict)
            backpointer = defaultdict(dict)
            
            words = line.split()    

            T = len(words)
            ##### Start #####
            
            ## Init at t=1 ##
            word = words[0]
            
            ##### seen #####
            if word in emissionProb:
                for eachTag in emissionProb[word]:
                    probability[eachTag][0] = emissionProb[word][eachTag] * transitionProb['s0'][eachTag]
                    backpointer[eachTag][0] = 's0'
            ##### tu moi #####
            else:
                for eachTag in allPossibleTags:
                    if eachTag != 's0':
                        probability[eachTag][0] = transitionProb['s0'][eachTag]
                        backpointer[eachTag][0] = 's0'
                               
            i = 1
            while(i<T):
                word = words[i]
                ### get the tags of previous word 
                if words[i-1] in emissionProb:
                    previousTagsList = emissionProb[words[i-1]].keys()
                else:
                    previousTagsList = allPossibleTags

                ##### seen #####
                if word in emissionProb:
                    for eachTag in emissionProb[word]:
                        maxVal = -1;
                        currentBackPtr = ''
                        for eachPrevTag in previousTagsList:
                            if eachPrevTag != 's0':
                                probabilityVal = probability[eachPrevTag][i-1] * transitionProb[eachPrevTag][eachTag] * emissionProb[word][eachTag]
                                if probabilityVal > maxVal:
                                    maxVal = probabilityVal
                                    currentBackPtr = eachPrevTag
                        
                        probability[eachTag][i] = maxVal
                        backpointer[eachTag][i] = currentBackPtr
                        
                ##### tu moi #####
                else:
                    for eachTag in allPossibleTags:
                        if eachTag != 's0':
                            maxVal = -1;
                            currentBackPtr = '' 
                            for eachPrevTag in previousTagsList:
                                if eachPrevTag != 's0':
                                    probabilityVal = probability[eachPrevTag][i-1] * transitionProb[eachPrevTag][eachTag]
                                    if probabilityVal > maxVal:
                                        maxVal = probabilityVal
                                        currentBackPtr = eachPrevTag
                            
                            probability[eachTag][i] = maxVal
                            backpointer[eachTag][i] = currentBackPtr
                 
                i+=1
            display_out_file(probability,'probability.txt')
            display_out_file(backpointer,'backpointer.txt')
            #####  #####
            posTags = list()
            
            maxProbableVal = -1
            mostProbableState = ''
            for state in allPossibleTags:
                #duyet nguoc len
                # neu prob cua tag voi word[T-1]
                if (i-1) in probability[state] and probability[state][i-1] > maxProbableVal:
                    maxProbableVal = probability[state][i-1]
                    mostProbableState = state

            posTags.append(mostProbableState)
            counter = i-1;
            prevState = mostProbableState

            while(counter > 0):
                prevState = backpointer[prevState][counter]

                counter -= 1
                posTags.append(prevState)
            taggedLine = ''
            tagsLen = len(posTags)
                        
            for word in words:
                taggedLine += word + '/' + posTags[tagsLen-1] + ' '
                tagsLen -= 1
                 
            fout.write(taggedLine.strip() + "\n")
    fout.close()        
        
if __name__ == "__main__":main()