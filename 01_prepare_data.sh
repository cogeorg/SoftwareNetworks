#!/usr/bin/bash
BASEDIR=/c/Users/user-pc/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/libraries-1.4.0-2018-12-22/
BASENAME=npm
# BASENAME=test1
DEPFILE=dependencies_$BASENAME.csv

# ###########################################################################
#
# TEST RUN
#
# ###########################################################################

#
# STEP 1 -- NOT NECESSARY SINCE INPUT FILES ARE MANUALLY PREPARED
#

#
# STEP 2
#
# execute in data directory...
# cd $BASEDIR ; split -l 100000 -d -a 5 $DEPFILE  ; mv x* dependencies/ ; cd dependencies ; for i in `ls` ; do mv $i $i.csv ; done ; cd ..

# ...then execute in this directory:
# ./20_merge_data.py \
#   $BASEDIR/ \
#   dependencies/ \
#   dependencies_restricted/ \
#   $BASENAME

# cd $BASEDIR/dependencies_restricted/ ; \
#     rm ../dependencies_$BASENAME-merged.csv 2>/dev/null ; \
#     cat *.csv | grep -v "Project ID,Pro" >> ../dependencies_$BASENAME-merged.csv ; \
#     cd -

# ./30_create_dependency_graph.py \
#   $BASEDIR/ \
#   dependencies_$BASENAME-merged.csv \
#   dependencies_$BASENAME-merged.gexf \
#   versions_$BASENAME-restricted.csv


# ###########################################################################
#
# PRODUCTION RUN
#
# ###########################################################################

#
# STEP 1 -- PREPARE ORIGINAL DATA
#
# FIRST:
# Download raw data from: https://zenodo.org/record/2536573/files/Libraries.io-open-data-1.4.0.tar.gz
# THEN:
# ./10_prepare_dependencies.py \
#   $BASEDIR \
#   dependencies-1.4.0-2018-12-22.csv \
#   $DEPFILE

# ./11_prepare_projects.py \
#   $BASEDIR/ \
#   projects-1.4.0-2018-12-22.csv \
#   projects_npm.csv

# ./12_prepare_versions.py \
#   $BASEDIR \
#   versions-1.4.0-2018-12-22.csv \
#   versions_npm-restricted.csv \
#   2011-01-01 \
#   2021-12-31

#
# STEP 2 - CREATE DEPENDENCY GRAPH
#
# execute in data directory...
# cd $BASEDIR/ ; split -l 100000 -d -a 5 $DEPFILE  ; mv x* dependencies/ ; cd dependencies ; for i in `ls` ; do mv $i $i.csv ; done ; cd ..

# ...then execute in this directory:
# ./20_merge_data.py \
#   $BASEDIR/ \
#   dependencies/ \
#   dependencies_restricted/ \
#   $BASENAME

# cd $BASEDIR/dependencies_restricted/ ; \
#     rm ../dependencies_npm-merged.csv 2>/dev/null ; \
#     cat *.csv | grep -v "Project ID,Pro" >> ../dependencies_npm-merged.csv ; \
#     cd -

./30_create_dependency_graph.py \
  $BASEDIR \
  dependencies_npm-merged.csv \
  dependencies_npm-merged \
  versions_npm-restricted.csv \
  1

# ./31_prepare_oslom.py \
#   $BASEDIR \
#   sampled-0.01_dependencies_$BASENAME


#
# STEP 3 - ANALYZE DEPENDENCY GRAPH
# 
# ./80_analyze_graph.py \
#   $BASEDIR \
#   sampled-0.01_dependencies_$BASENAME \
#   analyze_graph
  