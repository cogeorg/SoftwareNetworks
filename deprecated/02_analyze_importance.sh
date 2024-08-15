#!/usr/bin/env bash

# ###########################################################################
#
# TEST RUN
#
# ###########################################################################
GITDIR=~/git/SoftwareNetworks/
BASEDIR=~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/
BASENAME=Cargo
# FILENAME=test2
# FILENAME=test_fast_gnp_1000_0.03
FILENAME=dependencies_Cargo-repo2-matched-lcc

#
# GENERATE RANDOM NETWORKS
#
# ./79_generate_test_networks.py \
#   $BASEDIR/$BASENAME \
#   test \
#   8000 \
#   fast_gnp \
#   0.003

# # GRAPH ANALYSIS
# ./80_analyze_graph.py \
#   $BASEDIR/$BASENAME/ \
#   $FILENAME

# CENTRALITY ANALYSIS -- DOES SOMETIMES NOT CONVERGE
# ./81_analyze_graph.py \
#   $BASEDIR/$BASENAME/ \
#   $FILENAME

# CHECK FOR CYCLES OF LENGTH UP TO 6
# ./81_find_cycles.py \
#   $BASEDIR/$BASENAME/ \
#   $FILENAME

#
# COMPUTE IMPORTANCE
#
# ./200_compute_importance.py \
#   $BASEDIR/$BASENAME/ \
#   $FILENAME \
#   6

# FILENAME=test2
# FILENAME=test_fast_gnp_8000_0.003
# FILENAME=dependencies_Cargo-repo2-matched-lcc
# ./200_compute_importance-centrality.py \
#   $BASEDIR/$BASENAME/ \
#   $FILENAME

# ###########################################################################
#
# PRODUCTION RUN
#
# ###########################################################################
GITDIR=~/git/SoftwareNetworks/
BASEDIR=~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/
BASENAME=Cargo
FILENAME=dependencies_Cargo-repo2-matched-lcc

# # Run first to compute contagion without protection
# ./200_compute_importance.py \
#   $BASEDIR/$BASENAME/ \
#   $FILENAME \
#   6

# then compute different measures of importance to decide which nodes to protect
# ./200_compute_importance-centrality.py \
#   $BASEDIR/$BASENAME/ \
#   $FILENAME
# run 52_analyze_covariates.do lines 100-128 before running the below

# then compute the new contagion (at same depth as before) with some nodes protected
# this uses the hybrid measure 0.5*betweenness + 0.5*expected fatality as measure of importance
PROTECTIONFILENAME=centrality_dependencies_Cargo-repo2-matched-lcc2.csv
./201_compute_importance-protected.py \
  $BASEDIR/$BASENAME/ \
  $FILENAME \
  $PROTECTIONFILENAME \
  6 \
  10 \
  betef
./201_compute_importance-protected.py \
  $BASEDIR/$BASENAME/ \
  $FILENAME \
  $PROTECTIONFILENAME \
  6 \
  100 \
  betef

# this uses indegree as measure of importance
PROTECTIONFILENAME=centrality_dependencies_Cargo-repo2-matched-lcc2_indeg.csv
./201_compute_importance-protected.py \
  $BASEDIR/$BASENAME/ \
  $FILENAME \
  $PROTECTIONFILENAME \
  6 \
  10 \
  indeg

./201_compute_importance-protected.py \
  $BASEDIR/$BASENAME/ \
  $FILENAME \
  $PROTECTIONFILENAME \
  6 \
  100 \
  indeg
# then continue with 52_analyze_covariates.do lines 134ff