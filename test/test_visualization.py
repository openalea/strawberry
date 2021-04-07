from openalea.deploy.shared_data import shared_data
import openalea.strawberry
from openalea.mtg.io import read_mtg_file
from openalea.mtg.algo import orders, split
import openalea
from oawidgets.plantgl import PlantGL
from openalea.strawberry import visualization, visualization2d


def name(f):
    return f.basename().splitext()[0]

def test_import_mtg():
    files = shared_data(openalea.strawberry).glob('*.mtg')
    mtg_path = dict((name(f), f) for f in files)
    gariguette = read_mtg_file(mtg_path['Gariguette'])
    straws = split(gariguette)
    assert isinstance(straws[0], openalea.mtg.mtg.MTG)


def test_3D():
    files = shared_data(openalea.strawberry).glob('*.mtg')
    mtg_path = dict((name(f), f) for f in files)
    gariguette = read_mtg_file(mtg_path['Gariguette'])
    gariguette.properties()['order'] = orders(gariguette)
    scene=visualization.plot3d(gariguette,by=["Sample_date"],hide_leaves=False,display=False)
    assert scene.isValid() == True

    p = PlantGL(scene, group_by_color=True)
    assert len(p.object_ids) == 103

    #p = PlantGL(scene, group_by_color=False)
    #assert len(p.object_ids) == 103


def __test_2D():
    files = shared_data(openalea.strawberry).glob('*.mtg')
    mtg_path = dict((name(f), f) for f in files)
    gariguette = read_mtg_file(mtg_path['Gariguette'])
    gariguette.properties()['order'] = orders(gariguette)
    scene=visualization2d.plot2d(gariguette,gariguette.vertices(scale=1)[53:54],dist=[3]*3,display=False)
    PlantGL(scene)
    