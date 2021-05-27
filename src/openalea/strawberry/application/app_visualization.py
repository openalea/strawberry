import ipyvuetify as v
import ipywidgets as widgets

from oawidgets.plantgl import PlantGL
from pgljupyter import SceneWidget

from openalea.mtg.algo import orders

from openalea.strawberry import visu3d 

from openalea.strawberry.application.layout import layout_output_wgt
import openalea.strawberry.application.misc as misc
from openalea.strawberry.application.misc import get_vid_of_genotype


# # ----------------------------------------------------------------
# # Print on widget function
# # ----------------------------------------------------------------

def print_3d_growth_developement(mtg, genotype):
    if mtg:
        with plot3d_growth_developement:
            plot3d_growth_developement.clear_output()
            print('3d growth developement')
            vids_selected = get_vid_of_genotype(misc.all_mtg, genotypes=[genotype])
            misc.all_mtg.properties()['order'] = orders(misc.all_mtg)
            scene=visu3d.plot3d(misc.all_mtg,by=["Sample_date"],hide_leaves=False,display=False, vids=vids_selected)
            display(SceneWidget(scene))
#             display(PlantGL(scene, group_by_color=parameter_color.v_model))
    else:
        with plot3d_growth_developement:
            plot3d_growth_developement.clear_output()
            print('Select a Genotype')


def print_3d_floral_intensity(mtg, genotype):
    if mtg:
        with plot3d_floral_intensity:
            plot3d_floral_intensity.clear_output()
            print('3d floral_intensity ')
            vids_selected = get_vid_of_genotype(misc.all_mtg, genotypes=[genotype])
            misc.all_mtg.properties()['order'] = orders(misc.all_mtg)
            scene=visu3d.plot3d(misc.all_mtg,by=["Sample_date"],hide_leaves=True,display=False, vids=vids_selected)
            display(SceneWidget(scene))
#             display(PlantGL(scene, group_by_color=parameter_color.v_model))    
    else:
        with plot3d_growth_developement:
            plot3d_growth_developement.clear_output()
            print('Select a Genotype') 


def print_2d_single_p():
    with plot2d_single_p:
        plot2d_single_p.clear_output()
        print('2d Single plant')


# # ----------------------------------------------------------------
# # On event trigger
# # ----------------------------------------------------------------

def on_change_3d(widget, event, data):
    print_3d_floral_intensity(misc.all_mtg, data)
    print_3d_growth_developement(misc.all_mtg, data)


def on_change_tab_3d(widget, event, data):
    genotype_selection_3d.v_model = ""

    
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

parameter_color = v.Select(items=[True, False], 
                        label="Group by color", 
                        multiple=False, chips=True, 
                        v_model=False)

row_param3d = v.Row(children=[v.Col(children=[genotype_selection_3d]),
                          v.Col(children=[parameter_color])
                         ])

row_param2d = v.Row(children=[v.Col(children=[genotype_selection_2d]),                          
                         ])

plot3d_growth_developement = widgets.Output(layout=layout_output_wgt)

plot3d_floral_intensity = widgets.Output(layout=layout_output_wgt)

panel_3d = v.Row(children=[v.Col(cols=12, sm=12, md=6, children=[v.Container(fluid=True, children=[plot3d_growth_developement])]), 
                           v.Col(cols=12, sm=12, md=6, children=[v.Container(fluid=True, children=[plot3d_floral_intensity])])])

tab_3d_content = v.Row(children=[v.Col(col=12, sm=11, md=11,
                                children=[row_param3d,
                                      panel_3d
                                      ])
                         ])

plot2d_single_p = v.Container(
                              fluid=True,
                              children=[
                                    v.Img(src="2d_single_p.png")    
                            ])

plot2d_most_central = v.Container(
                              fluid=True,
                              children=[
                                    v.Img(src="2d_most_central.png")    
                            ])

panel_2d = v.Row(children=[v.Col(cols=12, sm=12, md=6, children=[plot2d_single_p]), 
                           v.Col(cols=12, sm=12, md=6, children=[plot2d_most_central,])])


tab_2d_content = v.Row(children=[v.Col(col=12, sm=11, md=11,
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
tab_3d.on_event('change', on_change_tab_3d)

