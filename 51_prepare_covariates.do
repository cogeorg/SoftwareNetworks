//
// 1_maintainer_githubID.dta
//
cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/covariates

insheet using "Maintainer_GithubID.csv", delimiter(",") names clear 
	rename project name_project
save "1_maintainer_githubID.dta", replace


//
// 2_maintainer_github_metadata.dta
//
cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/covariates

insheet using "Maintainer_github_metadata.csv", delimiter(",") names clear 
	rename contributor_github_url maintainer_github_url

	// data not filled for 2/3 of the maintainers
	gen pct_code_review = round(100*code_review / contributions)
	gen pct_commits = round(100*commits / contributions)
	gen pct_issues = round(100*issues / contributions)
	gen pct_pull_requests = round(100*pull_requests / contributions)
	
save "2_maintainer_github_metadata-full.dta", replace
outsheet using "2_maintainer_github_metadata-full.csv", delimiter(",") replace

	sort maintainer_github_url year
	bysort maintainer_github_url: gen MaintainerSeniority = _N
	bysort maintainer_github_url: egen MaintainerActivity = sum(contributions)
	gen MaintainerAvgActivity = MaintainerActivity / MaintainerSeniority

	keep maintainer_github_url Maintainer*
	duplicates drop
	
save "2_maintainer_github_metadata.dta", replace
outsheet using "2_maintainer_github_metadata.csv", delimiter(",") replace
 

//
// 2_contributor_commits.dta
//
cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/covariates

insheet using "Contributor_commits-clean.csv", delimiter(";") names clear 
	
	drop if contributor_github_url == ""  // 5,476 observations lost
	sort name_project contributor_github_url
	
save "2_contributor_commits-full.dta", replace
outsheet using "2_contributor_commits-full.csv", delimiter(",") replace

	bysort name_project: gen num_contributors_alt = _N

	bysort contributor_github_url: gen ContributorExperience = _N
	bysort contributor_github_url: egen ContributorTotalCommits = sum(contributor_commits)
	gen ContributorActivty = ContributorExperience / ContributorTotalCommits

	keep name_project contributor_github_url Contributor*
	
	duplicates drop
	
save "2_contributor_commits.dta", replace
outsheet using "2_contributor_commits.csv", delimiter(",") replace


//
// 3_covariates_maintainers.dta
//
cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/covariates

insheet using "covariates_maintainers-1.csv", delimiter(";") clear
	drop v10
	rename date_first_release str_date_first_release
	rename date_latest_release str_date_latest_release
	gen date_first_release = date(str_date_first_release, "YMD")
	format date_first_release %td
	gen date_latest_release = date(str_date_latest_release, "YMD")
	format date_latest_release %td

duplicates drop


	// Activity, Maturity
	gen Maturity = date_latest_release - date_first_release

	gen Activity = 30*num_total_releases / Maturity
	replace Activity = 0 if Activity == .

	// Other variables
	rename num_stars Popularity
	rename num_forks NumForks
	rename num_contributors NumContributors
	rename size_repository Size  // in Byte
	rename num_watchers NumWatchers 

	//
	// Create categories
	//
	foreach var of varlist Activity Maturity Popularity NumForks NumContributors Size NumWatchers {
		
		quietly su `var', d

		gen cat2_`var' = 0
		replace cat2_`var' = 1 if `var' >= r(p50)

		gen cat4_`var' = 0
		replace cat4_`var' = 1 if `var' > r(p25)  // p25 = 0 which is a problem
		replace cat4_`var' = 2 if `var' >= r(p50)
		replace cat4_`var' = 3 if `var' >= r(p75)

	}

outsheet using "3_covariates_maintainers.csv", delimiter(",") names replace
save "3_covariates_maintainers.dta", replace




	order name_project node_id key1 str_date_first_release str_date_latest_release date_first_release date_latest_release Maturity Activity Popularity NuMForks NumContributors Size NumWatchers


//
// MAPPING
//
cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/

// 4_projects_cargo.dta -- to prepare mapping
insheet using "projects_Cargo.csv", delimiter(";") clear
	rename projectid key1
	rename name name_project
	keep key1 name_project
duplicates drop
save "covariates/4_projects_cargo.dta", replace
outsheet using "covariates/4_projects_cargo.csv", delimiter(",") replace

// 5_master_covariates_Cargo-merged.dta -- the actual mapping
insheet using "key_dependencies_Cargo-merged.dat", delimiter(";") clear   // created by 30_create_dependency_graph.py so that node names can be used in gephi
	split key, p("-")
	replace key3 = key3 + "-" + key4 if key4 != ""
	drop key4
	replace key2 = key2 + "-" + key3 if key3 != ""
	drop key3
save "covariates/5_key_dependencies_Cargo-merged.dta", replace
outsheet using "covariates/5_key_dependencies_Cargo-merged.csv", delimiter(",") replace

	destring key1, replace
	merge m:1 key1 using "covariates/4_projects_cargo.dta"
keep if _merge == 3
	drop _merge

	sort name_project
	keep name_project key1 node_id
duplicates drop
	merge m:1 name_project using "covariates/3_covariates_maintainers.dta"
keep if _merge == 3
	drop _merge

save "covariates/5_master_covariates_Cargo-merged.dta", replace
outsheet using "covariates/5_master_covariates_Cargo-merged.csv", delimiter(",") replace