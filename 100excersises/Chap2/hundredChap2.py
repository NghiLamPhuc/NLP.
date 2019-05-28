import os
cwd = os.getcwd()
#current working dir
def read_File_Stringtype(url,filename):
    f = open(url + filename,'r',encoding='utf8')
    input_file = f.read()
    f.close()
    return input_file

def write_Listline_File(List, filename, url):
    f = open(filename,'w',encoding='utf8')
    for t in List:
        f.write("%s\n" % t)
    f.close()

f = read_File_Stringtype(cwd,"\\hightemp.txt")
#print (f)

#10
def count_Line(f):
    count = 0
    for i in range(len(f)):
        if f[i] == "\n":
            count += 1
    return f
#wc -l hightemp.txt
#11
def tab_To_Space(f): return f.replace("\t"," ")
#sed -e "s/\t/ /g" hightemp.txt
#12
def get_col_in_txt_file(strFile):
    col1 = list()
    col2 = list()
    file = strFile.split('\n')
    del file[-1]
    for line in file:
        lineSpt = line.split()
        col1.append(lineSpt[0])
        col2.append(lineSpt[1])
    return col1,col2

#a,b = get_col_in_txt_file(f)
#write_Listline_File(a,'col1.txt',cwd+'\\Chap2')
#write_Listline_File(b,'col2.txt',cwd+'\\Chap2')

#13
def combine_col():
    combineCols = list()
    combineStr = ""
    col1 = read_File_Stringtype(cwd,"\\col1.txt")
    col2 = read_File_Stringtype(cwd,"\\col2.txt")
    col1Splited = col1.split()
    col2Splited = col2.split()
    for i in range(len(col1Splited)):
        combineStr = col1Splited[i] + "\t" + col2Splited[i]
        combineCols.append(combineStr)
    return combineCols

a = combine_col()
write_Listline_File(a,"Combine col1 col2.txt",cwd+'\\Chap2')


