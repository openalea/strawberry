==================================
Install with docker
==================================


1. Docker installation
-------------------------

Follow official website instruction to install docker :

https://docs.docker.com/get-docker/

2. Download and run the strawberry docker image
----------------------------------------------------------------------------------

.. code-block:: shell

    docker run -itp 8888:8888 gheidsieck/strawberry

then, start the notebook in the docker terminal with:
.. code-block:: shell

    conda activate strawberry
    jupyter-notebook

finally, copy the link (e.g. http://127.0.0.1:8888/?token=xxx) into your browser.