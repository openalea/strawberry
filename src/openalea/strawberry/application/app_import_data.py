import ipyvuetify as v
import ipywidgets as widgets

import pandas as pd
import numpy as np
from pathlib import Path
import os
import qgrid

import oawidgets.mtg

from openalea.mtg.io import read_mtg_file
from openalea.mtg.algo import union
from openalea.mtg import MTG

import openalea.strawberry.application.app_visualization as p2
import openalea.strawberry.application.app_plant_scale as p3
import openalea.strawberry.application.app_module_scale as p4
import openalea.strawberry.application.app_node_scale as p5

from openalea.strawberry.application.misc import (get_vid_of_genotype, get_genotypes, get_vid_from_nbplant, get_files, fix_inferior_character_for_qgrid, replace_inf_alt, get_table_mtg)
import openalea.strawberry.application.misc as misc

from openalea.strawberry.application.layout import layout_output_wgt

qgrid.set_grid_option('maxVisibleRows', 10)


# # ----------------------------------------------------------------
# # Load files
# # ----------------------------------------------------------------
files, file_paths = get_files()


# # ----------------------------------------------------------------
# # Print on widget function
# # ----------------------------------------------------------------

def print_preview(mtg, genotype="", p_nb=1, width="800px", height="600px"):
    with p1_wgt_graphMTG:
        p1_wgt_graphMTG.clear_output()
        vid = get_vid_from_nbplant(misc.all_mtg, genotype, p_nb)
        p = oawidgets.mtg.plot(mtg.sub_mtg(vid), scale=p1_wgt_parameters.v_model, height=height, width=width)
        display(p)

        
def print_files_description():
    with p1_wgt_files_description:
        p1_wgt_files_description.clear_output()
        # nb of files selected
        nb_files = len(p1_wgt_files_selection.v_model)

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
        df_fixed = fix_inferior_character_for_qgrid(df)
        p1_wgt_tableMTG.df = df_fixed
    else:
        p1_wgt_tableMTG.df= pd.DataFrame()
    
    # update genotype selection
    p1_wgt_genotypes_selection.items=get_genotypes(misc.all_mtg)
    p2.p2_wgt_genotype_selection_3D.items=get_genotypes(misc.all_mtg)
    p2.p2_wgt_genotype_selection_2D.items=get_genotypes(misc.all_mtg)
    p3.p3_wgt_genotypes_selection_t1.items=get_genotypes(misc.all_mtg)
    p3.p3_wgt_genotypes_selection_t2.items=get_genotypes(misc.all_mtg)
    p4.p4_wgt_genotypes_selection_t1.items=get_genotypes(misc.all_mtg)
    p4.p4_wgt_genotypes_selection_t2.items=get_genotypes(misc.all_mtg)
    p4.p4_wgt_genotypes_selection_t4.items=get_genotypes(misc.all_mtg)
    p5.p5_wgt_genotypes_selection_t4.items=get_genotypes(misc.all_mtg)
    
    # update file description
    print_files_description()


def on_click_allp(widget, event, data):
    if data:
        p1_wgt_plants_slider.disabled = True
        p1_wgt_plants_nb.disabled = True
    else:
        p1_wgt_plants_slider.disabled = False
        p1_wgt_plants_nb.disabled = False
    
def on_change_genotype(widget, event, data):
    # update plant selection 
    p1_wgt_plants_slider.disabled=False
    p1_wgt_plants_nb.disabled=False
    p1_wgt_cb_allplants.disabled=False    
    p1_wgt_plants_slider.max = len(get_vid_of_genotype(misc.all_mtg, [data]))
    p1_wgt_plants_slider.v_model=1
    
    # update mtg preview
    print_preview(misc.all_mtg, genotype=data, p_nb= p1_wgt_plants_slider.v_model ,width="500px", height="800px")
    
    
def on_change_nbplant(widget, event, data):
    # update mtg preview
    print_preview(misc.all_mtg, genotype=p1_wgt_genotypes_selection.v_model, p_nb= data ,width="500px", height="800px")

def on_change_parameters(widget, event, data):
    # update mtg preview
    if misc.all_mtg:
        print_preview(misc.all_mtg, genotype=p1_wgt_genotypes_selection.v_model, p_nb= p1_wgt_plants_slider.v_model ,width="1000px", height="1000px")

        

# # ----------------------------------------------------------------
# # Widgets
# # ----------------------------------------------------------------

p1_wgt_files_upload = v.FileInput(row=True, wrap=True, align_center=True, 
            chips=True, 
            multiple=True,
            counter=True,
            v_model=None,
            label="Import Files",
            truncate_length=22)

p1_wgt_files_selection = v.Select(v_model=None, items=files, 
                        label="Select Files", 
                        multiple=True, chips=True, counter=True)

p1_wgt_files_selection.on_event('change', on_change_get_files)

p1_wgt_export = v.Btn(children=['Export Analyses'])

p1_wgt_genotypes_selection = v.Select(items=[],
            chips=True, 
            multiple=False,
            counter=True,
            v_model="",
            label="Select Genotypes",
            truncate_length=22)

p1_wgt_parameters = v.Select(items=[{"text":"scale 1",
                                     "value":1},
                                    {"text":"scale 2",
                                     "value":2}], 
                        label="Select Parameters", 
                        multiple=False, chips=True,
                        v_model=2)

p1_wgt_plants_slider = v.Slider(max=100,
             min=1,
           label="#p",
           thumb_label=True,
            v_model="",
            disabled=True)

p1_wgt_plants_nb = v.TextField(type_="number", 
                class_="mt-0 pt-0",
                v_model='',
                disabled=True)


p1_wgt_plants_selection=v.Row(children=[v.Col(cols=12, sm=7, md=7,
                                              children=[p1_wgt_plants_slider]),
                                        v.Col(cols=12, sm=1, md=1,
                                              children=[p1_wgt_plants_nb]) 
                                       ])

p1_wgt_cb_allplants = v.Checkbox(v_model=False,label="Select all plants", disabled=True)



p1_col1 = v.Col(cols=12, sm=3, md=3,
                children=[
                      p1_wgt_files_selection,
                      v.Divider(),
                      p1_wgt_files_upload,
                      v.Divider(),
                      p1_wgt_genotypes_selection,
                      v.Divider(),
                      p1_wgt_plants_selection,
                      v.Divider(),
                      p1_wgt_cb_allplants,
                      v.Divider(),
                      p1_wgt_parameters,
                      v.Divider(),
                      p1_wgt_export
                  ])

p1_wgt_tableMTG = qgrid.show_grid(pd.DataFrame(), show_toolbar=False, 
                                  grid_options={'forceFitColumns': False, 'editable':True, 'defaultColumnWidth':50})

p1_panel_table_mtg = v.Container(
#                               style_='width: 600px; height: 300px',
                              label="The MTG as a table",
                              fluid=True,
                              children=[
                                    p1_wgt_tableMTG    
                            ])

p1_wgt_graphMTG = widgets.Output(layout=layout_output_wgt)

p1_panel_graph_mtg = v.Container(
                              label="The MTG as a graph",
                              fluid=True,
                              children=[
                                    p1_wgt_graphMTG    
                            ])


p1_col2 = v.Col(cols=12, sm=8, md=8,
                children=[
                          p1_panel_table_mtg,
                          v.Divider(),
                          p1_panel_graph_mtg,
                      ])


p1_content1 = v.Row(children=[
                              p1_col1,
                              p1_col2,
                          ])

# p1_log_content = v.Textarea(background_color="black",
#                             dark=True,
#                             auto_grow=True,
#                             value= "ICI s'afficheront les messages d'erreurs et les infos sur les imports"
#                            )

# p1_log = v.Row(children=[
#                   p1_log_content
#               ])

p1_tab1 = v.Row(children=[
                    v.Col(col=12, sm=11, md=11,
                          children=[p1_content1,
#                                     p1_log,
                                   ])
                ])



p1_wgt_files_description = widgets.Output(layout=layout_output_wgt)

p1_panel_files_description = v.Container(
                              fluid=False,
                              children=[
                                    p1_wgt_files_description    
                            ])


p1_tab2 = v.Row(children=[v.Col(cols=12, sm=3, md=3,
                                children=[p1_wgt_files_selection]),
                          v.Col(cols=12, sm=7, md=9,
                                children=[p1_panel_files_description])
                          ])


p1 = v.Tabs( 
            children=[
            v.Tab(children=['Import Files']),
            v.Tab(children=['Files Description']),
            v.TabItem(children=[
                p1_tab1
            ]),
            v.TabItem(children=[
                p1_tab2
            ])
        ])

p1_container_main = v.Container(fluid=True, 
                                   class_='grid-list-md box',
                                   children=[
                                       p1
                                   ])


# # ----------------------------------------------------------------
# # Link widgets - event
# # ----------------------------------------------------------------

widgets.jslink((p1_wgt_plants_slider,'v_model'), (p1_wgt_plants_nb,'v_model'))

p1_wgt_cb_allplants.on_event('change', on_click_allp)
p1_wgt_genotypes_selection.on_event('change', on_change_genotype)
p1_wgt_plants_slider.on_event('change', on_change_nbplant)
p1_wgt_plants_nb.on_event('change', on_change_nbplant)
p1_wgt_parameters.on_event('change', on_change_parameters)





