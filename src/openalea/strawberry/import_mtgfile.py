from __future__ import absolute_import
from __future__ import print_function

import glob
from openalea.mtg import *
from openalea.core import path
from openalea.deploy.shared_data import shared_data
import openalea.strawberry

def name(f):
    return f.basename().splitext()[0]

def import_mtgfile(filename):
    """
    parameters:
    -----------
    filename : names of mtg
    
    return:
    -------
    a function which import mtg corresponding to the mtg names
    """
    def name(f):
        "return base name without extension"
        return f.basename().splitext()[0]
    
    filenames = filename
    files = shared_data(openalea.strawberry).glob('*.mtg')
    mtg_path = dict((name(f), f) for f in files)
    mtgfile = dict((k,f) for k,f in mtg_path.items() if k in filenames)
    if len(filenames) == 1:
        g = MTG(mtgfile[filenames[0]])
        return g
    else:
        metaMTG= MTG()
        for i in mtgfile:
            metaMTG = algo.union(metaMTG, MTG(mtgfile[i]))
        return metaMTG   


def plant_number_by_varieties(g):
    """
    parameter:
    g : a current mtg

    Note: Genotype variable can be explicitely defined

    """
    genotype = set(g.property("Genotype").values())

    for geno in genotype:
        no_plants= list(g.property("Genotype").values()).count(geno)
        # print(geno, ":", no_plants, "plants")
