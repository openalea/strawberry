import ipyvuetify as v
import ipywidgets as widgets

import pandas as pd
import qgrid
import plotly.graph_objs as go

import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

from openalea.strawberry.analysis import (extract_at_node_scale, df2waffle, plot_waffle)

import openalea.strawberry.application.misc as misc
from openalea.strawberry.application.misc import (get_vid_of_genotype, transfert_figure, transfert_figure_pie, create_download_link)
from openalea.strawberry.application.layout import layout_output_wgt, layout_gofigure



# # ----------------------------------------------------------------
# # Print on widget function
# # ----------------------------------------------------------------


# # ----------------------------------------------------------------
# # On event trigger
# # ----------------------------------------------------------------

def on_change_node_waffle_genotype(widget, event, data):
    genotype=p5_wgt_genotypes_selection_t4.v_model
    vids=get_vid_of_genotype(misc.all_mtg, [genotype])
    df=extract_at_node_scale(misc.all_mtg, vids=vids)
    param = list(df.columns)
    param.remove("Genotype")
    param.remove('date')
    p5_wgt_date_selection.items=list(df.date.unique())
    p5_wgt_date_selection.v_model=""
    p5_wgt_parameter_selection.items=param
    order = list(df.order.unique())
    order.append({'text':'All', 'value': None})
    p5_wgt_order_selection.items=order
    
def on_change_node_waffle_date(widget, event, data):
    if not p5_wgt_parameter_selection.v_model:
        pass
    else:
        with p5_waffle:
            p5_waffle.clear_output()
            genotype=p5_wgt_genotypes_selection_t4.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_node_scale(misc.all_mtg, vids=vids)
            tmp=df2waffle(df, index='rank', date=data, variable=p5_wgt_parameter_selection.v_model, order=p5_wgt_order_selection.v_model)

            # TODO: remove the legend here (which only apply to branching_type)
            l_names = {"1":"Stolon", 
               "2":"Vegetative bud",
               "3":"Initiated bud",
               "4":"Aborted bud",
               "5":"Floral bud",
               "6":"Branch crown"}

            fig=plot_waffle(tmp, 
#                             layout=layout,
                            legend_name=l_names,
                            plot_func=p5_wgt_plot_type.v_model)
            
            display(fig)
            
    
def on_change_node_waffle_parameter(widget, event, data):
    if not p5_wgt_date_selection.v_model:
        pass
    else:
        with p5_waffle:
            p5_waffle.clear_output()
            genotype=p5_wgt_genotypes_selection_t4.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_node_scale(misc.all_mtg, vids=vids)
            tmp=df2waffle(df, index='rank', date=p5_wgt_date_selection.v_model, variable=data, order=p5_wgt_order_selection.v_model)
            
            # TODO: remove the legend here (which only apply to branching_type)
            l_names = {"1":"Stolon", 
               "2":"Vegetative bud",
               "3":"Initiated bud",
               "4":"Aborted bud",
               "5":"Floral bud",
               "6":"Branch crown"}

            fig=plot_waffle(tmp, 
#                             layout=layout,
                            legend_name=l_names,
                            plot_func=p5_wgt_plot_type.v_model)
            display(fig)

def on_change_node_plot_type(widget, event, data):
    if not p5_wgt_date_selection.v_model:
        pass
    elif not p5_wgt_parameter_selection.v_model:
        pass
    else:
        with p5_waffle:
            p5_waffle.clear_output()
            genotype=p5_wgt_genotypes_selection_t4.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_node_scale(misc.all_mtg, vids=vids)
            tmp=df2waffle(df, index='rank', date=p5_wgt_date_selection.v_model, variable=p5_wgt_parameter_selection.v_model, order=p5_wgt_order_selection.v_model)
            
            # TODO: remove the legend here (which only apply to branching_type)
            l_names = {"1":"Stolon", 
               "2":"Vegetative bud",
               "3":"Initiated bud",
               "4":"Aborted bud",
               "5":"Floral bud",
               "6":"Branch crown"}

            fig=plot_waffle(tmp, 
#                             layout=layout,
                            legend_name=l_names,
                            plot_func=data)
            display(fig)
            
            
def on_change_node_order(widget, event, data):
    if not p5_wgt_date_selection.v_model or not p5_wgt_parameter_selection.v_model:
        pass
    else:
        with p5_waffle:
            p5_waffle.clear_output()
            genotype=p5_wgt_genotypes_selection_t4.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_node_scale(misc.all_mtg, vids=vids)
            tmp=df2waffle(df, index='rank', date=p5_wgt_date_selection.v_model, variable=p5_wgt_parameter_selection.v_model, order=data)
            
            # TODO: remove the legend here (which only apply to branching_type)
            l_names = {"1":"Stolon", 
               "2":"Vegetative bud",
               "3":"Initiated bud",
               "4":"Aborted bud",
               "5":"Floral bud",
               "6":"Branch crown"}

            fig=plot_waffle(tmp, 
#                             layout=layout,
                            legend_name=l_names,
                            plot_func=p5_wgt_plot_type.v_model)
            display(fig)

# # ----------------------------------------------------------------
# # Widgets
# # ----------------------------------------------------------------

p5_wgt_genotypes_selection_t4 = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Genotype",
            truncate_length=22)

p5_wgt_date_selection = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Date",
            truncate_length=22)

p5_wgt_parameter_selection = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Parameter",
            truncate_length=22)

p5_wgt_plot_type = v.Select(items=["matplotlib", 'plotly.imshow', 'plotly.heatmap'],
            chips=True, 
            multiple=False,
            v_model="matplotlib",
            label="Select a plot library",
            truncate_length=22)

p5_wgt_order_selection = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model=None,
            label="Select Order",
            truncate_length=22)

p5_select_waffle = v.Row(children=[p5_wgt_genotypes_selection_t4,
                                   p5_wgt_date_selection,
                                   p5_wgt_parameter_selection,
                                   p5_wgt_order_selection,
                                   p5_wgt_plot_type])

p5_waffle = widgets.Output(layout=layout_output_wgt)

p5_tab4 = v.Row(children=[v.Col(
                            children=[
                                p5_select_waffle,
                                p5_waffle,
                              ]),
                        ])

p5 = v.Tabs( 
            children=[
            v.Tab(children=['Waffle']),
            v.TabItem(children=[
                p5_tab4
            ]),
        ])


p5_container_main = v.Container(fluid=True, 
                                   class_='grid-list-md box',
                                   children=[
                                       p5
                                   ])

# # ----------------------------------------------------------------
# # Link widgets - event
# # ----------------------------------------------------------------

p5_wgt_genotypes_selection_t4.on_event('change', on_change_node_waffle_genotype)
p5_wgt_date_selection.on_event('change', on_change_node_waffle_date)
p5_wgt_parameter_selection.on_event('change', on_change_node_waffle_parameter)
p5_wgt_plot_type.on_event('change', on_change_node_plot_type)
p5_wgt_order_selection.on_event('change', on_change_node_order)






