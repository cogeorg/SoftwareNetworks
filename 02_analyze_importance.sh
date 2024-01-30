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

./200_compute_importance.py \
  $BASEDIR/$BASENAME/ \
  $FILENAME \
  6
