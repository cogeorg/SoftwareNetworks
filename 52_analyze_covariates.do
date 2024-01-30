cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/
// insheet using deghist_dependencies_Cargo-repo2.csv, delimiter(";") clear

cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/
use 20_master_Cargo-matched.dta, clear	
	// some summary stats
	su ev_centrality, detail
	su pagerank, detail
	su in_degree, detail
	su out_degree, detail
	
use 20_master_Cargo-matched.dta, clear	
	// table for most central projects
	gsort - in_degree

	local vars ev_centrality in_degree pagerank Popularity Size NumContributors 
	foreach var of local vars {
		gen `var'_rounded = round(`var', 0.001)
		drop `var'
		rename `var'_rounded `var'
	}
	
	order projectname ev_centrality in_degree pagerank Popularity Size NumContributors
	keep  projectname ev_centrality in_degree pagerank Popularity Size NumContributors
	keep in 1/10
	
	texsave using 5_centralities_list.tex, replace

use 20_master_Cargo-matched.dta, clear	
	 su Size Popularity NumForks NumWatchers NumContributors Maturity
	 su Size Popularity NumForks NumWatchers NumContributors Maturity, detail
	 
	
//
// SYSTEMICNESS
//
cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/
// forvalues i=2/5 {
// 	insheet using "importance_dependencies_Cargo-repo2-matched-lcc-`i'.csv", delimiter(";") clear
// 	rename v1 repoid
// 	save "importance_dependencies_Cargo-repo2-matched-lcc-`i'.dta", replace
// }
//

insheet using "importance_dependencies_Cargo-repo2-matched-lcc-6.csv", delimiter(";") clear
	rename v1 repoid
	drop v8
	
merge 1:1 repoid using repositories_Cargo.dta
	keep if _merge == 3
	drop _merge 
	
	rename v3 in_degree
	gsort - in_degree // the one-step systemicness, i.e. in-degree
	
	drop repoid v2
	order projectname in_degree
	rename v4 syst_2
	rename v5 syst_3
	rename v6 syst_4
	rename v7 syst_5
	
	keep projectname in_degree syst_*
	// MANUALLY create table of systemicness 
	su syst_*, d
	su syst_*
	
	keep in 1/3527
	
	// create table of most important repos
	keep in 1/10
	texsave using 6_importance_list.tex, replace
	
	
//
// BETWEENNESS
//
insheet using "centrality_dependencies_Cargo-repo2-matched-lcc.csv", delimiter(";") clear
	rename v1 repoid
	rename v2 betweenness
	
merge 1:1 repoid using repositories_Cargo.dta
	keep if _merge == 3
	drop _merge 
	
	gsort - betweenness
	
	
// ============================================================================
//
// DEPRECATED
// 
// ============================================================================

// cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareProductionNetworks/Data/Cargo/covariates
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
// insheet using Maintainer_GithubID.csv, delimiter(",") clear names
//
// merge m:1 maintainer_github_url using 2_maintainer_github_metadata-full-total.dta
// 	keep if _merge == 3
// 	drop _merge

// PROJECT.MAJOR.MINOR.VERSION LEVEL
// TODO: double check why we have so few matches between centrality and popularity


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
