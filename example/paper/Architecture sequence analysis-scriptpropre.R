###########################################################################
#                             Architecture analysis                       #
#                                 Marc 2017                               #
###########################################################################

# 1.Packages 
install.packages("plyr")
install.packages("ggplot2")
install.packages("ggthemes")
install.packages("agricolae")
install.packages("PMCMR")
install.packages("lmtest")

#2. Loading packages
library(plyr)
library(ggplot2)
library(ggthemes)
library(agricolae)
library(PMCMR)
library(lmtest)
#library(FSA)

#3.Import dataset
DataSet <- read.csv(
  "Z:/G1/Fraise/Marc-Labadie/R/R-users/FraFlo/DataRaw/Achitecture_module_nonoverlapping_path.csv", 
  sep=";",na.strings = "")
DataSet<- DataSet[,-c(17:18)]


#3.1 Modification of Compactly display the internal structure of an R object
str(DataSet)
#DataSet$Index<- as.factor(DataSet$Index)
DataSet$genotype<- as.factor(DataSet$genotype)
DataSet$date<- as.factor(DataSet$date)
DataSet$Crown_status<- as.factor(DataSet$Crown_status)
DataSet$type_of_crown<- as.factor(DataSet$type_of_crown)

str(DataSet)
#3.2 Replace genotype id, date id, crown status id and type of crown id by
# respective factor names
DataSet$genotype<- factor(x = DataSet$genotype,levels = levels(x = DataSet$genotype),
                          labels = c("Gariguette","Ciflorette","Clery","Capriss","Darselect","Cir107"))

DataSet$date<- factor(x = DataSet$date,levels = levels(x = DataSet$date),
                      labels = c("Mid-December","Early-Junuary","Mid-February","Early-March","Early-April","Early-June"))
DataSet$Crown_status<- factor(x = DataSet$Crown_status,levels = levels(x = DataSet$Crown_status),
                              labels = c("NA","Terminal_Vegetative_bud","Terminal_initiated_bud","Terminal_Floral_bud","Terminal_Inflorescence"))
DataSet$type_of_crown<- factor(x = DataSet$type_of_crown,levels = levels(x = DataSet$type_of_crown),
                               labels = c("Primary_Crown","Extention_Crown","Branch_Crown"))

##########################################################################

#4.Analysis
dat<-DataSet



# 4.1-Table data resum mean, sd, N by genotype as function of order
#      for No.total leaves, No. total flower, No. stolon

dat.resum<-ddply(.data = dat,.variables = c("genotype","Index"),summarise,
                 MeanTotalLeave= round(mean(x = nb_total_leaves,na.rm = T),0),
                 SdTotalLeave= sd(x = nb_total_leaves,na.rm = T),
                 MeanTotalFlower= round(mean(x = nb_total_flowers,na.rm = T),0),
                 SdTotalFlower= sd(x = nb_total_flowers,na.rm = T),
                 MeanStolon= round(mean(x = stolons,na.rm = T),0),
                 SdStolon= sd(x = stolons,na.rm = T),
                 N=length(nb_total_leaves))

# 4.2- Pointwise of variables for all genotype

# 4.2.1- No. total leaves for all genotype
plot(x = dat.resum$Index,y = dat.resum$MeanTotalLeave,type="n",las=1,xlab = "Module order",ylab = "Mean of No. Total leaves",
     ylim=c(0,15),font.axis=2,font.lab=2,main = "Mean of No.total leaves by genotype \n as fonction of module order")
points(x = dat.resum[dat.resum$genotype=="Capriss",]$Index,
       y = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalLeave,
       type="o",lwd=2,pch=19,cex=0.8,col="orange")
segments(x0 = dat.resum[dat.resum$genotype=="Capriss",]$Index,y0 = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Capriss",]$Index,y1 = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalLeave+dat.resum[dat.resum$genotype=="Capriss",]$SdTotalLeave,
         col="orange")
segments(x0 = dat.resum[dat.resum$genotype=="Capriss",]$Index,y0 = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Capriss",]$Index,y1 = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalLeave-dat.resum[dat.resum$genotype=="Capriss",]$SdTotalLeave,
         col="orange")
points(x = dat.resum[dat.resum$genotype=="Cir107",]$Index,
       y = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalLeave,
       type="o",lwd=2,pch=19,cex=0.8,col="blue")
segments(x0 = dat.resum[dat.resum$genotype=="Cir107",]$Index,y0 = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Cir107",]$Index,y1 = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalLeave+dat.resum[dat.resum$genotype=="Cir107",]$SdTotalLeave,
         col="blue")
segments(x0 = dat.resum[dat.resum$genotype=="Cir107",]$Index,y0 = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Cir107",]$Index,y1 = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalLeave-dat.resum[dat.resum$genotype=="Cir107",]$SdTotalLeave,
         col="blue")
points(x = dat.resum[dat.resum$genotype=="Ciflorette",]$Index,
       y = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalLeave,
       type="o",lwd=2,pch=19,cex=0.8,col="purple")
segments(x0 = dat.resum[dat.resum$genotype=="Ciflorette",]$Index,y0 = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Ciflorette",]$Index,y1 = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalLeave+dat.resum[dat.resum$genotype=="Ciflorette",]$SdTotalLeave,
         col="purple")
segments(x0 = dat.resum[dat.resum$genotype=="Ciflorette",]$Index,y0 = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Ciflorette",]$Index,y1 = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalLeave-dat.resum[dat.resum$genotype=="Ciflorette",]$SdTotalLeave,
         col="purple")
points(x = dat.resum[dat.resum$genotype=="Clery",]$Index,
       y = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalLeave,
       type="o",lwd=2,pch=19,cex=0.8,col="maroon")
segments(x0 = dat.resum[dat.resum$genotype=="Clery",]$Index,y0 = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Clery",]$Index,y1 = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalLeave+dat.resum[dat.resum$genotype=="Clery",]$SdTotalLeave,
         col="maroon")
segments(x0 = dat.resum[dat.resum$genotype=="Clery",]$Index,y0 = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Clery",]$Index,y1 = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalLeave-dat.resum[dat.resum$genotype=="Clery",]$SdTotalLeave,
         col="maroon")
points(x = dat.resum[dat.resum$genotype=="Darselect",]$Index,
       y = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalLeave,
       type="o",lwd=2,pch=19,cex=0.8,col="darkgreen")
segments(x0 = dat.resum[dat.resum$genotype=="Darselect",]$Index,y0 = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Darselect",]$Index,y1 = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalLeave+dat.resum[dat.resum$genotype=="Darselect",]$SdTotalLeave,
         col="darkgreen")
segments(x0 = dat.resum[dat.resum$genotype=="Darselect",]$Index,y0 = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Darselect",]$Index,y1 = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalLeave-dat.resum[dat.resum$genotype=="Darselect",]$SdTotalLeave,
         col="darkgreen")
points(x = dat.resum[dat.resum$genotype=="Gariguette",]$Index,
       y = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave,
       type="o",lwd=2,pch=19,cex=0.8,col="darkred")
segments(x0 = dat.resum[dat.resum$genotype=="Gariguette",]$Index,y0 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Gariguette",]$Index,y1 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave+dat.resum[dat.resum$genotype=="Gariguette",]$SdTotalLeave,
         col="red")
segments(x0 = dat.resum[dat.resum$genotype=="Gariguette",]$Index,y0 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Gariguette",]$Index,y1 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave-dat.resum[dat.resum$genotype=="Gariguette",]$SdTotalLeave,
         col="red")
legend("topright",legend = c("Capriss","Ciflorette","Cir107","Clery","Darselect","Gariguette"),
       lwd =c(2,2,2,2,2,2),pch=c(19,19,19,19,19,19),col = c("orange","purple","blue","maroon","darkgreen","darkred"),
       cex= 0.8)

#Gariguette

plot(x = dat.resum$Index,y = dat.resum$MeanTotalLeave,type="n",las=1,xlab = "Module order",ylab = "Mean of No. leaves",
     ylim=c(0,15),font.axis=2,font.lab=2,main = "")
points(x = dat.resum[dat.resum$genotype=="Gariguette",]$Index,
       y = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave,
       type="o",lwd=2,pch=19,cex=0.8,col="red")
segments(x0 = dat.resum[dat.resum$genotype=="Gariguette",]$Index,y0 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Gariguette",]$Index,y1 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave+dat.resum[dat.resum$genotype=="Gariguette",]$SdTotalLeave,
         col="red")
segments(x0 = dat.resum[dat.resum$genotype=="Gariguette",]$Index,y0 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave,
         x1 = dat.resum[dat.resum$genotype=="Gariguette",]$Index,y1 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave-dat.resum[dat.resum$genotype=="Gariguette",]$SdTotalLeave,
         col="red")
legend("topright",legend = c("Gariguette"),lwd =c(2),pch=c(19),col = c("red"),cex= 0.8)




"Observation: stabilisation of Mean No. total leaves after order1"

# 4.1.2 Existe t il une stabilisation du nombre de feuille à partir de l'ordre 1 pour chaque genotype
"""
hypothese: Si pour chaque variété, le nombre total de feuilles est constant à partir de l'ordre 1
alors la pente est proche ou égale à 0 
==> 1. calcul de la pente pour chaque variétés--> regression linéaire
    2. Est ce que la pente est proche de 0
    3. Calcul de l'interval de confiance à 95% de la pente
       ==> si la pente est proche de 0 et si l'intervalle de confiance encadre 0
           alors on peut considérer que la pente est égale à 0.
"""
#4.1.2.1- regression linéaire pour chaque variétés a partir de l'ordre 1.

#----- filtre du jeu de données par variétés--------
data_without0<- dat[!dat$Index=="0",]

capriss_without0<-data_without0[data_without0$genotype=="Capriss",]
ciflorette_without0<-data_without0[data_without0$genotype=="Ciflorette",]
cir107_without0<-data_without0[data_without0$genotype=="Cir107",]
clery_without0<-data_without0[data_without0$genotype=="Clery",]
darselect_without0<-data_without0[data_without0$genotype=="Darselect",]
gariguette_without0<-data_without0[data_without0$genotype=="Gariguette",]

#sans 0 et sans 1
capriss_without0<-data_without0[data_without0$genotype=="Capriss"& !data_without0$Index=="1",]
ciflorette_without0<-data_without0[data_without0$genotype=="Ciflorette"& !data_without0$Index=="1",]
cir107_without0<-data_without0[data_without0$genotype=="Cir107" & !data_without0$Index=="1",]
clery_without0<-data_without0[data_without0$genotype=="Clery"& !data_without0$Index=="1",]
darselect_without0<-data_without0[data_without0$genotype=="Darselect" & !data_without0$Index=="1",]
gariguette_without0<-data_without0[data_without0$genotype=="Gariguette"& !data_without0$Index=="1",]

#----- regression linéaire--------
capriss_linearmodel<-lm(nb_total_leaves~Index,data =capriss_without0)
capriss.param<-coef(capriss_linearmodel) 
ciflorette_linearmodel<-lm(nb_total_leaves~Index,data =ciflorette_without0)
ciflorette.param<-coef(ciflorette_linearmodel) 
cir107_linearmodel<-lm(nb_total_leaves~Index,data =cir107_without0)
cir107.param<-coef(cir107_linearmodel) 
clery_linearmodel<-lm(nb_total_leaves~Index,data =clery_without0)
clery.param<-coef(clery_linearmodel) 
darselect_linearmodel<-lm(nb_total_leaves~Index,data =darselect_without0)
darselect.param<-coef(darselect_linearmodel) 
gariguette_linearmodel<-lm(nb_total_leaves~Index,data =gariguette_without0)
gariguette.param<- coef(gariguette_linearmodel)

"""
==> Pour chaque génotype la pentes est proche de 0,
    Nous pouvons raisonnablement penser que le nombre de feuille
    à partir de l'ordre 1 est constant --> stabilité à partir de l'ordre 1"""

#----- Calcul de l'interval de confiance de la pente et de l'intersept à 95% --------
"""
http://perso.ens-lyon.fr/lise.vaudor/regression-lineaire-erreur-et-incertitude/
eq droite lineaire: y= b + ax+ epsylon
                    y= intersept+ slope(Index)+residuals
                    ICpente95%= confint(model,param= varname(pente),level=0.95)
"""
capriss.ICpente<-confint(object = capriss_linearmodel,parm = "Index",level = 0.95)
capriss.ICintercept<-confint(object = capriss_linearmodel,parm = "(Intercept)",level = 0.95)

ciflorette.ICpente<-confint(object = ciflorette_linearmodel,parm = "Index",level = 0.95)
ciflorette.ICintercept<-confint(object = ciflorette_linearmodel,parm = "(Intercept)",level = 0.95)

cir107.ICpente<-confint(object = cir107_linearmodel,parm = "Index",level = 0.95)
cir107.ICintercept<-confint(object = cir107_linearmodel,parm = "(Intercept)",level = 0.95)

clery.ICpente<-confint(object = clery_linearmodel,parm = "Index",level = 0.95)
clery.ICintercept<-confint(object = clery_linearmodel,parm = "(Intercept)",level = 0.95)

darselect.ICpente<-confint(object = darselect_linearmodel,parm = "Index",level = 0.95)
darselect.ICintercept<-confint(object = darselect_linearmodel,parm = "(Intercept)",level = 0.95)

gariguette.ICpente<-confint(object = gariguette_linearmodel,parm = "Index",level = 0.95)
gariguette.ICintercept<-confint(object = gariguette_linearmodel,parm = "(Intercept)",level = 0.95)

#table resum info regression lineaire pour chaque varieté: pente, IClower,ICupper
dat.reg<-data.frame(matrix(nrow = 6,ncol = 4))
colnames(dat.reg)<-c("Varieties","slope","IC95% lower","IC95% upper")
dat.reg[,1]<-c("Capriss","Ciflorette","Cir107","Clery","Darselect","Gariguette")
dat.reg[,2]<-c(capriss_linearmodel$coefficients[[2]],ciflorette_linearmodel$coefficients[[2]],
               cir107_linearmodel$coefficients[[2]],clery_linearmodel$coefficients[[2]],
               darselect_linearmodel$coefficients[[2]],gariguette_linearmodel$coefficients[[2]])
dat.reg[,3]<-c(capriss.ICpente[[1]],ciflorette.ICpente[[1]],cir107.ICpente[[1]],
               clery.ICpente[[1]],darselect.ICpente[[1]],gariguette.ICpente[[1]])
dat.reg[,4]<-c(capriss.ICpente[[2]],ciflorette.ICpente[[2]],cir107.ICpente[[2]],
               clery.ICpente[[2]],darselect.ICpente[[2]],gariguette.ICpente[[2]])

# Representation de la verification pour H0: la pente est nul au seuil 95%
"""
representation variable residuelle entre -1 et 1, il faut regarder si:
l'interval de confiance encadre 0. 
"""
# Capriss
plot(x = capriss_linearmodel$residuals,type="n",ylim=c(-1,1),main = "Capriss",
     ylab = "Slope values",xlab="Individuals",font.axis=2,font.lab=2,las=1)
abline(h=0)
abline(h=capriss.ICpente[1],lty=2,col="red")
abline(h=capriss.ICpente[2],lty=2,col="red")
abline(h=capriss.param[2],lty=1,col="blue")
legend("topright",legend = c("slope","IC95%"),col = c("blue","red"),lty=c(1,2))

# Ciflorette
plot(x = ciflorette_linearmodel$residuals,type="n",ylim=c(-1,1),main = "Ciflorette",
     ylab = "Slope values",xlab="Individuals",font.axis=2,font.lab=2,las=1)
abline(h=0)
abline(h=ciflorette.ICpente[1],lty=2,col="red")
abline(h=ciflorette.ICpente[2],lty=2,col="red")
abline(h=ciflorette.param[2],lty=1,col="blue")
legend("topright",legend = c("slope","IC95%"),col = c("blue","red"),lty=c(1,2))

# Cir107
plot(x = cir107_linearmodel$residuals,type="n",ylim=c(-1,1),main = "Cir107",
     ylab = "Slope values",xlab="Individuals",font.axis=2,font.lab=2,las=1)
abline(h=0)
abline(h=cir107.ICpente[1],lty=2,col="red")
abline(h=cir107.ICpente[2],lty=2,col="red")
abline(h=cir107.param[2],lty=1,col="blue")
legend("topright",legend = c("slope","IC95%"),col = c("blue","red"),lty=c(1,2))

# clery
plot(x = clery_linearmodel$residuals,type="n",ylim=c(-1,1),main = "Clery",
     ylab = "Slope values",xlab="Individuals",font.axis=2,font.lab=2,las=1)
abline(h=0)
abline(h=clery.ICpente[1],lty=2,col="red")
abline(h=clery.ICpente[2],lty=2,col="red")
abline(h=clery.param[2],lty=1,col="blue")
legend("topright",legend = c("slope","IC95%"),col = c("blue","red"),lty=c(1,2))

# darselect
plot(x = darselect_linearmodel$residuals,type="n",ylim=c(-1,1),main = "Darselect",
     ylab = "Slope values",xlab="Individuals",font.axis=2,font.lab=2,las=1)
abline(h=0)
abline(h=darselect.ICpente[1],lty=2,col="red")
abline(h=darselect.ICpente[2],lty=2,col="red")
abline(h=darselect.param[2],lty=1,col="blue")
legend("topright",legend = c("slope","IC95%"),col = c("blue","red"),lty=c(1,2))

# gariguette
plot(x = gariguette_linearmodel$residuals,type="n",ylim=c(-1,1),main = "Gariguette",
     ylab = "Slope values",xlab="Individuals",font.axis=2,font.lab=2,las=1)
abline(h=0)
abline(h=gariguette.ICpente[1],lty=2,col="red")
abline(h=gariguette.ICpente[2],lty=2,col="red")
abline(h=gariguette.param[2],lty=1,col="blue")
legend("topright",legend = c("slope","IC95%"),col = c("blue","red"),lty=c(1,2))

#----- Representation des données et model --------
dat.resum_without0<-dat.resum[!dat.resum$Index==0,]
# calcul confidence interval of model
attach(dat.resum_without0)

capriss.pred.frame<-data.frame(Index=1:5)
capriss.pc<-predict(capriss_linearmodel, interval="confidence",
            newdata=capriss.pred.frame)
ciflorette.pred.frame<-data.frame(Index=1:5)
ciflorette.pc<-predict(ciflorette_linearmodel, interval="confidence",
                    newdata=ciflorette.pred.frame)
cir107.pred.frame<-data.frame(Index=1:5)
cir107.pc<-predict(cir107_linearmodel, interval="confidence",
                       newdata=cir107.pred.frame)
clery.pred.frame<-data.frame(Index=1:5)
clery.pc<-predict(clery_linearmodel, interval="confidence",
                   newdata=clery.pred.frame)
darselect.pred.frame<-data.frame(Index=1:5)
darselect.pc<-predict(darselect_linearmodel, interval="confidence",
                  newdata=darselect.pred.frame)
gariguette.pred.frame<-data.frame(Index=1:5)
gariguette.pc<-predict(gariguette_linearmodel, interval="confidence",
                      newdata=gariguette.pred.frame)

# Representation graphique

plot(x = dat.resum_without0$Index,y = dat.resum_without0$MeanTotalLeave,
     main="Mean of No.Total Leaves\n for all varieties",
     ylab = "Mean of No.Total Leaves", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,6))
points(x = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$Index,
       y=dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$MeanTotalLeave,
       col="orange",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$MeanTotalLeave+dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$SdTotalLeave)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$MeanTotalLeave-dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$SdTotalLeave)
points(x = dat.resum_without0[dat.resum_without0$genotype=="Cirflorette",]$Index,
       y=dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$MeanTotalLeave,
       col="purple",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Cirflorette",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Cirflorette",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Cirflorette",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Cirflorette",]$MeanTotalLeave+dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$SdTotalLeave)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Cirflorette",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Cirflorette",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Cirflorette",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Cirflorette",]$MeanTotalLeave-dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$SdTotalLeave)
points(x = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$Index,
       y=dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$MeanTotalLeave,
       col="blue",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$MeanTotalLeave+dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$SdTotalLeave)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$MeanTotalLeave-dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$SdTotalLeave)
points(x = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$Index,
       y=dat.resum_without0[dat.resum_without0$genotype=="Clery",]$MeanTotalLeave,
       col="maroon",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$MeanTotalLeave+dat.resum_without0[dat.resum_without0$genotype=="Clery",]$SdTotalLeave)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$MeanTotalLeave-dat.resum_without0[dat.resum_without0$genotype=="Clery",]$SdTotalLeave)
points(x = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$Index,
       y=dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$MeanTotalLeave,
       col="darkgreen",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$MeanTotalLeave+dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$SdTotalLeave)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$MeanTotalLeave-dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$SdTotalLeave)
points(x = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$Index,
       y=dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$MeanTotalLeave,
       col="darkred",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$MeanTotalLeave+dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$SdTotalLeave)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$MeanTotalLeave-dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$SdTotalLeave)
legend("topright",legend = c("Capriss","Ciflorette","Cir107","Clery","Darselect","Gariguette"),
       lwd =c(2,2,2,2,2,2),pch=c(19,19,19,19,19,19),col = c("orange","purple","blue","maroon","darkgreen","darkred"),
       cex= 0.8)
# representation par genotype + incertitude sur la pente

#Capriss
plot(x = dat.resum_without0$Index,y = dat.resum_without0$MeanTotalLeave,
     main="Mean of No.Total Leaves\n for Capriss",
     ylab = "Mean of No.Total Leaves", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,8))
points(x = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$Index,
       y=dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$MeanTotalLeave,
       col="orange",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$MeanTotalLeave+dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$SdTotalLeave,
         col="orange")
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$MeanTotalLeave-dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$SdTotalLeave,
         col="orange")
abline(capriss_linearmodel,lwd=2,lty=1)
abline(capriss.ICintercept[1],capriss.ICpente[1],col="red",lty=2)
abline(capriss.ICintercept[2],capriss.ICpente[2],col="red",lty=2)
matlines(capriss.pred.frame,capriss.pc[,2:3],lty=c(2,2),col="blue")
text(x = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$Index,y =1,
     labels = dat.resum_without0[dat.resum_without0$genotype=="Capriss",]$N)
legend("topright",legend = c("Confidence interval of slope at 95%","linear model","Confidence interval of model at 95%"),col=c("red","black","blue"),lty=c(2,1,2),cex=0.8)

#Ciflorette
plot(x = dat.resum_without0$Index,y = dat.resum_without0$MeanTotalLeave,
     main="Mean of No.Total Leaves, linear model and IC95% \n for ciflorette",
     ylab = "Mean of No.Total Leaves", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,8))
points(x = dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$Index,
       y=dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$MeanTotalLeave,
       col="purple",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$MeanTotalLeave+dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$SdTotalLeave,
         col="purple")
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$MeanTotalLeave-dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$SdTotalLeave,
         col="purple")
abline(ciflorette_linearmodel,lwd=2,lty=1)
abline(ciflorette.ICintercept[1],ciflorette.ICpente[1],col="red",lty=2)
abline(ciflorette.ICintercept[2],ciflorette.ICpente[2],col="red",lty=2)
matlines(ciflorette.pred.frame,ciflorette.pc[,2:3],lty=c(2,2),col="blue")
text(x = dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$Index,y =1,
     labels = dat.resum_without0[dat.resum_without0$genotype=="Ciflorette",]$N)
legend("topright",legend = c("Confidence interval of slope at 95%","linear model","Confidence interval of model at 95%"),col=c("red","black","blue"),lty=c(2,1,2),cex=0.8)

#Cir107
plot(x = dat.resum_without0$Index,y = dat.resum_without0$MeanTotalLeave,
     main="Mean of No.Total Leaves, linear model and IC95% \n for Cir107",
     ylab = "Mean of No.Total Leaves", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,8))
points(x = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$Index,
       y=dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$MeanTotalLeave,
       col=" blue",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$MeanTotalLeave+dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$SdTotalLeave,
         col="blue")
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$MeanTotalLeave-dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$SdTotalLeave,
         col="blue")
abline(cir107_linearmodel,lwd=2,lty=1)
abline(cir107.ICintercept[1],cir107.ICpente[1],col="red",lty=2)
abline(cir107.ICintercept[2],cir107.ICpente[2],col="red",lty=2)
matlines(cir107.pred.frame,cir107.pc[,2:3],lty=c(2,2),col="blue")
text(x = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$Index,y =1,
     labels = dat.resum_without0[dat.resum_without0$genotype=="Cir107",]$N)
legend("topright",legend = c("Confidence interval of slope at 95%","linear model","Confidence interval of model at 95%"),col=c("red","black","blue"),lty=c(2,1,2),cex=0.8)

#Clery
plot(x = dat.resum_without0$Index,y = dat.resum_without0$MeanTotalLeave,
     main="Mean of No.Total Leaves, linear model and IC95% \n for Clery",
     ylab = "Mean of No.Total Leaves", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,8))
points(x = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$Index,
       y=dat.resum_without0[dat.resum_without0$genotype=="Clery",]$MeanTotalLeave,
       col="maroon",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$MeanTotalLeave+dat.resum_without0[dat.resum_without0$genotype=="Clery",]$SdTotalLeave,
         col="maroon")
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$MeanTotalLeave-dat.resum_without0[dat.resum_without0$genotype=="Clery",]$SdTotalLeave,
         col="maroon")
abline(clery_linearmodel,lwd=2,lty=1)
abline(clery.ICintercept[1],clery.ICpente[1],col="red",lty=2)
abline(clery.ICintercept[2],clery.ICpente[2],col="red",lty=2)
matlines(clery.pred.frame,clery.pc[,2:3],lty=c(2,2),col="blue")
text(x = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$Index,y =1,
     labels = dat.resum_without0[dat.resum_without0$genotype=="Clery",]$N)
legend("topright",legend = c("Confidence interval of slope at 95%","linear model","Confidence interval of model at 95%"),col=c("red","black","blue"),lty=c(2,1,2),cex=0.8)

#Darselect
plot(x = dat.resum_without0$Index,y = dat.resum_without0$MeanTotalLeave,
     main="Mean of No.Total Leaves, linear model and IC95% \n for Darselect",
     ylab = "Mean of No.Total Leaves", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,8))
points(x = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$Index,
       y=dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$MeanTotalLeave,
       col="darkgreen",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$MeanTotalLeave+dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$SdTotalLeave,
         col="darkgreen")
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$MeanTotalLeave-dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$SdTotalLeave,
         col="darkgreen")
abline(darselect_linearmodel,lwd=2,lty=1)
abline(darselect.ICintercept[1],darselect.ICpente[1],col="red",lty=2)
abline(darselect.ICintercept[2],darselect.ICpente[2],col="red",lty=2)
matlines(darselect.pred.frame,darselect.pc[,2:3],lty=c(2,2),col="blue")
text(x = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$Index,y =1,
     labels = dat.resum_without0[dat.resum_without0$genotype=="Darselect",]$N)
legend("topright",legend = c("Confidence interval of slope at 95%","linear model","Confidence interval of model at 95%"),col=c("red","black","blue"),lty=c(2,1,2),cex=0.8)

#Gariguette
plot(x = dat.resum_without0$Index,y = dat.resum_without0$MeanTotalLeave,
     main="Mean of No.Total Leaves, linear model and IC95% \n for Gariguette",
     ylab = "Mean of No.Total Leaves", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,8))
points(x = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$Index,
       y=dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$MeanTotalLeave,
       col="darkred",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$MeanTotalLeave+dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$SdTotalLeave,
         col="darkred")
segments(x0 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$Index,y0 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$MeanTotalLeave,
         x1 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$Index,y1 = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$MeanTotalLeave-dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$SdTotalLeave,
         col="darkred")
abline(gariguette_linearmodel,lwd=2,lty=1)
abline(gariguette.ICintercept[1],gariguette.ICpente[1],col="red",lty=2)
abline(gariguette.ICintercept[2],gariguette.ICpente[2],col="red",lty=2)
matlines(gariguette.pred.frame,gariguette.pc[,2:3],lty=c(2,2),col="blue")
text(x = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$Index,y =1,
     labels = dat.resum_without0[dat.resum_without0$genotype=="Gariguette",]$N)
legend("topright",legend = c("Confidence interval of slope at 95%","linear model","Confidence interval of model at 95%"),col=c("red","black","blue"),lty=c(2,1,2),cex=0.8)

#4.2.1.2 Difference between varieties for order 0 and >=1
dat.NoTotal_leaves<- dat[,c(14,1,4)]

dat.NoTotal_leaves$groups[dat.NoTotal_leaves$Index==0]<-0
dat.NoTotal_leaves$groups[dat.NoTotal_leaves$Index==1]<-1
dat.NoTotal_leaves$groups[dat.NoTotal_leaves$Index==2]<-1
dat.NoTotal_leaves$groups[dat.NoTotal_leaves$Index==3]<-1
dat.NoTotal_leaves$groups[dat.NoTotal_leaves$Index==4]<-1
dat.NoTotal_leaves$groups[dat.NoTotal_leaves$Index==5]<-1

str(dat.NoTotal_leaves)

dat.NoTotal_leaves$groups<- as.numeric(x = dat.NoTotal_leaves$groups)

NoTotal_leave.resum<- ddply(.data = dat.NoTotal_leaves,.variables = c("genotype","groups"),.fun = summarize,
                            Mean= round(median(nb_total_leaves,na.rm=T),0),
                            #Sd= sd(nb_total_leaves,na.rm=T),
                            N= length(nb_total_leaves))
NoTotal_leave.resum$Se<-NoTotal_leave.resum$Sd/sqrt(NoTotal_leave.resum$N)
yliminf<- min(NoTotal_leave.resum$Mean-NoTotal_leave.resum$Se)
ylimsup<- max(NoTotal_leave.resum$Mean+NoTotal_leave.resum$Se)
dat.NoTotal_leaves0<- dat.NoTotal_leaves[dat.NoTotal_leaves$groups=="0",]
dat.NoTotal_leaves1<- dat.NoTotal_leaves[dat.NoTotal_leaves$groups=="1",]

#ANOVA non Parametric Kruskal Wallis. Comparison between varieties for order0 then for order1

kruskal.test(nb_total_leaves~genotype,data=dat.NoTotal_leaves0)
k.duntest<-posthoc.kruskal.dunn.test(nb_total_leaves~genotype,data=dat.NoTotal_leaves0,p.adjust.method = "BH")
k.duntest$p.value

kruskal.test(nb_total_leaves~genotype,data=dat.NoTotal_leaves1)
k.duntest<-posthoc.kruskal.dunn.test(nb_total_leaves~genotype,data=dat.NoTotal_leaves1,p.adjust.method = "BH")
k.duntest$p.value


kruskal(y = dat.NoTotal_leaves1$nb_total_leaves,trt = dat.NoTotal_leaves1$genotype,alpha=0.05,group=T,console=T )
kruskal.test(dat.NoTotal_leaves$nb_total_leaves~interaction(dat.NoTotal_leaves$genotype,dat.NoTotal_leaves$groups),data=dat.NoTotal_leaves)
k.duntest<-posthoc.kruskal.dunn.test(dat.NoTotal_leaves$nb_total_leaves~interaction(dat.NoTotal_leaves$genotype,dat.NoTotal_leaves$groups),data=dat.NoTotal_leaves,p.adjust.method = "BH")
k.duntest$p.value

plot(x = NoTotal_leave.resum$groups,y=NoTotal_leave.resum$Mean,type="n",
     ylim=c(yliminf,ylimsup),ylab="Mean of No.Total Leaves",xlab="Module order",
     font.axis=2,font.lab=2,las=1)
points(x = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Capriss",]$groups,
       y = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Capriss",]$Mean,
       col="orange",type="o",pch=19,lty=1)
arrows(x0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Capriss",]$groups,
       y0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Capriss",]$Mean,
       x1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Capriss",]$groups,
       y1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Capriss",]$Mean+NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Capriss",]$Se,
       angle=90,col="orange",length = 0.1)
arrows(x0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Capriss",]$groups,
       y0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Capriss",]$Mean,
       x1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Capriss",]$groups,
       y1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Capriss",]$Mean-NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Capriss",]$Se,
       angle=90,col="orange",length = 0.1)

points(x = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Ciflorette",]$groups,
       y = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Ciflorette",]$Mean,
       col="purple",type="o",pch=19,lty=1)
arrows(x0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Ciflorette",]$groups,
       y0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Ciflorette",]$Mean,
       x1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Ciflorette",]$groups,
       y1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Ciflorette",]$Mean+NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Ciflorette",]$Se,
       angle=90,col="purple",length = 0.1)
arrows(x0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Ciflorette",]$groups,
       y0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Ciflorette",]$Mean,
       x1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Ciflorette",]$groups,
       y1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Ciflorette",]$Mean-NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Ciflorette",]$Se,
       angle=90,col="purple",length = 0.1)

points(x = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Cir107",]$groups,
       y = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Cir107",]$Mean,
       col="blue",type="o",pch=19,lty=1)
arrows(x0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Cir107",]$groups,
       y0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Cir107",]$Mean,
       x1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Cir107",]$groups,
       y1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Cir107",]$Mean+NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Cir107",]$Se,
       angle=90,col="blue",length = 0.1)
arrows(x0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Cir107",]$groups,
       y0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Cir107",]$Mean,
       x1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Cir107",]$groups,
       y1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Cir107",]$Mean-NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Cir107",]$Se,
       angle=90,col="blue",length = 0.1)

points(x = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Clery",]$groups,
       y = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Clery",]$Mean,
       col="maroon",type="o",pch=19,lty=1)
arrows(x0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Clery",]$groups,
       y0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Clery",]$Mean,
       x1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Clery",]$groups,
       y1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Clery",]$Mean+NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Clery",]$Se,
       angle=90,col="maroon",length = 0.1)
arrows(x0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Clery",]$groups,
       y0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Clery",]$Mean,
       x1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Clery",]$groups,
       y1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Clery",]$Mean-NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Clery",]$Se,
       angle=90,col="maroon",length = 0.1)

points(x = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Darselect",]$groups,
       y = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Darselect",]$Mean,
       col="darkgreen",type="o",pch=19,lty=1)
arrows(x0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Darselect",]$groups,
       y0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Darselect",]$Mean,
       x1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Darselect",]$groups,
       y1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Darselect",]$Mean+NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Darselect",]$Se,
       angle=90,col="darkgreen",length = 0.1)
arrows(x0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Darselect",]$groups,
       y0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Darselect",]$Mean,
       x1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Darselect",]$groups,
       y1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Darselect",]$Mean-NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Darselect",]$Se,
       angle=90,col="darkgreen",length = 0.1)

points(x = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Gariguette",]$groups,
       y = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Gariguette",]$Mean,
       col="darkred",type="o",pch=19,lty=1)
arrows(x0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Gariguette",]$groups,
       y0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Gariguette",]$Mean,
       x1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Gariguette",]$groups,
       y1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Gariguette",]$Mean+NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Gariguette",]$Se,
       angle=90,col="darkred",length = 0.1)
arrows(x0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Gariguette",]$groups,
       y0 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Gariguette",]$Mean,
       x1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Gariguette",]$groups,
       y1 = NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Gariguette",]$Mean-NoTotal_leave.resum[NoTotal_leave.resum$genotype=="Gariguette",]$Se,
       angle=90,col="darkred",length = 0.1)

#==========================================================================

# 4.2.2- No. total flowers for all genotype
plot(x = dat.resum$Index,y = dat.resum$MeanTotalFlower,type="n",las=1,xlab = "Module order",ylab = "Mean of No. Total leaves",
     ylim=c(0,25),font.axis=2,font.lab=2,main = "Mean of No.total flowers by genotype \n as fonction of module order")
points(x = dat.resum[dat.resum$genotype=="Capriss",]$Index,
       y = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalFlower,
       type="o",lwd=2,pch=19,cex=0.8,col="orange")
segments(x0 = dat.resum[dat.resum$genotype=="Capriss",]$Index,y0 = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalFlower,
         x1 = dat.resum[dat.resum$genotype=="Capriss",]$Index,y1 = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalFlower+dat.resum[dat.resum$genotype=="Capriss",]$SdTotalFlower,
         col="orange")
segments(x0 = dat.resum[dat.resum$genotype=="Capriss",]$Index,y0 = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalFlower,
         x1 = dat.resum[dat.resum$genotype=="Capriss",]$Index,y1 = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalFlower-dat.resum[dat.resum$genotype=="Capriss",]$SdTotalFlower,
         col="orange")
points(x = dat.resum[dat.resum$genotype=="Cir107",]$Index,
       y = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalFlower,
       type="o",lwd=2,pch=19,cex=0.8,col="blue")
segments(x0 = dat.resum[dat.resum$genotype=="Cir107",]$Index,y0 = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalFlower,
         x1 = dat.resum[dat.resum$genotype=="Cir107",]$Index,y1 = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalFlower+dat.resum[dat.resum$genotype=="Cir107",]$SdTotalFlower,
         col="blue")
segments(x0 = dat.resum[dat.resum$genotype=="Cir107",]$Index,y0 = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalFlower,
         x1 = dat.resum[dat.resum$genotype=="Cir107",]$Index,y1 = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalFlower-dat.resum[dat.resum$genotype=="Cir107",]$SdTotalFlower,
         col="blue")
points(x = dat.resum[dat.resum$genotype=="Ciflorette",]$Index,
       y = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalFlower,
       type="o",lwd=2,pch=19,cex=0.8,col="purple")
segments(x0 = dat.resum[dat.resum$genotype=="Ciflorette",]$Index,y0 = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalFlower,
         x1 = dat.resum[dat.resum$genotype=="Ciflorette",]$Index,y1 = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalFlower+dat.resum[dat.resum$genotype=="Ciflorette",]$SdTotalFlower,
         col="purple")
segments(x0 = dat.resum[dat.resum$genotype=="Ciflorette",]$Index,y0 = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalFlower,
         x1 = dat.resum[dat.resum$genotype=="Ciflorette",]$Index,y1 = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalFlower-dat.resum[dat.resum$genotype=="Ciflorette",]$SdTotalFlower,
         col="purple")
points(x = dat.resum[dat.resum$genotype=="Clery",]$Index,
       y = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalFlower,
       type="o",lwd=2,pch=19,cex=0.8,col="maroon")
segments(x0 = dat.resum[dat.resum$genotype=="Clery",]$Index,y0 = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalFlower,
         x1 = dat.resum[dat.resum$genotype=="Clery",]$Index,y1 = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalFlower+dat.resum[dat.resum$genotype=="Clery",]$SdTotalFlower,
         col="maroon")
segments(x0 = dat.resum[dat.resum$genotype=="Clery",]$Index,y0 = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalFlower,
         x1 = dat.resum[dat.resum$genotype=="Clery",]$Index,y1 = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalFlower-dat.resum[dat.resum$genotype=="Clery",]$SdTotalFlower,
         col="maroon")
points(x = dat.resum[dat.resum$genotype=="Darselect",]$Index,
       y = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalFlower,
       type="o",lwd=2,pch=19,cex=0.8,col="darkgreen")
segments(x0 = dat.resum[dat.resum$genotype=="Darselect",]$Index,y0 = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalFlower,
         x1 = dat.resum[dat.resum$genotype=="Darselect",]$Index,y1 = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalFlower+dat.resum[dat.resum$genotype=="Darselect",]$SdTotalFlower,
         col="darkgreen")
segments(x0 = dat.resum[dat.resum$genotype=="Darselect",]$Index,y0 = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalFlower,
         x1 = dat.resum[dat.resum$genotype=="Darselect",]$Index,y1 = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalFlower-dat.resum[dat.resum$genotype=="Darselect",]$SdTotalFlower,
         col="darkgreen")
points(x = dat.resum[dat.resum$genotype=="Gariguette",]$Index,
       y = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalFlower,
       type="o",lwd=2,pch=19,cex=0.8,col="darkred")
segments(x0 = dat.resum[dat.resum$genotype=="Gariguette",]$Index,y0 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalFlower,
         x1 = dat.resum[dat.resum$genotype=="Gariguette",]$Index,y1 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalFlower+dat.resum[dat.resum$genotype=="Gariguette",]$SdTotalFlower,
         col="darkred")
segments(x0 = dat.resum[dat.resum$genotype=="Gariguette",]$Index,y0 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalFlower,
         x1 = dat.resum[dat.resum$genotype=="Gariguette",]$Index,y1 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalFlower-dat.resum[dat.resum$genotype=="Gariguette",]$SdTotalFlower,
         col="darkred")
legend("topright",legend = c("Capriss","Ciflorette","Cir107","Clery","Darselect","Gariguette"),
       lwd =c(2,2,2,2,2,2),pch=c(19,19,19,19,19,19),col = c("orange","purple","blue","maroon","darkgreen","darkred"),
       cex= 0.7)



"Observation: stabilisation of Mean No. total leaves after order1"

# 4.1.2 Existe t il une stabilisation du nombre de fleurs à partir de l'ordre 1 pour chaque genotype
"""
hypothese: Si pour chaque variété, le nombre total de feuilles est constant à partir de l'ordre 1
alors la pente est proche ou égale à 0 
==> 1. calcul de la pente pour chaque variétés--> regression linéaire
2. Est ce que la pente est proche de 0
3. Calcul de l'interval de confiance à 95% de la pente
==> si la pente est proche de 0 et si l'intervalle de confiance encadre 0
alors on peut considérer que la pente est égale à 0.
"""
#4.1.2.1- regression linéaire pour chaque variétés a partir de l'ordre 1.

#----- filtre du jeu de données par variétés--------

#Varieties without Order 0
data_without0<- dat[!dat$Index=="0",]

capriss_without0<-data_without0[data_without0$genotype=="Capriss",]
ciflorette_without0<-data_without0[data_without0$genotype=="Ciflorette",]
cir107_without0<-data_without0[data_without0$genotype=="Cir107",]
clery_without0<-data_without0[data_without0$genotype=="Clery",]
darselect_without0<-data_without0[data_without0$genotype=="Darselect",]
gariguette_without0<-data_without0[data_without0$genotype=="Gariguette",]

#Varieties without order0 and 1 
data_without0<- dat[!dat$Index=="0",]
data_without0_1<-data_without0[!data_without0$Index=="1",]

capriss_without0_1<-data_without0_1[data_without0_1$genotype=="Capriss",]
ciflorette_without0_1<-data_without0_1[data_without0_1$genotype=="Ciflorette",]
cir107_without0_1<-data_without0_1[data_without0_1$genotype=="Cir107",]
clery_without0_1<-data_without0_1[data_without0_1$genotype=="Clery",]
darselect_without0_1<-data_without0_1[data_without0_1$genotype=="Darselect",]
gariguette_without0_1<-data_without0_1[data_without0_1$genotype=="Gariguette",]

#----- regression linéaire--------
capriss_linearmodel<-lm(nb_total_flowers~Index,data =capriss_without0_1)
capriss.param<-coef(capriss_linearmodel) 
ciflorette_linearmodel<-lm(nb_total_flowers~Index,data =ciflorette_without0_1)
ciflorette.param<-coef(ciflorette_linearmodel) 
cir107_linearmodel<-lm(nb_total_flowers~Index,data =cir107_without0_1)
cir107.param<-coef(cir107_linearmodel) 
clery_linearmodel<-lm(nb_total_flowers~Index,data =clery_without0_1)
clery.param<-coef(clery_linearmodel) 
darselect_linearmodel<-lm(nb_total_flowers~Index,data =darselect_without0_1)
darselect.param<-coef(darselect_linearmodel) 
gariguette_linearmodel<-lm(nb_total_flowers~Index,data =gariguette_without0_1)
gariguette.param<- coef(gariguette_linearmodel)

"""
==> Pour chaque génotype la pentes est proche de 0,
Nous pouvons raisonnablement penser que le nombre de fleurs
à partir de l'ordre 1 est constant --> stabilité à partir de l'ordre 1"""

#----- Calcul de l'interval de confiance de la pente et de l'intersept à 95% --------

capriss.ICpente<-confint(object = capriss_linearmodel,parm = "Index",level = 0.95)
capriss.ICintercept<-confint(object = capriss_linearmodel,parm = "(Intercept)",level = 0.95)

ciflorette.ICpente<-confint(object = ciflorette_linearmodel,parm = "Index",level = 0.95)
ciflorette.ICintercept<-confint(object = ciflorette_linearmodel,parm = "(Intercept)",level = 0.95)

cir107.ICpente<-confint(object = cir107_linearmodel,parm = "Index",level = 0.95)
cir107.ICintercept<-confint(object = cir107_linearmodel,parm = "(Intercept)",level = 0.95)

clery.ICpente<-confint(object = clery_linearmodel,parm = "Index",level = 0.95)
clery.ICintercept<-confint(object = clery_linearmodel,parm = "(Intercept)",level = 0.95)

darselect.ICpente<-confint(object = darselect_linearmodel,parm = "Index",level = 0.95)
darselect.ICintercept<-confint(object = darselect_linearmodel,parm = "(Intercept)",level = 0.95)

gariguette.ICpente<-confint(object = gariguette_linearmodel,parm = "Index",level = 0.95)
gariguette.ICintercept<-confint(object = gariguette_linearmodel,parm = "(Intercept)",level = 0.95)

#table resum info regression lineaire pour chaque varieté: pente, IClower,ICupper
dat.reg<-data.frame(matrix(nrow = 6,ncol = 4))
colnames(dat.reg)<-c("Varieties","slope","IC95% lower","IC95% upper")
dat.reg[,1]<-c("Capriss","Ciflorette","Cir107","Clery","Darselect","Gariguette")
dat.reg[,2]<-c(capriss_linearmodel$coefficients[[2]],ciflorette_linearmodel$coefficients[[2]],
               cir107_linearmodel$coefficients[[2]],clery_linearmodel$coefficients[[2]],
               darselect_linearmodel$coefficients[[2]],gariguette_linearmodel$coefficients[[2]])
dat.reg[,3]<-c(capriss.ICpente[[1]],ciflorette.ICpente[[1]],cir107.ICpente[[1]],
               clery.ICpente[[1]],darselect.ICpente[[1]],gariguette.ICpente[[1]])
dat.reg[,4]<-c(capriss.ICpente[[2]],ciflorette.ICpente[[2]],cir107.ICpente[[2]],
               clery.ICpente[[2]],darselect.ICpente[[2]],gariguette.ICpente[[2]])

# Representation de la verification pour H0: la pente est nul au seuil 95%
"""
representation variable residuelle entre -1 et 1, il faut regarder si:
l'interval de confiance encadre 0. 
"""
# Capriss
plot(x = capriss_linearmodel$residuals,type="n",main = "Capriss",
     ylab = "Slope values",xlab="Individuals",font.axis=2,font.lab=2,las=1)
abline(h=0)
abline(h=capriss.ICpente[1],lty=2,col="red")
abline(h=capriss.ICpente[2],lty=2,col="red")
abline(h=capriss.param[2],lty=1,col="blue")
legend("topright",legend = c("slope","IC95%"),col = c("blue","red"),lty=c(1,2))

# Ciflorette
plot(x = ciflorette_linearmodel$residuals,type="n",main = "Ciflorette",
     ylab = "Slope values",xlab="Individuals",font.axis=2,font.lab=2,las=1)
abline(h=0)
abline(h=ciflorette.ICpente[1],lty=2,col="red")
abline(h=ciflorette.ICpente[2],lty=2,col="red")
abline(h=ciflorette.param[2],lty=1,col="blue")
legend("topright",legend = c("slope","IC95%"),col = c("blue","red"),lty=c(1,2))

# Cir107
plot(x = cir107_linearmodel$residuals,type="n",main = "Cir107",
     ylab = "Slope values",xlab="Individuals",font.axis=2,font.lab=2,las=1)
abline(h=0)
abline(h=cir107.ICpente[1],lty=2,col="red")
abline(h=cir107.ICpente[2],lty=2,col="red")
abline(h=cir107.param[2],lty=1,col="blue")
legend("topright",legend = c("slope","IC95%"),col = c("blue","red"),lty=c(1,2))

# clery
plot(x = clery_linearmodel$residuals,type="n",main = "Clery",
     ylab = "Slope values",xlab="Individuals",font.axis=2,font.lab=2,las=1)
abline(h=0)
abline(h=clery.ICpente[1],lty=2,col="red")
abline(h=clery.ICpente[2],lty=2,col="red")
abline(h=clery.param[2],lty=1,col="blue")
legend("topright",legend = c("slope","IC95%"),col = c("blue","red"),lty=c(1,2))

# darselect
plot(x = darselect_linearmodel$residuals,type="n",main = "Darselect",
     ylab = "Slope values",xlab="Individuals",font.axis=2,font.lab=2,las=1)
abline(h=0)
abline(h=darselect.ICpente[1],lty=2,col="red")
abline(h=darselect.ICpente[2],lty=2,col="red")
abline(h=darselect.param[2],lty=1,col="blue")
legend("topright",legend = c("slope","IC95%"),col = c("blue","red"),lty=c(1,2))

# gariguette
plot(x = gariguette_linearmodel$residuals,type="n",main = "Gariguette",
     ylab = "Slope values",xlab="Individuals",font.axis=2,font.lab=2,las=1)
abline(h=0)
abline(h=gariguette.ICpente[1],lty=2,col="red")
abline(h=gariguette.ICpente[2],lty=2,col="red")
abline(h=gariguette.param[2],lty=1,col="blue")
legend("topright",legend = c("slope","IC95%"),col = c("blue","red"),lty=c(1,2))

#----- Representation des données et model --------
dat.resum_without0<-dat.resum[!dat.resum$Index==0,]
dat.resum_without0_1<-dat.resum_without0[!dat.resum_without0$Index=="1",]

# calcul confidence interval of model
attach(dat.resum_without0_1)

capriss.pred.frame<-data.frame(Index=2:5)
capriss.pc<-predict(capriss_linearmodel, interval="confidence",
                    newdata=capriss.pred.frame)
ciflorette.pred.frame<-data.frame(Index=2:5)
ciflorette.pc<-predict(ciflorette_linearmodel, interval="confidence",
                       newdata=ciflorette.pred.frame)
cir107.pred.frame<-data.frame(Index=2:5)
cir107.pc<-predict(cir107_linearmodel, interval="confidence",
                   newdata=cir107.pred.frame)
clery.pred.frame<-data.frame(Index=2:5)
clery.pc<-predict(clery_linearmodel, interval="confidence",
                  newdata=clery.pred.frame)
darselect.pred.frame<-data.frame(Index=2:5)
darselect.pc<-predict(darselect_linearmodel, interval="confidence",
                      newdata=darselect.pred.frame)
gariguette.pred.frame<-data.frame(Index=1:5)
gariguette.pc<-predict(gariguette_linearmodel, interval="confidence",
                       newdata=gariguette.pred.frame)


# Representation graphique

plot(x = dat.resum_without0_1$Index,y = dat.resum_without0_1$MeanTotalFlower,
     main="Mean of No.Total Flowers\n for all varieties",
     ylab = "Mean of No.Total Flowers", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,10))
points(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$Index,
       y=dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$MeanTotalFlower,
       col="orange",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$MeanTotalFlower+dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$SdTotalFlower)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$MeanTotalFlower-dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$SdTotalFlower)

points(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$Index,
       y = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$MeanTotalFlower,
       col="purple",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$MeanTotalFlower+dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$SdTotalFlower)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$MeanTotalFlower-dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$SdTotalFlower)

points(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$Index,
       y=dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$MeanTotalFlower,
       col="blue",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$MeanTotalFlower+dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$SdTotalFlower)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$MeanTotalFlower-dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$SdTotalFlower)

points(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$Index,
       y=dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$MeanTotalFlower,
       col="maroon",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$MeanTotalFlower+dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$SdTotalFlower)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$MeanTotalFlower-dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$SdTotalFlower)

points(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$Index,
       y=dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$MeanTotalFlower,
       col="darkgreen",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$MeanTotalFlower+dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$SdTotalFlower)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$MeanTotalFlower-dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$SdTotalFlower)

points(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$Index,
       y=dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$MeanTotalFlower,
       col="darkred",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$MeanTotalFlower+dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$SdTotalFlower)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$MeanTotalFlower-dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$SdTotalFlower)

#legend("topleft",legend = c("Capriss","Ciflorette","Cir107","Clery","Darselect","Gariguette"),
#       lwd =c(2,2,2,2,2,2),pch=c(19,19,19,19,19,19),col = c("orange","purple","blue","maroon","darkgreen","darkred"),
#       cex= 0.7)

# representation par genotype + incertitude sur la pente

#Capriss
plot(x = dat.resum_without0_1$Index,y = dat.resum_without0_1$MeanTotalFlower,
     main="Mean of No.Total flowers\n for Capriss",
     ylab = "Mean of No.Total flowers", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,15))
points(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$Index,
       y=dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$MeanTotalFlower,
       col="orange",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$MeanTotalFlower+dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$SdTotalFlower,
         col="orange")
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$MeanTotalFlower-dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$SdTotalFlower,
         col="orange")
abline(capriss_linearmodel,lwd=2,lty=1)
abline(capriss.ICintercept[1],capriss.ICpente[1],col="red",lty=2)
abline(capriss.ICintercept[2],capriss.ICpente[2],col="red",lty=2)
matlines(capriss.pred.frame,capriss.pc[,2:3],lty=c(2,2),col="blue")
text(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$Index,y =1,
     labels = dat.resum_without0_1[dat.resum_without0_1$genotype=="Capriss",]$N)
legend("topright",legend = c("Confidence interval of slope at 95%","linear model","Confidence interval of model at 95%"),col=c("red","black","blue"),lty=c(2,1,2),cex=0.8)

#Ciflorette
plot(x = dat.resum_without0_1$Index,y = dat.resum_without0_1$MeanTotalFlower,
     main="Mean of No.Total Flowers, linear model and IC95% \n for ciflorette",
     ylab = "Mean of No.Total Flowers", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,15))
points(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$Index,
       y=dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$MeanTotalFlower,
       col="purple",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$MeanTotalFlower+dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$SdTotalFlower,
         col="purple")
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$MeanTotalFlower-dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$SdTotalFlower,
         col="purple")
abline(ciflorette_linearmodel,lwd=2,lty=1)
abline(ciflorette.ICintercept[1],ciflorette.ICpente[1],col="red",lty=2)
abline(ciflorette.ICintercept[2],ciflorette.ICpente[2],col="red",lty=2)
matlines(ciflorette.pred.frame,ciflorette.pc[,2:3],lty=c(2,2),col="blue")
text(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$Index,y =1,
     labels = dat.resum_without0_1[dat.resum_without0_1$genotype=="Ciflorette",]$N)
legend("topright",legend = c("Confidence interval of slope at 95%","linear model","Confidence interval of model at 95%"),col=c("red","black","blue"),lty=c(2,1,2),cex=0.8)

#Cir107
plot(x = dat.resum_without0_1$Index,y = dat.resum_without0_1$MeanTotalFlower,
     main="Mean of No.Total Flowers, linear model and IC95% \n for Cir107",
     ylab = "Mean of No.Total Flowers", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,15))
points(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$Index,
       y=dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$MeanTotalFlower,
       col=" blue",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$MeanTotalFlower+dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$SdTotalFlower,
         col="blue")
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$MeanTotalFlower-dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$SdTotalFlower,
         col="blue")
abline(cir107_linearmodel,lwd=2,lty=1)
abline(cir107.ICintercept[1],cir107.ICpente[1],col="red",lty=2)
abline(cir107.ICintercept[2],cir107.ICpente[2],col="red",lty=2)
matlines(cir107.pred.frame,cir107.pc[,2:3],lty=c(2,2),col="blue")
text(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$Index,y =1,
     labels = dat.resum_without0_1[dat.resum_without0_1$genotype=="Cir107",]$N)
legend("topright",legend = c("Confidence interval of slope at 95%","linear model","Confidence interval of model at 95%"),col=c("red","black","blue"),lty=c(2,1,2),cex=0.8)

#Clery
plot(x = dat.resum_without0_1$Index,y = dat.resum_without0_1$MeanTotalFlower,
     main="Mean of No.Total Flowers, linear model and IC95% \n for Clery",
     ylab = "Mean of No.Total Flowers", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,15))
points(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$Index,
       y = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$MeanTotalFlower,
       col="maroon",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$MeanTotalFlower+dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$SdTotalFlower,
         col="maroon")
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$MeanTotalFlower-dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$SdTotalFlower,
         col="maroon")
abline(clery_linearmodel,lwd=2,lty=1)
abline(clery.ICintercept[1],clery.ICpente[1],col="red",lty=2)
abline(clery.ICintercept[2],clery.ICpente[2],col="red",lty=2)
matlines(clery.pred.frame,clery.pc[,2:3],lty=c(2,2),col="blue")
text(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$Index,y =1,
     labels = dat.resum_without0_1[dat.resum_without0_1$genotype=="Clery",]$N)
legend("topright",legend = c("Confidence interval of slope at 95%","linear model","Confidence interval of model at 95%"),col=c("red","black","blue"),lty=c(2,1,2),cex=0.8)

#Darselect
plot(x = dat.resum_without0_1$Index,y = dat.resum_without0_1$MeanTotalFlower,
     main="Mean of No.Total Flowers, linear model and IC95% \n for Darselect",
     ylab = "Mean of No.Total Flowers", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,15))
points(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$Index,
       y=dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$MeanTotalFlower,
       col="darkgreen",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$MeanTotalFlower+dat.resum_without0[dat.resum_without0_1$genotype=="Darselect",]$SdTotalFlower,
         col="darkgreen")
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$MeanTotalFlower-dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$SdTotalFlower,
         col="darkgreen")
abline(darselect_linearmodel,lwd=2,lty=1)
abline(darselect.ICintercept[1],darselect.ICpente[1],col="red",lty=2)
abline(darselect.ICintercept[2],darselect.ICpente[2],col="red",lty=2)
matlines(darselect.pred.frame,darselect.pc[,2:3],lty=c(2,2),col="blue")
text(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$Index,y =1,
     labels = dat.resum_without0_1[dat.resum_without0_1$genotype=="Darselect",]$N)
legend("topright",legend = c("Confidence interval of slope at 95%","linear model","Confidence interval of model at 95%"),col=c("red","black","blue"),lty=c(2,1,2),cex=0.8)

#Gariguette
plot(x = dat.resum_without0_1$Index,y = dat.resum_without0_1$MeanTotalLeave,
     main="Mean of No.Total Flowers, linear model and IC95% \n for Gariguette",
     ylab = "Mean of No.Total Flowers", xlab= "Module order",
     font.axis=2, las=1, font.lab=2,type="n",
     ylim=c(0,15))
points(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$Index,
       y=dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$MeanTotalFlower,
       col="darkred",type="o",pch=19,lty=1)
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$MeanTotalFlower+dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$SdTotalFlower,
         col="darkred")
segments(x0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$Index,y0 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$MeanTotalFlower,
         x1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$Index,y1 = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$MeanTotalFlower-dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$SdTotalFlower,
         col="darkred")
abline(gariguette_linearmodel,lwd=2,lty=1)
abline(gariguette.ICintercept[1],gariguette.ICpente[1],col="red",lty=2)
abline(gariguette.ICintercept[2],gariguette.ICpente[2],col="red",lty=2)
matlines(gariguette.pred.frame,gariguette.pc[,2:3],lty=c(2,2),col="blue")
text(x = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$Index,y =1,
     labels = dat.resum_without0_1[dat.resum_without0_1$genotype=="Gariguette",]$N)
legend("topright",legend = c("Confidence interval of slope at 95%","linear model","Confidence interval of model at 95%"),col=c("red","black","blue"),lty=c(2,1,2),cex=0.8)



#4.2.1.2 Difference between varieties for order 0 and >=1
dat.NoTotal_flowers<- dat[,c(14,1,7)]

dat.NoTotal_flowers$groups[dat.NoTotal_flowers$Index==0]<-0
dat.NoTotal_flowers$groups[dat.NoTotal_flowers$Index==1]<-1
dat.NoTotal_flowers$groups[dat.NoTotal_flowers$Index==2]<-2
dat.NoTotal_flowers$groups[dat.NoTotal_flowers$Index==3]<-2
dat.NoTotal_flowers$groups[dat.NoTotal_flowers$Index==4]<-2
dat.NoTotal_flowers$groups[dat.NoTotal_flowers$Index==5]<-2

str(dat.NoTotal_flowers)

dat.NoTotal_flowers$groups<- as.numeric(x = dat.NoTotal_flowers$groups)


NoTotal_flowers.resum<- ddply(.data = dat.NoTotal_flowers,.variables = c("genotype","groups"),.fun = summarize,
                            Mean= mean(nb_total_flowers,na.rm=T),
                            Sd= sd(nb_total_flowers,na.rm=T),
                            N= length(nb_total_flowers))
NoTotal_flowers.resum$Se<-NoTotal_flowers.resum$Sd/sqrt(NoTotal_flowers.resum$N)

yliminf<- min(NoTotal_flowers.resum$Mean-NoTotal_flowers.resum$Se)
ylimsup<- max(NoTotal_flowers.resum$Mean+NoTotal_flowers.resum$Se)
dat.NoTotal_flowers0<- dat.NoTotal_flowers[dat.NoTotal_flowers$groups=="0",]
dat.NoTotal_flowers1<- dat.NoTotal_flowers[dat.NoTotal_flowers$groups=="1",]
dat.NoTotal_flowers2<- dat.NoTotal_flowers[dat.NoTotal_flowers$groups=="2",]

#ANOVA non Parametric Kruskal Wallis. Comparison between varieties for order0 then for order1

kruskal.test(nb_total_flowers~genotype,data=dat.NoTotal_flowers0)
k.duntest<-posthoc.kruskal.dunn.test(nb_total_flowers~genotype,data=dat.NoTotal_flowers0,p.adjust.method = "BH")
k.duntest$p.value

kruskal.test(nb_total_flowers~genotype,data=dat.NoTotal_flowers1)
k.duntest<-posthoc.kruskal.dunn.test(nb_total_flowers~genotype,data=dat.NoTotal_flowers1,p.adjust.method = "BH")
k.duntest$p.value

kruskal.test(nb_total_flowers~genotype,data=dat.NoTotal_flowers2)
k.duntest<-posthoc.kruskal.dunn.test(nb_total_flowers~genotype,data=dat.NoTotal_flowers2,p.adjust.method = "BH")
k.duntest$p.value


kruskal(y = dat.NoTotal_flowers$nb_total_flowers,trt = interaction(dat.NoTotal_flowers$genotype,dat.NoTotal_flowers$groups),alpha=0.05,group=T,console=T )
kruskal.test(dat.NoTotal_flowers$nb_total_flowers~interaction(dat.NoTotal_flowers$genotype,dat.NoTotal_flowers$groups),data=dat.NoTotal_flowers)
k.duntest<-posthoc.kruskal.dunn.test(dat.NoTotal_flowers$nb_total_flowers~interaction(dat.NoTotal_flowers$genotype,dat.NoTotal_flowers$groups),data=dat.NoTotal_flowers,p.adjust.method = "BH")
k.duntest$p.value

plot(x = NoTotal_flowers.resum$groups,y=NoTotal_flowers.resum$Mean,type="n",
     ylim=c(yliminf,ylimsup),ylab="Mean of No.Total Flowers",xlab="Module order",
     font.axis=2,font.lab=2,las=1)
points(x = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Capriss",]$groups,
       y = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Capriss",]$Mean,
       col="orange",type="o",pch=19,lty=1)
arrows(x0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Capriss",]$groups,
       y0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Capriss",]$Mean,
       x1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Capriss",]$groups,
       y1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Capriss",]$Mean+NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Capriss",]$Se,
       angle=90,col="orange",length = 0.1)
arrows(x0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Capriss",]$groups,
       y0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Capriss",]$Mean,
       x1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Capriss",]$groups,
       y1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Capriss",]$Mean-NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Capriss",]$Se,
       angle=90,col="orange",length = 0.1)
points(x = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Ciflorette",]$groups,
       y = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Ciflorette",]$Mean,
       col="purple",type="o",pch=19,lty=1)
arrows(x0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Ciflorette",]$groups,
       y0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Ciflorette",]$Mean,
       x1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Ciflorette",]$groups,
       y1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Ciflorette",]$Mean+NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Ciflorette",]$Se,
       angle=90,col="purple",length = 0.1)
arrows(x0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Ciflorette",]$groups,
       y0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Ciflorette",]$Mean,
       x1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Ciflorette",]$groups,
       y1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Ciflorette",]$Mean-NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Ciflorette",]$Se,
       angle=90,col="purple",length = 0.1)
points(x = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Cir107",]$groups,
       y = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Cir107",]$Mean,
       col="blue",type="o",pch=19,lty=1)
arrows(x0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Cir107",]$groups,
       y0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Cir107",]$Mean,
       x1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Cir107",]$groups,
       y1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Cir107",]$Mean+NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Cir107",]$Se,
       angle=90,col="blue",length = 0.1)
arrows(x0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Cir107",]$groups,
       y0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Cir107",]$Mean,
       x1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Cir107",]$groups,
       y1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Cir107",]$Mean-NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Cir107",]$Se,
       angle=90,col="blue",length = 0.1)
points(x = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Clery",]$groups,
       y = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Clery",]$Mean,
       col="maroon",type="o",pch=19,lty=1)
arrows(x0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Clery",]$groups,
       y0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Clery",]$Mean,
       x1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Clery",]$groups,
       y1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Clery",]$Mean+NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Clery",]$Se,
       angle=90,col="maroon",length = 0.1)
arrows(x0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Clery",]$groups,
       y0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Clery",]$Mean,
       x1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Clery",]$groups,
       y1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Clery",]$Mean-NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Clery",]$Se,
       angle=90,col="maroon",length = 0.1)
points(x = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Darselect",]$groups,
       y = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Darselect",]$Mean,
       col="darkgreen",type="o",pch=19,lty=1)
arrows(x0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Darselect",]$groups,
       y0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Darselect",]$Mean,
       x1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Darselect",]$groups,
       y1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Darselect",]$Mean+NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Darselect",]$Se,
       angle=90,col="darkgreen",length = 0.1)
arrows(x0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Darselect",]$groups,
       y0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Darselect",]$Mean,
       x1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Darselect",]$groups,
       y1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Darselect",]$Mean-NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Darselect",]$Se,
       angle=90,col="darkgreen",length = 0.1)
points(x = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Gariguette",]$groups,
       y = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Gariguette",]$Mean,
       col="darkred",type="o",pch=19,lty=1)
arrows(x0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Gariguette",]$groups,
       y0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Gariguette",]$Mean,
       x1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Gariguette",]$groups,
       y1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Gariguette",]$Mean+NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Gariguette",]$Se,
       angle=90,col="darkred",length = 0.1)
arrows(x0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Gariguette",]$groups,
       y0 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Gariguette",]$Mean,
       x1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Gariguette",]$groups,
       y1 = NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Gariguette",]$Mean-NoTotal_flowers.resum[NoTotal_flowers.resum$genotype=="Gariguette",]$Se,
       angle=90,col="darkred",length = 0.1)

#_________________________________________________________________________
#________________________________________________________________________
#Nb_stolon
dat.stolon<-dat[,c(14,1,11)]

dat.stolon.resum<- ddply(.data = dat.stolon,.variable= c("genotype","Index"),summarize,
                         Mean= mean(stolons,na.rm=T),
                         Sd= sd(stolons,na.rm=T),
                         N= length(stolons))
dat.stolon.resum$Se<- dat.stolon.resum$Sd/sqrt(dat.stolon.resum$N)

plot(x = dat.stolon.resum$Index,y = dat.stolon.resum$Mean,type="n",las=1,xlab = "Module order",ylab = "Mean of No. stolon",
     ylim=c(0,5),font.axis=2,font.lab=2,main = "Mean of No.stolon by genotype \n as fonction of module order")
points(x = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Index,
       y = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Mean,
       type="o",lwd=2,pch=19,cex=0.8,col="orange")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Index,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Index,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Mean+dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Sd,
         col="orange")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Index,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Index,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Mean-dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Sd,
         col="orange")
points(x = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Index,
       y = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Mean,
       type="o",lwd=2,pch=19,cex=0.8,col="blue")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Index,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Index,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Mean+dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Sd,
         col="blue")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Index,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Index,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Mean-dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Sd,
         col="blue")
points(x = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Index,
       y = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Mean,
       type="o",lwd=2,pch=19,cex=0.8,col="purple")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Index,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Index,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Mean+dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Sd,
         col="purple")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Index,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Index,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Mean-dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Sd,
         col="purple")
points(x = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Index,
       y = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Mean,
       type="o",lwd=2,pch=19,cex=0.8,col="maroon")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Index,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Index,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Mean+dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Sd,
         col="maroon")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Index,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Index,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Mean-dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Sd,
         col="maroon")
points(x = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Index,
       y = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Mean,
       type="o",lwd=2,pch=19,cex=0.8,col="darkgreen")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Index,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Index,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Mean+dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Sd,
         col="darkgreen")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Index,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Index,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Mean-dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Sd,
         col="darkgreen")
points(x = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Index,
       y = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Mean,
       type="o",lwd=2,pch=19,cex=0.8,col="darkred")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Index,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Index,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Mean+dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Sd,
         col="darkred")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Index,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Index,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Mean-dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Sd,
         col="darkred")
legend("topright",legend = c("Capriss","Ciflorette","Cir107","Clery","Darselect","Gariguette"),
       lwd =c(2,2,2,2,2,2),pch=c(19,19,19,19,19,19),col = c("orange","purple","blue","maroon","darkgreen","darkred"),
       cex= 0.7)

dat.stolon0<-dat.stolon[dat.stolon$Index=="0",]
dat.stolon1<-dat.stolon[dat.stolon$Index=="1",]
dat.stolon2<-dat.stolon[dat.stolon$Index=="2",]
dat.stolon3<-dat.stolon[dat.stolon$Index=="3",]
dat.stolon4<-dat.stolon[dat.stolon$Index=="4",]
dat.stolon5<-dat.stolon[dat.stolon$Index=="5",]

kruskal.test(stolons~genotype,data=dat.stolon0)
k.duntest<-posthoc.kruskal.dunn.test(stolons~genotype,data=dat.stolon0,p.adjust.method = "BH")
k.duntest$p.value

kruskal.test(stolons~genotype,data=dat.stolon1)
k.duntest<-posthoc.kruskal.dunn.test(stolons~genotype,data=dat.stolon1,p.adjust.method = "BH")
k.duntest$p.value

kruskal.test(stolons~genotype,data=dat.stolon2)
k.duntest<-posthoc.kruskal.dunn.test(stolons~genotype,data=dat.stolon2,p.adjust.method = "BH")
k.duntest$p.value

kruskal.test(stolons~genotype,data=dat.stolon3)
k.duntest<-posthoc.kruskal.dunn.test(stolons~genotype,data=dat.stolon3,p.adjust.method = "BH")
k.duntest$p.value

kruskal.test(stolons~genotype,data=dat.stolon4)
k.duntest<-posthoc.kruskal.dunn.test(stolons~genotype,data=dat.stolon4,p.adjust.method = "BH")
k.duntest$p.value

kruskal.test(stolons~genotype,data=dat.stolon5)
k.duntest<-posthoc.kruskal.dunn.test(stolons~genotype,data=dat.stolon5,p.adjust.method = "BH")
k.duntest$p.value

#grouping c( 0,1,2,>=3)
dat.stolon$groups[dat.stolon$Index==0]<-0
dat.stolon$groups[dat.stolon$Index==1]<-1
dat.stolon$groups[dat.stolon$Index==2]<-2
dat.stolon$groups[dat.stolon$Index==3]<-3
dat.stolon$groups[dat.stolon$Index==4]<-3
dat.stolon$groups[dat.stolon$Index==5]<-3

dat.stolon.resum<- ddply(.data = dat.stolon,.variable= c("genotype","groups"),summarize,
                         Mean= mean(stolons,na.rm=T),
                         Sd= sd(stolons,na.rm=T),
                         N= length(stolons))
dat.stolon.resum$Se<- dat.stolon.resum$Sd/sqrt(dat.stolon.resum$N)

plot(x = dat.stolon.resum$groups,y = dat.stolon.resum$Mean,type="n",las=1,xlab = "Module order",ylab = "Mean of No. stolon",
     ylim=c(0,5),font.axis=2,font.lab=2,main = "Mean of No.stolon by genotype \n as fonction of module order")
points(x = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$groups,
       y = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Mean,
       type="o",lwd=2,pch=19,cex=0.8,col="orange")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$groups,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$groups,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Mean+dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Sd,
         col="orange")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$groups,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$groups,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Mean-dat.stolon.resum[dat.stolon.resum$genotype=="Capriss",]$Sd,
         col="orange")
points(x = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$groups,
       y = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Mean,
       type="o",lwd=2,pch=19,cex=0.8,col="blue")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$groups,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$groups,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Mean+dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Sd,
         col="blue")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$groups,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$groups,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Mean-dat.stolon.resum[dat.stolon.resum$genotype=="Cir107",]$Sd,
         col="blue")
points(x = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$groups,
       y = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Mean,
       type="o",lwd=2,pch=19,cex=0.8,col="purple")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$groups,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$groups,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Mean+dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Sd,
         col="purple")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$groups,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$groups,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Mean-dat.stolon.resum[dat.stolon.resum$genotype=="Ciflorette",]$Sd,
         col="purple")
points(x = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$groups,
       y = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Mean,
       type="o",lwd=2,pch=19,cex=0.8,col="maroon")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$groups,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$groups,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Mean+dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Sd,
         col="maroon")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$groups,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$groups,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Mean-dat.stolon.resum[dat.stolon.resum$genotype=="Clery",]$Sd,
         col="maroon")
points(x = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$groups,
       y = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Mean,
       type="o",lwd=2,pch=19,cex=0.8,col="darkgreen")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$groups,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$groups,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Mean+dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Sd,
         col="darkgreen")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$groups,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$groups,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Mean-dat.stolon.resum[dat.stolon.resum$genotype=="Darselect",]$Sd,
         col="darkgreen")
points(x = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$groups,
       y = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Mean,
       type="o",lwd=2,pch=19,cex=0.8,col="darkred")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$groups,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$groups,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Mean+dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Sd,
         col="darkred")
segments(x0 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$groups,y0 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Mean,
         x1 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$groups,y1 = dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Mean-dat.stolon.resum[dat.stolon.resum$genotype=="Gariguette",]$Sd,
         col="darkred")
legend("topright",legend = c("Capriss","Ciflorette","Cir107","Clery","Darselect","Gariguette"),
       lwd =c(2,2,2,2,2,2),pch=c(19,19,19,19,19,19),col = c("orange","purple","blue","maroon","darkgreen","darkred"),
       cex= 0.7)

dat.stolon0<-dat.stolon[dat.stolon$groups=="0",]
dat.stolon1<-dat.stolon[dat.stolon$groups=="1",]
dat.stolon2<-dat.stolon[dat.stolon$groups=="2",]
dat.stolon3<-dat.stolon[dat.stolon$groups=="3",]



kruskal.test(stolons~genotype,data=dat.stolon0)
k.duntest<-posthoc.kruskal.dunn.test(stolons~genotype,data=dat.stolon0,p.adjust.method = "BH")
k.duntest$p.value

kruskal.test(stolons~genotype,data=dat.stolon1)
k.duntest<-posthoc.kruskal.dunn.test(stolons~genotype,data=dat.stolon1,p.adjust.method = "BH")
k.duntest$p.value

kruskal.test(stolons~genotype,data=dat.stolon2)
k.duntest<-posthoc.kruskal.dunn.test(stolons~genotype,data=dat.stolon2,p.adjust.method = "BH")
k.duntest$p.value

kruskal.test(stolons~genotype,data=dat.stolon3)
k.duntest<-posthoc.kruskal.dunn.test(stolons~genotype,data=dat.stolon3,p.adjust.method = "BH")
k.duntest$p.value


kruskal.test(dat.stolon$stolons~interaction(dat.stolon$genotype,dat.stolon$groups),data=dat.stolon)
k.duntest<-posthoc.kruskal.dunn.test(dat.stolon$stolon~interaction(dat.stolon$genotype,dat.stolon$groups),data=dat.stolon3,p.adjust.method = "BH")
k.duntest$p.value


#_______________________________________________________________________
#crown status par ordre
#Branching
BranchCrown<-dat[dat$type_of_crown=="Branch_Crown",]

#Nombre de branches par genotype et par index
Branching<-aggregate(cbind(BranchCrown$type_of_crown)~BranchCrown$genotype+BranchCrown$Index,FUN=length)
colnames(Branching)<-c("genotype","Index","branch_Crowns")

#Nombre de branche par genotype et plante
Branching.plante<-aggregate(cbind(BranchCrown$type_of_crown)~BranchCrown$genotype+BranchCrown$plant+BranchCrown$Index,FUN=length)
colnames(Branching.plante)<-c("genotype","plant","Index","branch_Crowns")

#Moyenne du nombre de branches par genotype et par Index
Means<- ddply(.data = Branching.plante,.variables = c("genotype","Index"),.fun = summarise,
                       means= mean(x = branch_Crowns,na.rm=T),
                       sd= sd(x = branch_Crowns,na.rm=T))#,median.openflower= median(x = sum.open_flower,na.rm = T))

# Moyenne du numbre de branches par genotype
Means.Genotype<- ddply(.data = Branching.plante,.variables = c("genotype"),.fun = summarise,
              means= mean(x = branch_Crowns,na.rm=T),
              sd= sd(x = branch_Crowns,na.rm=T))#,median.openflower= median(x = sum.open_flower,na.rm = T))

# Test de kruskal sur le nombre moyen de branche par genotype
kruskal(Branching.plante$branch_Crowns,Branching.plante$genotype,group=T, consol=T)
"""
Groups, Treatments and mean of the ranks
a 	 Capriss 	 80.73077 
ab 	 Ciflorette 	 60.66667 
b 	 Cir107 	 58.80952 
b 	 Gariguette 	 58.44118 
b 	 Clery 	 51.13043 
b 	 Darselect 	 42.61905"""

#Group index1 VS Index 2-5
Branching.plante$groups[Branching.plante$Index==1]<-1
Branching.plante$groups[Branching.plante$Index==2]<-2
Branching.plante$groups[Branching.plante$Index==3]<-2
Branching.plante$groups[Branching.plante$Index==4]<-2
Branching.plante$groups[Branching.plante$Index==5]<-2

Branching.planteorder1<-Branching.plante[Branching.plante$groups==1,]
Branching.planteorder2<-Branching.plante[Branching.plante$groups==2,]

#Test de kruskal sur le  nombre de branch pour order 1
kruskal(Branching.planteorder1$branch_Crowns,Branching.planteorder1$genotype,group=T, consol=T)
"""Groups, Treatments and mean of the ranks
a 	 Capriss 	 48.72222 
b 	 Cir107 	 40.38889 
c 	 Ciflorette 	 27.66667 
cd 	 Clery 	 20.27778 
de 	 Gariguette 	 17.72222 
e 	 Darselect 	 10.22222"""

#Test de kruskal sur le numbre moyen de branch pour l'order 2-5'
kruskal(Branching.planteorder2$branch_Crowns,Branching.planteorder2$genotype,group=T, consol=T)
"""Groups, Treatments and mean of the ranks
a 	 Gariguette 	 37.75 
ab 	 Ciflorette 	 33.88889 
ab 	 Clery 	 32.71429 
ab 	 Cir107 	 27.66667 
b 	 Darselect 	 24.41667 
b 	 Capriss 	 20 """
posthoc.kruskal.dunn.test(Branching.planteorder1$branch_Crowns,Branching.planteorder1$genotype,method="BH")

#Extension crown
ExtensionCrown<-dat[dat$type_of_crown=="Extention_Crown",]

#Nombre de Extension par genotype et par index
Extension<-aggregate(cbind(ExtensionCrown$type_of_crown)~ExtensionCrown$genotype+ExtensionCrown$Index,FUN=length)
colnames(Extension)<-c("genotype","Index","Extention_Crown")

#Nombre de Extension par genotype et plante
Extension.plante<-aggregate(cbind(ExtensionCrown$type_of_crown)~ExtensionCrown$genotype+ExtensionCrown$plant+ExtensionCrown$Index,FUN=length)
colnames(Extension.plante)<-c("genotype","plant","Index","Extention_Crown")

#Moyenne du nombre de branches par genotype et par Index
Means<- ddply(.data = Extension.plante,.variables = c("genotype","Index"),.fun = summarise,
              means= mean(x = Extention_Crown,na.rm=T),
              )#,median.openflower= median(x = sum.open_flower,na.rm = T))

# Moyenne du numbre de branches par genotype
Means.Genotype<- ddply(.data = Extension.plante,.variables = c("genotype"),.fun = summarise,
                       means= mean(x = Extention_Crown,na.rm=T),
                       sd= sd(x = Extention_Crown,na.rm=T))#,median.openflower= median(x = sum.open_flower,na.rm = T))

# Test de kruskal sur le nombre moyen de branche par genotype
kruskal(Extension.plante$Extention_Crown,Extension.plante$genotype,group=T, consol=T)


Extension.plante$groups[Branching.plante$Index==1]<-1
Extension.plante$groups[Branching.plante$Index==2]<-2
Extension.plante$groups[Branching.plante$Index==3]<-2
Extension.plante$groups[Branching.plante$Index==4]<-2
Extension.plante$groups[Branching.plante$Index==5]<-2

Branching.planteorder1<-Branching.plante[Branching.plante$groups==1,]
Branching.planteorder2<-Branching.plante[Branching.plante$groups==2,]



"""           Gariguette Ciflorette Clery   Capriss Darselect
Ciflorette 0.76212    -          -       -       -        
Clery      0.99936    0.91929    -       -       -        
Capriss    0.00042    0.05151    0.00175 -       -        
Darselect  0.91438    0.17343    0.75342 3.1e-06 -        
Cir107     0.02720    0.52141    0.07289 0.87175 0.00068  

Groups, Treatments and mean of the ranks
a 	 Capriss 	 48.72222 
b 	 Cir107 	 40.38889 
c 	 Ciflorette 	 27.66667 
cd 	 Clery 	 20.27778 
de 	 Gariguette 	 17.72222 
e 	 Darselect 	 10.22222
"""




##############################################
#Comparaison branch crown extension crown propre
Caprissbea<-Capriss[!Capriss$Index=="4",]
Ciflorettebea<-Ciflorette[!Ciflorette$Index=="5",]
Cir107bea<-Cir107[Cir107$Index=="3",]
Darselectbea<-Darselect[!Darselect$Index=="5",]
Gariguetttebea<-Gariguette[!Gariguette$Index=="5",]
Gariguetttebea<-Gariguetttebea[!Gariguetttebea$Index=="4",]

contingence.total<-merge(Caprissbea,Ciflorettebea)

#par genotype
contingence<-table(dat$type_of_crown, dat$genotype)
addmargins(contingence) 

prop.table(contingence,2) #pourcentage en colone

contingence2<-contingence[2:3,1:6]
addmargins(contingence2)
prop.table(contingence2,2)
 
chisq.test(contingence2)

""" Pearson's Chi-squared test

data:  contingence2
X-squared = 23.902, df = 5, p-value = 0.0002267 """

"""                Gariguette Ciflorette Clery Capriss Darselect Cir107
Extention_Crown        116        154   129     169       139    181
Branch_Crown            71         90    80     158        53    132"""

fisher.test(contingence2[,c(5,6)])

"Gariguette-Ciflorette 0.8412
 Gariguette-Clery 1
 Gariguette-Capriss 0.02681
 Gariguette-Darselect 0.03743
 Gariguette-Cir107 0.3971 ???
 Ciflorette-Clery 0.7711
 Ciflorette-Capriss 0.008095
 Ciflorette-Darselect 0.05073
 Ciflorette-Cir107 0.2225
 Clery-Capriss 0.02585
 Clery-Darselect 0.02593
 Clery-Cir107 0.4132
 Capriss-Darselect 3.428e-06
 Capriss-Cir107 0.1314
 Darselect-Cir107 0.001186
"

#par Genotype par order
Capriss<-dat[dat$genotype=="Capriss",]
Ciflorette<-dat[dat$genotype=="Ciflorette",]
Cir107<-dat[dat$genotype=="Cir107",]
Clery<-dat[dat$genotype=="Clery",]
Darselect<-dat[dat$genotype=="Darselect",]
Gariguette<-dat[dat$genotype=="Gariguette",]

Contingencegenotype_order<-table(dat$genotype, dat$Index)
addmargins(Contingencegenotype_order)

#table de contingence par odre pour chaque varieties
Capriss$groups[Capriss$Index=="0"]<-0
Capriss$groups[Capriss$Index=="1"]<-1
Capriss$groups[Capriss$Index=="2"]<-2
Capriss$groups[Capriss$Index=="3"]<-3
Capriss$groups[Capriss$Index=="4"]<-3
Capriss$groups[Capriss$Index=="5"]<-3

contingence.Capriss<-table(Capriss$type_of_crown,Capriss$groups)
contingence.Capriss<-contingence.Capriss[2:3,2:4]
Capriss.prop<-prop.table(contingence.Capriss,2)

chisq.test(contingence.Capriss[,c(1:3)])
chisq.test(contingence.Capriss[,c(2:3)])

contingence.Ciflorette<-table(Ciflorette$type_of_crown,Ciflorette$Index)
contingence.Ciflorette<-contingence.Ciflorette[2:3,2:5]
Ciflorette.prop<-prop.table(contingence.Ciflorette,2)
Ciflorette.prop<-prop.table(contingence.Ciflorette,1)

chisq.test(contingence.Ciflorette[,c(2:4)]) #p-value = 0.2764
chisq.test(contingence.Ciflorette[,c(3,4)]) #p-value = 0.753


Cir107$groups[Cir107$Index=="0"]<-0
Cir107$groups[Cir107$Index=="1"]<-1
Cir107$groups[Cir107$Index=="2"]<-2
Cir107$groups[Cir107$Index=="3"]<-3
Cir107$groups[Cir107$Index=="4"]<-3

contingence.Cir107<-table(Cir107$type_of_crown,Cir107$groups)
contingence.Cir107<-contingence.Cir107[2:3,2:4]
Cir107.prop<-prop.table(contingence.Cir107,2)
Cir107.prop<-prop.table(contingence.Cir107,1)

chisq.test(contingence.Cir107[,c(2:3)]) #p-value = 0.6813

contingence.Clery<-table(Clery$type_of_crown,Clery$Index)
contingence.Clery<-contingence.Clery[2:3,2:5]
Clery.prop<-prop.table(contingence.Clery,2)
Clery.prop<-prop.table(contingence.Clery,1)

chisq.test(contingence.Clery[,c(2:4)]) #p-value = 1


fisher.test(contingence.Clery[,c(3,4)]) #p-value = 1
fisher.test(contingence.Clery[,c(2,3)]) #p-value = 0.7944

Darselect$groups[Darselect$Index=="0"]<-0
Darselect$groups[Darselect$Index=="1"]<-1
Darselect$groups[Darselect$Index=="2"]<-2
Darselect$groups[Darselect$Index=="3"]<-3
Darselect$groups[Darselect$Index=="4"]<-4
Darselect$groups[Darselect$Index=="5"]<-4

contingence.Darselect<-table(Darselect$type_of_crown,Darselect$groups)
contingence.Darselect<-contingence.Darselect[2:3,2:5]
Darselect.prop<-prop.table(contingence.Darselect,2)
Darselect.prop<-prop.table(contingence.Darselect,1)

chisq.test(contingence.Darselect[,c(2:4)]) #p-value = 1

Gariguette$groups[Gariguette$Index=="0"]<-0
Gariguette$groups[Gariguette$Index=="1"]<-1
Gariguette$groups[Gariguette$Index=="2"]<-2
Gariguette$groups[Gariguette$Index=="3"]<-3
Gariguette$groups[Gariguette$Index=="4"]<-4
Gariguette$groups[Gariguette$Index=="5"]<-4

contingence.Gariguette<-table(Gariguette$type_of_crown,Gariguette$groups)
contingence.Gariguette<-contingence.Gariguette[2:3,2:5]
Gariguette.prop<-prop.table(contingence.Gariguette,2)
Gariguette.prop<-prop.table(contingence.Gariguette,1)

chisq.test(contingence.Gariguette[,c(2:4)]) 








#regroupement à partir de l'order 1 vs 2-5

dat$groups[dat$Index=="0"]<-0
dat$groups[dat$Index=="1"]<-1
dat$groups[dat$Index=="2"]<-2
dat$groups[dat$Index=="3"]<-2
dat$groups[dat$Index=="4"]<-2
dat$groups[dat$Index=="5"]<-2

#séparation du jeu de donnée en entre 1 vs 2-5
Order1<-dat[dat$groups=="1",]
Order2_5<-dat[dat$groups=="2",]

contingence_order1<-table(Order1$type_of_crown,Order1$genotype)
contingence_order1<-contingence_order1[2:3,1:6]
prop.table(contingence_order1,2)

"                Gariguette Ciflorette Clery Capriss Darselect Cir107
Extention_Crown         37         40    40      36        48     39
Branch_Crown            57         75    58     154        39    115"

contingence_order2_5<-table(Order2_5$type_of_crown,Order2_5$genotype)
contingence_order2_5<-contingence_order2_5[2:3,1:6]
prop.table(contingence_order2_5,2)

fisher.test(contingence_order1[,c(5,6)])
"
Gariguette-Ciflorette 0.5646
Gariguette-Clery 0.8834
Gariguette-Capriss 0.0003002
Gariguette-Darselect 0.0377
Gariguette-Cir107 0.02338
Ciflorette-Clery 0.3962
Ciflorette-Capriss 0.002579
Ciflorette-Darselect 0.004302
Ciflorette-Cir107 0.105
Clery-Capriss 0.0001189
Clery-Darselect 0.05648
Clery-Cir107 0.01213
Capriss-Darselect 3.235e-09
Capriss-Cir107 0.189
Darselect-Cir107 6.266e-06
"
fisher.test(contingence_order2_5[,c(4,6)])

"
Gariguette-Ciflorette 0.5457
Gariguette-Clery 0.4615
Gariguette-Capriss 0.001777
Gariguette-Darselect 0.8387
Gariguette-Cir107 0.3254 
Ciflorette-Clery 0.106 
Ciflorette-Capriss 0.007644 
Ciflorette-Darselect 0.6957
Ciflorette-Cir107 0.8516
Clery-Capriss 1.471e-05
Clery-Darselect 0.273
Clery-Cir107 0.05188
Capriss-Darselect 0.002702
Capriss-Cir107 0.0114
Darselect-Cir107 0.5604
"

Table <- read.csv(
  "Z:/G1/Marc-Labadie/R/R-users/FraFlo/DataRaw/Table_de_contingence.csv", 
  sep=";",na.strings = "")

Tableorder1<-Table[,c(1,2)]
Tableorder1<-t(Tableorder1)

Table<-as.matrix(Table)
  
res<-chisq.test(Table[1:6,2:3],correct = T,B = 2000)

summary(res)

"""	Pearson's Chi-squared test

data:  Table
X-squared = 49.875, df = 20, p-value = 0.0002308
il n'y a d'effet du génotype sur le type de bougeons terminal
"""



res$observed
res$expected
res$residuals
res$residuals^2

install.packages('gtools')
library(gtools)
fisher.multcomp(Table)

prop.test(Table[2,],Table[3,])

"""                Gariguette Ciflorette Clery Capriss Darselect Cir107
Primary_Crown            0          0     0       0         0      0
Extention_Crown        116        154   129     169       139    181
Branch_Crown            71         90    80     158        53    132"""

"""

2-sample test for equality of proportions with continuity correction
genotype comparison      Pvalue 
Gariguette- Ciflorette   0.8967
Gariguette- Clery        1
Gariguette - Capriss     0.02932 ***
Gariguette - Darselect   0.04131 ***
Gariguette - Cir107      0.4053  ?
Ciflorette- Clery        0.8354  
Ciflorette - Capriss     0.008261 ***
Ciflorette - Darselect   0.0516 
Ciflorette - Cir107      0.2391  ?
Clery - Capriss          0.02833 ***
Clery - Darselect        0.03065 ***
Clery - Cir107           0.4255
Capriss - Darselect      5.476e-06 ***
Capriss - Cir107         0.1384
Darselect - Cir107       0.001358 ***
"""

Table<-table(CrownStatus$genotype,CrownStatus$type_of_crown)
res<-chisq.test(Table[1:6,2:3],correct = T,B = 2000)
"""
Pearson's Chi-squared test

data:  Table[1:6, 2:3]
X-squared = 23.902, df = 5, p-value = 0.0002267"""

res$observed
res$expected
res$residuals
res$residuals^2


prop.test(Table[1:2,c(2,3)])

aggregate(cbind(type_of_crown)~genotype+plant,data=dat2,length(dat2$type_of_crown))



Tab<- aggregate(cbind(DataSet$nb_visible_leaves)~DataSet$genotype+DataSet$date+DataSet$Index,FUN = sum)

###############################


dat$groups[dat$Index==0]<-0
dat$groups[dat$Index==1]<-1
dat$groups[dat$Index==2]<-1
dat$groups[dat$Index==3]<-1
dat$groups[dat$Index==4]<-1
dat$groups[dat$Index==5]<-1

ggplot(data=dat.resum, aes(x= dat.resum$groups,y=dat.resum$MeanTotalLeave),col=dat.resum$genotype)+
  geom_point(aes(x= dat.resum$groups,y=dat.resum$MeanTotalLeave))

dat.resum<-ddply(.data = dat,.variables = c("genotype","groups"),summarise,
                 MeanTotalLeave= round(mean(x = nb_total_leaves,na.rm = T),2),
                 SdTotalLeave= round(sd(x = nb_total_leaves,na.rm = T),2),N=length(nb_total_leaves))


  plot(x = dat.resum$groups,y = dat.resum$MeanTotalLeave,type="n",las=1,xlab = "Module order",ylab = "Mean of No. Total leaves",
       ylim=c(0,15),font.axis=2,font.lab=2,main = "Mean of No.total leaves by genotype \n as fonction of module order")
  points(x = dat.resum[dat.resum$genotype=="Capriss",]$groups,
         y = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalLeave,
         type="o",lwd=2,pch=19,cex=0.8,col="orange")
  segments(x0 = dat.resum[dat.resum$genotype=="Capriss",]$groups,y0 = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalLeave,
           x1 = dat.resum[dat.resum$genotype=="Capriss",]$groups,y1 = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalLeave+dat.resum[dat.resum$genotype=="Capriss",]$SdTotalLeave,
           col="orange")
  segments(x0 = dat.resum[dat.resum$genotype=="Capriss",]$groups,y0 = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalLeave,
           x1 = dat.resum[dat.resum$genotype=="Capriss",]$groups,y1 = dat.resum[dat.resum$genotype=="Capriss",]$MeanTotalLeave-dat.resum[dat.resum$genotype=="Capriss",]$SdTotalLeave,
           col="orange")
  points(x = dat.resum[dat.resum$genotype=="Cir107",]$groups,
         y = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalLeave,
         type="o",lwd=2,pch=19,cex=0.8,col="blue")
  segments(x0 = dat.resum[dat.resum$genotype=="Cir107",]$groups,y0 = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalLeave,
           x1 = dat.resum[dat.resum$genotype=="Cir107",]$groups,y1 = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalLeave+dat.resum[dat.resum$genotype=="Cir107",]$SdTotalLeave,
           col="blue")
  segments(x0 = dat.resum[dat.resum$genotype=="Cir107",]$groups,y0 = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalLeave,
           x1 = dat.resum[dat.resum$genotype=="Cir107",]$groups,y1 = dat.resum[dat.resum$genotype=="Cir107",]$MeanTotalLeave-dat.resum[dat.resum$genotype=="Cir107",]$SdTotalLeave,
           col="blue")
  points(x = dat.resum[dat.resum$genotype=="Ciflorette",]$groups,
         y = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalLeave,
         type="o",lwd=2,pch=19,cex=0.8,col="purple")
  segments(x0 = dat.resum[dat.resum$genotype=="Ciflorette",]$groups,y0 = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalLeave,
           x1 = dat.resum[dat.resum$genotype=="Ciflorette",]$groups,y1 = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalLeave+dat.resum[dat.resum$genotype=="Ciflorette",]$SdTotalLeave,
           col="purple")
  segments(x0 = dat.resum[dat.resum$genotype=="Ciflorette",]$groups,y0 = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalLeave,
           x1 = dat.resum[dat.resum$genotype=="Ciflorette",]$groups,y1 = dat.resum[dat.resum$genotype=="Ciflorette",]$MeanTotalLeave-dat.resum[dat.resum$genotype=="Ciflorette",]$SdTotalLeave,
           col="purple")
  points(x = dat.resum[dat.resum$genotype=="Clery",]$groups,
         y = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalLeave,
         type="o",lwd=2,pch=19,cex=0.8,col="maroon")
  segments(x0 = dat.resum[dat.resum$genotype=="Clery",]$groups,y0 = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalLeave,
           x1 = dat.resum[dat.resum$genotype=="Clery",]$groups,y1 = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalLeave+dat.resum[dat.resum$genotype=="Clery",]$SdTotalLeave,
           col="maroon")
  segments(x0 = dat.resum[dat.resum$genotype=="Clery",]$groups,y0 = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalLeave,
           x1 = dat.resum[dat.resum$genotype=="Clery",]$groups,y1 = dat.resum[dat.resum$genotype=="Clery",]$MeanTotalLeave-dat.resum[dat.resum$genotype=="Clery",]$SdTotalLeave,
           col="maroon")
  points(x = dat.resum[dat.resum$genotype=="Darselect",]$groups,
         y = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalLeave,
         type="o",lwd=2,pch=19,cex=0.8,col="darkgreen")
  segments(x0 = dat.resum[dat.resum$genotype=="Darselect",]$groups,y0 = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalLeave,
           x1 = dat.resum[dat.resum$genotype=="Darselect",]$groups,y1 = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalLeave+dat.resum[dat.resum$genotype=="Darselect",]$SdTotalLeave,
           col="darkgreen")
  segments(x0 = dat.resum[dat.resum$genotype=="Darselect",]$groups,y0 = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalLeave,
           x1 = dat.resum[dat.resum$genotype=="Darselect",]$groups,y1 = dat.resum[dat.resum$genotype=="Darselect",]$MeanTotalLeave-dat.resum[dat.resum$genotype=="Darselect",]$SdTotalLeave,
           col="darkgreen")
  points(x = dat.resum[dat.resum$genotype=="Gariguette",]$groups,
         y = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave,
         type="o",lwd=2,pch=19,cex=0.8,col="darkred")
  segments(x0 = dat.resum[dat.resum$genotype=="Gariguette",]$groups,y0 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave,
           x1 = dat.resum[dat.resum$genotype=="Gariguette",]$groups,y1 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave+dat.resum[dat.resum$genotype=="Gariguette",]$SdTotalLeave,
           col="red")
  segments(x0 = dat.resum[dat.resum$genotype=="Gariguette",]$groups,y0 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave,
           x1 = dat.resum[dat.resum$genotype=="Gariguette",]$groups,y1 = dat.resum[dat.resum$genotype=="Gariguette",]$MeanTotalLeave-dat.resum[dat.resum$genotype=="Gariguette",]$SdTotalLeave,
           col="red")
  legend("topright",legend = c("Capriss","Ciflorette","Cir107","Clery","Darselect","Gariguette"),
         lwd =c(2,2,2,2,2,2),pch=c(19,19,19,19,19,19),col = c("orange","purple","blue","maroon","darkgreen","darkred"),
         cex= 0.8)
  

Order0<-dat[dat$group==0,]
Order1<-dat[dat$group==1,]

kruskal(Order0$nb_total_leaves, Order0$genotype,consol=T, group=T)
posthoc.kruskal.nemenyi.test(Order0$nb_total_leaves~Order0$genotype,p.adjust.method = "BH")

kruskal(Order1$nb_total_leaves, Order1$genotype,consol=T, group=T)
posthoc.kruskal.nemenyi.test(Order1$nb_total_leaves~Order1$genotype,p.adjust.method = "BH")

Capriss<- dat[dat$genotype=="Capriss",]

kruskal(Capriss$nb_total_leaves,trt=Capriss$groups,group=T, console=T)
posthoc.kruskal.nemenyi.test(Capriss$nb_total_leaves~Capriss$groups,p.adjust.method = "BH")

"	Pairwise comparisons using Tukey and Kramer (Nemenyi) test	
                   with Tukey-Dist approximation for independent samples 

data:  Capriss$nb_total_leaves by Capriss$groups 

0       1       2      
1 < 2e-16 -       -      
2 4.1e-14 0.00927 -      
3 4.4e-14 0.08646 0.00018

P value adjustment method: none"

Ciflorette<- dat[dat$genotype=="Ciflorette",]
kruskal(Ciflorette$nb_total_leaves,trt=Ciflorette$groups,group=T, console=T)
posthoc.kruskal.nemenyi.test(Ciflorette$nb_total_leaves~Ciflorette$groups,p.adjust.method = "BH")

"		Pairwise comparisons using Tukey and Kramer (Nemenyi) test	
                   with Tukey-Dist approximation for independent samples 

data:  Ciflorette$nb_total_leaves by Ciflorette$groups 

0       1    2   
1 3.4e-14 -    -   
2 3.0e-11 0.51 -   
3 4.7e-14 0.70 0.14

"

Cir107<- dat[dat$genotype=="Cir107",]

kruskal(Cir107$nb_total_leaves,trt=Cir107$groups,group=T, console=T)
posthoc.kruskal.nemenyi.test(Cir107$nb_total_leaves~Cir107$groups,p.adjust.method = "BH")

"		Pairwise comparisons using Tukey and Kramer (Nemenyi) test	
                   with Tukey-Dist approximation for independent samples 

data:  Cir107$nb_total_leaves by Cir107$groups 

  0       1     2    
1 7.6e-14 -     -    
2 4.0e-14 0.011 -    
3 1.3e-11 0.836 0.469
"
Clery<- dat[dat$genotype=="Clery",]

kruskal(Clery$nb_total_leaves,trt=Clery$groups,group=T, console=T)
posthoc.kruskal.nemenyi.test(Clery$nb_visible_leaves~Clery$groups,p.adjust.method = "BH")
"		Pairwise comparisons using Tukey and Kramer (Nemenyi) test	
                   with Tukey-Dist approximation for independent samples 

data:  Clery$nb_visible_leaves by Clery$groups 

0       1    2   
1 2.7e-14 -    -   
2 7.2e-14 0.99 -   
3 4.4e-14 0.28 0.23
"
Darselect<- dat[dat$genotype=="Darselect",]

kruskal(Darselect$nb_total_leaves,trt=Darselect$groups,group=T, console=T)
posthoc.kruskal.nemenyi.test(Darselect$nb_total_leaves~Darselect$groups,p.adjust.method = "BH")
"	Pairwise comparisons using Tukey and Kramer (Nemenyi) test	
                   with Tukey-Dist approximation for independent samples
data:  Darselect$nb_total_leaves by Darselect$groups 

0       1     2    
1 4.0e-10 -     -    
2 5.2e-14 0.074 -    
3 2.8e-14 0.002 0.643
"

Gariguette<- dat[dat$genotype=="Gariguette",]

kruskal(Gariguette$nb_total_leaves,trt=Gariguette$groups,group=T, console=T)
posthoc.kruskal.nemenyi.test(Gariguette$nb_total_leaves~Gariguette$groups,p.adjust.method = "BH")

"		Pairwise comparisons using Tukey and Kramer (Nemenyi) test	
                   with Tukey-Dist approximation for independent samples 

data:  Gariguette$nb_total_leaves by Gariguette$groups 

0       1    2   
1 4.4e-14 -    -   
2 5.1e-14 0.59 -   
3 3.6e-14 0.74 0.23

P value adjustment method: none  "


kruskal(Gariguette$nb_visible_leaves,trt=Gariguette$groups,group=T, console=T)



group0<- dat[!dat$groups==0,]
group1<- dat[dat$groups==1,]
group2<- dat[dat$groups==2,]
group3<- dat[dat$groups==3,]

kruskal(group0$nb_total_flowers,trt=interaction(group0$genotype,group0$groups),group = T,console = T)


order_contingenceGariguette<-table(Gariguette$Index,Gariguette$date)

prop.table(order_contingenceGariguette,1)









##############################
dat

Gariguette
Gariguette_inflorescence()
