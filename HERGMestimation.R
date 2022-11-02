# Estimation for the rust network data

rm(list=ls())

library(tidyverse)
library(lighthergm)

# Folders and files 
#datafolder <- "/Users/Angelo/Dropbox/SoftwareNetworks/Data/Cargo/" # Macbook 15
datafolder <- "C:/Users/amele1/Dropbox/SoftwareNetworks/Data/Cargo/" # ResPC New
datafilename <- "enc_dependencies_Cargo-merged-lcc.dat"
datafile <- paste(datafolder, datafilename, sep = "")

# extract data
el <- read_delim(datafile, delim = " ")
el
head(el)
tail(el)
max(el)

# since it was created with python, need to add 1 to each node id 
el <- el + 1

# create network from adjacency list
net <- network::network.edgelist(el, network::network.initialize(max(el), directed = FALSE))

# run estimation 
specification <- net ~ edges + kstar(2)
estimates <- lighthergm::hergm(specification, 
                               n_clusters = 10,
                               n_cores = 40,
                               estimate_parameters = TRUE,
                               verbose = 1,
                               n_em_step_max = 10000,
                               method_second_step = "MPLE",
                               clustering_with_features = FALSE)


file_to_save <- paste(datafolder, "first_estimate_rust.Rdata", sep = "")
save.image(file = file_to_save)