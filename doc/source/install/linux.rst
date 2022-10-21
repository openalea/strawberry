==================================
Developer Install - Ubuntu (linux)
==================================

.. contents::


1. Miniconda installation
-------------------------

Follow official website instruction to install miniconda :

https://docs.conda.io/en/latest/miniconda.html

2. Create virtual environment and activate it
---------------------------------------------

In Anaconda Prompt:

.. code:: shell

    conda create --name strawberry -c conda-forge -c openalea3 openalea.strawberry -y
    conda activate strawberry


3. Install the strawberry package
---------------------------------

.. code:: shell

    git clone https://github.com/openalea/strawberry.git
    cd strawberry
    python setup.py develop

5. Optional packages
---------------------

.. code:: shell

    conda install -c conda-forge pytest
