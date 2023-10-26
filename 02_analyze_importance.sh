#!/usr/bin/env bash

# ###########################################################################
#
# TEST RUN
#
# ###########################################################################
GITDIR=~/git/SoftwareNetworks/
BASEDIR=~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/
BASENAME=Cargo
FILENAME=test_fast_gnp_1000_0.03

#
# GENERATE RANDOM NETWORKS
#
# ./79_generate_test_networks.py \
#   $BASEDIR/$BASENAME \
#   test \
#   64 \
#   fast_gnp \
#   0.03

# # GRAPH ANALYSIS
# ./80_analyze_graph.py \
#   $BASEDIR/$BASENAME/ \
#   $FILENAME

# CENTRALITY ANALYSIS
# ./81_analyze_graph.py \
#   $BASEDIR/$BASENAME/ \
#   $FILENAME

# CHECK FOR CYCLES
./81_find_cycles.py \
  $BASEDIR/$BASENAME/ \
  $FILENAME

# COMPUTE IMPORTANCE
# ./200_compute_importance.py \
#   $BASEDIR/$BASENAME/ \
#   $FILENAME \
#   5


# ###########################################################################
#
# PRODUCTION RUN
#
# ###########################################################################
GITDIR=~/git/SoftwareNetworks/
BASEDIR=~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/
BASENAME=Cargo

# ./200_compute_importance.py \
#   $BASEDIR/$BASENAME/ \
#   dependencies_$BASENAME-repo2
