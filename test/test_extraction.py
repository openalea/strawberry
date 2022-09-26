from openalea.deploy.shared_data import shared_data
import openalea.strawberry
from openalea.mtg.io import read_mtg_file
from openalea.mtg.algo import union
from openalea.mtg import MTG


from openalea.strawberry.analysis import extract_at_module_scale, extract_at_node_scale, extract_at_plant_scale

def name(f):
    return f.basename().splitext()[0]

def test_extract_at_module_scale():
    files = shared_data(openalea.strawberry).glob('*.mtg')

    mtg_path = dict((name(f), f) for f in files)
    mtg = MTG()
    for k, genotype in enumerate(mtg_path):
        if (genotype=="Sicile") or (genotype=="Nils") or (genotype=='origine_stolon_gariguetteDV_6novembre2018') \
        or (genotype=='friendlyfruit_varieties') or (genotype=='figure0_paper'):
            pass
        else:
            mtg = union(mtg, read_mtg_file(mtg_path[genotype]))

    genotypes = mtg.property('Genotype')

    for geno in set(genotypes.values()):
        vids=[vid for vid in mtg.vertices(scale=1) if genotypes.get(vid) == geno]
        df = extract_at_module_scale(mtg, vids)
        assert not df.empty
        assert set(df['Genotype']) == {geno}


def test_extract_at_node_scale():
    files = shared_data(openalea.strawberry).glob('*.mtg')

    mtg_path = dict((name(f), f) for f in files)
    mtg = MTG()
    for k, genotype in enumerate(mtg_path):
        if (genotype=="Sicile") or (genotype=="Nils") or (genotype=='origine_stolon_gariguetteDV_6novembre2018') \
        or (genotype=='friendlyfruit_varieties') or (genotype=='figure0_paper'):
            pass
        else:
            mtg = union(mtg, read_mtg_file(mtg_path[genotype]))

    genotypes = mtg.property('Genotype')

    for geno in set(genotypes.values()):
        vids=[vid for vid in mtg.vertices(scale=1) if genotypes.get(vid) == geno]
        df = extract_at_node_scale(mtg, vids)
        assert not df.empty
        assert set(df['Genotype']) == {geno}


def test_extract_at_plant_scale():
    files = shared_data(openalea.strawberry).glob('*.mtg')

    mtg_path = dict((name(f), f) for f in files)
    mtg = MTG()
    for k, genotype in enumerate(mtg_path):
        if (genotype=="Sicile") or (genotype=="Nils") or (genotype=='origine_stolon_gariguetteDV_6novembre2018') \
        or (genotype=='friendlyfruit_varieties') or (genotype=='figure0_paper'):
            pass
        else:
            mtg = union(mtg, read_mtg_file(mtg_path[genotype]))

    genotypes = mtg.property('Genotype')

    for geno in set(genotypes.values()):
        vids=[vid for vid in mtg.vertices(scale=1) if genotypes.get(vid) == geno]
        df = extract_at_plant_scale(mtg, vids)
        assert not df.empty
        assert set(df['Genotype']) == {geno}