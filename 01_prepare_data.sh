#!/usr/bin/env bash
# BASEDIR=~/Downloads/
BASEDIR=~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/
GITDIR=~/Git/SoftwareProductionNetworks/

# ###########################################################################
#
# PRODUCTION RUN 1.6.0 -- Cargo
#
# ###########################################################################
VERSION=1.6.0-2020-01-12
BASENAME=Cargo
LANGUAGE=Rust
DEPFILE=dependencies_$BASENAME.csv

#
# STEP 1 -- PREPARE ORIGINAL DATA
#
# USES libraries-1.6.0-2020-01-12.tar.gz
#

# ./10_prepare_repositories-1.6.0.py \
#   $BASEDIR \
#   libraries-$VERSION/repositories-$VERSION.csv \
#   $BASENAME/repositories_$BASENAME.csv \
#   $LANGUAGE

# ./10_prepare_projects-1.6.0.py \
#   $BASEDIR \
#   libraries-$VERSION/projects-$VERSION.csv \
#   $BASENAME/projects_$BASENAME.csv \
#   $BASENAME

# ON REPO LEVEL
# ./10_prepare_dependencies-1.6.0.py \
#   /Volumes/Transcend/Data/ \
#   libraries-$VERSION/repository_dependencies-$VERSION.csv \
#   $BASENAME/repo_dependencies_$BASENAME.csv \
#   $BASENAME
# DEPRECATED -- ON PROJECT LEVEL
./11_prepare_dependencies-1.6.0.py \
  ~/Downloads/ \
  libraries-$VERSION/dependencies-$VERSION.csv \
  $BASENAME/dependencies_$BASENAME.csv \
  $BASENAME
# TEST
# ./10_prepare_dependencies-1.6.0.py \
#   ~/Downloads/ \
#   libraries-$VERSION/repository_dependencies-test.csv \
#   $BASENAME/dependencies_test.csv \
#   $BASENAME

#
# CREATE REPO-DEPENDENCY GRAPH
#
# FIRST: RUN CARGO PART OF 51_prepare_dependencies.do 
# ./30_create_dependency_graph-1.6.0.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-repo2-matched.csv dependencies_$BASENAME-repo2-matched 0.0

#
# ANALYZE DEPENDENCY GRAPH
# 
# ./80_analyze_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-repo2-matched True True False False 
# CREATE CENTRALITIES USING GEPHI WITH THE LCC FILE
# ./81_analyze_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-repo2-lcc  # TODO: CRASHES SOMETIMES FOR LARGE NETWORKS (~1M EDGES); IN THAT CASE, USE GEPHI


# ###########################################################################
#
# PRODUCTION RUN 1.6.0 -- Pypi
#
# ###########################################################################
VERSION=1.6.0-2020-01-12
BASENAME=Pypi
LANGUAGE=Python
DEPFILE=dependencies_$BASENAME.csv

#
# STEP 1 -- PREPARE ORIGINAL DATA
#
# USES libraries-1.6.0-2020-01-12.tar.gz
#

# ./10_prepare_repositories-1.6.0.py \
#   $BASEDIR \
#   libraries-$VERSION/repositories-$VERSION.csv \
#   $BASENAME/repositories_$BASENAME.csv \
#   $LANGUAGE

# ./10_prepare_projects-1.6.0.py \
#   $BASEDIR \
#   libraries-$VERSION/projects-$VERSION.csv \
#   $BASENAME/projects_$BASENAME.csv \
#   $BASENAME

# ON PROJECT LEVEL
# ./11_prepare_dependencies-1.6.0.py \
#   $BASEDIR \
#   libraries-$VERSION/dependencies-$VERSION.csv \
#   $BASENAME/dependencies_$BASENAME.csv \
#   $BASENAME
# ON REPO LEVEL
# ./10_prepare_dependencies-1.6.0.py \
#   /Volumes/Transcend/Data/ \
#   libraries-$VERSION/repository_dependencies-$VERSION.csv \
#   $BASENAME/repo_dependencies_$BASENAME.csv \
#   $BASENAME
# TEST
# ./10_prepare_dependencies-1.6.0.py \
#   ~/Downloads/ \
#   libraries-$VERSION/repository_dependencies-test.csv \
#   $BASENAME/dependencies_test.csv \
#   $BASENAME

#
# CREATE REPO-DEPENDENCY GRAPH
#
# FIRST: RUN PYPI PART OF 51_prepare_dependencies.do 
# ./30_create_dependency_graph-1.6.0.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-repo2.csv dependencies_$BASENAME-repo2 0.0
# ./30_create_dependency_graph-1.6.0.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-repo2-matched.csv dependencies_$BASENAME-repo2-matched 0.0

#
# ANALYZE DEPENDENCY GRAPH
# 
# ./80_analyze_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-repo2-matched False False False False 
# CREATE CENTRALITIES USING GEPHI WITH THE LCC FILE
# ./81_analyze_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-repo2-matched-lcc  # TODO: CRASHES SOMETIMES FOR LARGE NETWORKS (~1M EDGES); IN THAT CASE, USE GEPHI



# ###########################################################################
#
# PRODUCTION RUN 1.6.0 -- CRAN
#
# ###########################################################################
VERSION=1.6.0-2020-01-12
BASENAME=Cran
LANGUAGE=r
DEPFILE=dependencies_$BASENAME.csv

#
# STEP 1 -- PREPARE ORIGINAL DATA
#
# USES libraries-1.6.0-2020-01-12.tar.gz
#

# ./10_prepare_repositories-1.6.0.py \
#   $BASEDIR \
#   libraries-$VERSION/repositories-$VERSION.csv \
#   $BASENAME/repositories_$BASENAME.csv \
#   $LANGUAGE

# ./10_prepare_projects-1.6.0.py \
#   $BASEDIR \
#   libraries-$VERSION/projects-$VERSION.csv \
#   $BASENAME/projects_$BASENAME.csv \
#   $BASENAME

# ON REPO LEVEL
# ./10_prepare_dependencies-1.6.0.py \
#   /Volumes/Transcend/Data/ \
#   libraries-$VERSION/repository_dependencies-$VERSION.csv \
#   $BASENAME/repo_dependencies_$BASENAME.csv \
#   $BASENAME
# cp /Volumes/Transcend/Data/$BASENAME/repo_dependencies_$BASENAME.csv $BASEDIR/$BASENAME 

#
# CREATE REPO-DEPENDENCY GRAPH
# Note: for large networks, sampling might be helpful. The last number is the sampling probability.
# TODO: sampling not yet implemented for 1.6.0
# ./30_create_dependency_graph-1.6.0.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-repo2.csv dependencies_$BASENAME-repo2 0.0

#
# ANALYZE DEPENDENCY GRAPH
# 
# ./80_analyze_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-repo2
# ./81_analyze_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-repo2-lcc  # TODO: CRASHES SOMETIMES; IN THAT CASE, USE GEPHI


# ###########################################################################
#
# PRODUCTION RUN 1.4.0 -- Cargo
#
# ###########################################################################
BASENAME=Cargo
DEPFILE=dependencies_$BASENAME.csv

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
# NB: In the last x0**** file generated this way was an extra line which had to be manually removed for the next command to work. Will fix at some point.
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
# CREATE VERSION-DEPENDENCY GRAPH
#

# Note: for large networks, sampling might be helpful. The last number is the sampling probability.
# ./30_create_dependency_graph.py $BASEDIR dependencies_npm-merged.csv dependencies_npm-merged versions_npm-restricted.csv 0.01 

# Note: 0.0 means no cuts applied
# ./30_create_dependency_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-merged.csv dependencies_$BASENAME-merged versions_$BASENAME.csv 0.0
# ./31_create_dependency_graph-projects.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-projects.csv dependencies_$BASENAME-projects  0.0

#
# PREPARE COVARIATES
#
# NOTES: 
# 1. Cargo_project_metadata.csv was created using a scraper of the libraries.io website.
# 2. 50_prepare_covariates.py generates files necessary for repo-dependency graph
#
# python3 50_prepare_covariates.py $BASEDIR/Cargo/covariates/ Cargo_project_metadata.csv covariates_maintainers-1.csv
#./51_prepare_covariates-contributors.py $BASEDIR/Cargo/covariates/ Contributor_commits.csv covariates-contributors-1.csv

#
# ANALYZE VERSION / PROJECT / REPO DEPENDENCY GRAPH USING NETWORKX 
#

# ./80_analyze_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-merged
# ./80_analyze_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-projects
# ./81_analyze_graph.py $BASEDIR/$BASENAME/ dependencies_$BASENAME-repo-nomissing
