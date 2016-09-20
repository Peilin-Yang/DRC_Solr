#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
f = open("documents_new_underscore_field.xml","r")
mystring = f.read()

fout = open("out.xml","w")
counter=0

# Month conversion dictionary
Mon = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12', 'Jan.': '01', 'Feb.': '02', 'Mar.': '03', 'Apr.': '04', 'Aug.': '08', 'Sept.': '09', 'Oct.': '10', 'Nov.': '11', 'Dec.': '12'}

# first spilt each sentence
# and then find and replace all the year, month and day elements
# only consider this kind of form: 2009 Sept. 10 

for item in mystring.split("\n"):
	if ("<field name=\"Date_of_Publication\">" in item) or ("<field name=\"Date_of_Copyright\">" in item) :
		data_sentence = item.strip()
                #<field name="Date_of_Copyright">2006-12-22</field> find the date string between > and <	
		oldstr = data_sentence.partition('>')[2].partition('<')[0]
                year=day=month=""
                result = re.search("[1-3][0-9][0-9][0-9]", oldstr)
		if result:
	                 year = result.group()
                         #print year
                
                #Date has form like "Sept. 1962" or "1962" 
                year_last_element = 1
                result = re.search("[1-3][0-9][0-9][0-9]$", oldstr)
                if result:
			year_last_element = 0

                # date element has two date: 2005 April 26; 2005 May 3
                # date element has colon or semicolon or hyphen or slash
                # ignore line with punctuation 
		semicolon_in_line = 1
                result1 = re.search(";", oldstr)
                result2 = re.search(":", oldstr)
                result3 = re.search("-", oldstr)
	        result4 = re.search("/", oldstr)
	        result5 = re.search(",", oldstr)
		result6 = re.search("\(", oldstr)
		result7 = re.search("\)", oldstr)
		result8 = re.search("\[", oldstr)
		result9 = re.search("\]", oldstr)
                if result1 or result2 or result3 or result4 or result5 or result6 or result7 or result8 or result9:
			semicolon_in_line = 0


		#{0,1} repeat 0 or 1 time
                result = re.search("[1-9][0-9]{0,1}$", oldstr)
		if result:
	                 day = result.group()
                         # convert day to two digit like 01, ...... ,09

			 # place a 0 in front of numbers in a list if they are less than ten
                         if int(day) < 10:
				newday = "%02d" % int(day)
                                day = str(newday)
                         #print day

                for key in Mon: 
			result = re.search(key, oldstr)
			if result:
				month = Mon[key]
				#print month

		if year and month and day and year_last_element and semicolon_in_line:
			newstr = year+'-'+month+'-'+day
			fout.write("    "+data_sentence.replace(oldstr, newstr)+"\n")
		#elif year and month and not day:
			#newstr = year +'-'+month	
			#fout.write("    "+data_sentence.replace(oldstr, newstr)+"\n")
		else:
			fout.write("    "+data_sentence+"\n") 
	else:
		fout.write(item+"\n")	
		#counter=counter+1

