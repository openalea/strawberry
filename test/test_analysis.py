import pandas as pd
from openalea.mtg.io import read_mtg_file

from openalea.strawberry.analysis import extract_at_module_scale, extract_at_node_scale
from openalea.strawberry.analysis import occurence_module_order_along_time, prob_axillary_production
import openalea.strawberry
from openalea.strawberry.data import data_directory


def name(f):
    return f.basename().splitext()[0]


def test_extract_at_module_scale():
    files = data_directory.glob('*.mtg')
    mtg_path = dict((name(f), f) for f in files)
    gariguette = read_mtg_file(mtg_path['Gariguette'])
    gariguette_extraction_at_module_scale = extract_at_module_scale(gariguette)
    assert len(gariguette_extraction_at_module_scale) == 241

    gariguette_frequency = occurence_module_order_along_time(data= gariguette_extraction_at_module_scale,frequency_type= "cdf")
    assert len(gariguette_frequency) == 6


    # remove object value from mean & std
    fd = gariguette_extraction_at_module_scale
    fd.date = pd.to_datetime(fd.date)
    props = [x for x in fd if x in ["Genotype", "order"] or fd[x].dtype!=object]

    mean= fd.filter(props).groupby(["Genotype", "order"]).mean()
    sd= fd.filter(props).groupby(["Genotype", "order"]).std()
    assert len(mean) == 6
    assert len(sd) == 6

def test_extraction_at_node_scale():
    files = data_directory.glob('*.mtg')
    mtg_path = dict((name(f), f) for f in files)
    gariguette = read_mtg_file(mtg_path['Gariguette'])
    gariguette_extraction_at_node_scale = extract_at_node_scale(gariguette)
    assert len(gariguette_extraction_at_node_scale) == 784

    gariguette_axillary_prod=prob_axillary_production(gariguette,order=0)
    assert len(gariguette_axillary_prod)==19

