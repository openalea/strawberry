 meteo<- read.csv(file = "C:\\Users\\mlabadie\\Documents\\GitHub\\strawberry\\share\\data\\meteo\\meteo_douville.csv",header= TRUE,sep= ";",na.string="",dec=",")

 install.packages(pkgs = c("plyr","dplyr","reshape","ggplot2","rmarkdown","knitr","scales","mice","VIM","imputeTS"))

library(plyr)
library(dplyr)
library(reshape)
library(ggplot2)
library(rmarkdown)
library(knitr)
library(scales)
library(mice)
library(VIM)
library(imputeTS)

fc_summary.data<-function(data,varname, index.variable){
  if (length(x = index.variable)==1){
    if (length(x = varname)==1){
      dat<- do.call(data.frame,aggregate(x =data[varname],
                                         by=list(data[,index.variable[1]]),
                                         function(x)c(mean=mean(x,na.rm = T),
                                                      sd=sd(x,na.rm = T)
                                         )
      ))
      
      colnames(dat)<-c(index.variable,
                       paste(varname,".mean",sep = ""),
                       paste(varname,".sd",sep = ""))
    }else
      dat<- do.call(data.frame,aggregate(x =data[varname],
                                         by=list(data[,index.variable[1]]),
                                         function(x)c(mean=mean(x,na.rm = T),
                                                      sd=sd(x,na.rm = T)
                                         )
      ))
    
  }else if(length(x = index.variable)==2){
    if (length(x = varname)==1){
      dat<- do.call(data.frame,aggregate(x =data[varname],
                                         by=list(data[,index.variable[1]],data[,index.variable[2]]),
                                         function(x)c(mean=mean(x,na.rm = T),
                                                      sd=sd(x,na.rm = T)
                                         )
      ))
      
      colnames(dat)<-c(index.variable,
                       paste(varname,".mean",sep = ""),
                       paste(varname,".sd",sep = ""))
    }else
      dat<- do.call(data.frame,aggregate(x =data[varname],
                                         by=list(data[,index.variable[1]],
                                                 data[,index.variable[2]]),
                                         function(x)c(mean=mean(x,na.rm = T),
                                                      sd=sd(x,na.rm = T)
                                         )
      ))
    
  } else if (length(x = index.variable)==3){
    if (length(x = varname)==1){
      dat<- do.call(data.frame,aggregate(x =data[varname],
                                         by=list(data[,index.variable[1]],
                                                 data[,index.variable[2]],
                                                 data[,index.variable[3]]),
                                         function(x)c(mean=mean(x,na.rm = T),
                                                      sd=sd(x,na.rm = T)
                                         )
      ))
      
      colnames(dat)<-c(index.variable,
                       paste(varname,".mean",sep = ""),
                       paste(varname,".sd",sep = ""))
    }else
      dat<- do.call(data.frame,aggregate(x =data[varname],
                                         by=list(data[,index.variable[1]],
                                                 data[,index.variable[2]],
                                                 data[,index.variable[3]]),
                                         function(x)c(mean=mean(x,na.rm = T),
                                                      sd=sd(x,na.rm = T)
                                         )
      ))
    
  }else if (length(x = index.variable)==4){
    if (length(x = varname)==1){
      dat<- do.call(data.frame,aggregate(x =data[varname],
                                         by=list(data[,index.variable[1]],
                                                 data[,index.variable[2]],
                                                 data[,index.variable[3]],
                                                 data[,index.variable[4]]),
                                         function(x)c(mean=mean(x,na.rm = T),
                                                      sd=sd(x,na.rm = T)
                                         )
      ))
      
      colnames(dat)<-c(index.variable,
                       paste(varname,".mean",sep = ""),
                       paste(varname,".sd",sep = ""))
    }else
      dat<- do.call(data.frame,aggregate(x =data[varname],
                                         by=list(data[,index.variable[1]],
                                                 data[,index.variable[2]],
                                                 data[,index.variable[3]],
                                                 data[,index.variable[4]]),
                                         function(x)c(mean=mean(x,na.rm = T),
                                                      sd=sd(x,na.rm = T)
                                         )
      ))
  }else
    
    print("You have too much factor")
  
  

  names(dat)[match("Group.1",names(dat))] <- index.variable[1]
  names(dat)[match("Group.2",names(dat))] <- index.variable[2]
  names(dat)[match("Group.3",names(dat))] <- index.variable[3]
  names(dat)[match("Group.4",names(dat))] <- index.variable[4]
  return(dat)
}

index.variable<- "Date"

time.variable <- c("Date", 
                    "Heure")

numeric.variable<- c("Temp_amb",
                     "Hygro","Temp_sol","Ray_ext")
                     
dat.summary<-fc_summary.data(data = meteo,varname = numeric.variable,index.variable = index.variable)

fc_plot.summary.data <- function(data,Sd,idx.variable,modality,design,color,linetype){
  
  idx.variable <- idx.variable
  
  # Creation of empty list to stock variable corresponding to mean and standard variation
  Mean.variable<- grep(pattern = "mean$",colnames(data))
  Sd.variable<- grep(pattern = "sd$",colnames(data))
  
  # Creation of empty list for plot
  plotmeanlist<- vector(mode = "list",length = length(Mean.variable))
  
  # Incrementation of variable name in the differnet list
  names(plotmeanlist)<- names(data[,Mean.variable])
  
  if (Sd==TRUE){
    
    if (is.null(modality)){
      
      dat<-melt(data = data,
                id.vars = c(idx.variable),
                measure.vars = c(Mean.variable,Sd.variable))
      
      for (i in 1:length(Mean.variable))local({
        i <-i
        plot<-ggplot()+
          geom_line(mapping = aes(
            x = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,idx.variable],
            y = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,"value"],
            col= interaction(color[1],linetype[1]),
            linetype=interaction(color[1],linetype[1]))
            
          )+
          geom_point(mapping = aes(
            x = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,idx.variable],
            y = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,"value"],
            col= interaction(color[1],linetype[1]),
            linetype=interaction(color[1],linetype[1]))
          )+
          geom_line(mapping = aes(
            x = dat[dat[,"variable"]==colnames(data[,Sd.variable])[i],][,idx.variable],
            y = dat[dat[,"variable"]==colnames(data[,Sd.variable])[i],][,"value"]
            ,col= interaction(color[2],linetype[2]),
            linetype= interaction(color[2],linetype[2]))
          )+
          xlab(idx.variable)+
          ylab(colnames(data[,Mean.variable])[i])+
          design
        
        # Store all plots in a plotmeanlist
        plotmeanlist[[i]] <<- plot
      })
    }
    else if (!is.null(modality)){
      dat<-melt(data = data,
                id.vars = c(idx.variable,modality),
                measure.vars = c(Mean.variable,Sd.variable))
      
      # Plot mean and standard deviation for all variable and return plotmeanlist
      for (i in 1:length(Mean.variable))local({
        i <-i
        plot<-ggplot()+
          geom_line(mapping = aes(
            x = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,idx.variable],
            y = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,"value"],
            color= data[,modality],
            group=data[,modality]),
            linetype=linetype[1]
          )+
          geom_point(mapping = aes(
            x = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,idx.variable],
            y = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,"value"],
            color= data[,modality],group=data[,modality]),
            linetype=linetype[1]
          )+
          geom_line(mapping = aes(
            x = dat[dat[,"variable"]==colnames(data[,Sd.variable])[i],][,idx.variable],
            y = dat[dat[,"variable"]==colnames(data[,Sd.variable])[i],][,"value"],
            color= data[,modality],group=data[,modality]),
            linetype=linetype[2]
          )+
          xlab(idx.variable)+
          ylab(colnames(data[,Mean.variable])[i])+
          design+
          guides(color=guide_legend(title = modality))
        
        # Store all plots in a plotmeanlist
        
        plotmeanlist[[i]] <<- plot
      })
    }
  }
  else if (Sd==FALSE){
    if (is.null(modality)){
      
      dat<-melt(data = data,
                id.vars = c(idx.variable),
                measure.vars = c(Mean.variable))
      
      for (i in 1:length(Mean.variable))local({
        i <-i
        plot<-ggplot()+
          geom_line(mapping = aes(
            x = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,idx.variable],
            y = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,"value"],
            col=interaction(color[1],linetype[1]),
            linetype=interaction(color[1],linetype[1]))
          )+
          geom_point(mapping = aes(
            x = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,idx.variable],
            y = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,"value"],
            col=interaction(color[1],linetype[1]),
            linetype=interaction(color[1],linetype[1]))
          )+
          
          xlab(idx.variable)+
          ylab(colnames(data[,Mean.variable])[i])+
          design
        
        # Store all plots in a plotmeanlist
        
        plotmeanlist[[i]] <<- plot
      })
    }
    else if (!is.null(modality)){
      
      dat<-melt(data = data,
                id.vars = c(idx.variable,modality),
                measure.vars = c(Mean.variable))
      
      for (i in 1:length(Mean.variable))local({
        i <-i
        plot<-ggplot()+
          geom_line(mapping = aes(
            x = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,idx.variable],
            y = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,"value"],
            color= data[,modality],
            group=data[,modality]),
            linetype=linetype[1]
          )+
          geom_point(mapping = aes(
            x = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,idx.variable],
            y = dat[dat[,"variable"]==colnames(data[,Mean.variable])[i],][,"value"],
            color= data[,modality],
            group=data[,modality]),
            linetype=linetype[1]
          )+
          
          xlab(idx.variable)+
          ylab(colnames(data[,Mean.variable])[i])+
          design+
          guides(color=guide_legend(title = modality))
        
        # Store all plots in a plotmeanlist
        plotmeanlist[[i]] <<- plot
      })
    }
  }
  
  
  # Function return plotmean list
  return(plotmeanlist)
}

windowsFonts(Times= windowsFont("TT Times"))


# New Phytologist Journal -------------------------------------------------

Newphytol_theme<-theme_bw(base_size = 12,base_family = "Times")+
  theme(
    panel.border = element_rect(colour = "black",size = 0.5),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    axis.title.x = element_text(family = "Times",size = 12,colour = "black") ,
    axis.title.y = element_text(family = "Times",size = 12,colour = "black"),
    axis.text.x = element_text(family = "Times",size = 10,colour = "black"),
    axis.text.y = element_text(family = "Times",size = 10,colour = "black"), 
    axis.title = element_text(family = "Times",size = 12),
    legend.text = element_text(family = "Times",size = 12),
    line = element_line(size = 0.5))

str(dat.summary)
dat.summary$Date<-as.Date(dat.summary$Date,format="%d/%m/%Y")


ggplot(data=dat.summary,aes(x=Date,y=Temp_amb.mean))+geom_point()+geom_line()

summary.plot<-fc_plot.summary.data(data = dat.summary,Sd = T,idx.variable = "Date",modality =NULL,design = Newphytol_theme,color = c("#00000000","#000000"),linetype = c("solid","dashed"))
summary.plot$Temp_amb.mean
write.csv(x=dat.summary,file="C:\\Users\\mlabadie\\Documents\\GitHub\\strawberry\\share\\data\\meteo\\daily_weather.csv")

#  scale_color_manual(name="",values = c("black.solid"="black","black.dashed"="black"),labels=c("sd","mean"))+
#  scale_linetype_manual(name="",values = c("black.solid"="solid","black.dashed"="dashed"),labels=c("sd","mean"))

imp.nakalman.arima<-na_kalman(x = dat.summary,model = "auto.arima")
plot(imp.nakalman.arima)
# imp.seac<-na_seadec(x = meteo$Temp_amb,find_frequency=TRUE)
# plot(imp.seac)
# imp.nakalman.TS<-na_kalman(x = meteo$Temp_amb,model = "StructTS")
# plot(imp.nakalman.TS)
ggplot_na_imputations(dat.summary)
ggplot_na_distribution(imp.nakalman.arima$Temp_amb.mean)

imp.mice<- mice(data = dat.summary,m = 30,maxit = 30, method = "pmm")
summary(imp.mice)
stripplot(imp.mice, pch = 20, cex = 1.2)
xyplot(imp.mice, Temp_amb.mean~Date)
xyplot(imp.mice, Hygro~Date)
xyplot(imp.mice, Ray_ext~Date)
densityplot(imp.mice)
imp.mice.complete<-complete(imp.mice,1)

ggplot(data=imp.mice.complete,aes(x=Date,y=Temp_amb.mean))+geom_point()+geom_line()

write.csv(x=imp.mice.complete,file="C:\\Users\\mlabadie\\Documents\\GitHub\\strawberry\\share\\data\\meteo\\weather_completed.csv")


imp.mice_sum<- mice(data = dat.summary,m = 30,maxit = 1000, method = "pmm")
summary(imp.mice)

xyplot(imp.mice_sum, Temp_amb.mean~Date)
densityplot(imp.mice_sum$)
imp.mice_sum.complete<-complete(imp.mice_sum,1)

meteo['Temp_amb_imp']<-imp.mice_sum.complete$imp$Temp_amb.mean
write.csv(x=imp.mice_sum.complete,file="C:\\Users\\mlabadie\\Documents\\GitHub\\strawberry\\share\\data\\meteo\\meteo_completed.csv")

library(VIM)
aggr_plot <- aggr(meteo, col=c('navyblue','red'), numbers=TRUE, sortVars=TRUE, labels=names(meteo), cex.axis=.7, gap=3, ylab=c("Histogram of missing data","Pattern"))

weather<-dat.summary[c(1,2,4,6,8)]
names(weather)
colnames(weather)<-c(['date',"Temperature","Hygrometrie","Temperature_sol","rayonnement"])
write.csv(x=dat.summary[c(1,2,4,6,8)],file="C:\\Users\\mlabadie\\Documents\\GitHub\\strawberry\\share\\data\\meteo\\meteo_completed.csv")

