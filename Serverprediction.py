#python3.6
#coding:utf-8
#import uuid #unused
import subprocess
#import re # unused
#import json # unused
#import os # unused
#import time # unused
#import thread # unused
#import shutil # unused
#import pickle # unused
import sys


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
    csvfile = open(csvfilepath, "r")
    csvfilelines = csvfile.readlines()
    lines = []
    for line in csvfilelines:
        lines.append(line)
    csvfile.close()
    no = len(NameList)
    csvfilenewcont = ""
    for i in range(no):
        templine = NameList[i] + "," + lines[i]
        csvfilenewcont += templine
    csvfile = open(csvfilepath, "w")
    csvfile.write(csvfilenewcont)
    csvfile.close()


def csv2list(csvfilepath):
    csvfile = open(csvfilepath)
    csvfilelines = csvfile.readlines()
    lines = []
    for line in csvfilelines:
        lines.append(line)
    lines = lines[1:]
    csvfile.close()
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
    htmlcont = table
    htmlfile = open(htmlfilepath, "w")
    htmlfile.write(htmlcont)
    htmlfile.close()


def geneDownloadfile(SVMresultlist, RFresultlist, XGBresultlist):
    no = len(SVMresultlist)
    tablecont = ""
    tableheader = "lncRNA,protein,HLPI-SVM Ensemble,HLPI-RF Ensemble,HLPI-XGB Ensemble,Comprehensive evaluation\n"
    for i in range(no):
        svmprob = str("%.4f" % float(SVMresultlist[i]["prob"]))
        rfprob = str("%.4f" % float(RFresultlist[i]["prob"]))
        xgbprob = str("%.4f" % float(XGBresultlist[i]["prob"]))
        evaluation = "No significant interaction"
        if (float(xgbprob)>=0.8):
            if (float(rfprob)<=0.8 and float(svmprob)<=0.8):
                evaluation = "No significant interaction"
            else:
                evaluation = "Interaction"
        else:
            if (float(rfprob)>0.8 and float(svmprob)>0.8):
                evaluation = "Interaction"
            else:
                evaluation = "No significant interaction"
        line = "%s,%s,%s,%s,%s,%s\n" % (SVMresultlist[i]["lncRNA"], SVMresultlist[i]["protein"], svmprob, rfprob, xgbprob, evaluation)
        tablecont += line
    table = tableheader + tablecont
    filepath = wd + "HLPI-Ensemble.csv"
    filecont = table
    resultfile = open(filepath, "w")
    resultfile.write(filecont)
    resultfile.close()


wd = "./task/"
psewd = "./pse/"
taskid = str(sys.argv[1])
wd += taskid + "/"
try:
    kmer = f"python kmer.py .{wd}lncRNAseq.fasta .{wd}lncRNAFeature_kmer.csv RNA -k 2 -f csv"
    acc = f"python acc.py .{wd}lncRNAseq.fasta .{wd}lncRNAFeature_DAC.csv RNA DAC -lag 2 -all_index -f csv"
    pse = f"python pse.py .{wd}lncRNAseq.fasta .{wd}lncRNAFeature_PC-PseDNC-General.csv RNA PC-PseDNC-General -all_index -f csv"
    child = subprocess.Popen(kmer, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=psewd)
    child.communicate()
    child = subprocess.Popen(acc, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=psewd)
    child.communicate()
    child = subprocess.Popen(pse, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=psewd)
    child.communicate()
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
    kmer = f"python kmer.py .{wd}proteinseq.fasta .{wd}proteinFeature_kmer.csv Protein -k 2 -f csv"
    acc = f"python acc.py .{wd}proteinseq.fasta .{wd}proteinFeature_AC.csv Protein AC -lag 2 -all_index -f csv"
    pse = f"python pse.py .{wd}proteinseq.fasta .{wd}proteinFeature_PC-PseAAC-General.csv Protein PC-PseAAC-General -all_index -f csv"
    child = subprocess.Popen(kmer, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=psewd)
    child.communicate()
    child = subprocess.Popen(acc, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=psewd)
    child.communicate()
    child = subprocess.Popen(pse, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=psewd)
    child.communicate()
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
lncRNANameListfile = open(lncRNANameListfilepath, "w")
lncRNANameListfile.write(lncRNANameListfilecont)
lncRNANameListfile.close()
taskprogress(40)
proteinNameListfilepath = wd + "proteinNameList.csv"
proteinNameListfilecont = ""
for proteinName in proteinseqNameList:
    proteinNameListfilecont += proteinName + "\n"
proteinNameListfile = open(proteinNameListfilepath, "w")
proteinNameListfile.write(proteinNameListfilecont)
proteinNameListfile.close()
taskprogress(45)
pairsfilepath = wd + "pairs.csv"
pairstext = "ncRNA,protein\n"
for lncRNAName in lncRNAseqNameList:
    for proteinName in proteinseqNameList:
        pairstext += lncRNAName + "," + proteinName + "\n"
pairsfile = open(pairsfilepath, "w")
pairsfile.write(pairstext)
pairsfile.close()
taskprogress(50)
try:
    fc = "Rscript ./models/Featurecombination.r " + taskid # checked
    child = subprocess.Popen(fc, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    child.communicate()
except BaseException:
    geneErrorLog("An error occurred while generating the feature combination.")
    sys.exit(0)
taskprogress(55)
try:
    fc = "Rscript ./models/SVMavg.r " + taskid # checked
    child = subprocess.Popen(fc, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    child.communicate()
except BaseException:
    geneErrorLog("The error occurred when using the Support Vector Machines Ensemble model.")
    sys.exit(0)
taskprogress(70)
try:
    fc = "Rscript ./models/RFavg.r " + taskid # checked
    child = subprocess.Popen(fc, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    child.communicate()
except BaseException:
    geneErrorLog("The error occurred when using the Random Forest Ensemble model.")
    sys.exit(0)
taskprogress(85)
try:
    fc = "Rscript ./models/XGBavg.r " + taskid # checked
    child = subprocess.Popen(fc, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    child.communicate()
except BaseException:
    geneErrorLog("The error occurred when using the XGBoost Ensemble model.")
    sys.exit(0)
taskprogress(95)
# if not (os.path.exists(wd+"SVMavg.csv") and os.path.exists(wd+"RFavg.csv") and os.path.exists(wd+"XGBavg.csv")):
#     geneErrorLog("The error occurred after all the ensemble models were constructed.")
try:
    SVMavgresultlist = csv2list(wd + "SVMavg.csv")
    RFavgresultlist = csv2list(wd + "RFavg.csv")
    XGBavgresultlist = csv2list(wd + "XGBavg.csv")
    formatresult2html(SVMavgresultlist, RFavgresultlist, XGBavgresultlist)
    geneDownloadfile(SVMavgresultlist, RFavgresultlist, XGBavgresultlist)
except BaseException:
    geneErrorLog("The error occurred after all the constructed.")
    sys.exit(0)
# if not (os.path.exists(wd+"result.html")):
#     geneErrorLog("The error occurred after all the constructed.")
taskprogress(100)
