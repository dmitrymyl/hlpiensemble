# HLPI-Ensemble
A tool for predicting lncRNA-protein interaction from sequences. Based on http://ccsipb.lnu.edu.cn/hlpiensemble/index.php web server.
## Requirements
The package was tested under following dependencies:

Package | Version
--- | ---
python | 3.6.7
R | 3.5.1
R::dplyr | 0.7.8
R::caret | 6.0.82
R::randomForest | 4.6.14
R::xgboost | 0.82.1
R::kernlab | 0.9.26
R::doParallel | 1.0.14
R::foreach | 1.4.4
R::iterators | 1.0.9

Currently, the package works only under UNIX. Windows users should suggest using WSL or Cygwin.
 
## Installation
One needs `git >= 1.8.2` and `git-lfs` to be installed to deal with large binaries at `models/*.Rdata`. Run
```
git clone https://github.com/dmitrymyl/hlpiensemble.git
```
and files will be fetched via `git` and `git lfs`. After that, the package is ready for usage.

## Usage
The master script is `hlpiensemble.py` that allows one to run prediction from any directory. One should do as follows:
```
python3 path/to/repo/hlpiensemble.py -rna rna.fasta -protein protein.fasta -mode result -output here.csv -taskname some_task
```
Command line arguments are:

argument|type|description|default
---|---|---|---
-rna|mandatory|fasta file containing one or many RNA sequences. Allowed symbols for sequences are A, T, G, C, U.|None
-protein|mandatory|fasta file containing one or many protein sequences. Allowed symbols for sequences are 20 amino acid letter.|None
-mode|optional|Mode of output. If "result", will produce a .csv file. If "full", will produce a directory with all intermediate files.|result
-output|mandatory|Name of the output file/directory.|None
-taskname|optional|Name of task|some_task
-cores|optional|Number of cores to use for prediction|1
--timing|optional|Whether to profile execution time or not|False

## How predictions are made
The training dataset was NPInter v2.0 database of lncRNA-protein interactions. Several features (named pse, kmer and acc) are exctracted from sequences and then applied to
three mainstream algorithms: RF, SVM, XGBoost.

## Execution scheme
The programme works in hlpiensemble directory. It copies sequence files (upcasing sequences and replacing Ts with Us in RNA sequence) to `path/to/hlpiensemble/task/taskname` directory. Intermediate files and prediction results are produced in the same directory. Completing prediction, programme copies `HLPI-Ensemble.csv` file to specified place in `-output` (with renaming) in case of `result` mode or move the entire directory to specified place (with renaming) in case of `full` mode. In both modes, `task/taskname` directory will be deleted.

If one consider parallel execution of hlpiensemble.py script, one should be aware of different names for tasks to prevent overwriting of results.

## Output
The output is `.csv` file containing probabilities of interaction predicted by each algorithm for each pair of RNA and protein.

## Time complexity

### Testing scheme
It is tested how the length of RNA and protein, the number of sequences and number of cores influence performance.
For length, 5 RNAs and 5 proteins are generated with length from 100 to 1000 with step 100, i.e. 10 RNA files and 10 protein files. Then all-to-all runs are performed, i.e. 100 runs.
For number, 1 to 10 RNAs and proteins of length of 100 are generated and all-to-all runs are performed, i.e. 100 runs.
For parallel processing, 10 RNAs of length of 100 and 10 proteins of length of 100 are taken and then processed with 1 to 10 cores, i.e. 10 runs.

### How to reproduce testing
For evaluating execution time one has to generate sequence samples, test them and process results. To do so, one has to do following from the package directory:
```
cd time_samples
bash generate_samples.sh
cd ../time_results
bash length.sh
bash number.sh
bash parallel.sh
```
After execution one has to run `time_results/time_results.ipynb` notebook to produce plots.

### Results
Due to 1 run per case there is lack of data and inconsistent results on time performance. It seems like length of sequences and their number do not influence execution time. However, running multiple cores in R negatively influences performance due to costs of parallelism applied.

## Contributions
The initial author Fule Liu developed most of the prediction backend. [@dmitrymyl](https://github.com/dmitrymyl) adopted [web server](http://ccsipb.lnu.edu.cn/hlpiensemble/index.php) to CLI usage, including paths tweaks and master script, parallelism and time testing.

## Citation
Please cite **Huan Hu, Li Zhang, Haixin Ai, Hui Zhang, Yetian Fan, Qi Zhao & Hongsheng Liu (2018) HLPI-Ensemble: Prediction of human lncRNA-protein interactions based on ensemble strategy, RNA Biology, 15:6, 797-806, DOI: 10.1080/15476286.2018.1457935** in your paper if you use this software.
