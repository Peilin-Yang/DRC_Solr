"""
load data from the server
"""

import os
import json
import sys
import re
import argparse
import subprocess
import codecs

def main():
    # parser = argparse.ArgumentParser(description=__doc__)
    # parser.add_argument("")
    # args=parser.parse_args()
    cmd = "git rev-parse --show-toplevel"
    process = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)

    REMOTE_ROOT = "/infolab/infolab5/ypeilin/Installation/htdocs/DRC_Project/solr-4.10.0/"
    root_dir = process.communicate()[0].rstrip()
        
    data_dir = [
        "DISCAT_NEWEST_AWSTAT_Final_labeling_New_Data_2_new_merge_fields/solr/collection1/data",
        "DISCAT_NEWEST_AWSTAT_Final_labeling_New_Data_2_new_merge_fields/solr/news/data",
        "DISCAT_NEWEST_AWSTAT_Final_labeling_New_Data_2_new_merge_fields/logs"
    ]
    
    for name in data_dir:
        source_dir = os.path.join(REMOTE_ROOT,name)
        dest_dir = os.path.join(root_dir,name)
        cmd = "rsync -azv infolab:%s %s"\
                %(source_dir,dest_dir)

        os.system(cmd)
        #print cmd


    

if __name__=="__main__":
    main()

