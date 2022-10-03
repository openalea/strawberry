from openalea.deploy.shared_data import shared_data

import openalea.strawberry
from openalea.strawberry.import_mtgfile import import_mtgfile, import_mtg_from_csv, strawberry_reader_csv




def name(f):
    return f.basename().splitext()[0]

mtg_files = shared_data(openalea.strawberry).glob('*.mtg')

excel_files = shared_data(openalea.strawberry).glob('*.xlsx')
import os

def test_import_mtgfile():
    """test import_mtgfile function by filename or list of filename
    """
    mtg_files = shared_data(openalea.strawberry).glob('*.mtg')
    mtg_path= dict((name(f), f) for f in mtg_files) 
    genotypes= list(mtg_path.keys())
    
    for geno in genotypes:
        g= import_mtgfile(geno)
        assert (isinstance(g, openalea.mtg.mtg.MTG), "data not exist or data in"+ geno + "not respect the formalism")
    
    metaMTG= import_mtgfile(genotypes)
    assert isinstance(metaMTG, openalea.mtg.mtg.MTG)   

def test_import_mtg_from_csv():
    """test import of mtg from excel files
    """
    excel_files = shared_data(openalea.strawberry).glob('*/*.xlsx')
    g= import_mtg_from_csv(files=excel_files,first_property="experimental_names",symbol_at_scale=dict(P=1,T=2, F=3, f=3, b=3, HT=3, bt=3, ht=3,s=3)) 
    assert (isinstance(g, openalea.mtg.mtg.MTG),"data not exist or data not respect the formalism")    
    
def test_strawberry_reader_csv():
    """ test one excel files
    """
    excel_files = shared_data(openalea.strawberry).glob('*/*.xlsx')
    for file in excel_files:
        g=strawberry_reader_csv(file=file)
        assert (isinstance(g, openalea.mtg.mtg.MTG), "data not exist or data in"+ file + "not respect the formalism")   