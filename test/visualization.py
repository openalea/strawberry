from openalea.strawberry.import_mtgfile import import_mtgfile
from openalea.mtg.algo import orders, split
import openalea
from oawidgets.plantgl import PlantGL
from openalea.strawberry import visualization, visualisation2d


def test_import_mtg():
    gariguette = import_mtgfile(filename= ["Gariguette"])
    straws = split(Gariguette)
    assert isinstance(straws[0], openalea.mtg.mtg.MTG)


def test_3D():
    gariguette = import_mtgfile(filename= ["Gariguette"])
    gariguette.properties()['order'] = orders(gariguette)
    scene=visualization.plot3d(gariguette,by=["Sample_date"],hide_leaves=False,display=False)
    assert scene.isValid() == True

    p = PlantGL(scene, group_by_color=True)
    assert len(p.object_ids) == 103

    p = PlantGL(scene, group_by_color=False)
    assert len(p.object_ids) == 103


def test_2D():
    gariguette = import_mtgfile(filename= ["Gariguette"])
    gariguette.properties()['order'] = orders(gariguette)
    scene=visualisation2d.plot2d(gariguette,gariguette.vertices(scale=1)[53:54],dist=[3]*3,display=False)
    PlantGL(scene)
    