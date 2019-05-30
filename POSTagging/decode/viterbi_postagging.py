import json
import os
cwd = os.getcwd()
chdir = os.path.normpath(cwd + os.sep + os.pardir)

LINK_INPUT_FILE = cwd + '\\input\\'
LINK_OUT_FILE = cwd + '\\outfile\\'
LINK_OUTPUT = cwd + '\\output\\'

def read_dictionary(url, fileName):
    dictionary = json.load(open(url + fileName, encoding = 'utf-8'))
    return dictionary

#print (read_dictionary(chdir + '\\train\\outfile\\', 'transition_probability.txt'))
#print (read_dictionary(chdir + '\\train\\outfile\\', 'emission_probability.txt'))
    










def main():
    
    return 0

if __name__ == "__main__": main()
