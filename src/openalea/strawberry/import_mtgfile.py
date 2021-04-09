from __future__ import absolute_import
from __future__ import print_function

import openalea.strawberry
from openalea.mtg import MTG, algo
from openalea.deploy.shared_data import shared_data


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
