
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
def do_run(base_directory, input_directory, output_directory, identifier):
    print("<<<<<< WORKING ON: " + base_directory + input_directory + " WITH IDENTIFIER: " + identifier + " WRITING TO: " + base_directory + output_directory)

    versions_file_name = base_directory + identifier + "/versions_" + identifier + ".csv"
    if True:
        print("   << READING VERSIONS: ", versions_file_name)

    versions = pd.read_csv(
                    versions_file_name,
                    skiprows=1,  # ignore header
                    delimiter=";",
                    names=["Project ID", "Version Number", "Published Timestamp"],
                    dtype={
                        "Project ID": int,
                        "Version Number": str,
                        "Published Timestamp": str
                        }
                    )
    if False:
        print(versions.dtypes)

    for file_name in os.listdir(base_directory + input_directory):
        merge_file_name = base_directory + input_directory + file_name
        if True:
            print("      << MERGING WITH: " + merge_file_name)
        try:
            dependencies = pd.read_csv(
                                merge_file_name,
                                skiprows=1,  # ignore header
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
            if False:
                print(dependencies.dtypes)
        except:
            print("        << READ ERROR! " + file_name)

        try:
            merged = pd.merge(dependencies, versions, on=["Project ID", "Version Number"])
            if False:
                print(merged)
            merged.to_csv(base_directory + output_directory + file_name)
        except:
            print("        << MERGE ERROR!", merged)

    print("  >>> FILES WRITTEN TO:" + base_directory + output_directory)
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
    identifier = args[4]


#
# CODE
#
    do_run(base_directory, input_directory, output_directory, identifier)
