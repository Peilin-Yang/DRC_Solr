"""
process query log
"""
import re
import os,sys
import time
import argparse
import urllib,urlparse

# def store_record(record,logs):
#     if len(logs['queries']) != 0:
#         for query in logs['queries']:
#             if query not in record:
#                 record[query] = []
#             record[query] += logs['queries'][query]


def read_log(log_file, duration_time_threshold):
    logs = []
    previous_time = 0

    with open(log_file) as f:
        for line in f:
            m = re.search("^(.+?)\s+-\s+-\s+\[(.+?)\] \"GET (.+?) HTTP",line)
            if m is not None:
                ip,complex_time, url = m.group(1),m.group(2),m.group(3)
                url = urllib.unquote(url)

                #get time of each query
                mt = re.match("^(.+)\s(\+|\-)(\d{2})(\d{2})$", complex_time)
                t = 0
                time_string = ""
                if mt is not None:
                    time_string = mt.group(1)
                    t =  int(time.mktime(time.strptime(mt.group(1),"%d/%b/%Y:%H:%M:%S") ))
                    # offset = int( mt.group(3) )*3600 + int( mt.group(4) )*60
                    # if mt.group(2) == "+":
                    #     offset *= -1
                    # t += offset
                    #print line
                    #print ip,t, q_filed, query_string
                else:
                    print "error time format"
                    print line

                single_data = {
                        "time_string" : time_string,
                        "epoch" : t
                    }

                #get query and possible docid, relevance judgment

                paras = urlparse.parse_qs(urlparse.urlsplit(url).query)
                #print paras
                    
                has_words  = re.compile("\w")
                if "q" in paras:
                    #ignore the query has no words
                    if not has_words.search(paras["q"][0]):
                        continue

                    # deal with the relevance judgment
                    elif("relevent" in paras):
                        url = re.sub("Id:","Id=",url)
                        paras = urlparse.parse_qs(urlparse.urlsplit(url).query)

                        #print "a relevance judgment"
                        judgment = "true"
                        if paras["relevent"][0].lower() == "false":
                            judgment = "false"

                            
                        single_data["query"] = paras["q"][0],
                        single_data["docid"] = paras["Id"][0]
                        single_data["relevant"] = judgment

                    elif "mlt" in paras:
                        #print "a click"
                        mqs = re.search("^(Id:([\w-]+) ?)?(.+)$",paras["q"][0])
                        query_string = mqs.group(3)
                        docid = mqs.group(2)
                        #print "doc id", mqs.group(2)

                        # skip the clicked document without query
                        if not has_words.search(query_string):
                            continue

                        single_data["query"] = query_string
                        single_data["docid"] = docid
                        single_data["clicked"] = "true"

                    else:
                        single_data["query"] =  paras["q"][0]

                    if logs and "clicked" in logs[-1]:
                        dur_time = t - previous_time
                        logs[-1]["duration"] = dur_time

                        if dur_time >= duration_time_threshold:
                            logs[-1]["dur_judge"] = "true"
                        else:
                            logs[-1]["dur_judge"] = "false"

                    previous_time = t
                    #print single_data["query"]
                    logs.append(single_data)


                
                
            else:
                print "error line!"
                print line
            #raw_input("press enter to continue")

    print logs
    # print "catched %d, ignore %d" %(catched,ignore)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log_file","-l",default="/home/lukuang/Desktop/process_solr_logs/logs/all_logs")
    parser.add_argument("--duration_time_threshold","-s",type=int, default=1800)
    parser.add_argument("dest_file")

    args = parser.parse_args()
    read_log(args.log_file,args.duration_time_threshold)



if __name__=="__main__":
    main()