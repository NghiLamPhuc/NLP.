import json
import os

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

LINK_INPUT_FILE = cwd + '\\input\\'
LINK_OUT_FILE = cwd + '\\outfile\\'
LINK_OUTPUT = cwd + '\\output\\'

#print (read_dictionary(chdir + '\\train\\outfile\\', 'transition_probability.txt'))
#print (read_dictionary(chdir + '\\train\\outfile\\', 'emission_probability.txt'))
    










def main():
    
    return 0

if __name__ == "__main__": main()
