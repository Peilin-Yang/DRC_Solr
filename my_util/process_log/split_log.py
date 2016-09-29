"""
split query log
"""
import re
import os,sys
import time
import argparse
import urllib,urlparse

COLLECTIONS = ["news", "collection1"]


def get_log_data_for_single_file(log_file,COLLECTIONS,collection_tags):
    log_data = {}

    for collection_name in COLLECTIONS:
        log_data[collection_name] = []

    # seperate query logs for two collections
    with open(log_file) as f:
        for line in f:
            for collection_name in collection_tags:
                if collection_tags[collection_name] in line:
                    log_data[collection_name].append(line)

    return log_data



def split_log(log_dir,dest_dir,COLLECTIONS,multi_file):
    collection_tags = {}
    
    for collection_name in COLLECTIONS:
        collection_tags[collection_name] = "/solr/%s/browse" %(collection_name)

    log_data = { 
        "news":[],
        "collection1":[]
        }

    for single_file in sorted(os.walk(log_dir).next()[2]):
        #whether it is a log file for past days
        #print "file %s" %single_file
        m = re.search("request\.([\d\_]+)\.log",single_file)
        if m:
            log_file = os.path.join(log_dir,single_file)
            day_log = get_log_data_for_single_file(log_file,COLLECTIONS,collection_tags)
            
            if multi_file:
                date = m.group(1)
                            
                # output log
                for collection_name in day_log:
                    # if no meaningful log for the day
                    # ignore the day
                    if day_log[collection_name]:
                        single_dest_file = os.path.join(dest_dir,collection_name,"%s.log"%(date))
                        with open(single_dest_file,"w") as f:
                            for line in day_log[collection_name]:
                                f.write(line)

            else:
                for collection_name in day_log:
                    log_data[collection_name] += day_log[collection_name]

        # else:
        #     print "skip file %s" %single_file

        if not multi_file:
            for collection_name in log_data:
                single_dest_file = os.path.join(dest_dir,collection_name,"all.log")
                with open(single_dest_file,"w") as f:
                    for line in log_data[collection_name]:
                        f.write(line)



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log_dir","-lr",default="/home/lukuang/Desktop/DRC_project/DRC_Solr-1/DISCAT_NEWEST_AWSTAT_Final_labeling_New_Data_2_new_merge_fields/logs")
    parser.add_argument("--dest_dir","-dr",default="/home/lukuang/Desktop/DRC_project/DRC_Solr-1/my_util/process_log/data")
    parser.add_argument("--multi_file","-m",action="store_true")
    #parser.add_argument("--session_threshold","-s",type=int, default=1800)

    args = parser.parse_args()

    split_log(args.log_dir,args.dest_dir,COLLECTIONS,args.multi_file)



if __name__=="__main__":
    main()