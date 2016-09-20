#!/usr/bin/python



with open("out2.txt", "wt") as fout:
    with open("out.xml", "rt") as fin:
        for line in fin:
            if "<field name=\"Date_of_Publication\">" in line:
		data_sentence = line.strip()
		dd=data_sentence.partition('>')[2].partition('<')[0]
		fout.write(dd+"\n")


