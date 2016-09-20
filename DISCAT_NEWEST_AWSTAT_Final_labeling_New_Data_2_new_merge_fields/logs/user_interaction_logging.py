#!/usr/bin/python

import re
from datetime import datetime

# example date format  '24/Jun/2015:19:09:31'

def __datetime(date_str):
    return datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S')

f = open("request.2015_06_24.log","r")
mystring = f.read()

fout = open("user_interaction_data.log","w")

counter = 0
query_term = ""
query_term_old = ""
accessing_time_no_timezone = ""
last_accessing_time = ""
for item in mystring.split("\n"):
#extract user ip address, initial accessing time and query terms
    if ("GET /solr/collection1/browse?q=" in item) :
        #tt = item.strip()
        # example log info:  
        # 128.4.13.197 -  -  [24/Jun/2015:12:33:58 -0700] "GET /solr/collection1/browse?q=+K.+Tsuchiya HTTP/1.1" 200 7398
#        print item
        # get the ip info
        ip_address = item.partition(' ')[0]
        accessing_time_with_timezone = item.partition('[')[2].partition(']')[0]
        accessing_time_no_timezone = accessing_time_with_timezone.partition(' ')[0]
        query_term = item.partition('"')[2].partition('"')[0]
        # delete "GET /solr/collection1/browse?q="
        oldstr = "GET /solr/collection1/browse?q="
        query_term = query_term.replace(oldstr, "")
        # delete  HTTP/1.1
        query_term = query_term.partition(' ')[0]
        # addtional check for admin click
        # e.g. hello+wolrd&pt=none&d=&sfield=store&fq=&queryOpts=spatial&queryOpts=spatial
        spatial=re.search('queryOpts=spatial', query_term);
        if spatial:
            query_term = query_term.partition('&pt')[0] 
        # replace + with space
        query_term = query_term.replace("+", " ")
       # print " %s      %s      %s " % (ip_address, accessing_time_no_timezone, query_term) 
        
#--------------------------------------------------------------------------------------#
######## to do: finish the duration time calculation ( the logic below is not correct )
    # accessing duration time
    if counter is not 0 and query_term_old is not query_term and last_accessing_time is not "":
        start = __datetime(accessing_time_no_timezone)
        end = __datetime(last_accessing_time)
        delta = end - start
    #print delta  # prints: 1 day, 7:50:05
        tt = delta.total_seconds()
        print " last_accessing_time %s " % tt# prints: 114605.0 

    query_term_old = query_term
   # print "hahaha %s" % query_term_old
#----------------------------------------------------------------------------------#
        # collect which link user clicked
        # e.g. 128.4.13.197 -  -  [24/Jun/2015:19:10:36 +0000] "GET /solr/collection1/browse?&q=Id:36583+%20K.%20Tsuchiya&mlt=true HTTP/1.1" 200 9958
    if ("&mlt=true" in item):
#        print query_term
        linkID = item.partition('&q=')[2].partition('&mlt')[0]
        # delete %20 and + 
#        link = link.replace("+", " ");
#        link = link.replace("%20", " ");
        # get the document ID 
        linkID = linkID.partition('+')[0]
        last_accessing_time = item.partition('[')[2].partition(']')[0]
        last_accessing_time = last_accessing_time.partition(' ')[0]       
    #    print " %s      %s " % (query_term, linkID) 
    #    print last_accessing_time

#------------------------------------------------------------------------------------#
        # collect relevant info
    if ("&relevent=" in item):
        relevant = item.partition('&relevent=')[2].partition(' ')[0]
    #    print " %s      %s    relevant: %s " % (query_term, linkID, relevant)
        last_accessing_time = item.partition('[')[2].partition(']')[0]
        last_accessing_time = last_accessing_time.partition(' ')[0] 
     #   print last_accessing_time 
    counter += 1


