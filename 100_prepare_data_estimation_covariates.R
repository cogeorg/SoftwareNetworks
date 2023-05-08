### Create dataset to estimate using covariates.

library(lighthergm)
library(network)
library(tidyverse)


# file with data for estimation
# change folder to the folder where the data are in your system
datafolder <- "C:/Users/amele1/Dropbox/SoftwareNetworks/Data/Cargo/" # ResPC New
#datafolder <- "/Users/Angelo_1/Dropbox/SoftwareNetworks/Data/Cargo/" # MacBook14
#datafolder <- "/Users/Angelo/Dropbox/SoftwareNetworks/Data/Cargo/" # MacBook15
network_datafilename <- "enc_dependencies_Cargo-merged-lcc.dat"
network_datafile <- paste(datafolder, network_datafilename, sep = "")
covariates_datafilename <- "master_covariates_Cargo-merged.csv"
covariates_datafile <- paste(datafolder, covariates_datafilename, sep = "")


# extract edgelist data
el <- read_delim(network_datafile, delim = " ")
# since it was created with python, need to add 1 to each node id 
el <- el + 1

# covariates
covariates <- read_csv2(covariates_datafile)
# since it was created with python, need to add 1 to each node id 
covariates$node_id <- covariates$node_id + 1

# create network from adjacency list
#covariates_estimation <- covariates[c(1,16,18,20,26)]
covariates_estimation <- covariates[c(1,17,19,21,27)]
net <- network::network(el, vertices = covariates_estimation, directed = FALSE)

# create the features as sparse matrix to improve computational speed 
#specification <- 'net ~ edges + kstar(2) + nodematch("cat2_Activity") + nodematch("cat2_Maturity") +  nodematch("cat2_Popularity") + nodematch("cat2_Size") '
specification <- 'net ~ edges + kstar(2) + nodematch("cat4_Activity") + nodematch("cat4_Maturity") +  nodematch("cat4_Popularity") + nodematch("cat4_Size") '
feature_matrix <- lighthergm::get_list_sparse_feature_adjmat(net, as.formula(specification))
list_feature_matrix <- lighthergm::compute_multiplied_feature_matrices(net, feature_matrix)


# save file
outputfile <- paste(datafolder, "network_data.Rdata", sep = "")

save(net, list_feature_matrix, file = outputfile)
