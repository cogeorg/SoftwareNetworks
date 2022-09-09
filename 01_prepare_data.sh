#!/usr/bin/bash
GITDIR=/c/Users/user-pc/git/SoftwareNetworks
BASEDIR=/c/Users/user-pc/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/test1/
BASENAME=test1
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
cd $BASEDIR ; split -l 100000 -d -a 5 $DEPFILE  ; mv x* dependencies/ ; cd dependencies ; for i in `ls` ; do mv $i $i.csv ; done ; cd $GITDIR

# ...then execute in git directory:
./20_merge_data.py \
  $BASEDIR/ \
  dependencies/ \
  dependencies_restricted/ \
  $BASENAME

cd $BASEDIR/dependencies_restricted/ ; \
    rm ../dependencies_$BASENAME-merged.csv 2>/dev/null ; \
    cat *.csv | grep -v "Project ID,Pro" >> ../dependencies_$BASENAME-merged.csv ; \
    cd $GITDIR

./30_create_dependency_graph.py \
  $BASEDIR/ \
  dependencies_$BASENAME-merged.csv \
  dependencies_$BASENAME-merged.gexf \
  versions_$BASENAME-restricted.csv \
  0