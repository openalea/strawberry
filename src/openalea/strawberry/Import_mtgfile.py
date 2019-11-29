


def import_mtgfile(filename):
    """
    parameters:
    -----------
    filename = names of mtg
    
    return:
    -------
    a function which import mtg corresponding to the mtg names
    """
    filenames = filename
    files = shared_data(openalea.strawberry).glob('*.mtg')
    mtg_path = dict((f.namebase, f) for f in files)
    mtgfile = dict((k,f) for k,f in mtg_path.items() if k in filenames)
    if len(filenames) == 1:
        g = MTG(mtgfile[filenames[0]])
        return g
    else:
        metaMTG= MTG()
        for i in mtgfile:
            metaMTG = algo.union(metaMTG, MTG(mtgfile[i]))
        return metaMTG   