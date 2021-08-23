import ipyvuetify as v
import ipywidgets as widgets

from openalea.mtg.algo import orders

from openalea.strawberry import visu3d, visu2d 

from openalea.strawberry.application.layout import layout_output_wgt
import openalea.strawberry.application.misc as misc
from openalea.strawberry.application.misc import get_vid_of_genotype, display3d
from openalea.strawberry.analysis import extract_at_plant_scale, median_individuals

# # ----------------------------------------------------------------
# # Print on widget function
# # ----------------------------------------------------------------

def print_3d_growth_developement(g, genotype):
    if g:
        with plot3d_growth_developement:
            plot3d_growth_developement.clear_output()
            print('3d growth developement')
            vids_selected = get_vid_of_genotype(g, genotypes=[genotype])
            g.properties()['order'] = orders(g)
            scene=visu3d.plot3d(g,by=["Sample_date"],hide_leaves=False,display=False, vids=vids_selected)
            display3d(scene)
    else:
        with plot3d_growth_developement:
            plot3d_growth_developement.clear_output()
            print('Select a Genotype')


def print_3d_floral_intensity(g, genotype):
    if g:
        with plot3d_floral_intensity:
            plot3d_floral_intensity.clear_output()
            print('3d floral_intensity ')
            vids_selected = get_vid_of_genotype(g, genotypes=[genotype])
            g.properties()['order'] = orders(g)
            scene=visu3d.plot3d(g,by=["Sample_date"],hide_leaves=True,display=False, vids=vids_selected)
            display3d(scene) 
    else:
        with plot3d_floral_intensity:
            plot3d_floral_intensity.clear_output()
            print('Select a Genotype') 


def print_2d_single_p(g, genotype, vid):
    with plot2d_single_p:
        plot2d_single_p.clear_output()
        vids_selected = get_vid_of_genotype(g, genotypes=[genotype])
        g.properties()['order'] = orders(g)
        scene=visu2d.plot2d(g,[vids_selected[vid]],dist=[3]*3,display=False)
        display3d(scene)

def print_2d_median(g, genotype):
    with plot2d_most_central:
        plot2d_most_central.clear_output()
        vids_selected=get_vid_of_genotype(g, genotypes=[genotype])
        g.properties()['order'] = orders(g)
        df = extract_at_plant_scale(g, vids=vids_selected)
        df_median=median_individuals(df,)
        # selection of vid of median individuals
        pids = list(df_median.vid)
        n = len(pids)
        scene= visu2d.plot2d(g, pids, dist=[6]*n, display=False)
        display3d(scene)


# # ----------------------------------------------------------------
# # On event trigger
# # ----------------------------------------------------------------

def on_change_3d(widget, event, data):
    print_3d_floral_intensity(misc.all_mtg, data)
    print_3d_growth_developement(misc.all_mtg, data)


def on_change_tab_3d(widget, event, data):
    genotype_selection_3d.v_model = ""
    with plot3d_floral_intensity:
        plot3d_floral_intensity.clear_output()
    with plot3d_growth_developement:
        plot3d_growth_developement.clear_output()

def on_change_geno_2d(widget, event, data):
    id_selection_2d.items = list(range(len(get_vid_of_genotype(misc.all_mtg, [data]))))
    id_selection_2d.v_model=1

    print_2d_median(misc.all_mtg, data)
    print_2d_single_p(misc.all_mtg, data, vid=id_selection_2d.v_model)

    
def on_change_id_2d(widget, event, data):
    print_2d_single_p(misc.all_mtg, genotype= genotype_selection_2d.v_model, vid=data)


# # ----------------------------------------------------------------
# # Widgets
# # ----------------------------------------------------------------

genotype_selection_3d = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Genotype",
            truncate_length=22)

genotype_selection_2d = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Genotype",
            truncate_length=22)

id_selection_2d = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Plant ID",
            truncate_length=22)

parameter_color = v.Select(items=[True, False], 
                        label="Group by color", 
                        multiple=False, chips=True, 
                        v_model=False)

menu_plant_3d = v.Row(children=[v.Col(children=[genotype_selection_3d]),
                          v.Col(children=[parameter_color])
                         ])

row_param2d = v.Row(children=[v.Col(children=[genotype_selection_2d]), 
                          v.Col(children=[id_selection_2d])                         
                         ])

plot3d_growth_developement = widgets.Output(layout=layout_output_wgt)

plot3d_floral_intensity = widgets.Output(layout=layout_output_wgt)

panel_3d = v.Row(children=[v.Col(children=[v.Container(fluid=True, children=[plot3d_growth_developement])]), 
                           v.Col(children=[v.Container(fluid=True, children=[plot3d_floral_intensity])])])

tab_3d_content = v.Row(children=[v.Col(col=12, sm=12, md=12,
                                children=[menu_plant_3d,
                                      panel_3d
                                      ])
                         ])

plot2d_single_p = widgets.Output(layout=layout_output_wgt)

plot2d_most_central = widgets.Output(layout=layout_output_wgt)

panel_2d = v.Row(children=[v.Col(children=[plot2d_single_p]), 
                           v.Col(children=[plot2d_most_central,])])


tab_2d_content = v.Row(children=[v.Col(col=12, sm=12, md=12,
                                children=[row_param2d,
                                      panel_2d
                                      ])
                         ])

# Instantiate tab 3d here to link it to an event
tab_3d = v.Tab(children=['3d Visualization'])

container_main = v.Container(fluid=True, 
                            class_='grid-list-md box',
                            children=[
                                v.Tabs( children=[
                                    v.Tab(children=['2d Visualization']),
                                    tab_3d,
                                    v.TabItem(children=[tab_2d_content]),
                                    v.TabItem(children=[tab_3d_content]), 
                                ])
                            ])


# # ----------------------------------------------------------------
# # Link widgets - event
# # ----------------------------------------------------------------

genotype_selection_3d.on_event("change", on_change_3d)
parameter_color.on_event("change", on_change_3d)
genotype_selection_2d.on_event("change", on_change_geno_2d)
id_selection_2d.on_event("change", on_change_id_2d)

tab_3d.on_event('change', on_change_tab_3d)
