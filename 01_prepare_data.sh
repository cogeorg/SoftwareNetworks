#!/usr/bin/env bash

#
# STEP 1 -- PREPARE ORIGINAL DATA
#
# FIRST:
# Download raw data from: https://zenodo.org/record/2536573/files/Libraries.io-open-data-1.4.0.tar.gz
# THEN:
# ./10_prepare_dependencies.py \
#   ~/Downloads/libraries-1.4.0-2018-12-22/ \
#   dependencies-1.4.0-2018-12-22.csv \
#   dependencies_npm.csv

# ./11_prepare_projects.py \
#   ~/Downloads/libraries-1.4.0-2018-12-22/ \
#   projects-1.4.0-2018-12-22.csv \
#   projects_npm.csv

# ./12_prepare_versions.py \
#   ~/Downloads/libraries-1.4.0-2018-12-22/ \
#   versions-1.4.0-2018-12-22.csv \
#   versions_npm-restricted.csv \
#   2010-12-18 \
#   2021-12-31

#
# STEP 2
#
# execute in data directory...
# cd ~/Downloads/libraries-1.4.0-2018-12-22/ ; split -l 100000 -d -a 5 dependencies_npm.csv  ; mv x* dependencies/ ; cd dependencies ; for i in `ls` ; do mv $i $i.csv ; done ; cd ..

# ...then execute in this directory:
# ./20_merge_data.py \
#   ~/Downloads/libraries-1.4.0-2018-12-22/ \
#   dependencies/ \
#   dependencies_restricted/

# cd ~/Downloads/libraries-1.4.0-2018-12-22/dependencies_restricted/ ; rm ../dependencies_npm-merged.csv 2>/dev/null ; cat *.csv | grep -v "Project ID,Pro" >> ../dependencies_npm-merged.csv ; cd ~/git/Bugs/dependency/


./30_create_dependency_graph.py \
  ~/Downloads/libraries-1.4.0-2018-12-22/ \
  dependencies_npm-merged.csv \
  dependencies_npm-merged.gexf \
  versions_npm-restricted.csv
