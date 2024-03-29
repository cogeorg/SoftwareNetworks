## Summary
This is the repository for "Software Networks" by Co-Pierre Georg and Angelo Mele. It roughly follows the <a href="https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow">gitflow</a> workflow and uses several branches that correspond to stable states of the development and, eventually, to different versions of the paper. 

## Branches
The repository includes the following branches:
- main: The main development branch where things are in motion and might break.
- v0.1: A first stable branch corresponding to a full test run of highly stylized sample data.

## Data
The raw data can easily be downloaded from <a href="https://zenodo.org/record/2536573/files/Libraries.io-open-data-1.4.0.tar.gz">libraries.io</a>, but for replicability, you can also find the downloaded and pre-processed data in our <a href="https://www.dropbox.com/sh/29ditj5ulup6s96/AAC0n0naMm_w4PVAhwO3jm_aa?dl=0">Dropbox</a> which also contains the necessary folders our code needs. The following folders from our Dropbox are relevant:
```
Data/
+ backup/
+ libraries-1.4.0-2018-12-22/
+ npm/
+ test1/
Production/
+ dependencies/
+ dependencies-restricted/
```
Where `libraries-1.4.0-2018-12-22/` contains the raw data, `test1/` contains sample data for the first step of debugging, and `npm/` contains our processed dataset, including `enc_sampled-x_dependencies_npm-merged.dat` files, where `x` indicates what percentage of the full dataset has been sampled. These files are used primarily for testing and debugging on realistic but more manageable small datasets.

