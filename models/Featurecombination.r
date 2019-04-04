Args<-commandArgs(TRUE)
taskid<-Args[1]
setwd(paste0("/var/www/html/hlpiensemble/task/",taskid,"/"))
library(dplyr)
#ncRNA特征类型向量
ncRNAFeatureClassNameList <- c("kmer","DAC","PC-PseDNC-General")
#protein特征类型向量
proteinFeatureClassNameList <- c("kmer","AC","PC-PseAAC-General")
#读取ncRNA名称列表
ncRNANameList<-read.csv("lncRNANameList.csv",header = FALSE)
#读取protein名称列表
proteinNameList <- read.csv("proteinNameList.csv",header = FALSE)
#读取训练数据的名称和标签列表
traindataNameAndLabelList <- read.csv("pairs.csv")
for(ncRNAFeatureClassName in ncRNAFeatureClassNameList){
    for(proteinFeatureClassName in proteinFeatureClassNameList){
        #读取ncRNA的某个特征类别文件
        ncRNAFeatureList<-read.csv(paste("lncRNAFeature_",ncRNAFeatureClassName,".csv",sep =''),header = FALSE)
        #将ncRNA名称添加到该特征类别
        ncRNAFeatureList<-cbind(ncRNANameList,ncRNAFeatureList)
        #赋列名
        colnames(ncRNAFeatureList) <- c('ncRNA', rownames(seq(1,ncol(ncRNAFeatureList)-1), do.NULL = FALSE, prefix = "nc"))
        
        #读取protein的某个特征类别文件
        proteinFeatureList<-read.csv(paste("proteinFeature_",proteinFeatureClassName,".csv",sep =''),header = FALSE)
        #将protein名称添加到该特征类别
        proteinFeatureList<-cbind(proteinNameList,proteinFeatureList)
        #赋列名
        colnames(proteinFeatureList) <- c('protein', rownames(seq(1,ncol(proteinFeatureList)-1), do.NULL = FALSE, prefix = "pro"))
        
        #将ncRNA添加到训练数据
        traindata <- left_join(traindataNameAndLabelList, ncRNAFeatureList, by = c("ncRNA"))
        #将protein添加到训练数据
        traindata <- left_join(traindata, proteinFeatureList, by = c("protein"))
        #输出训练数据
        write.csv(traindata,paste("data_lncRNA",ncRNAFeatureClassName,"_protein",proteinFeatureClassName,".csv",sep=''))
    }
}