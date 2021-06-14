[![Documentation Status](https://readthedocs.org/projects/strawberry/badge/?version=latest)](https://strawberry.readthedocs.io/en/latest/?badge=latest)

# OpenAlea.Strawberry


**Authors** : Marc Labadie, Christophe Pradal, Geatan Heidsieck

**Institutes** : INRA / CIRAD / Inria 

**Status** : Python package 

**License** : [Cecill-C](https://cecill.info/licences/Licence_CeCILL-C_V1-en.html)

**URL** : https://github.com/openalea-incubator/strawberry

## About 


### Description 


Strawberry is a package for architecture analysis and 2D/3D reconstruction.
It contains Python code



### Content 

The Strawberry package contains :
* geometry : Definition  of geometric shapes for mtg visualisation
* visualisation : 2D and 3D representation of mtg. Plot analysis results.
* analysis : extraction of data from mtg


## Installation

### Requirements

* Python > 3.0
* OpenAlea.Deploy
* OpenAlea.MTG
* Jupyter Notebook
* OpenAlea.PlantGL
* Matplotlib
* Pandas
* oawidgets
* pvis
* k3d


### Installation 

```
conda create -n strawberry -c conda-forge python=3.8 pandas pvis k3d openalea.deploy jupyter
```
```
conda activate strawberry
```
```
conda install -c fredboudon -c conda-forge openalea.mtg openalea.plantgl 
```
```
conda install -c openalea openalea.strawberry
```



Documentation
-------------
    
    https://strawberry.readthedocs.io

