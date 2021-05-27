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

def plot_3D_growth_developement(mtg, vids=[]):
    if not vids:
        return None
    else:
        mtg.properties()['order'] = orders(mtg)
        scene=visu3d.plot3d(mtg,by=["Sample_date"],hide_leaves=False,display=False, vids=vids)
        p = PlantGL(scene, group_by_color=p2_wgt_parameters.v_model)
        return p 

def print_3D_growth_developement(mtg, genotype):
    if mtg:
        with p2_wgt_3D_growth_developement:
            p2_wgt_3D_growth_developement.clear_output()
            print('3D growth developement')
            vids_selected = get_vid_of_genotype(misc.all_mtg, genotypes=[genotype])
            misc.all_mtg.properties()['order'] = orders(misc.all_mtg)
            scene=visu3d.plot3d(misc.all_mtg,by=["Sample_date"],hide_leaves=False,display=False, vids=vids_selected)
            display(SceneWidget(scene))
#             display(PlantGL(scene, group_by_color=p2_wgt_parameters.v_model))
    else:
        with p2_wgt_3D_growth_developement:
            p2_wgt_3D_growth_developement.clear_output()
            print('Select a Genotype')


def print_3D_floral_intensity(mtg, genotype):
    if mtg:
        with p2_wgt_3D_floral_intensity:
            p2_wgt_3D_floral_intensity.clear_output()
            print('3D floral_intensity ')
            vids_selected = get_vid_of_genotype(misc.all_mtg, genotypes=[genotype])
            misc.all_mtg.properties()['order'] = orders(misc.all_mtg)
            scene=visu3d.plot3d(misc.all_mtg,by=["Sample_date"],hide_leaves=True,display=False, vids=vids_selected)
            display(SceneWidget(scene))
#             display(PlantGL(scene, group_by_color=p2_wgt_parameters.v_model))    
    else:
        with p2_wgt_3D_growth_developement:
            p2_wgt_3D_growth_developement.clear_output()
            print('Select a Genotype') 

def plot_2D_single_p(mtg):
    return mtg
    
    
def print_2D_single_p():
    with p2_wgt_2D_single_p:
        p2_wgt_2D_single_p.clear_output()
        print('2D Single plant')
        print(plot_2D_single_p(0))



# # ----------------------------------------------------------------
# # On event trigger
# # ----------------------------------------------------------------

def on_change_3d(widget, event, data):
    # select the mtg from genotype
    print_3D_floral_intensity(misc.all_mtg, data)
    print_3D_growth_developement(misc.all_mtg, data)

def on_change_tab_3d(widget, event, data):
    p2_wgt_genotype_selection_3D.v_model = ""

    
# # ----------------------------------------------------------------
# # Widgets
# # ----------------------------------------------------------------

p2_wgt_genotype_selection_3D = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Genotype",
            truncate_length=22)

p2_wgt_genotype_selection_2D = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Genotype",
            truncate_length=22)

p2_wgt_parameters = v.Select(items=[True, False], 
                        label="Group by color", 
                        multiple=False, chips=True, 
                        v_model=False)


p2_row1 = v.Row(children=[v.Col(children=[p2_wgt_genotype_selection_3D]),
                          v.Col(children=[p2_wgt_parameters])
                         ])

p2_row12 = v.Row(children=[v.Col(children=[p2_wgt_genotype_selection_2D]),                          
                         ])

p2_wgt_3D_growth_developement = widgets.Output(layout=layout_output_wgt)


p2_panel_3D_growth_developement = v.Container(
                              style_='max-height: 120px;',
                              pa="0",
                              fluid=True,
                              children=[
                                    p2_wgt_3D_growth_developement    
                            ])

p2_col2 = v.Col(cols=12, sm=12, md=6, class_="pa-0",
                children=[
                          p2_panel_3D_growth_developement,
                      ])


p2_wgt_3D_floral_intensity = widgets.Output(layout=layout_output_wgt)

p2_panel_3D_floral_intensity = v.Container(
                              fluid=True,
                              children=[
                                    p2_wgt_3D_floral_intensity    
                            ])

p2_col3 = v.Col(cols=12, sm=12, md=6, class_="pa-0",
                children=[
                          p2_panel_3D_floral_intensity,
                      ])
p2_panel_3D = v.Row(children=[p2_col2, p2_col3])

p2_tab1 = v.Row(children=[v.Col(col=12, sm=11, md=11,
                                children=[p2_row1,
                                      p2_panel_3D
                                      ])
                         ])

p2_wgt_2D_single_p = v.Img(src="2D_single_p.png")

#

p2_panel_2D_single_p = v.Container(
                              fluid=True,
                              children=[
                                    p2_wgt_2D_single_p    
                            ])

p2_col4 = v.Col(cols=12, sm=12, md=6, class_="pa-0",
                children=[
                          p2_panel_2D_single_p,
                      ])

p2_wgt_2D_most_central = v.Img(src="2D_most_central.png")

p2_panel_2D_most_central = v.Container(
                              fluid=True,
                              children=[
                                    p2_wgt_2D_most_central    
                            ])

p2_col5 = v.Col(cols=12, sm=12, md=6, class_="pa-0",
                children=[
                          p2_panel_2D_most_central,
                      ])


p2_panel_2D = v.Row(children=[p2_col4, p2_col5])


p2_tab2 = v.Row(children=[v.Col(col=12, sm=11, md=11,
                                children=[p2_row12,
                                      p2_panel_2D
                                      ])
                         ])

p2_t1 = v.Tab(children=['3D Visualization'])


p2 = v.Tabs( 
            children=[
            v.Tab(children=['2D Visualization']),
            p2_t1,
            v.TabItem(children=[
                p2_tab2
            ]),
            v.TabItem(children=[
                p2_tab1
            ]), 
        ])

p2_container_main = v.Container(fluid=True, 
                                   class_='grid-list-md box',
                                   children=[
                                       p2
                                   ])


# # ----------------------------------------------------------------
# # Link widgets - event
# # ----------------------------------------------------------------

p2_wgt_genotype_selection_3D.on_event("change", on_change_3d)

p2_wgt_parameters.on_event("change", on_change_3d)

p2_t1.on_event('change', on_change_tab_3d)

