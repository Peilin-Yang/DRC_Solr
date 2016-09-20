#!/usr/bin/python


import re
f = open("COAST_NATURAL_ANONYMOUS_new_1.xml","r")
mystring = f.read()

fout = open("COAST_NATURAL_ANONYMOUS_new_2.xml","w")

counter=1
oldstr_1=""
oldstr_2=""
oldstr_3=""
newstr=""

for item in mystring.split("\n"):
    fout.write(item+"\n")
    if ("<field name=\"Title\">" in item) or ("<field name=\"Title_Analytic\">" in item) or ("<field name=\"Title_Monographic\">" in item) or ("<field name=\"Series_Title\">" in item):
        data_sentence = item.strip()
        if (counter%4==1):
            oldstr_1 = data_sentence.partition('>')[2].partition('<')[0]
           # print oldstr
        elif(counter%4==2):
            oldstr_2 = data_sentence.partition('>')[2].partition('<')[0]
        elif(counter%4==3):
            oldstr_3 = data_sentence.partition('>')[2].partition('<')[0]
        else:
            newstr = oldstr_1 + "    " + oldstr_2 + "    " + oldstr_3 + "    " + data_sentence.partition('>')[2].partition('<')[0] 
        counter=counter+1
        #print newstr
    #print counter
    if ("<field name=\"Author_combination\">" in item):
        fout.write("    <field name=\"Title_combination\">"+ newstr +"</field>" +"\n")


fout.close()
f.close()