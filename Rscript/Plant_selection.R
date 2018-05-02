################################################################################
#                     Fraflo: Architecture study                               #
#                 ---------------------------------                            #
#             Identification of the most representative                        #
#                     plante of the population                                 #
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

#load script of Extraction dataframeMTG
source("Z:/G1/Marc-Labadie/R/R-users/FraFlo/Script/Architecture analysis/Extraction dataframeMTG.R")

#Dataframe Donnée par Génotype, date et plante
Data.Genotype.Plante<-aggregate(cbind(F_number,f_number,total_leaves,HT_number,ht_number,total_Inflorescence,
                                     bt_number,s_number)~Genotype+Plante+date,data = Data,FUN = sum)

#Fonction pour obtenir le nombre d'ordre par Genotype date et Plante
Data_order<- ddply(.data = Data,.variables = c("Genotype","Plante","date"),summarize,order_number=length(na.omit(order)))

Data.Genotype.Plante<- merge(Data.Genotype.Plante,Data_order,by=c("Genotype","Plante","date"), all = T)
#View(Data.Genotype.Plante)

# Dataframe, Median pour chaque génotype, date et Plante
Data.Genotype.median<-aggregate(cbind(F_number,f_number,total_leaves,HT_number,ht_number,total_Inflorescence,bt_number,
                                      s_number,order_number)~Genotype+date,data = Data.Genotype.Plante,FUN = median)
#View(Data.Genotype.median)

#Filtre des deux tableaux par genotype
Data.Capriss<- Data.Genotype.Plante[Data.Genotype.Plante$Genotype=="Capriss",]
Data.Capriss.med<-Data.Genotype.median[Data.Genotype.median$Genotype=="Capriss",]
Data.Ciflorette<- Data.Genotype.Plante[Data.Genotype.Plante$Genotype=="Ciflorette",]
Data.Ciflorette.med<-Data.Genotype.median[Data.Genotype.median$Genotype=="Ciflorette",]
Data.Cir107<- Data.Genotype.Plante[Data.Genotype.Plante$Genotype=="Cir107",]
Data.Cir107.med<-Data.Genotype.median[Data.Genotype.median$Genotype=="Cir107",]
Data.Clery<- Data.Genotype.Plante[Data.Genotype.Plante$Genotype=="Clery",]
Data.Clery.med<-Data.Genotype.median[Data.Genotype.median$Genotype=="Clery",]
Data.Darselect<- Data.Genotype.Plante[Data.Genotype.Plante$Genotype=="Darselect",]
Data.Darselect.med<-Data.Genotype.median[Data.Genotype.median$Genotype=="Darselect",]
Data.Gariguette<- Data.Genotype.Plante[Data.Genotype.Plante$Genotype=="Gariguette",]
Data.Gariguette.med<-Data.Genotype.median[Data.Genotype.median$Genotype=="Gariguette",]

#fonction pour calculer l'ecart median


fc.ecartmedian<-function(Data.Genotype,Data.Genotype.median,nb.ind){
  
  Data.Genotype<-Data.Genotype
  Data.Genotype.med<-Data.Genotype.median
  nb.ind=nb.ind
  
  Data.Genotype<-Data.Genotype[order(Data.Genotype[,1],Data.Genotype[,3]),]
  
  Data.Genotype.plante.ecart_med<- data.frame(matrix(nrow = nrow(Data.Genotype),ncol = ncol(Data.Genotype)))
  Data.Genotype.plante.ecart_med[1:3]<-Data.Genotype[1:3]
  colnames(Data.Genotype.plante.ecart_med)[1:ncol(Data.Genotype)]<-colnames(Data.Genotype)[1:ncol(Data.Genotype)]
  Data.Genotype.plante.ecart_med<-Data.Genotype.plante.ecart_med[order(Data.Genotype.plante.ecart_med[,1], 
                                                                      Data.Genotype.plante.ecart_med[,3]),]
  date1<-1:nb.ind
  date2<-(nb.ind+1):(nb.ind*2)
  date3<-(nb.ind*2+1):(nb.ind*3)
  date4<-(nb.ind*3+1):(nb.ind*4)
  date5<-(nb.ind*4+1):(nb.ind*5)
  date6<-(nb.ind*5+1):(nb.ind*6)
  
  
  for(i in 4:ncol(Data.Genotype)){
    Data.Genotype.plante.ecart_med[date1,i]<-abs(Data.Genotype[date1,i]-Data.Genotype.med[1,i-1])
    Data.Genotype.plante.ecart_med[date2,i]<-abs(Data.Genotype[date2,i]-Data.Genotype.med[2,i-1])
    Data.Genotype.plante.ecart_med[date3,i]<-abs(Data.Genotype[date3,i]-Data.Genotype.med[3,i-1])
    Data.Genotype.plante.ecart_med[date4,i]<-abs(Data.Genotype[date4,i]-Data.Genotype.med[4,i-1])
    Data.Genotype.plante.ecart_med[date5,i]<-abs(Data.Genotype[date5,i]-Data.Genotype.med[5,i-1])
    Data.Genotype.plante.ecart_med[date6,i]<-abs(Data.Genotype[date6,i]-Data.Genotype.med[6,i-1])
  }
  Data.Genotype.plante.ecart_med
} 

Data.Capriss.ecart_median<-fc.ecartmedian(Data.Genotype = Data.Capriss,Data.Genotype.median = Data.Capriss.med,nb.ind = 9)
Data.Cir107.ecart_median<-fc.ecartmedian(Data.Genotype = Data.Cir107,Data.Genotype.median = Data.Cir107.med,nb.ind = 9)
Data.Gariguette.ecart_median<-fc.ecartmedian(Data.Genotype = Data.Gariguette,Data.Genotype.median = Data.Gariguette.med,nb.ind = 9)
Data.Clery.ecart_median<-fc.ecartmedian(Data.Genotype = Data.Clery,Data.Genotype.median = Data.Clery.med,nb.ind = 9)
Data.Ciflorette.ecart_median<-fc.ecartmedian(Data.Genotype = Data.Ciflorette,Data.Genotype.median = Data.Ciflorette.med,nb.ind = 9)
Data.Darselect.ecart_median<-fc.ecartmedian(Data.Genotype = Data.Darselect,Data.Genotype.median = Data.Darselect.med,nb.ind = 9)

#Data Ecart à la médian normalize by ecart moyen à la médian
fc_ecartmedian.norm<-function(Data.genotype.ecartmedian,nb.ind){

  DATA=Data.genotype.ecartmedian
  nb.ind=nb.ind
  date1<-1:nb.ind
  date2<-(nb.ind+1):(nb.ind*2)
  date3<-(nb.ind*2+1):(nb.ind*3)
  date4<-(nb.ind*3+1):(nb.ind*4)
  date5<-(nb.ind*4+1):(nb.ind*5)
  date6<-(nb.ind*5+1):(nb.ind*6)
  
  Data<- data.frame(matrix(nrow = nrow(DATA),ncol = ncol(DATA)))
  Data[1:3]<-DATA[1:3]
  colnames(Data)[1:ncol(DATA)]<-colnames(DATA)[1:ncol(DATA)]
  
  
  for (i in 4:ncol(DATA)){
    Varnames<-colnames(Data)
    Data[date1,i]<-DATA[date1,i]/sum(DATA[date1,i]/nb.ind)
    Data[date2,i]<-DATA[date2,i]/sum(DATA[date2,i]/nb.ind)
    Data[date3,i]<-DATA[date3,i]/sum(DATA[date3,i]/nb.ind)
    Data[date4,i]<-DATA[date4,i]/sum(DATA[date4,i]/nb.ind)
    Data[date5,i]<-DATA[date5,i]/sum(DATA[date5,i]/nb.ind)
    Data[date6,i]<-DATA[date6,i]/sum(DATA[date6,i]/nb.ind)
    Data[is.na(Data[,i]),Varnames[i]]<-0
  }
  Data$dist<- Data[,4]+Data[,5]+Data[,6]+Data[,7]+Data[,8]+Data[,9]+Data[,10]+Data[,11]
  Data.Genotype.Plante.ecart_median_norm<-Data
}

Data.Capriss.ecartmedian.norm<-fc_ecartmedian.norm(Data.genotype.ecartmedian = Data.Capriss.ecart_median,nb.ind = 9)
Data.Ciflorette.ecartmedian.norm<-fc_ecartmedian.norm(Data.genotype.ecartmedian = Data.Ciflorette.ecart_median,nb.ind = 9)
Data.Cir107.ecartmedian.norm<-fc_ecartmedian.norm(Data.genotype.ecartmedian = Data.Cir107.ecart_median,nb.ind = 9)
Data.Clery.ecartmedian.norm<-fc_ecartmedian.norm(Data.genotype.ecartmedian = Data.Clery.ecart_median,nb.ind = 9)
Data.Darselect.ecartmedian.norm<-fc_ecartmedian.norm(Data.genotype.ecartmedian = Data.Darselect.ecart_median,nb.ind = 9)
Data.Gariguette.ecartmedian.norm<-fc_ecartmedian.norm(Data.genotype.ecartmedian = Data.Gariguette.ecart_median,nb.ind = 9)

Data.ecartmedian_norm.genotype<-rbind(Data.Capriss.ecartmedian.norm,Data.Ciflorette.ecartmedian.norm,
                                      Data.Cir107.ecartmedian.norm,Data.Clery.ecartmedian.norm,
                                      Data.Gariguette.ecartmedian.norm)

Data.ecartmedian_norm.genotype<-Data.ecartmedian_norm.genotype[,c(1,3,2,4:11)]
View(Data.Darselect.ecartmedian.norm)
#Data parametre de selection
Parameter.selection.Capriss<-ddply(.data =Data.Capriss.ecartmedian.norm,.variables = c("Genotype","date"),summarize,dist=min(dist,na.rm = T) )
Parameter.selection.Ciflorette<-ddply(.data =Data.Ciflorette.ecartmedian.norm,.variables = c("Genotype","date"),summarize,dist=min(dist,na.rm = T) )
Parameter.selection.Cir107<-ddply(.data =Data.Cir107.ecartmedian.norm,.variables = c("Genotype","date"),summarize,dist=min(dist,na.rm = T) )
Parameter.selection.Clery<-ddply(.data =Data.Clery.ecartmedian.norm,.variables = c("Genotype","date"),summarize,dist=min(dist,na.rm = T) )
Parameter.selection.Darselect<-ddply(.data =Data.Darselect.ecartmedian.norm,.variables = c("Genotype","date"),summarize,dist=min(dist,na.rm = T) )
Parameter.selection.Gariguette<-ddply(.data =Data.Gariguette.ecartmedian.norm,.variables = c("Genotype","date"),summarize,dist=min(dist,na.rm = T) )

#permet de faire un seul dataframe de parametre de selecion
Parameter.selection.genotype<-rbind(Parameter.selection.Capriss,Parameter.selection.Ciflorette,
                                    Parameter.selection.Cir107,Parameter.selection.Clery,
                                    Parameter.selection.Gariguette)

View(Parameter.selection.Capriss)
View(Data.Capriss.ecartmedian.norm)
#Plante selectionnée


#pour 1seul genotype
fc.plant_select<-function(Data.ecartmedian.norm.genotype,Parameter.selection.genotype){
  
  data1<- Data.ecartmedian.norm.genotype
  Parameter.selection.genotype<- Parameter.selection.genotype
  
  data1$date<-as.factor(data1$date)
  Parameter.selection.genotype$date<-as.factor(Parameter.selection.genotype$date)
  
  Plant.select<-data.frame(matrix(ncol = ncol(data1)))
  colnames(Plant.select)<-colnames(data1)
  
  for (i in 1 :nrow(data1)){
    for (k in 1:nlevels(Parameter.selection.genotype$date)){
      if (data1$date[i]==levels(Parameter.selection.genotype$date)[k] & data1$dist[i]==Parameter.selection.genotype$dist[k]){
        Plant.select=rbind(Plant.select,data1[i,])
      }
    }
  }
  Plant.select<- Plant.select[-c(1),]
  #write.csv(Plant.select,"plante.select.csv",sep = ";")
  View(Plant.select)
}

Plant.select.Cir107<-fc.plant_select(Data.ecartmedian.norm.genotype = Data.Cir107.ecartmedian.norm,Parameter.selection.genotype = Parameter.selection.Cir107)
Plant.select.Capriss<-fc.plant_select(Data.ecartmedian.norm.genotype = Data.Capriss.ecartmedian.norm,Parameter.selection.genotype = Parameter.selection.Capriss)
Plant.select.Clery<-fc.plant_select(Data.ecartmedian.norm.genotype = Data.Clery.ecartmedian.norm,Parameter.selection.genotype = Parameter.selection.Clery)
Plant.select.Darselect<-fc.plant_select(Data.ecartmedian.norm.genotype = Data.Darselect.ecartmedian.norm,Parameter.selection.genotype = Parameter.selection.Darselect)
Plant.select.Gariguette<-fc.plant_select(Data.ecartmedian.norm.genotype = Data.Gariguette.ecartmedian.norm,Parameter.selection.genotype = Parameter.selection.Gariguette)
Plant.select.Ciflorette<-fc.plant_select(Data.ecartmedian.norm.genotype = Data.Ciflorette.ecartmedian.norm,Parameter.selection.genotype = Parameter.selection.Ciflorette)


View(Plant.select.Darselect)
#pour plusieurs Genotype

Plant.select.genotype<-data.frame(matrix(ncol = ncol(Data.ecartmedian_norm.genotype)))
colnames(Plant.select.genotype)<-colnames(Data.ecartmedian_norm.genotype)

Data.ecartmedian_norm.genotype$date<-as.factor(Data.ecartmedian_norm.genotype$date)
Parameter.selection.genotype$date<-as.factor(Parameter.selection.genotype$date)

Data.ecartmedian_norm.genotype<-Data.ecartmedian_norm.genotype[order(Data.ecartmedian_norm.genotype$Genotype, Data.ecartmedian_norm.genotype$date),]
Parameter.selection.genotype<-Parameter.selection.genotype[order(Parameter.selection.genotype$Genotype, Parameter.selection.genotype$date),]


View(Data.ecartmedian_norm.genotype)

for (i in 1 :nrow(Data.ecartmedian_norm.genotype)){
  for (j in 1:nlevels (Parameter.selection.genotype$Genotype)){
    for (k in 1:nlevels(Parameter.selection.genotype$date)){
      if (Data.ecartmedian_norm.genotype$Genotype[i]==levels(Parameter.selection.genotype$Genotype)[j] & Data.ecartmedian_norm.genotype$date[i]==levels(Parameter.selection.genotype$date)[k] & Data.ecartmedian_norm.genotype$dist[i]==Parameter.selection.genotype$dist[(nlevels(Parameter.selection.genotype$date)*(j-1)+k)]){
        Plant.select.genotype=rbind(Plant.select.genotype,Data.ecartmedian_norm.genotype[i,])
      }
    } 
  }
} 

Data.ecartmedian_norm.genotype$Genotype[16]==levels(Parameter.selection.genotype$Genotype)[1] & Data.ecartmedian_norm.genotype$date[16]==levels(Parameter.selection.genotype$date)[3] & Data.ecartmedian_norm.genotype$dist[16]==Parameter.selection.genotype$dist[(nlevels(Parameter.selection.genotype$Genotype)*(1-1)+1)]
Data.ecartmedian_norm.genotype$Genotype[16]==levels(Parameter.selection.genotype$Genotype)[1]
Data.ecartmedian_norm.genotype$date[16]==levels(Parameter.selection.genotype$date)[3]
Data.ecartmedian_norm.genotype$dist[16]==Parameter.selection.genotype$dist[(nlevels(Parameter.selection.genotype$Genotype)*(1-1)+3-1)]

Attention k different de k de parametre.selection
paramètre$date[k]=paramètre$dist[k-1] or si k=1 paramètre$dist[k-1]=0 est R  naime pas
