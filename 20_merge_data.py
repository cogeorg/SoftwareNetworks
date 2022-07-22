#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os

import pandas as pd

# ###########################################################################
# METHODS
# ###########################################################################

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(base_directory, input_directory, output_directory, ):
    print("<<<<<< WORKING ON: " + base_directory + input_directory + " WRITING TO: " + base_directory + output_directory)

    versions = pd.read_csv(base_directory + "versions_npm-restricted.csv", delimiter=";")

    for file_name in os.listdir(base_directory + input_directory):
        print("      << MERGING: " + file_name)
        try:
            dependencies = pd.read_csv(base_directory + input_directory + file_name,
                               delimiter=";",
                               names=["Project ID","Project Name","Version Number","Dependency Requirements","Dependency Project ID"],
                               dtype = {
                                "Project ID": int,
                                "Project Name": str,
                                "Version Number": str,
                                "Dependency Requirements": str,
                                "Dependency Project ID": str
                               }
                               )
            merged = pd.merge(dependencies, versions, on=["Project ID", "Version Number"])
            merged.to_csv(base_directory + output_directory + file_name)
        except:
            print("        << ERROR! " + file_name)

    print("    >>> FILES WRITTEN TO:" + base_directory + output_directory)
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
    input_directory = args[2]
    output_directory = args[3]


#
# CODE
#
    do_run(base_directory, input_directory, output_directory)
