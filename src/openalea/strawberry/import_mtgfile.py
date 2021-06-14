from __future__ import absolute_import
from __future__ import print_function

import openalea.strawberry
from openalea.mtg import MTG, algo
from openalea.deploy.shared_data import shared_data


def name(f):
    """return base name without extension

    :param f: the file path
    :type f: string
    :return: basename
    :rtype: string
    """    
    return f.basename().splitext()[0]


def import_mtgfile(filename):
    """Import a MTG file from genotype name, in sharedata repo

    :param filename: genotype = name of the file
    :type filename: string
    :return: a MTG loaded from the file
    :rtype: MTG
    """    
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
    """Print plant number by varieties in a mtg

    :param g: MTG
    :type g: MTG
    """    
    genotype = set(g.property("Genotype").values())

    for geno in genotype:
        no_plants= list(g.property("Genotype").values()).count(geno)
        print(geno, ":", no_plants, "plants")