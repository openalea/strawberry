import os
from pathlib import Path
from openalea.mtg.io import read_mtg_file, write_mtg

import openalea.strawberry
from openalea.strawberry.analysis import extract_at_node_scale, extract_at_module_scale
from openalea.strawberry.analysis import df2waffle
from openalea.strawberry.data import data_directory


def name(f):
    return f.basename().splitext()[0]

def test_df2waffle():
    files = data_directory.glob('*.mtg')
    mtg_path = dict((name(f), f) for f in files)
    mtg = read_mtg_file(mtg_path['Capriss'])

    df = extract_at_node_scale(mtg)

    node_scale = df2waffle(df, index='rank', date='2015/03/02', variable='branching_type')
    assert node_scale.shape == (20, 9)

    df = extract_at_module_scale(mtg)
    module_scale=df2waffle(df, index='order', date='2015/03/02', variable='crown_status', aggfunc='median')
    assert module_scale.shape == (3, 9)

