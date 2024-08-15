// ============================================================================
//
// NPM -- 1.6.0
//
// ============================================================================
// cd ~/Dropbox/Papers/10_WorkInProgress/SoftwareUpdates/Data/NPM-1.6.0Wyss/
cd ~/Downloads/NPM/

//
// PREPARATIONS
//
{
// repositories 
insheet using repositories_NPM.csv, delimiter(";") names clear
	drop if repoid=="RepoID"
	destring repoid, replace
	destring size, replace
	drop if size == 0
	destring numstars, replace
	destring numforks, replace
	destring numwatchers, replace
	destring numcontributors, replace
	
	gen double createdtime=clock( substr(createdtimestamp,1,19), "YMDhms")
	format createdtime %tc
	
	gen double lastsyncedtime=clock( substr(lastsyncedtimestamp,1,19), "YMDhms")
	format lastsyncedtime %tc
save repositories_NPM.dta, replace

// projects
insheet using "projects_NPM.csv", delimiter(";") names clear
	rename projectid id 
	rename repositoryid repoid
save "projects_NPM.dta", replace
	rename id projectid
	keep projectid repoid	
	drop if repoid == .
	duplicates drop
save projectid_repoid.dta, replace 

// versions
insheet using versions_NPM.csv, delimiter(";") names clear
save versions_NPM.dta, replace
}


//
// CUTS
//
{
use versions_NPM.dta, clear
// first merge repoids
merge m:1 projectid using projectid_repoid.dta
	keep if _merge == 3
	drop _merge
	bysort repoid: gen num_versions = _N
	
	drop versionnumber publishedtimestamp
	
	duplicates drop  // NOTE: not unique on repoid, some repoids have multiple projectids with different projectnames
	
// then merge repo-based covariates
merge m:1 repoid using repositories_NPM.dta
	// repositories that exist in master but not in using are typically projects in other programming
	// languages (managed by NPM), i.e. this is the first cut
	keep if _merge == 3  
	drop _merge 
	
// apply additional cuts
	drop if size < 10
	drop if numstars < 1000
	drop if description == ""
	drop if createdtime < clock("01jan2015 00:00:01", "DMYhms")
	drop if createdtime > clock("31dec2018 23:59:59", "DMYhms") 
save covariates_NPM-cuts.dta, replace
	keep repoid
	duplicates drop
save repoid-cuts.dta, replace
outsheet using repoid-cuts.csv, delimiter(";") nonames replace
use repoid-cuts.dta, clear
	gen id_repo_new = _n
save repoid_id_repo_new.dta, replace

// apply cuts to project mapping
use projectid_repoid.dta, clear
merge m:1 repoid using repoid-cuts.dta 
	keep if _merge == 3
	drop _merge 
save projectid_repoid-cuts.dta, replace
outsheet using projectid_repoid-cuts.csv, delimiter(";") replace
}

//
// WYSS DATA -- RELEVANT ONLY FOR NPM
// 2024-08-12: NOT used for now since match between Wyss and covariates is bad
//
{
insheet using "Wyss_npm_data.csv", delimiter(",") clear
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
save "Wyss_npm_data.dta", replace

use Wyss_npm_data.dta, clear
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
save Wyss_npm_data2.dta, replace
outsheet using Wyss_npm_data2.csv, delimiter(";") names replace

use Wyss_npm_data2.dta, clear
	keep repo id_repo
save repo_id_repo-Wyss.dta, replace
}


//
// REPO DEPENDENCIES -- WYSS
// 2024-08-12: NOT used for now since match between Wyss and covariates is bad
//
{
insheet using repo_dependencies_NPM-matchedWyss.csv, names delimiter(";") clear

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

outsheet using repo_dependencies_NPM-matchedWyss+IDs.csv, nonames delimiter(";") replace

// check which repos exist in the final dependencies file...
insheet using repo_dependencies_NPM-matchedWyss+IDs.csv, nonames delimiter(";") clear
	rename v1 id_repo 
	drop v2 
	duplicates drop 
save tmp.dta, replace

insheet using repo_dependencies_NPM-matchedWyss+IDs.csv, nonames delimiter(";") clear
	rename v2 id_repo 
	drop v1
	duplicates drop
append using tmp.dta 
	duplicates drop
save id_repos_dependencies.dta, replace

// ...then make sure that all of those exist in Wyss data...
insheet using Wyss_npm_data2.csv, names delimiter(";") clear
	merge 1:1 id_repo using id_repos_dependencies.dta
	keep if _merge == 3
	drop _merge
outsheet using Wyss_npm_data3.csv, names delimiter(";") replace

// ...re-generate ids so that Wyss data has consecutive numbering
insheet using Wyss_npm_data3.csv, names delimiter(";") clear
	sort repo
	gen id_repo_new = _n 
	order id_repo id_repo_new repo
outsheet using Wyss_npm_data5.csv, names delimiter(";") replace
outsheet using Master/Wyss_npm_data5.csv, names delimiter(";") replace
	keep id_repo id_repo_new 
save id_repo_new.dta, replace

// ...and re-label repo dependencies
insheet using repo_dependencies_NPM-matchedWyss+IDs.csv, nonames delimiter(";") clear
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
outsheet using repo_dependencies_NPM-matchedWyss+newIDs.csv, nonames delimiter(";") replace
// this is the file the network is created with using 30_create_dependency_graph.py
// it does not contain bad identifiers and uses new consecutive IDs
}


//
// HOOK #1: REPO DEPENDENCIES -- CUTS
//
{
// replace with consecutive IDs
insheet using repo_dependencies_NPM-cuts.csv, delimiter(";") names clear
	rename from_repo repoid 
merge m:1 repoid using repoid_id_repo_new.dta 
	drop if _merge != 3
	drop _merge 
	rename id_repo_new id_from_repo_new
	drop repoid 
	
	rename to_repo repoid 
merge m:1 repoid using repoid_id_repo_new.dta 
	drop if _merge != 3
	drop _merge 
	rename id_repo_new id_to_repo_new 
	drop repoid
	
	drop if id_from_repo_new == id_to_repo_new // not sure why there are self-links, but likely from project -> repo consolidation
outsheet using repo_dependencies_NPM-cuts+newIDs.csv, delimiter(";") nonames replace
}  // now we can run 30_create_dependency_graph.py
