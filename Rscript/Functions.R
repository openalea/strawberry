
# Distribution function of number of module for successive orders ---------
fc_dist_module_by_order<-function(data, index){
  t<- table(data[,"genotype"],
        data[,"Index"])
  
  t<-data.frame(matrix(data = t,nrow = nrow(t),ncol = ncol(t)))
  colnames(t)<- levels(x = data[,index])
  row.names(t)<- c(levels(x = data$genotype))
  t[,"Frequency"]<-rowSums(t)
  t["Frequency",]<-colSums(t)
  
  return(t)
}


# Module order distribution for successive date of observation ------------

fc_dist_order_by_date<-function(data, genotype,prob){
  
  if (prob==F){
    t<-table(data[data[,"genotype"]==genotype,][,"Index"],
             data[data[,"genotype"]==genotype,][,"date"])
    
    t<-data.frame(matrix(data = t,nrow = nrow(t),ncol = ncol(t)))
    colnames(t)<- levels(x = dat$date)
    row.names(t)<- c(levels(x = dat$Index))
    t[,"Frequency"]<-rowSums(t)
    t["Frequency",]<-colSums(t)
    
    return(t)
    
  } else if (prob==T){
    t<-table(data[data[,"genotype"]==genotype,][,"Index"],
             data[data[,"genotype"]==genotype,][,"date"])
    
    t<-prop.table(x = t, 2)
    
    t<-data.frame(matrix(data = t,nrow = nrow(t),ncol = ncol(t)))
    colnames(t)<- levels(x = dat$date)
    row.names(t)<- c(levels(x = dat$Index))
    t["Frequency",]<-colSums(t)
    
    return(t)
    
  } else if (prob=="cumulative"){
    t<-table(data[data[,"genotype"]==genotype,][,"Index"],
             data[data[,"genotype"]==genotype,][,"date"])
    
    t<-prop.table(x = t, 2)
    
    test<-data.frame(matrix(data = t,nrow = nrow(t),ncol = ncol(t)))
    colnames(test)<- levels(x = dat$date)
    row.names(test)<- c(levels(x = dat$Index))
    
    d<-data.frame(matrix(nrow=nrow(test),ncol = ncol(test)))
    colnames(d)<-colnames(test)
    row.names(d)<-row.names(test)
    d[1,]<-test[1,]
    
    for (j in 1:ncol(d)){
      for (i in 2:nrow(d)){
        if(d[i-1,j]==1){
          break
        }
        res<-d[i,j]<-d[i-1,j]+test[i,j]
      }
    }
    
    return(d)
    
  }
}

# Plot Module order distribution for successive date of observation -------

fc_dist_order_by_date.plot<-function(data){

  #Creation of new dataframe name d
  d<- data.frame(matrix(nrow = nrow(data),ncol = ncol(data)))
  
  # Filter to remove Frequency column or row
  if (colnames(data)[ncol(data)]=="Frequency" & rownames(data)[nrow(data)]=="Frequency"){
    d[1:(nrow(d)-1),1:(ncol(d)-1)]<- data[1:(nrow(d)-1),1:(ncol(data)-1)]
    colnames(d)<-colnames(data[,1:(ncol(data)-1)])
    row.names(d)<- row.names(data[1:(nrow(data)-1)])
  }else if (colnames(tab2)[ncol(tab2)]=="Frequency"){
    d[,1:(ncol(d)-1)]<- data[,1:(ncol(data)-1)]
    colnames(d)<-colnames(data[,1:(ncol(data)-1)])
  }else if (rownames(data)[nrow(data)]=="Frequency"){
    d[1:(nrow(d)-1),]<- data[1:(nrow(d)-1),]
    row.names(d)<- row.names(data[1:(nrow(data)-1)])
  }else
    d[,1:ncol(d)]<-data[,1:ncol(data)]
  colnames(d)<-colnames(data)
  row.names(d)<- row.names(data)
  
  #Add new column order
  d$order<-rownames(d)
  
  #Data melt for plot with legend
  d<- melt(data = d,na.rm = T)
  
  #Plot data
  ggplot(data = d,
         mapping = aes(x = order,
                       y = value,
                       group=variable)
  )+
    geom_line(aes(color=variable))+
    geom_point(aes(color=variable))+
    xlab("Orders")+
    ylab("Probability")+
    guides(color= guide_legend(title = "Date"))+
    scale_y_continuous(expand = c(0,0))+
    scale_x_discrete(expand = c(0,0))+
    theme_cowplot(font_size = 12,font_family = "Times",line_size = 0.5)
  }


# Distribution of one varname for each module order ------------
fc_dist_variable_by_order<-function(data,genotype,varname,prob){
  
  if (prob==F){
    t1<-table(data[data[,"genotype"]==genotype,][,varname],
             dat[data[,"genotype"]==genotype,]$Index)
    
    t<-data.frame(matrix(data = t1,nrow = nrow(t1),ncol = ncol(t1)))
    colnames(t)<- levels(x = dat$Index)
    row.names(t)<- row.names(t1)
    
    t[,"Frequency"]<-rowSums(t)
    t["Frequency",]<-colSums(t)
    
    return(t)
  }else if (prob==T){
    
    t1<-table(data[data[,"genotype"]==genotype,][,varname],
             dat[data[,"genotype"]==genotype,]$Index)
    
    t1<-prop.table(x = t1, 2)
    
    t<-data.frame(matrix(data = t1,nrow = nrow(t1),ncol = ncol(t1)))
    colnames(t)<- levels(x = dat$Index)
    row.names(t)<- row.names(t1)
    
    t["Frequency",]<-colSums(t)
    
    return(t)
  }else if (prob=="cumulative"){
    
    t1<-table(data[data[,"genotype"]==genotype,][,varname],
             dat[data[,"genotype"]==genotype,]$Index)
    
    t1<-prop.table(x = t1, 2)
    
    test<-data.frame(matrix(data = t1,nrow = nrow(t1),ncol = ncol(t1)))
    colnames(test)<- levels(x = dat$Index)
    row.names(test)<- row.names(t1)
    
    d<-data.frame(matrix(nrow=nrow(test),ncol = ncol(test)))
    colnames(d)<-colnames(test)
    row.names(d)<-row.names(test)
    d[1,]<-test[1,]
    
    for (j in 1:ncol(d)){
      for (i in 2:nrow(d)){
        if(d[i-1,j]==1){
          break
        }
        res<-d[i,j]<-d[i-1,j]+test[i,j]
      }
    }
    return(d)
  }
}




# Plot distribution of one varname according to module orders -------------

fc_dist_variable_by_order.plot<-function(data){
  
  #Creation of new dataframe name d
  d<- data.frame(matrix(nrow = nrow(data),ncol = ncol(data)))
  
  # Filter to remove Frequency column or row
  if (colnames(data)[ncol(data)]=="Frequency" & rownames(data)[nrow(data)]=="Frequency"){
    d[1:(nrow(d)-1),1:(ncol(d)-1)]<- data[1:(nrow(d)-1),1:(ncol(data)-1)]
    colnames(d)<-colnames(data[,1:(ncol(data)-1)])
    row.names(d[1:(nrow(d)-1),])<- row.names(data[1:(nrow(data)-1),])
  }else if (colnames(tab2)[ncol(tab2)]=="Frequency"){
    d[,1:(ncol(d)-1)]<- data[,1:(ncol(data)-1)]
    colnames(d)<-colnames(data[,1:(ncol(data)-1)])
  }else if (rownames(data)[nrow(data)]=="Frequency"){
    d[1:(nrow(d)-1),]<- data[1:(nrow(d)-1),]
    row.names(d[1:(nrow(d)-1),])<- row.names(data[1:(nrow(data)-1),])
  }else
    d[,1:ncol(d)]<-data[,1:ncol(data)]
    colnames(d)<-colnames(data)
    row.names(d)<- row.names(data)
  
  #Add new column order
    d[,"idx"]<-rownames(d)
    d[,"idx"]<-as.numeric(d[,"idx"])

  
  #Data melt for plot with legend
  d<- melt(data = d,id.vars = "idx",na.rm = T)
  
  #Plot data
  ggplot(data = d,
         mapping = aes(x = idx,
                       y = value,
                       group=variable)
  )+
    geom_line(aes(color=variable))+
    geom_point(aes(color=variable))+
    xlab("index")+
    ylab("Probability")+
    guides(color= guide_legend(title = "Orders"))+
    scale_y_continuous(expand = c(0,0))+
    scale_x_continuous(expand = c(0,0))+
    theme_cowplot(font_size = 12,font_family = "Times",line_size = 0.5)
}

# Pointwise Mean of variable of modules for successive orders -------------
fc_pointwise_mean_variable_by_order<- function(data,varname){
  ggplot(data = data,
         mapping = aes(
           x = data[,"Index"],
           y = data[,varname],
           group=genotype)
  )+
    geom_line(mapping = aes(color=genotype))+
    geom_point(mapping = aes(color=genotype))+
    scale_y_continuous(expand = c(0,0))+
    scale_x_discrete(expand = c(0,0))+
    xlab("Orders")+
    ylab(varname)
}


# Linear trend regression (estimate slope and IC95% --------

fc_linear_trend_reg<-function(data,genotype,variable,Index){
  
  
  data$Index<-as.numeric(data$Index)
  
  model<-lm(formula = data[data[,"genotype"]==genotype,][,variable]~data[data[,"genotype"]==genotype,][,Index])
  
  d<-data.frame(matrix(ncol = 4, nrow=1))
  colnames(d)<-c("Genotype","Slope","IC_lower","IC_upper")
  d[,"Genotype"]<-genotype
  d[,"Slope"]<-coef(object = model)[2]
  d[,"IC_lower"]<-confint(object = model)[2]
  d[,"IC_upper"]<-confint(object = model)[4]
  
  return(d)
}


# Comparison krukal wallis and posthoc nemenei by order -------------------

fc_comp_varieties_kruskal_posthoc<-function(data,varname,group){
  
  k<-kruskal(y = data[,varname],
             trt = data[,"genotype"],
             alpha = 0.05,
             group = group,
             console = F)
  
  posthoc<- posthoc.kruskal.nemenyi.test(x = data[,varname],
                                         g = data[,"genotype"],
                                         dist = "Tukey")
  
  print(posthoc)
  
  res<-data.frame(matrix(nrow=6,ncol = 1))
  res[,"genotype"]<-row.names(k$mean)
  res[,"Mean"]<-k$means[1]
  res[,"Sd"]<-k$means[3]
  res[,"Group"]<-k$groups[2]
  res<-res[,-1]
  
  
  if (group==T){
    return(res)
  }else
    print(k)
}
