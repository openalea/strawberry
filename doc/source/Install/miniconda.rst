Install Miniconda
--------------------

Follow official website instruction to install miniconda :

http://conda.pydata.org/miniconda.html

Create virtual environment and activate it
---------------------------------------------

In Anaconda Prompt:

.. code:: shell

  conda create -n strawberry -c openalea -c openalea/label/unstable openalea.plantgl openalea.lpy boost=1.66 openalea.mtg
          conda activate strawberry

Install strawberry package
------------------------------

.. code:: shell

  conda install -c openalea openalea.strawberry

Install several packages managing tools:
-------------------------------------------

.. code:: shell

	conda install -c conda-forge jupyter k3d oawidgets matplotlib pandas