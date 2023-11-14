cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/

// insheet using deghist_dependencies_Cargo-repo2.csv, delimiter(";") clear

use 10_popularity_centrality-repo.dta, clear
	// table for most central projects
	gsort - in_degree

	order projectname ev_centrality in_degree pagerank Popularity Size NumContributors
	keep  projectname ev_centrality in_degree pagerank Popularity Size NumContributors
	keep in 1/10
	
	texsave using 5_centralities_list.tex, replace

use 10_popularity_centrality-repo.dta, clear
	// table for most popular projects
	gsort - Popularity
	
	order projectname ev_centrality in_degree pagerank Popularity Size NumContributors
	keep  projectname ev_centrality in_degree pagerank Popularity Size NumContributors
	keep in 1/10
	
	texsave using 5_popularity_list.tex, replace

	
	
	
	
cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareProductionNetworks/Data/Cargo/covariates
// // prepare maintainer data
// use 2_maintainer_github_metadata-full.dta, clear
// 	bysort maintainer_github_url: egen total_contributions = sum(contributions)
// 	drop if total_contributions > 125000 // there seem to be a handful of either malicious or automated accounts that we are dropping here
//
// 	keep maintainer_github_url total_contributions
// 	duplicates drop
// save 2_maintainer_github_metadata-full-total.dta, replace
//
// // prepare mapping
insheet using Maintainer_GithubID.csv, delimiter(",") clear names
//
// merge m:1 maintainer_github_url using 2_maintainer_github_metadata-full-total.dta
// 	keep if _merge == 3
// 	drop _merge

// PROJECT.MAJOR.MINOR.VERSION LEVEL
// TODO: double check why we have so few matches between centrality and popularity


// ============================================================================
//
// DEPRECATED
// 
// ============================================================================

// // 5_master_covariates_Cargo-merged.dta -- the actual mapping
// insheet using "key_dependencies_Cargo-merged.dat", delimiter(";") clear   // created by 30_create_dependency_graph.py so that node names can be used in gephi
// 	split key, p("-")
// 	replace key3 = key3 + "-" + key4 if key4 != ""
// 	drop key4
// 	replace key2 = key2 + "-" + key3 if key3 != ""
// 	drop key3
// save "covariates/5_key_dependencies_Cargo-merged.dta", replace
// outsheet using "covariates/5_key_dependencies_Cargo-merged.csv", delimiter(",") replace
//
// 	destring key1, replace
// 	merge m:1 key1 using "covariates/4_projects_cargo.dta"
// keep if _merge == 3
// 	drop _merge
//
// 	sort name_project
// 	keep name_project key1 node_id
// duplicates drop
// 	merge m:1 name_project using "covariates/3_covariates_maintainers.dta"
// keep if _merge == 3
// 	drop _merge
//
// save "covariates/5_master_covariates_Cargo-merged.dta", replace
// outsheet using "covariates/5_master_covariates_Cargo-merged.csv", delimiter(",") replace
