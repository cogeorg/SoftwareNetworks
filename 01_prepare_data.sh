#!/usr/bin/env bash
GITDIR=~/git/SoftwareNetworks/
BASEDIR=~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/

BASENAME=Cargo
DEPFILE=dependencies_$BASENAME.csv

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
#   libraries-1.4.0-2018-12-22/dependencies-1.4.0-2018-12-22.csv \
#   $BASENAME/$DEPFILE \
#   $BASENAME

# ./11_prepare_projects.py \
#   $BASEDIR/ \
#   libraries-1.4.0-2018-12-22/projects-1.4.0-2018-12-22.csv \
#   $BASENAME/projects_$BASENAME.csv \
#   $BASENAME

# ./12_prepare_versions.py \
#   $BASEDIR \
#   libraries-1.4.0-2018-12-22/versions-1.4.0-2018-12-22.csv \
#   $BASENAME/versions_$BASENAME.csv \
#   2011-01-01 \
#   2021-12-31 \
#   $BASENAME 

#
# STEP 2 - CREATE DEPENDENCY GRAPH
#
# execute in data directory...
# cd $BASEDIR/$BASENAME ; split -l 100000 -d -a 5 $DEPFILE  ; mv x* dependencies/ ; cd dependencies ; for i in `ls` ; do mv $i $i.csv ; done ; cd $GITDIR

# ...then execute in this directory:
# ./20_merge_data.py \
#   $BASEDIR/ \
#   $BASENAME/dependencies/ \
#   $BASENAME/ \
#   $BASENAME

# cd $BASEDIR/$BASENAME ; \
#     rm dependencies_$BASENAME-merged.csv 2>/dev/null ; \
#     cat x*.csv | grep -v "Project ID,Pro" >> dependencies_$BASENAME-merged.csv ; \
#     rm x*.csv
# cd $GITDIR


#
# IDENTIFY COMMUNITIES USING OSLOM
#
# the last argument indicates whether or not a sample is created.
# ./30_create_dependency_graph.py $BASEDIR dependencies_npm-merged.csv dependencies_npm-merged versions_npm-restricted.csv 0.001 
# ./31_prepare_oslom.py \
#   $BASEDIR \
#   sampled-0.001_dependencies_npm
# ./32_create_largest_component.py $BASEDIR enc_sampled-0.001_dependencies_npm-merged

# ./30_create_dependency_graph.py $BASEDIR dependencies_npm-merged.csv dependencies_npm-merged versions_npm-restricted.csv 0.01 
# ./31_prepare_oslom.py \
#   $BASEDIR \
#   sampled-0.01_dependencies_npm
# ./32_create_largest_component.py $BASEDIR enc_sampled-0.01_dependencies_npm-merged

# ./30_create_dependency_graph.py $BASEDIR dependencies_npm-merged.csv dependencies_npm-merged versions_npm-restricted.csv 0.05 
# ./31_prepare_oslom.py \
#   $BASEDIR \
#   sampled-0.05_dependencies_npm
# ./32_create_largest_component.py $BASEDIR enc_sampled-0.05_dependencies_npm-merged

# ./30_create_dependency_graph.py $BASEDIR dependencies_npm-merged.csv dependencies_npm-merged versions_npm-restricted.csv 0.10 
# ./31_prepare_oslom.py \
#   $BASEDIR \
#   sampled-0.1_dependencies_npm
# ./32_create_largest_component.py $BASEDIR enc_sampled-0.1_dependencies_npm-merged

# ./30_create_dependency_graph.py $BASEDIR dependencies_npm-merged.csv dependencies_npm-merged versions_npm-restricted.csv 0.25 
# ./31_prepare_oslom.py \
#   $BASEDIR \
#   sampled-0.25_dependencies_npm
# ./32_create_largest_component.py $BASEDIR enc_sampled-0.25_dependencies_npm-merged

# ./30_create_dependency_graph.py $BASEDIR dependencies_npm-merged.csv dependencies_npm-merged versions_npm-restricted.csv 0.50 
# ./31_prepare_oslom.py \
#   $BASEDIR \
#   sampled-0.5_dependencies_npm
# ./32_create_largest_component.py $BASEDIR enc_sampled-0.5_dependencies_npm-merged

# ./30_create_dependency_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-merged.csv dependencies_$BASENAME-merged versions_$BASENAME.csv 0.0
# ./31_prepare_oslom.py \
#   $BASEDIR/$BASENAME/ \
#   dependencies_$BASENAME
# ./32_create_largest_component.py $BASEDIR enc_sampled-0.0_dependencies_npm-merged

# THEN RUN OSLOM
# date ; cd OSLOM2/ ; ./oslom_undir.exe -r 1 -hr 1 -uw -f ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/$BASENAME/enc_dependencies_$BASENAME-merged.dat ; date

#
# ANALYZE GRAPH USING NETWORKX 
#
# FULL, MERGED GRAPH

# ./30_create_dependency_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-merged.csv dependencies_$BASENAME-merged versions_$BASENAME.csv 0.0
# ./32_create_largest_component.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-merged

# ./30_create_dependency_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-merged.csv dependencies_$BASENAME-merged versions_$BASENAME.csv 0.01
# ./32_create_largest_component.py $BASEDIR/$BASENAME/ sampled-0.01_dependencies_$BASENAME-merged
# ./80_analyze_graph.py \
#   $BASEDIR/$BASENAME/ \
#   sampled-0.01_dependencies_$BASENAME-merged

# ./30_create_dependency_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-merged.csv dependencies_$BASENAME-merged versions_$BASENAME.csv 0.1
# ./32_create_largest_component.py $BASEDIR/$BASENAME/ sampled-0.1_dependencies_$BASENAME-merged
# ./80_analyze_graph.py \
#   $BASEDIR/$BASENAME/ \
#   sampled-0.1_dependencies_$BASENAME-merged

# ./30_create_dependency_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-merged.csv dependencies_$BASENAME-merged versions_$BASENAME.csv 0.4
# ./32_create_largest_component.py $BASEDIR/$BASENAME/ sampled-0.4_dependencies_$BASENAME-merged
# ./80_analyze_graph.py \
#   $BASEDIR/$BASENAME/ \
#   sampled-0.4_dependencies_$BASENAME-merged

# ./30_create_dependency_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-merged.csv dependencies_$BASENAME-merged versions_$BASENAME.csv
# ./32_create_largest_component.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-merged
# ./80_analyze_graph.py \
#   $BASEDIR/$BASENAME/ \
#   dependencies_$BASENAME-merged

#
# PREPARE COVARIATES
#
python3 50_prepare_covariates.py ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/covariates/ Cargo_project_metadata.csv covariates_maintainers-1.csv
# python 51_prepare_covariates-contributors.py ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/covariates/ Contributor_commits.csv covariates-contributors-1.csv
