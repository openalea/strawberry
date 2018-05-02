################################################################################
#                     Fraflo: Architecture study                               #
#                 ---------------------------------                            #
#                                                                              #
#                    Extraction of MTG dataframe                               #
#                 ---------------------------------                            #
#                      Marc LABADIE 2014                                       #
#                                                                              #
################################################################################

# 1.Packages installation
installed.packages("plotrix")
installed.packages("RODBC")
installed.packages("agricolae")
installed.packages("gplots")
installed.packages("graphics")
installed.packages("mclust")
installed.packages("FactoMineR")
installed.packages("agricolae")
installed.packages("plyr")
installed.packages("ggplot2")
installed.packages("corrplot")
installed.packages("grid")
installed.packages("gridExtra")
installed.packages("igraph")
installed.packages("RColorBrewer")
installed.packages("qgraph")
installed.packages("reshape")

# 2. Packages loading
library(plotrix)
library(RODBC)
library(agricolae)
library(gplots)
library(graphics)
library(mclust)
library(FactoMineR)
library(agricolae)
library(plyr)
library(ggplot2)
library(corrplot)
library(grid)
library(gridExtra)
library(igraph)
library(RColorBrewer)
library(qgraph)
library(reshape)

caprisstest <- read.csv("Z:/G1/Marc-Labadie/Python/strawberry/example/Data.csv")
str(object = caprisstest)
caprisstest$date <-as.Date(caprisstest$date,format="%d-%m-%Y")


#Selection of data
F<- caprisstest[caprisstest$label=="F",] #Data developed leaves
f<- caprisstest[caprisstest$label=="f",] # Data primordia leaves
bt<- caprisstest[caprisstest$label=='bt',] # Data terminal bud
HT<- caprisstest[caprisstest$label=='HT',] #Data Inflorescence
ht<- caprisstest[caprisstest$label=='ht',] #Data primordia inflorescence
s<-caprisstest[caprisstest$label=='s',]

#Count number of leaves by Genotype Plante,date,order
F.n<-ddply(F,c("Genotype","Plante","date","order"),summarize,F_number=length(na.omit(label)))
f.n<-ddply(f,c("Genotype","Plante","date","order"),summarize,f_number=length(na.omit(label)))
bt.n<-ddply(bt,c("Genotype","Plante","date","order"),summarize,bt_number=length(na.omit(label)))
HT.n<-ddply(HT,c("Genotype","Plante","date","order"),summarize,HT_number=length(na.omit(label)))
ht.n<-ddply(ht,c("Genotype","Plante","date","order"),summarize,ht_number=length(na.omit(label)))
s.n<-ddply(s,c("Genotype","Plante","date","order"),summarize,s_number=length(na.omit(label)))



# Data function of organs
Data_leaves<- merge(x = F.n,y = f.n,by = c("Genotype","Plante","date","order"), all.x = T,all.y = T)
Data_leaves[is.na(Data_leaves$F_number),"F_number"]<- 0 # replace NA by 0 in F_number column
Data_leaves[is.na(Data_leaves$f_number),"f_number"]<- 0 # replace NA by 0 in f_number column
Data_leaves$total_leaves<- Data_leaves$F_number + Data_leaves$f_number #Add new column total leaves which is sum(F_number and f_number)

Data_Inflorescence<- merge(x = HT.n,y = ht.n,by = c("Genotype","Plante","date","order"), all.x = T,all.y = T)
Data_Inflorescence[is.na(Data_Inflorescence$HT_number),"HT_number"]<- 0 
Data_Inflorescence[is.na(Data_Inflorescence$ht_number),"ht_number"]<- 0 
Data_Inflorescence$total_Inflorescence<- Data_Inflorescence$HT_number + Data_Inflorescence$ht_number 

#Data final with all organs
Data<- merge(Data_leaves,Data_Inflorescence, by = c("Genotype","Plante","date","order"), all.x = T, all.y = T)
Data<- merge(Data, bt.n, by = c("Genotype","Plante","date","order"),all.x = T, all.y = T )
Data<-merge(Data,s.n,by=c("Genotype","Plante","date","order"),all=T)
Data[is.na(Data$F_number),"F_number"]<-0
Data[is.na(Data$f_number),"f_number"]<-0
Data[is.na(Data$total_leaves),"total_leaves"]<-0
Data[is.na(Data$HT_number),"HT_number"]<-0
Data[is.na(Data$ht_number),"ht_number"]<-0
Data[is.na(Data$total_Inflorescence),"total_Inflorescence"]<-0
Data[is.na(Data$bt_number),"bt_number"]<-0
Data[is.na(Data$s_number),"s_number"]<-0

View(Data)





 
