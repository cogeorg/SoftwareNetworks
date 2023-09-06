#!/usr/bin/env bash
GITDIR=~/git/SoftwareNetworks/
BASEDIR=~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/
BASENAME=Cargo

# ###########################################################################
#
# TEST RUN
#
# ###########################################################################

# ./200_compute_importance.py \
#   $BASEDIR/$BASENAME/ \
#   test1 \
#   0.1


# ###########################################################################
#
# PRODUCTION RUN
#
# ###########################################################################

./200_compute_importance.py \
  $BASEDIR/$BASENAME/ \
  dependencies_$BASENAME-merged \
  0.1
