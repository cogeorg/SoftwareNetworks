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
        token = token.replace(" commits", "")
        token = token.replace("1 commit", "1")
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


# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(base_directory, input_file_name, output_file_name):
    _errors = 0
    _count = 0

    out_text = "contributor_commits;contributor_github_url;contributor_name;name_project"
    out_text += "\n"

    print("<<<<<< WORKING ON: " + base_directory + input_file_name)

    with open(base_directory + input_file_name, encoding="utf-8", errors='replace') as infile:
        for line in infile:
            _count += 1
            tokens = line.strip().split(";")
            if len(tokens) == 4:  # some entries have a ";" in the github url
                try:
                    contributor_commits = ensure_int(tokens[0].strip())
                    contributor_github_url = tokens[1].strip()
                    contributor_name = tokens[2].strip()
                    name_project = tokens[3].strip()
                    if contributor_commits != "":  # some packages have no data
                        out_text += str(contributor_commits) + ";" + contributor_github_url + ";" + contributor_name + ";" + name_project + "\n"

                # for heading and other mistakes
                except:
                    _errors += 1 
                    # print(line)
            else:
                _errors += 1 
                if False:
                    print(len(tokens), tokens)

    # add output
    fname = base_directory + output_file_name
    with open(fname, "w", encoding="utf-8") as f:
        f.write(out_text)
    f.close()

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
