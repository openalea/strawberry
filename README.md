[![Documentation Status](https://readthedocs.org/projects/strawberry/badge/?version=latest)](https://strawberry.readthedocs.io/en/latest/?badge=latest)
[![Update](https://anaconda.org/openalea3/openalea.strawberry/badges/latest_release_date.svg)](https://anaconda.org/openalea3/openalea.strawberry/badges/latest_release_date.svg)
[![download](https://anaconda.org/openalea3/openalea.strawberry/badges/downloads.svg)](https://anaconda.org/openalea3/openalea.strawberry/badges/downloads.svg)
[![Plateform](https://anaconda.org/openalea3/openalea.strawberry/badges/platforms.svg)](https://anaconda.org/openalea3/openalea.strawberry/badges/platforms.svg)
[![licence](https://anaconda.org/openalea3/openalea.strawberry/badges/license.svg)](https://anaconda.org/openalea3/openalea.strawberry/badges/license.svg)


![openalea](https://raw.githubusercontent.com/openalea/openalea.rtfd.io/master/doc/_static/openalea_web.svg) <img src="/doc/source/_static/logo_strawberry.png" width="120"/>

# OpenAlea.Strawberry



**Authors** : Marc Labadie, Christophe Pradal, Gaëtan Heidsieck

**Institutes** : INRA / CIRAD / Inria 

**Status** : Python package 

**License** : [Cecill-C](https://cecill.info/licences/Licence_CeCILL-C_V1-en.html)

**URL** : https://github.com/openalea/strawberry


## Description 


Strawberry is a package for architecture analysis and 2D/3D reconstruction of strawberry plants.

 <img src="/doc/source/user/images/gariguette_3d_solo.png" width="300"> 

## Content 

The Strawberry package contains :
* import_mtgfile : Load mtg file
* geometry : Definition  of geometric shapes for mtg visualisation
* visualisation : 2D and 3D representation of mtg. Plot analysis results
* analysis : extraction of data from mtg

> **_NOTE:_** An user friendly way to access the package content through an application based on Voila & jupyter Notebook. 

## Installation

### Requirements
---
* Python > 3.0
* Jupyter Notebook
* Matplotlib
* Pandas
* oawidgets
* pvis
* k3d
* voila
* voila-vuetify
* nodejs
* cufflinks
* ipyvuetify
* plotly
* openpyxl
* openalea.deploy
* openalea.mtg
* openalea.plantgl
---


### User installation 

```
conda create --name strawberry -c openalea3 -c conda-forge openalea.strawberry
```

### Docker install

It is possible to use the package through a docker image.
You can access a functioning environment with:
```
docker run -it openalea/strawberry 
```
To start the notebook, you need to open the ports when starting the docker:
```
docker run -it -p 8888:8888 openalea/strawberry 
```
and start the notebook in the docker terminal with:
```
jupyter notebook --ip='*' --port=8888 --no-browser
```
then copy the link (e.g. http://127.0.0.1:8888/?token=xxx) into your browser.

### Developpers installation
```
conda create --name strawberry -c openalea3 -c conda-forge openalea.strawberry
```
```
git clone https://github.com/openalea/strawberry.git
cd strawberry
python setup.py develop
```

### Quick start

You can construct a 3d architecture and some analyses by doing:

```
import openalea.mtg as mtg
from oawidgets.plantgl import PlantGL
import openalea.strawberry as strawberry
g = strawberry.import_mtgfile.import_mtgfile(filename= ["Gariguette"])
g.properties()['order'] = mtg.algo.orders(g)
scene=straberry.visu3d.plot3d(g,by=["Sample_date"],hide_leaves=False,display=False)
PlantGL(scene, group_by_color=True)
```
```
meta_g = strawberry.import_mtgfile.import_mtgfile(filename=["Gariguette","Capriss","Darselect","Cir107","Ciflorette", "Clery"])
extracted_data = analysis.extract_at_module_scale(meta_g)
fig = strawberry.application.app_module_scale.plot_module_pointwisemean(meta_g, "nb_total_leaves")
display(fig)
```

You have more examples at: https://strawberry.readthedocs.io/en/latest/user/gallery.html.

### Application usage

Once you installed the package, you can start the interactive application using:
```
cd strawberry/src/openalea/strawberry/application
voila "Strawberry Application.ipynb" --template vuetify-default --VoilaConfiguration.enable_nbextensions=True --VoilaConfiguration.file_whitelist="['.*\.(png|jpg|gif|svg|mp4|avi|ogg|html|py|js)']" 
```


## Documentation

You can see the complete documentation with tutorials at: https://strawberry.readthedocs.io.


## Contributing

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

A detailed overview on how to contribute can be found in the ![contributing guide](http://virtualplants.github.io/contribute/devel/workflow-github.html#workflow-github).

### contributors
<a href="https://github.com/openalea/strawberry/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=openalea/strawberry" />
</a>
