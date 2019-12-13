.. strawberry documentation master file, created by
   sphinx-quickstart on Fri Dec 13 15:49:30 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Strawberry documentation
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Description:
===========

Strawberry is a package for architecture analysis and 2D/3D reconstruction. 
it is encoded in python 2.7


Authors:
=========
* Marc Labadie
* Christophe Pradal




Installation:
=============

Requierements:
------------

* OpenAlea.Deploy
* OpneAlea.MTG
* Jupyter Notebook
* OpenAlea.PlantGL
* Matplotlib
* Pandas
* oawidgets

installation:
-------------

1. Install Miniconda
+++++++++++++++++++++
Follow official website instruction to install miniconda :

http://conda.pydata.org/miniconda.html

2. Install strawberry module
++++++++++++++++++++++++++++

.. code:: shell
      
      conda create -n openalea -c openalea -c openalea/label/unstable openalea.plantgl openalea.lpy boost=1.66 openalea.mtg



.. code:: shell

      conda install -c openalea openalea.strawberry
      conda activate openalea

Documentation:
==============

Tutorial Jupyter Notebooks
--------------------------
Tutorial Jupyter Notebooks are available on the git repository in the folder examples/tutorials.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`