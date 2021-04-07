from openalea.strawberry.import_mtgfile import import_mtgfile
from openalea.strawberry.analysis import extract_at_module_scale
from openalea.strawberry.analysis import occurence_module_order_along_time, pointwisemean_plot, crowntype_distribution


def test_extract_at_module_scale():
    gariguette = import_mtgfile(filename= "Gariguette")
    gariguette_extraction_at_module_scale = extract_at_module_scale(gariguette)
    assert len(gariguette_extraction_at_module_scale) == 241

    gariguette_frequency = occurence_module_order_along_time(data= gariguette_extraction_at_module_scale,frequency_type= "cdf")
    assert len(gariguette_frequency) == 6

    mean= gariguette_extraction_at_module_scale.groupby(["Genotype", "order"]).mean()
    sd= gariguette_extraction_at_module_scale.groupby(["Genotype", "order"]).std()
    assert len(mean) == 6
    assert len(sd) == 6

    