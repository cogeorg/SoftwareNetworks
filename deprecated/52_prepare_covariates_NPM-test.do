// ============================================================================
//
// NPM -- 1.6.0 -- TEST
//
// ============================================================================
cd ~/Downloads/NPM-test/ 

// PREPARE WYSS DATA
insheet using "Wyss_npm-test_data.csv", delimiter(",") clear
	rename package projectname 
	sort projectname
	
	// create repo-based variables
	split repository, parse("https://github.com/")
	drop repository1
	split repository2, parse("/")
	drop repository2
	
	rename repository22 repo
	rename repository21 repo_user 
	
	order repo repo_user repository 
	drop projectname
save "Wyss_npm-test_data.dta", replace

use Wyss_npm-test_data.dta, clear
	sort repo	
	rename weekly_downloads downloads
	order repo repo_user repository downloads vulnerabilities issues_per_download size versions commits contributors open_issues closed_issues commits_with_bug commits_with_vuln mean_loc-halstead stars watchers forks issues
	keep repo repo_user repository  downloads vulnerabilities issues_per_download size versions commits contributors open_issues closed_issues commits_with_bug commits_with_vuln mean_loc-halstead stars watchers forks issues
	
	foreach var of varlist downloads-issues {
			bysort repo: egen foo = mean(`var')
			drop `var'
			rename foo `var'
	}
	bysort repo: gen num_packages = _N 
	duplicates drop
	
	bysort repo: gen foo = _N  // forking repos means that some packages have multiple repositories which might or might not be distinct
	drop if foo > 1  // drop those
	drop foo
	
	gen id_repo = _n	
save Wyss_npm-test_data2.dta, replace
outsheet using Wyss_npm-test_data2.csv, delimiter(";") names replace

use Wyss_npm-test_data2.dta, clear
	keep repo id_repo
save repo_id_repo-Wyss.dta, replace


// ANALYSIS BASED ON REPO DEPENDENCIES 
insheet using repo_dependencies_NPM-test-matchedWyss.csv, names delimiter(";") clear

	rename from_repo repo 
merge m:1 repo using repo_id_repo-Wyss.dta  // using the Wyss unique IDs 
	drop if _merge != 3
	drop _merge 
	rename repo from_repo
	rename id_repo id_from_repo 

	rename to_repo repo 
merge m:1 repo using repo_id_repo-Wyss.dta
	drop if _merge != 3
	drop _merge 
	rename repo to_repo
	rename id_repo id_to_repo 

	duplicates drop 
	
	sort id_from_repo id_to_repo  // based on Wyss unique IDs	
	keep id_from_repo id_to_repo

outsheet using repo_dependencies_NPM-test-matchedWyss+IDs.csv, nonames delimiter(";") replace


// check which repos exist in the final dependencies file...
insheet using repo_dependencies_NPM-test-matchedWyss+IDs.csv, nonames delimiter(";") clear
	rename v1 id_repo 
	drop v2 
	duplicates drop 
save tmp.dta, replace

insheet using repo_dependencies_NPM-test-matchedWyss+IDs.csv, nonames delimiter(";") clear
	rename v2 id_repo 
	drop v1
	duplicates drop
append using tmp.dta 
	duplicates drop
save id_repos_dependencies.dta, replace

// ...then make sure that all of those exist in Wyss data
insheet using Wyss_npm-test_data2.csv, names delimiter(";") clear
merge 1:1 id_repo using id_repos_dependencies.dta
	keep if _merge == 3
	drop _merge
outsheet using Wyss_npm-test_data3.csv, names delimiter(";") replace

// lastly, re-generate ids so that Wyss data has consecutive numbering
insheet using Wyss_npm-test_data3.csv, names delimiter(";") clear
	sort repo
	gen id_repo_new = _n 
	order id_repo id_repo_new repo
outsheet using Wyss_npm-test_data5.csv, names delimiter(";") replace
outsheet using Master/Wyss_npm-test_data5.csv, names delimiter(";") replace
	keep id_repo id_repo_new 
save id_repo_new.dta, replace

insheet using repo_dependencies_NPM-test-matchedWyss+IDs.csv, nonames delimiter(";") clear
	rename v1 id_repo 
merge m:1 id_repo using id_repo_new.dta 
	drop if _merge == 2
	drop _merge 
	rename id_repo_new id_repo_from 
	drop id_repo
	
	rename v2 id_repo 
merge m:1 id_repo using id_repo_new.dta 
	drop if _merge == 2
	drop _merge 
	rename id_repo_new id_repo_to 
	drop id_repo
	
	sort id_repo_from id_repo_to
outsheet using repo_dependencies_NPM-test-matchedWyss+newIDs.csv, nonames delimiter(";") replace
// this is the file the network file is created with using 30_create_dependency_graph-1.6.0.py
// it does not contain bad identifiers and uses new consecutive IDs
