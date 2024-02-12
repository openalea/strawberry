import openalea
from openalea.mtg.io import read_mtg_file
from openalea.mtg.algo import orders, split

from oawidgets.plantgl import PlantGL
import openalea.strawberry
from openalea.strawberry import visu2d, visu3d
from openalea.strawberry.data import data_directory


def name(f):
    return f.basename().splitext()[0]

def test_import_mtg():
    files = data_directory.glob('*.mtg')
    mtg_path = dict((name(f), f) for f in files)
    gariguette = read_mtg_file(mtg_path['Gariguette'])
    straws = split(gariguette)
    assert isinstance(straws[0], openalea.mtg.mtg.MTG)


def test_3D():
    files = data_directory.glob('*.mtg')
    mtg_path = dict((name(f), f) for f in files)
    gariguette = read_mtg_file(mtg_path['Gariguette'])
    gariguette.properties()['order'] = orders(gariguette)
    scene=visu3d.plot3d(gariguette,by=["Sample_date"],hide_leaves=False,display=False)
    assert scene.isValid() == True

    p = PlantGL(scene, group_by_color=True)
    assert len(p.object_ids) == 103

    #p = PlantGL(scene, group_by_color=False)
    #assert len(p.object_ids) == 103


def __test_2D():
    files = data_directory.glob('*.mtg')
    mtg_path = dict((name(f), f) for f in files)
    gariguette = read_mtg_file(mtg_path['Gariguette'])
    gariguette.properties()['order'] = orders(gariguette)
    scene=visu2d.plot2d(gariguette,gariguette.vertices(scale=1)[53:54],dist=[3]*3,display=False)
    PlantGL(scene)
    