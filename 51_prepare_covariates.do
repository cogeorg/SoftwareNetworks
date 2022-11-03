//
// 1_maintainer_githubID.dta
//
cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/covariates

insheet using Maintainer_GithubID.csv, delimiter(",") names clear 
	rename project name_project
save "1_maintainer_githubID.dta", replace

//
// 2_maintainer_github_metadata.dta
//
cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/covariates

insheet using Maintainer_github_metadata.csv, delimiter(",") names clear 
	rename contributor_github_url maintainer_github_url

	// data not filled for 2/3 of the maintainers
	gen pct_code_review = round(100*code_review / contributions)
	gen pct_commits = round(100*commits / contributions)
	gen pct_issues = round(100*issues / contributions)
	gen pct_pull_requests = round(100*pull_requests / contributions)
	
save "2_maintainer_githubID-full.dta", replace

	sort maintainer_github_url year
	bysort maintainer_github_url: gen mtn_years_active = _N
	bysort maintainer_github_url: egen mtn_tot_contributions = sum(contributions)
	gen mtn_avg_contributions = mtn_tot_contributions / mtn_years_active

	keep maintainer_github_url mtn_*
	duplicates drop
	
save "2_maintainer_githubID.dta", replace


//
// 2_contributor_commits.dta
//
cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/covariates

insheet using Contributor_commits-clean.csv, delimiter(";") names clear 
	
	drop if contributor_github_url == ""  // 5,476 observations lost
	sort name_project contributor_github_url
	
save "2_contributor_commits-full.dta", replace

	bysort name_project: gen num_contributors_alt = _N
	keep name_project num_contributors_alt
	
	duplicates drop
	
save "2_contributor_commits.dta", replace




//
// COVARIATES
//
cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/covariates

insheet using "covariates.csv", delimiter(";") clear
drop v10
rename date_first_release str_date_first_release
rename date_latest_release str_date_latest_release
gen date_first_release = date(str_date_first_release, "YMD")
format date_first_release %td
gen date_latest_release = date(str_date_latest_release, "YMD")
format date_latest_release %td

duplicates drop

gen days_active = date_latest_release - date_first_release

// num_total_releases
gen cat4_num_total_releases = 0
replace cat4_num_total_releases = 1 if num_total_releases >= 1
replace cat4_num_total_releases = 2 if num_total_releases >= 3
replace cat4_num_total_releases = 3 if num_total_releases >= 75

gen cat2_num_total_releases = 0
replace cat2_num_total_releases = 1 if num_total_releases >= 3

// size_repository
gen cat4_size_repository = 0
replace cat4_size_repository = 1 if size_repository >= 4997
replace cat4_size_repository = 2 if size_repository >= 58982
replace cat4_size_repository = 3 if size_repository >= 840704

gen cat2_size_repository = 0
replace cat2_size_repository = 1 if size_repository >= 58982

// num_stars
gen cat2_num_stars = 0
replace cat2_num_stars = 1 if num_stars >= 2

// num_contributors
gen cat2_num_contributors = 0
replace cat2_num_contributors = 1 if num_contributors >= 1

// norm_releases
gen norm_releases = 30*num_total_releases / days_active
gen cat4_norm_releases = 0
replace cat4_norm_releases = 1 if norm_releases >= 0.2412
replace cat4_norm_releases = 2 if norm_releases >= 0.4927
replace cat4_norm_releases = 3 if norm_releases >= 1.714

gen cat2_norm_releases = 0
replace cat2_norm_releases = 1 if norm_releases > 0.4927

// num_forks
gen cat2_num_forks = 0
replace cat2_num_forks = 1 if num_forks >= 1

// num_watchers
gen cat2_num_watchers = 0
replace cat2_num_watchers = 1 if num_watchers >= 1

save "covariates.dta", replace


//
// MAPPING
//
cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareNetworks/Data/Cargo/

// PREPARE MAPPING
insheet using "projects_Cargo.csv", delimiter(";") clear
rename projectid key1
rename name name_project
keep key1 name_project
duplicates drop
save "projects_Cargo.dta", replace

// CONSTRUCT ACTUAL MAPPING
insheet using "key_dependencies_Cargo-merged.dat", delimiter(";") clear   // created by 30_create_dependency_graph.py so that node names can be used in gephi
split key, p("-")
replace key3 = key3 + "-" + key4 if key4 != ""
drop key4
replace key2 = key2 + "-" + key3 if key3 != ""
drop key3
save "key_dependencies_Cargo-merged.dta", replace
destring key1, replace
merge m:1 key1 using "projects_Cargo.dta"
keep if _merge == 3
drop _merge

sort name_project
keep name_project key1 node_id
duplicates drop
merge m:1 name_project using "covariates/covariates.dta"
keep if _merge == 3
drop _merge

save "master_covariates_Cargo-merged.dta", replace
outsheet using "master_covariates_Cargo-merged.csv", delimiter(";") replace