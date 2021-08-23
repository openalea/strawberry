import ipyvuetify as v
import ipywidgets as widgets

import pandas as pd
import numpy as np

import oawidgets.mtg

from openalea.mtg.io import read_mtg_file
from openalea.mtg.algo import union
from openalea.mtg import MTG

import openalea.strawberry.application.app_visualization as p2
import openalea.strawberry.application.app_plant_scale as p3
import openalea.strawberry.application.app_module_scale as p4
import openalea.strawberry.application.app_node_scale as p5

from openalea.strawberry.application.misc import (get_vid_of_genotype, get_genotypes, get_vid_from_nbplant, get_files, get_table_mtg, create_grid, update_grid)
import openalea.strawberry.application.misc as misc

from openalea.strawberry.application.layout import layout_output_wgt


# # ----------------------------------------------------------------
# # Load files
# # ----------------------------------------------------------------
files, file_paths = get_files()


# # ----------------------------------------------------------------
# # Print on widget function
# # ----------------------------------------------------------------

def print_preview(g, genotype="", p_nb=1, width="800px", height="600px"):
    with graphMTG:
        graphMTG.clear_output()
        vid = get_vid_from_nbplant(g, genotype, p_nb)
        p = oawidgets.mtg.plot(g.sub_mtg(vid), scale=parameter_scale.v_model, height=height, width=width)
        display(p)

        
def print_files_description():
    with files_description:
        files_description.clear_output()
        # nb of files selected
        nb_files = len(files_selection.v_model)

        # experiments names:
        exp_names = set(misc.all_mtg.property('Experiment_name').values())

        # genotypes: 
        genotype_names = get_genotypes(misc.all_mtg)

        # mtg.properties: + list of possible values
        properties = [(p, set(misc.all_mtg.property(p).values())) for p in misc.all_mtg.property_names() if p not in ['edge_type', 'index', 'label', 
                                                                                                       'Experiment_name', 'Genotype', 
                                                                                                       '_line', 'DBI']]
        print('Number of files selected:', nb_files)
        print('Experiment names:', exp_names)
        print('List of genotypes:', genotype_names)
        for genotype in genotype_names:
            print(genotype, ':', len(get_vid_of_genotype(misc.all_mtg, [genotype])), ' plants')
        print('List of properties:', misc.all_mtg.property_names())
        print('\n')
        print('List of properties values:')

        for p in properties:
            if p[1]:
                if isinstance(next(iter(p[1])), float):
                    print(p[0], ' min:', min(p[1]), 'max:', max(p[1]), 'mean:', np.mean(list(p[1])), 'std:', np.std(list(p[1])), 'Q1:', np.quantile(list(p[1]), 0.25),'Q2:', np.quantile(list(p[1]), 0.50),'Q3:', np.quantile(list(p[1]), 0.75),)
                else:
                    print(p[0], ': ', p[1])


# # ----------------------------------------------------------------
# # On event trigger
# # ----------------------------------------------------------------

def on_change_upload(widget, event, data):
    # add the file to the mtg repository
    pass


def on_change_get_files(widget, event, data):
    # load mtgs
    misc.all_mtg = MTG()
    for file in data:
        mtg = read_mtg_file(file_paths[file])
        misc.all_mtg = union(misc.all_mtg, mtg)
    
    # update table
    if misc.all_mtg:
        df = get_table_mtg(misc.all_mtg)
        # TODO: 
        update_grid(df, tableMTG)
    else:
        update_grid(pd.DataFrame(), tableMTG)
    
    # update genotype selections
    genotypes_selection.items=get_genotypes(misc.all_mtg)
    p2.genotype_selection_3d.items=get_genotypes(misc.all_mtg)
    p2.genotype_selection_2d.items=get_genotypes(misc.all_mtg)
    p3.genotypes_selection_extraction.items=get_genotypes(misc.all_mtg)
    p3.genotypes_selection_analyze.items=get_genotypes(misc.all_mtg)
    p4.genotypes_selection_extraction.items=get_genotypes(misc.all_mtg)
    p4.genotypes_selection_single_genotype.items=get_genotypes(misc.all_mtg)
    p4.genotypes_selection_waffle.items=get_genotypes(misc.all_mtg)
    p5.genotypes_selection_waffle.items=get_genotypes(misc.all_mtg)
    
    # update file description
    print_files_description()


def on_click_allp(widget, event, data):
    if data:
        slider_n_plant.disabled = True
        box_n_plant.disabled = True
    else:
        slider_n_plant.disabled = False
        box_n_plant.disabled = False
    
def on_change_genotype(widget, event, data):
    # update plant selection 
    slider_n_plant.disabled=False
    box_n_plant.disabled=False
    cb_allplants.disabled=False    
    slider_n_plant.max = len(get_vid_of_genotype(misc.all_mtg, [data]))
    slider_n_plant.v_model=1
    
    # update mtg preview
    print_preview(misc.all_mtg, genotype=data, p_nb= slider_n_plant.v_model ,width="500px", height="800px")
    
    
def on_change_nbplant(widget, event, data):
    # update mtg preview
    print_preview(misc.all_mtg, genotype=genotypes_selection.v_model, p_nb= data ,width="500px", height="800px")

def on_change_parameters(widget, event, data):
    # update mtg preview
    if misc.all_mtg:
        print_preview(misc.all_mtg, genotype=genotypes_selection.v_model, p_nb= slider_n_plant.v_model ,width="1000px", height="1000px")

        

# # ----------------------------------------------------------------
# # Widgets
# # ----------------------------------------------------------------

files_upload = v.FileInput(row=True, wrap=True, align_center=True, 
            chips=True, 
            multiple=True,
            counter=True,
            v_model=None,
            label="Import Files",
            truncate_length=22)

files_selection = v.Select(v_model=None, items=files, 
                        label="Select Files", 
                        multiple=True, chips=True, counter=True)


export_all = v.Btn(children=['Export Analyses'])

genotypes_selection = v.Select(items=[],
            chips=True, 
            multiple=False,
            counter=True,
            v_model="",
            label="Select Genotypes",
            truncate_length=22)

parameter_scale = v.Select(items=[{"text":"scale 1",
                                     "value":1},
                                    {"text":"scale 2",
                                     "value":2}], 
                        label="Select Parameters", 
                        multiple=False, chips=True,
                        v_model=2)

slider_n_plant = v.Slider(max=100,
             min=1,
           label="#p",
           thumb_label=True,
            v_model="",
            disabled=True)

box_n_plant = v.TextField(type_="number", 
                class_="mt-0 pt-0",
                v_model='',
                disabled=True)

plant_selection=v.Row(children=[v.Col(cols=12, sm=7, md=7, children=[slider_n_plant]),
                                        v.Col(cols=12, sm=1, md=1, children=[box_n_plant]) 
                                       ])

cb_allplants = v.Checkbox(v_model=False,label="Select all plants", disabled=True)

menu_plant = v.Col(cols=12, sm=3, md=3,
                children=[
                      files_selection,
                      v.Divider(),
                      files_upload,
                      v.Divider(),
                      genotypes_selection,
                      v.Divider(),
                      plant_selection,
                      v.Divider(),
                      cb_allplants,
                      v.Divider(),
                      parameter_scale,
                      v.Divider(),
                      export_all
                  ])

tableMTG = create_grid()

panel_tableMTG = v.Container(
                              label="The MTG as a table",
                              fluid=True,
                              children=[tableMTG])

graphMTG=create_grid()

panel_graphMTG = v.Container(
                              label="The MTG as a graph",
                              fluid=True,
                              children=[graphMTG])


panel_MTG = v.Col(cols=12, sm=8, md=8,
                children=[
                          panel_tableMTG,
                          v.Divider(),
                          panel_graphMTG,
                      ])


tab_MTG_content = v.Row(children=[
                              menu_plant,
                              panel_MTG,
                          ])

files_description = widgets.Output(layout=layout_output_wgt)

panel_files_description = v.Container(
                              fluid=False,
                              children=[files_description])

tab_description_content = v.Row(children=[v.Col(cols=12, sm=3, md=3,
                                children=[files_selection]),
                          v.Col(cols=12, sm=7, md=9,
                                children=[panel_files_description])
                          ])

container_main = v.Container(fluid=True, 
                            class_='grid-list-md box',
                            children=[v.Tabs( children=[
                                        v.Tab(children=['Import Files']),
                                        v.Tab(children=['Files Description']),
                                        v.TabItem(children=[tab_MTG_content]),
                                        v.TabItem(children=[tab_description_content])
                                            ])
                                    ])


# # ----------------------------------------------------------------
# # Link widgets - event
# # ----------------------------------------------------------------

widgets.jslink((slider_n_plant,'v_model'), (box_n_plant,'v_model'))

files_selection.on_event('change', on_change_get_files)
cb_allplants.on_event('change', on_click_allp)
genotypes_selection.on_event('change', on_change_genotype)
slider_n_plant.on_event('change', on_change_nbplant)
box_n_plant.on_event('change', on_change_nbplant)
parameter_scale.on_event('change', on_change_parameters)
