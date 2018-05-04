from path import Path
from openalea.mtg import *
import glob

from openalea.deploy.shared_data import shared_data
import openalea.strawberry

mydir = Path().getcwd()/'..'/'..'/'share'/'data'
diploids = shared_data(openalea.strawberry).glob('Nils*.mtg')
#diploids = mydir.glob('Nils*.mtg')

def test_read_mtg():
    nils2 = diploids[1]

    g=MTG(nils2)

    n = g.nb_vertices(scale=1)
    assert(n == 112)

    return g
