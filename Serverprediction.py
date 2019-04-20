# python3.6
# coding:utf-8
import argparse
import sys
from subprocess import run, PIPE
from time import time


def geneErrorLog(msg):
    filepath = wd + "error.log"
    file = open(filepath, "a")
    file.write(str(msg) + "\n")
    file.close()


def taskprogress(p):
    filepath = wd + "taskprogress.log"
    file = open(filepath, "a")
    file.write(str(p) + "\n")
    file.close()


def getNameListBySeq(fastafilepath):
    NameList = list()
    with open(fastafilepath, 'r') as fastafile:
        for line in fastafile:
            if line.startswith(">"):
                NameList.append(line.rstrip()[1:])
    return NameList


def setName4Featurecsv(NameList, csvfilepath):
    with open(csvfilepath, "r") as csvfile:
        csvfilelines = csvfile.readlines()
        lines = []
        for line in csvfilelines:
            lines.append(line)
    no = len(NameList)
    csvfilenewcont = ""
    for i in range(no):
        templine = NameList[i] + "," + lines[i]
        csvfilenewcont += templine
    with open(csvfilepath, "w") as csvfile:
        csvfile.write(csvfilenewcont)


def csv2list(csvfilepath):
    with open(csvfilepath) as csvfile:
        csvfilelines = csvfile.readlines()
        lines = []
        for line in csvfilelines:
            lines.append(line)
        lines = lines[1:]
    resultlist = []
    for line in lines:
        templist = str(line).replace("\r", "").replace("\n", "").replace('"', '').split(",")
        if len(templist) > 1:
            resultlist.append({"lncRNA": templist[1], "protein": templist[2], "prob": templist[3]})
    return resultlist


def formatresult2html(SVMresultlist, RFresultlist, XGBresultlist):
    no = len(SVMresultlist)
    table = ""
    tableheader = '<table class="highlight centered"><thead><tr><th>lncRNA</th><th>protein</th><th>HLPI-SVM Ensemble</th><th>HLPI-RF Ensemble</th><th>HLPI-XGB Ensemble</th><th>Comprehensive evaluation</th></tr></thead><tbody>'
    tablecont = ""
    tabletail = "</tbody></table>"
    for i in range(no):
        svmprob = str("%.4f" % float(SVMresultlist[i]["prob"]))
        rfprob = str("%.4f" % float(RFresultlist[i]["prob"]))
        xgbprob = str("%.4f" % float(XGBresultlist[i]["prob"]))
        evaluation = "No significant interaction"
        if float(xgbprob) >= 0.8:
            if float(rfprob) <= 0.8 and float(svmprob) <= 0.8:
                evaluation = "No significant interaction"
            else:
                evaluation = "Interaction"
        else:
            if float(rfprob) > 0.8 and float(svmprob) > 0.8:
                evaluation = "Interaction"
            else:
                evaluation = "No significant interaction"
        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (SVMresultlist[i]["lncRNA"],SVMresultlist[i]["protein"],svmprob,rfprob,xgbprob,evaluation)
        tablecont += line
    table = tableheader + tablecont + tabletail
    htmlfilepath = wd + "result.html"
    with open(htmlfilepath, "w") as htmlfile:
        htmlfile.write(table)


def geneDownloadfile(SVMresultlist, RFresultlist, XGBresultlist, threshold=0.8):
    no = len(SVMresultlist)
    tablecont = ""
    tableheader = "lncRNA,protein,HLPI-SVM Ensemble,HLPI-RF Ensemble,HLPI-XGB Ensemble,Comprehensive evaluation\n"
    for i in range(no):
        svmprob = str("%.4f" % float(SVMresultlist[i]["prob"]))
        rfprob = str("%.4f" % float(RFresultlist[i]["prob"]))
        xgbprob = str("%.4f" % float(XGBresultlist[i]["prob"]))
        evaluation = "No significant interaction"
        if (float(xgbprob) >= threshold):
            if (float(rfprob) <= threshold and float(svmprob) <= threshold):
                evaluation = "No significant interaction"
            else:
                evaluation = "Interaction"
        else:
            if (float(rfprob) > threshold and float(svmprob) > threshold):
                evaluation = "Interaction"
            else:
                evaluation = "No significant interaction"
        line = "%s,%s,%s,%s,%s,%s\n" % (SVMresultlist[i]["lncRNA"], SVMresultlist[i]["protein"], svmprob, rfprob, xgbprob, evaluation)
        tablecont += line
    table = tableheader + tablecont
    filepath = wd + "HLPI-Ensemble.csv"
    filecont = table
    with open(filepath, "w") as resultfile:
        resultfile.write(filecont)


def timelog(msg, file, mode=False):
    if mode:
        with open(file, 'a') as timefile:
            timefile.write(str(msg))


def time_func(func, *args, **kwargs):
    start = time()
    result = func(*args, **kwargs)
    end = time()
    timing = end - start
    return result, timing


parser = argparse.ArgumentParser(description='Performs prediction of RNA-protein interactions.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-taskid', nargs='?', type=str, dest='taskid', help='task id')
parser.add_argument('-cores', nargs='?', type=int, default=1, dest='cores', help='number of cores to use')
parser.add_argument('--timing', action='store_true', dest='timing', help='whether to profile the execution time or not')
args = parser.parse_args()
wd = "./task/"
psewd = "./pse/"
taskid = args.taskid
wd += taskid + "/"
timefile = wd + 'timelog.tsv'
try:
    result, timing = time_func(run, f"python kmer.py .{wd}lncRNAseq.fasta .{wd}lncRNAFeature_kmer.csv RNA -k 2 -f csv",
                               shell=True, stdin=PIPE, stdout=PIPE, cwd=psewd)
    timelog(f"RNA:kmer:{timing}\n", timefile, mode=args.timing)
    result, timing = time_func(run, f"python acc.py .{wd}lncRNAseq.fasta .{wd}lncRNAFeature_DAC.csv RNA DAC -lag 2 -all_index -f csv",
                               shell=True, stdin=PIPE, stdout=PIPE, cwd=psewd)
    timelog(f"RNA:acc:{timing}\n", timefile, mode=args.timing)
    result, timing = time_func(run, f"python pse.py .{wd}lncRNAseq.fasta .{wd}lncRNAFeature_PC-PseDNC-General.csv RNA PC-PseDNC-General -all_index -f csv",
                               shell=True, stdin=PIPE, stdout=PIPE, cwd=psewd)
    timelog(f"RNA:pse:{timing}\n", timefile, mode=args.timing)
except BaseException:
    geneErrorLog("An error occurred while generating the lncRNA features.#1 %s")
    sys.exit(0)
taskprogress(10)
lncRNAseqNameList = []
try:
    lncRNAseqNameList = getNameListBySeq(wd + "lncRNAseq.fasta")
    # setName4Featurecsv(lncRNAseqNameList,wd+"lncRNAFeature_kmer.csv")
    # setName4Featurecsv(lncRNAseqNameList,wd+"lncRNAFeature_DAC.csv")
    # setName4Featurecsv(lncRNAseqNameList,wd+"lncRNAFeature_PC-PseDNC-General.csv")
except BaseException:
    geneErrorLog("An error occurred while generating the lncRNA features.#2")
    sys.exit(0)
taskprogress(15)
try:
    result, timing = time_func(run, f"python kmer.py .{wd}proteinseq.fasta .{wd}proteinFeature_kmer.csv Protein -k 2 -f csv",
                               shell=True, stdin=PIPE, stdout=PIPE, cwd=psewd)
    timelog(f"protein:kmer:{timing}\n", timefile, mode=args.timing)
    result, timing = time_func(run, f"python acc.py .{wd}proteinseq.fasta .{wd}proteinFeature_AC.csv Protein AC -lag 2 -all_index -f csv",
                               shell=True, stdin=PIPE, stdout=PIPE, cwd=psewd)
    timelog(f"protein:acc:{timing}\n", timefile, mode=args.timing)
    result, timing = time_func(run, f"python pse.py .{wd}proteinseq.fasta .{wd}proteinFeature_PC-PseAAC-General.csv Protein PC-PseAAC-General -all_index -f csv",
                               shell=True, stdin=PIPE, stdout=PIPE, cwd=psewd)
    timelog(f"protein:pse:{timing}\n", timefile, mode=args.timing)
except BaseException:
    geneErrorLog("An error occurred while generating the protein features.#1")
    sys.exit(0)
taskprogress(25)
proteinseqNameList = []
try:
    proteinseqNameList = getNameListBySeq(wd + "proteinseq.fasta")
    # setName4Featurecsv(proteinseqNameList,wd+"proteinFeature_kmer.csv")
    # setName4Featurecsv(proteinseqNameList,wd+"proteinFeature_AC.csv")
    # setName4Featurecsv(proteinseqNameList,wd+"proteinFeature_PC-PseAAC-General.csv")
except BaseException:
    geneErrorLog("An error occurred while generating the protein features.#2")
    sys.exit(0)
taskprogress(30)
lncRNANameListfilepath = wd + "lncRNANameList.csv"
lncRNANameListfilecont = ""
for lncRNAName in lncRNAseqNameList:
    lncRNANameListfilecont += lncRNAName + "\n"
with open(lncRNANameListfilepath, "w") as lncRNANameListfile:
    lncRNANameListfile.write(lncRNANameListfilecont)
taskprogress(40)
proteinNameListfilepath = wd + "proteinNameList.csv"
proteinNameListfilecont = ""
for proteinName in proteinseqNameList:
    proteinNameListfilecont += proteinName + "\n"
with open(proteinNameListfilepath, "w") as proteinNameListfile:
    proteinNameListfile.write(proteinNameListfilecont)
taskprogress(45)
pairsfilepath = wd + "pairs.csv"
pairstext = "ncRNA,protein\n"
for lncRNAName in lncRNAseqNameList:
    for proteinName in proteinseqNameList:
        pairstext += lncRNAName + "," + proteinName + "\n"
with open(pairsfilepath, "w") as pairsfile:
    pairsfile.write(pairstext)
taskprogress(50)
try:
    result, timing = time_func(run, f"Rscript ./models/Featurecombination.r {taskid} {args.cores}", shell=True, stdin=PIPE, stdout=PIPE)
    timelog(f"predict:featurecombination:{timing}\n", timefile, mode=args.timing)
except BaseException:
    geneErrorLog("An error occurred while generating the feature combination.")
    sys.exit(0)
taskprogress(55)
try:
    result, timing = time_func(run, f"Rscript ./models/SVMavg.r {taskid} {args.cores}", shell=True, stdin=PIPE, stdout=PIPE)
    timelog(f"predict:svm:{timing}\n", timefile, mode=args.timing)
except BaseException:
    geneErrorLog("The error occurred when using the Support Vector Machines Ensemble model.")
    sys.exit(0)
taskprogress(70)
try:
    result, timing = time_func(run, f"Rscript ./models/RFavg.r {taskid} {args.cores}", shell=True, stdin=PIPE, stdout=PIPE)
    timelog(f"predict:rf:{timing}\n", timefile, mode=args.timing)
except BaseException:
    geneErrorLog("The error occurred when using the Random Forest Ensemble model.")
    sys.exit(0)
taskprogress(85)
try:
    result, timing = time_func(run, f"Rscript ./models/XGBavg.r {taskid} {args.cores}", shell=True, stdin=PIPE, stdout=PIPE)
    timelog(f"predict:xgb:{timing}\n", timefile, mode=args.timing)
except BaseException:
    geneErrorLog("The error occurred when using the XGBoost Ensemble model.")
    sys.exit(0)
taskprogress(95)
try:
    SVMavgresultlist = csv2list(wd + "SVMavg.csv")
    RFavgresultlist = csv2list(wd + "RFavg.csv")
    XGBavgresultlist = csv2list(wd + "XGBavg.csv")
    formatresult2html(SVMavgresultlist, RFavgresultlist, XGBavgresultlist)
    geneDownloadfile(SVMavgresultlist, RFavgresultlist, XGBavgresultlist)
except BaseException:
    geneErrorLog("The error occurred after all the constructed.")
    sys.exit(0)
taskprogress(100)
