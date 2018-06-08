

####################### Calcul function ####################################### 

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




# Distribution of one varible for each module order ------------
fc_dist_variable_by_order<-function(data,genotype,varname,prob){

  if (prob==F){
    t1<-table(data[data[,"genotype"]==genotype,][,varname],
             data[data[,"genotype"]==genotype,]$Index)
    
    t<-data.frame(matrix(data = t1,nrow = nrow(t1),ncol = ncol(t1)))
    colnames(t)<- levels(x = data$Index)
    row.names(t)<- row.names(t1)
    
    t[,"Frequency"]<-rowSums(t)
    t["Frequency",]<-colSums(t) 
    
    return(t)
  }else if (prob==T){
    
    t1<-table(data[data[,"genotype"]==genotype,][,varname],
             data[data[,"genotype"]==genotype,]$Index)
    
    t1<-prop.table(x = t1, 2)
    
    t<-data.frame(matrix(data = t1,nrow = nrow(t1),ncol = ncol(t1)))
    colnames(t)<- levels(x = data$Index)
    row.names(t)<- row.names(t1)
    
    t["Frequency",]<-colSums(t)
    
    return(t)
  }else if (prob=="cumulative"){
    
    t1<-table(data[data[,"genotype"]==genotype,][,varname],
             data[data[,"genotype"]==genotype,]$Index)
    
    t1<-prop.table(x = t1, 2)
    
    test<-data.frame(matrix(data = t1,nrow = nrow(t1),ncol = ncol(t1)))
    colnames(test)<- levels(x = data$Index)
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
        d[i,j]<-d[i-1,j]+test[i,j]
      }
    }
    return(d)
  }
}


# Distribution of categorical variable for each module order --------------

fc_dist_cat_variable_by_order<-function(data,genotype,varname,prob){
  
  if (prob==F){
    t1<-table(data[data[,"genotype"]==genotype,][,varname],
              data[data[,"genotype"]==genotype,]$Index)
    
    t<-data.frame(matrix(data = t1,nrow = nrow(t1),ncol = ncol(t1)))
    colnames(t)<- levels(x = data$Index)
    row.names(t)<- row.names(t1)
    
    t[,"Frequency"]<-rowSums(t)
    t["Frequency",]<-colSums(t)
    
    
    t<-t(t)
    t<-data.frame(t)
    t[,"genotype"]<-genotype
    t[,"Index"]<-row.names(t)
    t<-t[!is.na(t["Branch_Crown"]),]
    
    
    return(t)
    
  }else if (prob==T){
    
    t1<-table(data[data[,"genotype"]==genotype,][,varname],
              data[data[,"genotype"]==genotype,]$Index)
    
    t1<-prop.table(x = t1, 2)
    
    t<-data.frame(matrix(data = t1,nrow = nrow(t1),ncol = ncol(t1)))
    colnames(t)<- levels(x = data$Index)
    row.names(t)<- row.names(t1)
    
    t["Frequency",]<-colSums(t)
    
    t<-t(t)
    t<-data.frame(t)
    t[,"genotype"]<-genotype
    t[,"Index"]<-row.names(t)
    t<-t[!is.na(t["Branch_Crown"]),]
    
    
    return(t)
    
  }else if (prob=="cumulative"){
    
    t1<-table(data[data[,"genotype"]==genotype,][,varname],
              data[data[,"genotype"]==genotype,]$Index)
    
    t1<-prop.table(x = t1, 2)
    
    test<-data.frame(matrix(data = t1,nrow = nrow(t1),ncol = ncol(t1)))
    colnames(test)<- levels(x = data$Index)
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
        d[i,j]<-d[i-1,j]+test[i,j]
      }
    }
    
    d<-t(d)
    d<-data.frame(d)
    d[,"genotype"]<-genotype
    d[,"Index"]<-row.names(d)
    d<-d[!is.na(d["Branch_Crown"]),]
    
    
    return(d)
  }
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

fc_comp_varieties_kruskal_posthoc<-function(data,varname,groupe){

  k<-kruskal(y = data[,varname],
             trt = data[,"genotype"],
             alpha = 0.05,
             group = groupe,
             console = F)
  
  posthoc<- posthoc.kruskal.nemenyi.test(x = data[,varname],
                                         g = data[,"genotype"],
                                         dist = "Tukey")
  
  print(posthoc)
  
  if (groupe==T){
    res<-k$means[1:3]
    colnames(res)<- c("mean","rank","std")
    res[,"genotype"]<-row.names(k$mean)
    colnames(k$groups)<-c("rank","groups")
    res<-merge(x = res,k$groups,by.y = "rank")
    res<-res[,c(4,2,3,5,1)]
    res<-res[,-5]
    res<-res[order(res[,"mean"],decreasing = T),]
    return(res)
  }else
    
    print(k)
}





# Chi test comparison to identify specificty of module order --------------

fc_chi_by_order<-function(data,genotype,varname,parameter,var.comp,idx.comp,table){
  t<- table(data[data[,"genotype"]==genotype,][,varname],
            data[data[,"genotype"]==genotype,][,"Index"])
  
  t1<- data.frame(
    matrix(
      data = t,
      nrow = nrow(t),
      ncol = ncol(t)
    ),
    row.names = row.names(t)
  )
  
  
  colnames(t1)<-colnames(t)
  
  res<-chisq.test(t1[var.comp,idx.comp])
  
  dat.res<- data.frame(as.numeric(res$p.value))
  colnames(dat.res)<-"p.value"
  dat.res[,"genotype"]=genotype
  dat.res[,"parameter"]=parameter
  dat.res<-dat.res[,c(2,3,1)]
  
  if(table==T){
    return(t)
  }
  return(dat.res)
}






###################### Plot function ##########################################

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
    theme_cowplot(font_size = 12,font_family = "Times",line_size = 0.8)
}





# Plot distribution of one variable according to module orders -------------

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
    theme_cowplot(font_size = 12,font_family = "Times",line_size = 0.8)
}





# Plot distribution of one categorical variable accoding to module --------

fc_dist_cat_variable_by_order.plot<-function(data,varname){
  #Creation of new dataframe name d
  data=tab12
  varname="Branch_Crown"
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
  
  # delete indesirable column 
  d<-d[,-c(1,4)]
  d<-d[!is.na(d[,"Branch_Crown"]==T),]
  
  
  
  #Data melt for plot with legend
  
  d<- melt(data = d,id.vars = c("Index","genotype"),na.rm = T)
  d<-d[d[,'variable']==varname,]
  
  #Plot data
  ggplot(data = d,
         mapping = aes(x = Index,
                       y = value,
                       group=genotype)
  )+
    geom_line(aes(color=genotype))+
    geom_point(aes(color=genotype))+
    ylab("Probability")+
    guides(color= guide_legend(title = "Orders"))+
    scale_y_continuous(expand = c(0,0),limits = c(0,1))+
    scale_x_discrete(name= "Order",expand = c(0,0))+
    theme_cowplot(font_size = 12,font_family = "Times",line_size = 0.8)
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
    theme_cowplot(font_size = 12,font_family = "Times",line_size = 0.8)+
    xlab("Orders")+
    ylab(varname)
}



