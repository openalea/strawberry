#selection de l'individu le plus central

# package loading
library(plyr)


# DataSet Import
DataSet <- read.csv(
  "Z:/G1/Fraise/Marc-Labadie/R/R-users/FraFlo/DataRaw/Achitecture_module_nonoverlapping_path_v2.csv", 
  sep=";")


# data transformation
dat<- DataSet[,-c(17,18)]

dat$genotype<-as.factor(dat$genotype)
dat$type_of_crown<- as.factor(dat$type_of_crown)

dat$genotype<- factor(x = dat$genotype,levels = levels(x = dat$genotype),
                       labels = c("Gariguette","Ciflorette","Clery","Capriss","Darselect","Cir107"))
dat$type_of_crown<- factor(x = dat$type_of_crown,levels = levels(x = dat$type_of_crown),
                               labels = c("Primary_Crown","Extention_Crown","Branch_Crown"))

# Median of variable as function of time and genotype

ordermax= ddply(.data = dat,.variables = c("genotype","date","plant"),.fun = summarise,
                ordermax= max(Index,na.rm = T))
branching.dat<- dat[dat$type_of_crown=="Branch_Crown",]
#write.csv(branching.dat,"branching.dat.csv")

No.branching= aggregate(cbind(type_of_crown)~genotype+date+plant,data = branching.dat,FUN = length)


Sum<- ddply(.data = dat,.variables = c("genotype","date","plant"),.fun = summarise,
            Sum.Total_leaf= sum(x = nb_total_leaves,na.rm = T),
            Sum.Total_flower= sum(x= nb_total_flowers,na.rm=T),
            Sum.stolon= sum(x= stolons,na.rm=T))#,sum.open_flower= sum(x=nb_open_flowers,na.rm=T))

Sum<- merge(x = Sum,y = ordermax,all = T)
Sum<- merge(x = Sum,y= No.branching, all=T)
#Sum[is.na(Sum$type_of_crown),"type_of_crown"]<-0

median<- ddply(.data = Sum,.variables = c("genotype","date"),.fun = summarise,
            median.Total_leaf= median(x = Sum.Total_leaf,na.rm = T),
            median.Total_flower= median(x = Sum.Total_flower,na.rm = T),
            median.stolon= median(x = Sum.stolon,na.rm = T),
            median.ordermax= median(x= ordermax,na.rm=T),
            median.branching= median(x = type_of_crown,na.rm=T))#,median.openflower= median(x = sum.open_flower,na.rm = T))


Capriss.plante<- Sum[Sum$genotype=="Capriss",]
Capriss.median<-median[median$genotype=="Capriss",]
Ciflorette.plante<- Sum[Sum$genotype=="Ciflorette",]
Ciflorette.median<-median[median$genotype=="Ciflorette",]
Cir107.plante<- Sum[Sum$genotype=="Cir107",]
Cir107.median<-median[median$genotype=="Cir107",]
Clery.plante<- Sum[Sum$genotype=="Clery",]
Clery.median<-median[median$genotype=="Clery",]
Darselect.plante<- Sum[Sum$genotype=="Darselect",]
Darselect.median<-median[median$genotype=="Darselect",]
Gariguette.plante<- Sum[Sum$genotype=="Gariguette",]
Gariguette.median<-median[median$genotype=="Gariguette",]



fc.ecartmedian<-function(Genotype,Genotype.median,nb.ind){
  
  Data.Genotype<-Genotype
  Data.Genotype.med<-Genotype.median
  nb.ind=nb.ind
  
  Data.Genotype.plante.ecart_med<- data.frame(matrix(nrow = nrow(Data.Genotype),ncol = ncol(Data.Genotype)))
  Data.Genotype.plante.ecart_med[1:3]<-Data.Genotype[1:3]
  colnames(Data.Genotype.plante.ecart_med)[1:ncol(Data.Genotype)]<-colnames(Data.Genotype)[1:ncol(Data.Genotype)]
  
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

capriss.ecartmedian<-fc.ecartmedian(Genotype = Capriss.plante,Genotype.median = Capriss.median,nb.ind = 9)
gariguette.ecartmedian<-fc.ecartmedian(Genotype = Gariguette.plante, Genotype.median = Gariguette.median,nb.ind = 9)
clery.ecartmedian<-fc.ecartmedian(Genotype = Clery.plante, Genotype.median = Clery.median,nb.ind = 9)
ciflorette.ecartmedian<-fc.ecartmedian(Genotype = Ciflorette.plante, Genotype.median = Clery.median,nb.ind = 9)
cir107.ecartmedian<-fc.ecartmedian(Genotype = Cir107.plante, Genotype.median = Clery.median,nb.ind = 9)
darselect.ecartmedian<-fc.ecartmedian(Genotype = Darselect.plante, Genotype.median = Clery.median,nb.ind = 9)


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
    Data[date1,i]<-DATA[date1,i]/(sum(DATA[date1,i]/nb.ind))
    Data[date2,i]<-DATA[date2,i]/(sum(DATA[date2,i]/nb.ind))
    Data[date3,i]<-DATA[date3,i]/(sum(DATA[date3,i]/nb.ind))
    Data[date4,i]<-DATA[date4,i]/(sum(DATA[date4,i]/nb.ind))
    Data[date5,i]<-DATA[date5,i]/(sum(DATA[date5,i]/nb.ind))
    Data[date6,i]<-DATA[date6,i]/(sum(DATA[date6,i]/nb.ind))
    Data[is.na(Data[,i]),Varnames[i]]<-0
  }
  Data$dist<- rowSums(x = Data[,4:ncol(Data)])
  Data.Genotype.Plante.ecart_median_norm<-Data
}

Capriss.dist<-fc_ecartmedian.norm(Data.genotype.ecartmedian = capriss.ecartmedian,nb.ind = 9)
Gariguette.dist<-fc_ecartmedian.norm(Data.genotype.ecartmedian = gariguette.ecartmedian,nb.ind = 9)
Clery.dist<-fc_ecartmedian.norm(Data.genotype.ecartmedian = clery.ecartmedian,nb.ind = 9)
cir107.dist<-fc_ecartmedian.norm(Data.genotype.ecartmedian = cir107.ecartmedian,nb.ind = 9)
ciflorette.dist<-fc_ecartmedian.norm(Data.genotype.ecartmedian = ciflorette.ecartmedian,nb.ind = 9)
darselect.dist<-fc_ecartmedian.norm(Data.genotype.ecartmedian = darselect.ecartmedian,nb.ind = 9)


Parameter.selection.Capriss<-ddply(.data =Capriss.dist,.variables = c("genotype","date"),summarize,dist=min(dist,na.rm = T) )
Parameter.selection.gariguette<-ddply(.data =Gariguette.dist,.variables = c("genotype","date"),summarize,dist=min(dist,na.rm = T) )
Parameter.selection.clery<-ddply(.data = Clery.dist,.variables = c("genotype","date"),summarize,dist=min(dist,na.rm = T) )
Parameter.selection.cir107<-ddply(.data = cir107.dist,.variables = c("genotype","date"),summarize,dist=min(dist,na.rm = T) )
Parameter.selection.ciflorette<-ddply(.data = ciflorette.dist,.variables = c("genotype","date"),summarize,dist=min(dist,na.rm = T) )
Parameter.selection.darselect<-ddply(.data = darselect.dist,.variables = c("genotype","date"),summarize,dist=min(dist,na.rm = T) )



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
  #write.csv(Plant.select,"plante.select.darselect.csv")
  View(Plant.select)
}

#Plant.select.Capriss<-fc.plant_select(Data.ecartmedian.norm.genotype = Capriss.dist,Parameter.selection.genotype = Parameter.selection.Capriss)
Plant.select.gariguette<-fc.plant_select(Data.ecartmedian.norm.genotype = Gariguette.dist,Parameter.selection.genotype = Parameter.selection.gariguette)
#Plant.select.Clery<-fc.plant_select(Data.ecartmedian.norm.genotype = Clery.dist,Parameter.selection.genotype = Parameter.selection.clery)
#Plant.select.cir107<-fc.plant_select(Data.ecartmedian.norm.genotype = cir107.dist,Parameter.selection.genotype = Parameter.selection.cir107)
#Plant.select.ciflorette<-fc.plant_select(Data.ecartmedian.norm.genotype = ciflorette.dist,Parameter.selection.genotype = Parameter.selection.ciflorette)
#Plant.select.darselect<-fc.plant_select(Data.ecartmedian.norm.genotype = darselect.dist,Parameter.selection.genotype = Parameter.selection.darselect)

#Test sur la medianne
Gariguette<-dat[dat$genotype=="Gariguette",]
Gariguettesans0<-Gariguette[!Gariguette$Index=="0",]
table(Gariguettesans0$nb_visible_leaves>=quantile(Gariguettesans0$nb_visible_leaves,0.5),Gariguettesans0$Index)

chisq.test(table(Gariguettesans0$nb_total_flowers>=quantile(Gariguettesans0$nb_total_flowers,0.5),Gariguettesans0$Index),correct = T
)
summary(a)

chisq.test(table(arbre$hau>=quantile(arbre$hau,0.5),arbre$type))
