#获取参数
Args<-commandArgs(TRUE)
taskid<-Args[1]
#设置工作目录
setwd(paste0("/var/www/html/hlpiensemble/task/",taskid,"/"))
#读取数据
kmer_kmer<-read.csv("data_lncRNAkmer_proteinkmer.csv")
kmer_AC<-read.csv("data_lncRNAkmer_proteinAC.csv")
kmer_PseAACGeneral<-read.csv("data_lncRNAkmer_proteinPC-PseAAC-General.csv")
DAC_kmer<-read.csv("data_lncRNADAC_proteinkmer.csv")
DAC_AC<-read.csv("data_lncRNADAC_proteinAC.csv")
DAC_PseAACGeneral<-read.csv("data_lncRNADAC_proteinPC-PseAAC-General.csv")
PCPseDNCGeneral_kmer<-read.csv("data_lncRNAPC-PseDNC-General_proteinkmer.csv")
PCPseDNCGeneral_AC<-read.csv("data_lncRNAPC-PseDNC-General_proteinAC.csv")
PCPseDNCGeneral_PseAACGeneral<-read.csv("data_lncRNAPC-PseDNC-General_proteinPC-PseAAC-General.csv")

kmer_kmer<-kmer_kmer[,c(-1,-2,-3)]
kmer_AC<-kmer_AC[,c(-1,-2,-3)]
kmer_PseAACGeneral<-kmer_PseAACGeneral[,c(-1,-2,-3)]
DAC_kmer<-DAC_kmer[,c(-1,-2,-3)]
DAC_AC<-DAC_AC[,c(-1,-2,-3)]
DAC_PseAACGeneral<-DAC_PseAACGeneral[,c(-1,-2,-3)]
PCPseDNCGeneral_kmer<-PCPseDNCGeneral_kmer[,c(-1,-2,-3)]
PCPseDNCGeneral_AC<-PCPseDNCGeneral_AC[,c(-1,-2,-3)]
PCPseDNCGeneral_PseAACGeneral<-PCPseDNCGeneral_PseAACGeneral[,c(-1,-2,-3)]

library(caret)
load(file="/var/www/html/hlpiensemble/models/FinalXGB.Rdata")

#kmer_kmer.pred.raw <- predict(FinalXGB_kmer_kmer.Fit, newdata=kmer_kmer, type = "raw")
kmer_kmer.pred.prob <- predict(FinalXGB_kmer_kmer.Fit, newdata=kmer_kmer, type = "prob")
#kmer_AC.pred.raw <- predict(FinalXGB_kmer_AC.Fit, newdata=kmer_AC, type = "raw")
kmer_AC.pred.prob <- predict(FinalXGB_kmer_AC.Fit, newdata=kmer_AC, type = "prob")
#kmer_PseAACGeneral.pred.raw <- predict(FinalXGB_kmer_PseAACGeneral.Fit, newdata=kmer_PseAACGeneral, type = "raw")
kmer_PseAACGeneral.pred.prob <- predict(FinalXGB_kmer_PseAACGeneral.Fit, newdata=kmer_PseAACGeneral, type = "prob")
#DAC_kmer.pred.raw <- predict(FinalXGB_DAC_kmer.Fit, newdata=DAC_kmer, type = "raw")
DAC_kmer.pred.prob <- predict(FinalXGB_DAC_kmer.Fit, newdata=DAC_kmer, type = "prob")
#DAC_AC.pred.raw <- predict(FinalXGB_DAC_AC.Fit, newdata=DAC_AC, type = "raw")
DAC_AC.pred.prob <- predict(FinalXGB_DAC_AC.Fit, newdata=DAC_AC, type = "prob")
#DAC_PseAACGeneral.pred.raw <- predict(FinalXGB_DAC_PseAACGeneral.Fit, newdata=DAC_PseAACGeneral, type = "raw")
DAC_PseAACGeneral.pred.prob <- predict(FinalXGB_DAC_PseAACGeneral.Fit, newdata=DAC_PseAACGeneral, type = "prob")
#PCPseDNCGeneral_kmer.pred.raw <- predict(FinalXGB_PCPseDNCGeneral_kmer.Fit, newdata=PCPseDNCGeneral_kmer, type = "raw")
PCPseDNCGeneral_kmer.pred.prob <- predict(FinalXGB_PCPseDNCGeneral_kmer.Fit, newdata=PCPseDNCGeneral_kmer, type = "prob")
#PCPseDNCGeneral_AC.pred.raw <- predict(FinalXGB_PCPseDNCGeneral_AC.Fit, newdata=PCPseDNCGeneral_AC, type = "raw")
PCPseDNCGeneral_AC.pred.prob <- predict(FinalXGB_PCPseDNCGeneral_AC.Fit, newdata=PCPseDNCGeneral_AC, type = "prob")
#PCPseDNCGeneral_PseAACGeneral.pred.raw <- predict(FinalXGB_PCPseDNCGeneral_PseAACGeneral.Fit, newdata=PCPseDNCGeneral_PseAACGeneral, type = "raw")
PCPseDNCGeneral_PseAACGeneral.pred.prob <- predict(FinalXGB_PCPseDNCGeneral_PseAACGeneral.Fit, newdata=PCPseDNCGeneral_PseAACGeneral, type = "prob")

#平均策略预测
avg.pred.prob.P<-(kmer_kmer.pred.prob$P+kmer_AC.pred.prob$P+kmer_PseAACGeneral.pred.prob$P+DAC_kmer.pred.prob$P+DAC_AC.pred.prob$P+DAC_PseAACGeneral.pred.prob$P+PCPseDNCGeneral_kmer.pred.prob$P+PCPseDNCGeneral_AC.pred.prob$P+PCPseDNCGeneral_PseAACGeneral.pred.prob$P)/9.0
kmer_kmer<-read.csv("data_lncRNAkmer_proteinkmer.csv")
pred.result<-cbind(kmer_kmer[,c(2,3)],avg.pred.prob.P)
names(pred.result)<-c("lncRNA","protein","XGB")
write.csv(pred.result,file="XGBavg.csv")