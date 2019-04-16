import os
import sys
import argparse
from subprocess import run


def retrieve_rna(rna_input, rna_output):
    with open(rna_input, 'r') as infile:
        with open(rna_output, 'w') as outfile:
            for line in infile:
                if line[0] == "\n":
                    continue
                if line[0] != ">":
                    line = line.upper().replace("T", "U")
                outfile.write(line)


def retrieve_protein(protein_input, protein_output):
    with open(protein_input, 'r') as infile:
        with open(protein_output, 'w') as outfile:
            for line in infile:
                if line[0] == "\n":
                    continue
                if line[0] != ">":
                    line = line.upper()
                outfile.write(line)


argparser = argparse.ArgumentParser(description='Master script for hlpiensemble.')
argparser.add_argument("-rna", nargs="?", type=str, dest='rna', help='fasta file with RNAs')
argparser.add_argument("-protein", nargs='?', type=str, dest='protein', help='fasta file with proteins')
argparser.add_argument("-mode", nargs='?', type=str, dest='mode', choices=['result', 'full'], default='result', help='output mode to provide: only result file (result, default) or full directory (full)')
argparser.add_argument("-output", nargs="?", type=str, dest='output', help='if mode=result, name of output file, if mode=full, name of output directory')
argparser.add_argument("-taskname", nargs="?", type=str, dest='taskname', default='some_task', help='task name, optional')
argparser.add_argument("-cores", nargs="?", type=int, dest='cores', default=1, help='number of cores to use (default: 1)')
args = argparser.parse_args()
source_path = os.path.abspath(os.path.dirname(sys.argv[0]))
taskdir = source_path + "/task/" + args.taskname
if not os.path.exists(taskdir):
    os.mkdir(taskdir)
retrieve_rna(args.rna, taskdir + "/lncRNAseq.fasta")
retrieve_protein(args.protein, taskdir + "/proteinseq.fasta")
run(["python", "Serverprediction.py", "-taskid", args.taskname, "-cores", str(args.cores)], cwd=source_path)
if args.mode == "result":
    run(["cp", f"{taskdir}/HLPI-Ensemble.csv", args.output])
    run(["rm", "-r", taskdir])
else:
    run(["mv", taskdir, args.output])
