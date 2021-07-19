import ipyvuetify as v
import ipywidgets as widgets

import pandas as pd
import plotly.graph_objs as go

import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

from openalea.strawberry.analysis import (extract_at_module_scale, extract_at_plant_scale, df2waffle, plot_pie)

import openalea.strawberry.application.misc as misc
from openalea.strawberry.application.misc import (get_vid_of_genotype, transfert_figure, transfert_figure_pie, create_grid, update_grid)
from openalea.strawberry.application.layout import layout_output_wgt, layout_gofigure


# # ----------------------------------------------------------------
# # On event trigger
# # ----------------------------------------------------------------

def on_change_genotype_p3_t1(widget, event, data):
    # update table
    df=pd.DataFrame()
    if misc.all_mtg:
        vids=get_vid_of_genotype(misc.all_mtg, genotypes=data)
        df = extract_at_plant_scale(misc.all_mtg, vids=vids)
    update_grid(df, df_plantscale)
    
    # update descriptors
    update_grid(df.describe(), df_description)
        

def on_change_genotype_p3_t2(widget, event, data):
    genotype=genotypes_selection_analyze.v_model
    vids=get_vid_of_genotype(misc.all_mtg, [genotype])
    df=extract_at_plant_scale(misc.all_mtg, vids=vids)
    param = list(df.columns)
    param.remove("Genotype")
    param.remove('date')
    date_selection_analyze.items=list(df.date.unique())
    date_selection_analyze.v_model=""
    variable_selection_analyze.items=param
    

def on_change_date_p3(widget, event, data):

    genotype=genotypes_selection_analyze.v_model
    vids=get_vid_of_genotype(misc.all_mtg, [genotype])
    df=extract_at_module_scale(misc.all_mtg, vids=vids)
    
    tmp=df2waffle(df, index='order', 
              date=data, 
              variable='stage', 
              crosstab=True)
    
    try:
        fig = plot_pie(tmp)
        fig.update_layout(title="Percentage representation of each stage at one date")
        transfert_figure_pie(fig,pie_plantscale)
    except ValueError:
        pass
            
            
    
def on_change_parameter_p3(widget, event, data):
#     if date ...
    genotype=genotypes_selection_analyze.v_model
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
    transfert_figure(p, plot_plantscale) 

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

menu_plant_extraction = v.Col(cols=12, sm=3, md=3,
                children=[
                          genotypes_selection_extraction,
                          export_extraction
                      ])

df_plantscale = create_grid()

panel_df = v.Container(
                        fluid=True,
                        children=[
                            df_plantscale    
                    ])

df_description = create_grid()

panel_description =v.Container(fluid=True,
                              children=[
                                    df_description    
                                ])

tab_extraction_content = v.Row(children=[menu_plant_extraction,
                          v.Col(cols=12, sm=7, md=9, children=[
                            panel_df,
                            panel_description,
                            ]),
                          ])

genotypes_selection_analyze = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Genotype",
            truncate_length=22)

date_selection_analyze = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Date",
            truncate_length=22)

variable_selection_analyze = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Variable",
            truncate_length=22)

menu_plant_analyze = v.Row(children=[genotypes_selection_analyze,
                                   date_selection_analyze,
                                   variable_selection_analyze,
                                   ])

plot_plantscale = go.FigureWidget(layout=layout_gofigure)
pie_plantscale = go.FigureWidget(layout=layout_gofigure)

tab_analyze_content = v.Row(children=[v.Col(
                            children=[
                                menu_plant_analyze,
                                v.Row(children=[plot_plantscale, pie_plantscale]),
                              ]),
                        ])

container_main = v.Container(fluid=True, 
                                   class_='grid-list-md box',
                                   children=[v.Tabs( 
                                        children=[
                                        v.Tab(children=['Export']),
                                        v.Tab(children=['Analyses']),
                                        v.TabItem(children=[tab_extraction_content,]),
                                        v.TabItem(children=[tab_analyze_content]),
                                        ])
                                   ])


# # ----------------------------------------------------------------
# # Link widgets - event
# # ----------------------------------------------------------------

genotypes_selection_extraction.on_event('change', on_change_genotype_p3_t1)
genotypes_selection_analyze.on_event('change', on_change_genotype_p3_t2)
date_selection_analyze.on_event('change', on_change_date_p3)
variable_selection_analyze.on_event('change', on_change_parameter_p3)



