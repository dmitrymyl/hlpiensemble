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

Currently, the package works only under UNIX.

## How to use it 
=======
 
## Usage
The master script is `hlpiensemble.py` that allows one to run prediction from any directory. For instance, in UNIX one should do as follows:
```
export PATH=path/to/hlpiensemble:$PATH
python3 hlpiensemble.py -rna rna.fasta -protein protein.fasta -mode result -output here.csv -taskname some_task
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

## How predictions are made
The training dataset was NPInter v2.0 database of lncRNA-protein interactions. Several features are excluded from sequences and then applied to
three mainstream algorithms: RF, SVM, XGBoost.

## Execution scheme
The programme works in hlpiensemble directory. It copies sequence files (upcasing sequences and replacing Ts with Us in RNA sequence) to `path/to/hlpiensemble/task/taskname` directory. Intermediate files and prediction results are produced in the same directory. Completing prediction, programme copies `HLPI-Ensemble.csv` file to specified place in `-output` (with renaming) in case of `result` mode or move the entire directory to specified place (with renaming) in case of `full` mode. In both modes, `task/taskname` directory will be deleted.

If one consider parallel execution of hlpiensemble.py script, one should be aware of different names for tasks to prevent overwriting of results.

## Output
The output is `.csv` file containing probabilities of interaction predicted by each algorithm for each pair of RNA and protein.

## Contributions
The initial author Fule Liu developed most of the prediction backend. [@dmitrymyl](https://github.com/dmitrymyl) adopted [web server](http://ccsipb.lnu.edu.cn/hlpiensemble/index.php) to CLI usage, including paths tweaks and master script.

## Citation
Please cite **Huan Hu, Li Zhang, Haixin Ai, Hui Zhang, Yetian Fan, Qi Zhao & Hongsheng Liu (2018) HLPI-Ensemble: Prediction of human lncRNA-protein interactions based on ensemble strategy, RNA Biology, 15:6, 797-806, DOI: 10.1080/15476286.2018.1457935** in your paper if you use this software.
