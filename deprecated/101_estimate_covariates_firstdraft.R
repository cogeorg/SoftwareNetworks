rm(list=ls())


library(lighthergm)
library(network)
library(tidyverse)


# file with data for estimation
# change folder to the folder where the data are in your system
#datafolder <- "C:/Users/amele1/Dropbox/SoftwareNetworks/Data/Cargo/" # ResPC New
datafolder <- "D:/SoftwareNetworks/"  # ResPC
#datafolder <- "/Users/Angelo_1/Dropbox/SoftwareNetworks/Data/Cargo/" # MacBook14
#datafolder <- "/Users/Angelo/Dropbox/SoftwareNetworks/Data/Cargo/" # MacBook15
network_datafilename <- "network_data.Rdata"
network_datafile <- paste(datafolder, network_datafilename, sep = "")



n_blocks <- 50

specification <- 'net ~ edges + kstar(2) + nodematch("cat4_Activity") + nodematch("cat4_Maturity") +  nodematch("cat4_Popularity") + nodematch("cat4_Size") '

initialization <- 1 # infomap for initial clustering
n_cores <- 40
n_em_step_max <- 10000
est_method <- "MPLE"





load(file = network_datafile)


# run estimation 
estimates_blocks <- lighthergm::hergm(object = as.formula(specification), 
                               n_clusters = n_blocks,
                               initialization_method = 1,
                               n_cores = n_cores,
                               estimate_parameters = FALSE,
                               verbose = 1,
                               n_em_step_max = n_em_step_max,
                               method_second_step = est_method,
                               clustering_with_features = FALSE #,
                               #list_multiplied_feature_matrices = list_feature_matrix,
                               #use_infomap_python = TRUE, 
                               #seed_infomap = 2)
)



n_em_step_max <- 100
estimates_blocks$checkpoint$clustering_with_features = TRUE
estimates_blocks$checkpoint$list_multiplied_feature_matrices = list_feature_matrix

# run estimation 
estimates <- lighthergm::hergm(object = estimates_blocks, 
                               n_clusters = n_blocks,
                               initialization_method = 1,
                               n_cores = n_cores,
                               estimate_parameters = TRUE,
                               verbose = 1,
                               n_em_step_max = n_em_step_max,
                               method_second_step = est_method,
                               clustering_with_features = TRUE,
                               list_multiplied_feature_matrices = list_feature_matrix
                               )



# checked EM_lower_bound, did not seem to converge, so add 100 iterations


n_em_step_max <- 100
estimates$checkpoint$clustering_with_features = TRUE
estimates$checkpoint$list_multiplied_feature_matrices = list_feature_matrix

# run estimation 
estimates <- lighthergm::hergm(object = estimates, 
                               n_clusters = n_blocks,
                               initialization_method = 1,
                               n_cores = n_cores,
                               estimate_parameters = TRUE,
                               verbose = 1,
                               n_em_step_max = n_em_step_max,
                               method_second_step = est_method,
                               clustering_with_features = TRUE,
                               list_multiplied_feature_matrices = list_feature_matrix
)



# checked EM_lower_bound, did not seem to converge, so add 200 iterations


n_em_step_max <- 200
estimates$checkpoint$clustering_with_features = TRUE
estimates$checkpoint$list_multiplied_feature_matrices = list_feature_matrix

# run estimation 
estimates <- lighthergm::hergm(object = estimates, 
                               n_clusters = n_blocks,
                               initialization_method = 1,
                               n_cores = n_cores,
                               estimate_parameters = TRUE,
                               verbose = 1,
                               n_em_step_max = n_em_step_max,
                               method_second_step = est_method,
                               clustering_with_features = TRUE,
                               list_multiplied_feature_matrices = list_feature_matrix
)




# checked EM_lower_bound, did not seem to converge, so add 100 iterations


n_em_step_max <- 100
estimates$checkpoint$clustering_with_features = TRUE
estimates$checkpoint$list_multiplied_feature_matrices = list_feature_matrix

# run estimation 
estimates <- lighthergm::hergm(object = estimates, 
                               n_clusters = n_blocks,
                               initialization_method = 1,
                               n_cores = n_cores,
                               estimate_parameters = TRUE,
                               verbose = 1,
                               n_em_step_max = n_em_step_max,
                               method_second_step = est_method,
                               clustering_with_features = TRUE,
                               list_multiplied_feature_matrices = list_feature_matrix
)



# checked EM_lower_bound, did not seem to converge, so add 500 iterations


n_em_step_max <- 500
estimates$checkpoint$clustering_with_features = TRUE
estimates$checkpoint$list_multiplied_feature_matrices = list_feature_matrix

# run estimation 
estimates <- lighthergm::hergm(object = estimates, 
                               n_clusters = n_blocks,
                               initialization_method = 1,
                               n_cores = n_cores,
                               estimate_parameters = TRUE,
                               verbose = 1,
                               n_em_step_max = n_em_step_max,
                               method_second_step = est_method,
                               clustering_with_features = TRUE,
                               list_multiplied_feature_matrices = list_feature_matrix
)




# checked EM_lower_bound, did not seem to converge, so add 200 iterations


n_em_step_max <- 200
estimates$checkpoint$clustering_with_features = TRUE
estimates$checkpoint$list_multiplied_feature_matrices = list_feature_matrix

# run estimation 
estimates <- lighthergm::hergm(object = estimates, 
                               n_clusters = n_blocks,
                               initialization_method = 1,
                               n_cores = n_cores,
                               estimate_parameters = TRUE,
                               verbose = 1,
                               n_em_step_max = n_em_step_max,
                               method_second_step = est_method,
                               clustering_with_features = TRUE,
                               list_multiplied_feature_matrices = list_feature_matrix
)




# checked EM_lower_bound, did not seem to converge, so add 100 iterations


n_em_step_max <- 100
estimates$checkpoint$clustering_with_features = TRUE
estimates$checkpoint$list_multiplied_feature_matrices = list_feature_matrix

# run estimation 
estimates <- lighthergm::hergm(object = estimates, 
                               n_clusters = n_blocks,
                               initialization_method = 1,
                               n_cores = n_cores,
                               estimate_parameters = TRUE,
                               verbose = 1,
                               n_em_step_max = n_em_step_max,
                               method_second_step = est_method,
                               clustering_with_features = TRUE,
                               list_multiplied_feature_matrices = list_feature_matrix
)

output_datafile <- paste(datafolder, "estimates_covariates_firstdraft.Rdata", sep = "")
save(estimates, estimates_blocks, file = output_datafile )
