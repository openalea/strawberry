.. _strawberry_quick_start:

Quick start to use Strawberry
##############################

You can construct a 3d architecture and some analyses by doing:

.. code-block:: python

  import openalea.mtg as mtg
  from oawidgets.plantgl import PlantGL
  import openalea.strawberry as strawberry
  
  g = strawberry.import_mtgfile.import_mtgfile(filename= ["Capriss"])
  g.properties()['order'] = mtg.algo.orders(g)
  scene=straberry.visu3d.plot3d(g,by=["Sample_date"],hide_leaves=False,display=False)
  PlantGL(scene, group_by_color=True)

.. image:: ./images/capriss_3d.png

.. code-block:: python

  meta_g = strawberry.import_mtgfile.import_mtgfile(filename=["Gariguette","Capriss","Darselect","Cir107","Ciflorette", "Clery"])
  extracted_data = analysis.extract_at_module_scale(meta_g)
  fig = strawberry.application.app_module_scale.plot_module_pointwisemean(meta_g, "nb_total_leaves")
  display(fig)


.. image:: ./images/multi_modulescale.png
