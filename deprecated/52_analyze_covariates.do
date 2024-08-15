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
	su syst_*
	su syst_*, d
save tmp.dta, replace
	forvalues i=2/5 {
		egen mean_syst_`i' = mean(syst_`i')
	}
	keep mean_syst*
	duplicates drop
	
	gen id = 1
	reshape long mean_syst_, i(id) j(round)
	drop id
	rename mean_syst_ k0
save mean_systemicness.dta, replace
	
use tmp.dta, clear
	keep in 1/3527
	su syst_*
	su syst_*, d
save tmp.dta, replace
	forvalues i=2/5 {
		egen mean_syst_`i' = mean(syst_`i')
	}
	keep mean_syst*
	duplicates drop
	
	gen id = 1
	reshape long mean_syst_, i(id) j(round)
	drop id
	rename mean_syst_ k0
save mean_systemicness_p99.dta, replace
	
use tmp.dta, clear
	// create table of most important repos
	keep in 1/10
	texsave using 6_importance_list.tex, replace
	
	
//
// BETWEENNESS + EXPECTED FATALITY
//
// run this before 201_compute_importance-protected.py 
insheet using "centrality_dependencies_Cargo-repo2-matched-lcc.csv", delimiter(";") clear
	rename v1 repoid
	rename v2 betweenness
	rename v3 ef
	rename v4 in_degree
	
merge 1:1 repoid using repositories_Cargo.dta
	keep if _merge == 3
	drop _merge 

	egen max_bet = max(betweenness)
	gen norm_bet = betweenness/max_bet
	egen max_ef = max(ef)
	gen norm_ef = ef / max_ef
	egen max_indeg = max(in_degree)
	gen norm_indeg = in_degree/max_indeg

	gen betef = 0.5*norm_bet + 0.5*norm_ef
	egen max_betef = max(betef)
	gen norm_betef = betef/max_betef
	
	gsort - norm_betef  // determines which nodes are being protected
	
	keep repoid projectname norm_*	
	order repoid projectname norm_bet norm_ef norm_betef
outsheet using "centrality_dependencies_Cargo-repo2-matched-lcc2.csv", delimiter(";") nonames replace
	gsort - norm_indeg  // determines which nodes are being protected
outsheet using "centrality_dependencies_Cargo-repo2-matched-lcc2_indeg.csv", delimiter(";") nonames replace
// run 201_compute_importance-protected.py using this file as input and before proceeding

//
// CONTAGION WITH PROTECTED NODES
//
cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/

// DATA PREPARATION
foreach num_nodes in 10 100 {  // iterate over number of protected nodes
	foreach protection in betef indeg {  // iterate over different measures of node importance for protection
		insheet using "importance_dependencies_Cargo-repo2-matched-lcc-`num_nodes'-6_`protection'.csv", delimiter(";") clear
		
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
			su syst_*
			su syst_*, d
		save tmp.dta, replace
			forvalues i=2/5 {
				egen mean_syst_`i' = mean(syst_`i')
			}
			keep mean_syst*
			duplicates drop

			gen id = 1
			reshape long mean_syst_, i(id) j(round)
			drop id
			rename mean_syst_ k`num_nodes'
		save mean_systemicness-`num_nodes'_`protection'.dta, replace
		
		use tmp.dta, clear
			keep in 1/3527
			su syst_*
			su syst_*, d
		save tmp.dta, replace
			forvalues i=2/5 {
				egen mean_syst_`i' = mean(syst_`i')
			}
			keep mean_syst*
			duplicates drop
			
			gen id = 1
			reshape long mean_syst_, i(id) j(round)
			drop id
			rename mean_syst_ k`num_nodes'
		save mean_systemicness_p99-`num_nodes'_`protection'.dta, replace
	}
}

//
// PLOTS
// 
use mean_systemicness.dta, clear
	foreach num_nodes in 10 100 {
		foreach protection in betef indeg {
			merge 1:1 round using mean_systemicness-`num_nodes'_`protection'.dta
				drop _merge
				rename k`num_nodes' k`num_nodes'_`protection'
		}
	}
	
	
	label variable round "k"
	label variable k0 "No node protected"
	label variable k10_betef "10 Most systemic nodes protected (ef)"
	label variable k100_betef "100 Most systemic nodes protected (ef)"
	label variable k10_indeg "10 Most systemic nodes protected (indeg)"
	label variable k100_indeg "100 Most systemic nodes protected (indeg)"
	
	twoway scatter k0 k10_indeg k100_indeg  k10_betef k100_betef round, /// 
		connect(l l l l l) ///
		lpattern(solid dash dash_dot dash dash_dot) ///
		msymbol(O T T D D) ///
		mcolor(black blue blue black black) ///
		clcolor(black blue blue black black) ///
		ytitle("k-step systemicness") ///
		legend(pos(11) ring(0))
graph export mean_systemicness.png, replace 

// p99	
use mean_systemicness_p99.dta, clear
	foreach num_nodes in 10 100 {
		foreach protection in betef indeg {
			merge 1:1 round using mean_systemicness_p99-`num_nodes'_`protection'.dta
				drop _merge
				rename k`num_nodes' k`num_nodes'_`protection'
		}
	}
	
	
	label variable round "k"
	label variable k0 "No node protected"
	label variable k10_betef "10 Most systemic nodes protected (ef)"
	label variable k100_betef "100 Most systemic nodes protected (ef)"
	label variable k10_indeg "10 Most systemic nodes protected (indeg)"
	label variable k100_indeg "100 Most systemic nodes protected (indeg)"
	
	twoway scatter k0 k10_indeg k100_indeg  k10_betef k100_betef round, /// 
		connect(l l l l l) ///
		lpattern(solid dash dash_dot dash dash_dot) ///
		msymbol(O T T D D) ///
		mcolor(black blue blue black black) ///
		clcolor(black blue blue black black) ///
		ytitle("k-step systemicness") ///
		legend(pos(11) ring(0))
graph export mean_systemicness_p99.png, replace 

	
	

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
