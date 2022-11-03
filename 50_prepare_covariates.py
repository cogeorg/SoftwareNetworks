#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os
import codecs
from datetime import datetime, timedelta

# ###########################################################################
# METHODS
# ###########################################################################

def ensure_int(token):
    if token == "":
        token = 0
    else:
        if "." in token:
            token = token.replace("K", "")
            token = int(float(token) * 1000)
        elif "K" in token:  # 1000 is written as 1K without dot
            token = token.replace("K", "")
            token = int(float(token) * 1000)
        elif "," in token:  # some entries have thousands separator
            token = int(token.replace(",",""))
        else:
            token = int(token)

    return token


def ensure_byte(token):
    if token == "":
        token = 0
    else:
        if "0 Bytes" in token:  # some entries have thousands separator
            token = 0
        elif "KB" in token:
            token = token.replace("KB", "")
            token = int(float(token) * 1024)
        elif "MB" in token:
            token = token.replace("MB", "")
            token = int(float(token) * 1024 * 1024)
        elif "GB" in token:
            token = token.replace("GB", "")
            token = int(float(token) * 1024 * 1024 * 1024)
        else:
            token = int(token)

    return token


def ensure_date(date_str):

    today = datetime.strptime('2022-10-24', '%Y-%m-%d')
    
    if date_str == "":
        date = today
    elif "hours ago" in date_str or "hour ago" in date_str:
        date = today
    elif "a day ago" in date_str:
        date = today - timedelta(days=1)
    elif "days ago" in date_str:
        date_token = date_str.split("days ago")
        date = today - timedelta(days=int(date_token[0]))
    elif "about a month ago" in date_str:
        date = today - timedelta(days=30)
    elif "months ago" in date_str:
        date_token = date_str.split("months ago")
        date = today - timedelta(days=30*int(date_token[0]))
    else:
        date = datetime.strptime(date_str, "%b %d, %Y")

    return date

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(base_directory, input_file_name, output_file_name):
    _errors = 0
    _count = 0

    out_text = "name_project;date_first_release;date_latest_release;num_total_releases;size_repository;num_contributors;num_forks;num_stars;num_watchers;"
    out_text += "\n"

    out_file = open(base_directory + output_file_name, 'w')

    print("<<<<<< WORKING ON: " + base_directory + input_file_name)

    with open(base_directory + input_file_name, encoding="utf-8", errors='replace') as infile:
        for line in infile:
            _count += 1
            tokens = line.strip().split(";")
            if len(tokens) == 11:  # some entries have a ";" in the github url
                try:
                    num_contributors = ensure_int(tokens[0])
                    date_first_release = ensure_date(tokens[1])
                    date_latest_release = ensure_date(tokens[3])
                    num_forks = ensure_int(tokens[2])
                    num_stars = ensure_int(tokens[4])
                    num_watchers = ensure_int(tokens[5])
                    name_project = tokens[8]
                    size_repository = ensure_byte(tokens[9])
                    num_total_releases = ensure_int(tokens[10])
                    
                    if date_first_release != "":  # some packages have no data
                        out_text += name_project + ";" + str(date_first_release)[:10] +";"+ str(date_latest_release)[:10] +";"
                        out_text += str(num_total_releases) +";"+ str(size_repository) +";"+ str(num_contributors) +";"+ str(num_forks) +";"+ str(num_stars) +";"+ str(num_watchers) +";"
                        # out_text += str(num_watchers)
                        out_text += "\n"

                # for heading and other mistakes
                except:
                    # _errors += 1 
                    if "Contributors" not in line:  # exclude heading
                        print(line)
            else:
                _errors += 1 
                if False:
                    print(len(tokens), tokens)

    # add output
    out_text += "\n"
    out_file.write(out_text)
    out_file.close()
    print("       <<< FOUND: " + str(_errors) + " ERRORS IN " + str(_count) + " LINES")
    print("    >>> FILE WRITTEN TO:" + base_directory + output_file_name)
    print(">>>>>> FINISHED")
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
#
#  MAIN
#
# -------------------------------------------------------------------------
if __name__ == '__main__':
#
# VARIABLES
#
    args = sys.argv
    base_directory = args[1]
    input_file_name = args[2]
    output_file_name = args[3]

#
# CODE
#
    do_run(base_directory, input_file_name, output_file_name)
