#!/usr/bin/env python3

import os, sys
import re
import csv

cpresult = sys.argv[-3]
workerresult = sys.argv[-2]
csvfile = sys.argv[-1]

tkc = cpresult.split('-cp')[0]

def score_parser(file):

    # Takes cpresult and workerresult as input and returns.
    # Parses the data and returns output in a list format

    with open (file) as data:
        for my_item in data:
            if "Profile Summary" in my_item:
                s = re.sub(r'\033\[(\d|;)+?m', '', my_item)
                output = re.findall(r'\d+', s)
        return output

def total_score():

    # Calculates total score of controlplane and worker nodes

    totalscore = []
    cpscore = score_parser(cpresult)
    workerscore = score_parser(workerresult)
    totalscore = [int(cpscore[i]) + int(workerscore[i]) for i in range(len(cpscore))]
    return totalscore

def write_to_csv(csvfile, tkc):

    # Calculates Pass percentage and writes data to csv file

    f = open(csvfile, 'a')
    writer = csv.writer(f)
    
    result = total_score()
    total = (result[0] + result[1] + result[2])
    pass_per = (result[0]/total)*100
    fail_per = (result[1]/total)*100
    skip_per = (result[2]/total)*100

    headers = ["tkc", "score"]
    data = [tkc, int(pass_per)]
    
    writer.writerow(data)


write_to_csv(csvfile, tkc)
