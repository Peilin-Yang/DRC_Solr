#!/usr/bin/python


import re
f = open("COAST_NATURAL_ANONYMOUS.xml","r")
mystring = f.read()

fout = open("COAST_NATURAL_ANONYMOUS_new.xml","w")

counter=0
oldstr=""
newstr=""

for item in mystring.split("\n"):
    fout.write(item+"\n")
    if ("<field name=\"Date_of_Publication\">" in item) or ("<field name=\"Date_of_Copyright\">" in item) :
        data_sentence = item.strip()
        if (counter%2==0):
            oldstr = data_sentence.partition('>')[2].partition('<')[0]
           # print oldstr
        else:
            newstr = data_sentence.partition('>')[2].partition('<')[0]
            #print oldstr + " " + newstr
        counter=counter+1
    #print counter
    if ("<field name=\"Workform\">" in item):
        fout.write("    <field name=\"Date_combination\">"+oldstr + "    " + newstr + "</field>" +"\n")


fout.close()
f.close()
