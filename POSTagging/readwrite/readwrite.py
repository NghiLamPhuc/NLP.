import json
import pprint

def read_train_file(url, fileName):
    f = open(url + fileName, 'r', encoding = 'utf-8')
    file = f.read()
    f.close()
    return file

def read_dictionary(url, fileName):
    dictionary = json.load(open(url + fileName, encoding = 'utf-8'))
    return dictionary

def write_for_display_out_file(lst, url, fileName):
    file = url + fileName
    with open(file, 'w', encoding = 'utf-8') as fout:
        pprint.pprint(lst, fout)

def write_dict(dct, url, fileName):
    with open(url + fileName,'w', encoding = 'utf-8') as outfile:
        outfile.write(json.dumps(dct, ensure_ascii = False))

def write_Listline_File(List, url, filename):
    f = open(url + filename, 'w', encoding = 'utf8')
    for t in List:
        f.write("%s\n" % t)
    f.close()

def write_dict_two_type(dictionary, url, fileName):
    write_for_display_out_file(dictionary, url, 'display ' + fileName)
    write_dict(dictionary, url, fileName)
