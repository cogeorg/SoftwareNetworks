#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os
import codecs
import datetime

# ###########################################################################
# METHODS
# ###########################################################################

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(base_directory, input_file_name, output_file_name, repo):

    out_text = "Project ID;Project Name;Version Number;Dependency Project ID;Dependency Requirements\n"
    out_file = open(base_directory + output_file_name, 'w')
    out_file.write(out_text)
    out_file.close() # ensure file is empty
    out_file = open(base_directory + output_file_name, 'a')

    print("<<<<<< WORKING ON: " + base_directory + input_file_name)
    _count = 0
    _found = 0
    _error = 0

    with open(base_directory + input_file_name, encoding="utf-8", errors='replace') as infile:
        for line in infile:
            _count += 1
            if _count % 1000000 == 0:
                print("    << " + str(datetime.datetime.now()) + "  " + str(_count))
            tokens = line.strip().split(",")
            if tokens[1] == repo or tokens[1] == repo.upper() or tokens[1] == repo.lower():
                try:
                    out_file.write(tokens[3] + ";" + tokens[2] + ";" + tokens[4] + ";" + tokens[11] + ";" + tokens[10] + "\n")
                    _found += 1
                except UnicodeEncodeError:  # very rare, but possible
                    print("      << UNICODE ERROR LINE: " + str(_count))
                    _error += 1

    # add output
    out_text += "\n"
    out_file.write(out_text)
    out_file.close()
    print("    >>> FOUND: " + str(_found) + " OF TOTAL: " + str(_count) + " ENTRIES WITH: " + str(_error) + " ERRORS.")
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
    repo = args[4]

#
# CODE
#
    do_run(base_directory, input_file_name, output_file_name, repo)
