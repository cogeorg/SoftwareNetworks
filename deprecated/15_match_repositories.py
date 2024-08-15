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

def sanitize(token):
    components = token.split("/")
    if len(components) > 1:
        # token = components[0].replace("@", "") + "-" + components[1]
        token = components[1]
    token = token.replace('"','')
    return token


# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(input_file_name, matching_file_name, output_file_name):
    print("<<<<<< WORKING ON: ", input_file_name, matching_file_name, output_file_name)
    _count = 0
    _found = 0
    _error = 0

    matches = []
    out_text = "from_repo;to_repo\n"
    out_file = open(output_file_name, "w")
    out_file.write(out_text)
    out_file.close()
    out_file = open(output_file_name, "a")

    with open(matching_file_name, encoding="utf-8", errors='replace') as matching_file:
        for match in matching_file:
            matches.append(sanitize(match.strip().split(";")[0]))
    matching_file.close()
    print("    << " + str(datetime.datetime.now()) + "  " + "MATCHES:", len(matches))
    if False:
        for match in matches:
            print(match)

    with open(input_file_name, encoding="utf-8", errors='replace') as input_file:
        for line in input_file:
            _count += 1
            if _count % 1000000 == 0:
                print("    << " + str(datetime.datetime.now()) + "   COUNT: " + str(_count) + " FOUND: " + str(_found))
            tokens = line.strip().split(";")
            try:
                from_token = sanitize(tokens[1])
            except IndexError:
                from_token = ""
            if from_token in matches and tokens[3] in matches:
                _found += 1
                out_file.write(from_token + ";" + tokens[3] + "\n")

    out_file.close()

    print("    >>> FOUND: " + str(_found) + " OF TOTAL: " + str(_count) + " ENTRIES")
    print("    >>> FILE WRITTEN TO:" + output_file_name)
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
    input_file_name = args[1]
    matching_file_name = args[2]
    output_file_name = args[3]

#
# CODE
#
    do_run(input_file_name, matching_file_name, output_file_name)
