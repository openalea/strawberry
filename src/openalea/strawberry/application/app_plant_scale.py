import ipyvuetify as v
import ipywidgets as widgets

import pandas as pd
import qgrid
import plotly.graph_objs as go

import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

from openalea.strawberry.analysis import (extract_at_module_scale, extract_at_plant_scale, df2waffle, plot_pie)

import openalea.strawberry.application.misc as misc
from openalea.strawberry.application.misc import (get_vid_of_genotype, transfert_figure, transfert_figure_pie)
from openalea.strawberry.application.layout import layout_output_wgt, layout_gofigure


# # ----------------------------------------------------------------
# # Print on widget function
# # ----------------------------------------------------------------



# # ----------------------------------------------------------------
# # On event trigger
# # ----------------------------------------------------------------

def on_change_genotype_p3_t1(widget, event, data):
    # update table
    df=pd.DataFrame()
    if misc.all_mtg:
        vids=get_vid_of_genotype(misc.all_mtg, genotypes=data)
        df = extract_at_plant_scale(misc.all_mtg, vids=vids)
    p3_wgt_df_plantscale.df = df
    
    # update descriptors
    with p3_wgt_descriptors:
        p3_wgt_descriptors.clear_output()
        display(df.describe())
        

def on_change_genotype_p3_t2(widget, event, data):
    genotype=p3_wgt_genotypes_selection_t2.v_model
    vids=get_vid_of_genotype(misc.all_mtg, [genotype])
    df=extract_at_plant_scale(misc.all_mtg, vids=vids)
    param = list(df.columns)
    param.remove("Genotype")
    param.remove('date')
    p3_wgt_date_selection.items=list(df.date.unique())
    p3_wgt_date_selection.v_model=""
    p3_wgt_parameter_selection.items=param
    

def on_change_date_p3(widget, event, data):

    genotype=p3_wgt_genotypes_selection_t2.v_model
    vids=get_vid_of_genotype(misc.all_mtg, [genotype])
    df=extract_at_module_scale(misc.all_mtg, vids=vids)
    
    tmp=df2waffle(df, index='order', 
              date=data, 
              variable='stage', 
              crosstab=True)
    
    try:
        fig = plot_pie(tmp)
        fig.update_layout(title="Percentage representation of each stage at one date")
        transfert_figure_pie(fig,p3_pie)
    except ValueError:
        pass
            
            
    
def on_change_parameter_p3(widget, event, data):
#     if date ...
    genotype=p3_wgt_genotypes_selection_t2.v_model
    vids=get_vid_of_genotype(misc.all_mtg, [genotype])
    df=extract_at_plant_scale(misc.all_mtg, vids=vids)

    res = df.groupby('date').mean()
    
    p=res.iplot(kind = "line", 
              mode='lines+markers', 
              y=data,
              xTitle="Dates",
              yTitle=data,
#               yTitle="Probability",
#               title="Relative distribution of complete (True) and incomplete (False) module as function of date for {}".format(genotype),
              asFigure=True
             )
    transfert_figure(p, p3_plot) 

# # ----------------------------------------------------------------
# # Widgets
# # ----------------------------------------------------------------

export_extraction = v.Btn(children=['Export table'])

genotypes_selection_extraction = v.Select(items=[],
            chips=True, 
            multiple=True,
            counter=True,
            v_model="",
            label="Select Genotypes",
            truncate_length=22)

menu_plant = v.Col(cols=12, sm=3, md=3,
                children=[
                          genotypes_selection_extraction,
                          export_extraction
                      ])

p3_wgt_df_plantscale = qgrid.show_grid(pd.DataFrame(), show_toolbar=False, 
                                  grid_options={'forceFitColumns': False, 'editable':True, 'defaultColumnWidth':50})


p3_panel_table = v.Container(
                              fluid=True,
                              children=[
                                    p3_wgt_df_plantscale    
                            ])

p3_wgt_descriptors = widgets.Output(layout=layout_output_wgt)

p3_panel_descriptors =v.Container(fluid=True,
                              children=[
                                    p3_wgt_descriptors    
                                ])

p3_col2 = v.Col(cols=12, sm=7, md=9,
                children=[
                          p3_panel_table,
                          p3_panel_descriptors,
                      ])


p3_tab1 = v.Row(children=[menu_plant,
                          p3_col2,
                          ])

p3_wgt_genotypes_selection_t2 = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Genotype",
            truncate_length=22)

p3_wgt_date_selection = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Date",
            truncate_length=22)

p3_wgt_parameter_selection = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Parameter",
            truncate_length=22)



p3_select_genotype = v.Row(children=[p3_wgt_genotypes_selection_t2,
                                   p3_wgt_date_selection,
                                   p3_wgt_parameter_selection,
                                   ])

p3_plot = go.FigureWidget(layout=layout_gofigure)
p3_pie = go.FigureWidget(layout=layout_gofigure)

p3_tab2 = v.Row(children=[v.Col(
                            children=[
                                p3_select_genotype,
                                v.Row(children=[p3_plot, p3_pie]),
                              ]),
                        ])

p3 = v.Tabs( 
            children=[
            v.Tab(children=['Export']),
            v.Tab(children=['Analyses']),
            v.TabItem(children=[
                p3_tab1,]),
            v.TabItem(children=[p3_tab2]),

        ])


p3_container_main = v.Container(fluid=True, 
                                   class_='grid-list-md box',
                                   children=[
                                       p3
                                   ])


# # ----------------------------------------------------------------
# # Link widgets - event
# # ----------------------------------------------------------------

genotypes_selection_extraction.on_event('change', on_change_genotype_p3_t1)
p3_wgt_genotypes_selection_t2.on_event('change', on_change_genotype_p3_t2)
p3_wgt_date_selection.on_event('change', on_change_date_p3)
p3_wgt_parameter_selection.on_event('change', on_change_parameter_p3)



