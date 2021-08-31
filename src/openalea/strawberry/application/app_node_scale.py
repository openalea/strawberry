import ipyvuetify as v
import ipywidgets as widgets

import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

from openalea.strawberry.analysis import (extract_at_node_scale, df2waffle, plot_waffle)

import openalea.strawberry.application.misc as misc
from openalea.strawberry.application.misc import (get_vid_of_genotype)
from openalea.strawberry.application.layout import layout_output_wgt, layout_card
import openalea.strawberry.application.info as info


# # ----------------------------------------------------------------
# # Print on widget function
# # ----------------------------------------------------------------


# # ----------------------------------------------------------------
# # On event trigger
# # ----------------------------------------------------------------

def on_change_node_waffle_genotype(widget, event, data):
    genotype=genotypes_selection_waffle.v_model
    vids=get_vid_of_genotype(misc.all_mtg, [genotype])
    df=extract_at_node_scale(misc.all_mtg, vids=vids)
    param = list(df.columns)
    param.remove("Genotype")
    param.remove('date')
    date_selection_waffle.items=list(df.date.unique())
    date_selection_waffle.v_model=""
    variable_selection_waffle.items=param
    order = list(df.order.unique())
    order.append({'text':'All', 'value': None})
    order_selection_waffle.items=order
    
def on_change_node_waffle_date(widget, event, data):
    if not variable_selection_waffle.v_model:
        pass
    else:
        with waffle:
            waffle.clear_output()
            genotype=genotypes_selection_waffle.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_node_scale(misc.all_mtg, vids=vids)
            tmp=df2waffle(df, index='rank', date=data, variable=variable_selection_waffle.v_model, order=order_selection_waffle.v_model)

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
                            plot_func=plot_type_waffle.v_model)
            
            display(fig)
            
    
def on_change_node_waffle_parameter(widget, event, data):
    if not date_selection_waffle.v_model:
        pass
    else:
        with waffle:
            waffle.clear_output()
            genotype=genotypes_selection_waffle.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_node_scale(misc.all_mtg, vids=vids)
            tmp=df2waffle(df, index='rank', date=date_selection_waffle.v_model, variable=data, order=order_selection_waffle.v_model)
            
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
                            plot_func=plot_type_waffle.v_model)
            display(fig)

def on_change_node_plot_type(widget, event, data):
    if not date_selection_waffle.v_model:
        pass
    elif not variable_selection_waffle.v_model:
        pass
    else:
        with waffle:
            waffle.clear_output()
            genotype=genotypes_selection_waffle.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_node_scale(misc.all_mtg, vids=vids)
            tmp=df2waffle(df, index='rank', date=date_selection_waffle.v_model, variable=variable_selection_waffle.v_model, order=order_selection_waffle.v_model)
            
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
    if not date_selection_waffle.v_model or not variable_selection_waffle.v_model:
        pass
    else:
        with waffle:
            waffle.clear_output()
            genotype=genotypes_selection_waffle.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_node_scale(misc.all_mtg, vids=vids)
            tmp=df2waffle(df, index='rank', date=date_selection_waffle.v_model, variable=variable_selection_waffle.v_model, order=data)
            
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
                            plot_func=plot_type_waffle.v_model)
            display(fig)

# # ----------------------------------------------------------------
# # Widgets
# # ----------------------------------------------------------------

genotypes_selection_waffle = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Genotype",
            truncate_length=22)

date_selection_waffle = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Date",
            truncate_length=22)

variable_selection_waffle = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Variable",
            truncate_length=22)

plot_type_waffle = v.Select(items=["matplotlib", 'plotly.imshow', 'plotly.heatmap'],
            chips=True, 
            multiple=False,
            v_model="matplotlib",
            label="Select a plot library",
            truncate_length=22)

order_selection_waffle = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model=None,
            label="Select Order",
            truncate_length=22)

menu_plant_waffle = v.Row(children=[genotypes_selection_waffle,
                                   date_selection_waffle,
                                   variable_selection_waffle,
                                   order_selection_waffle,
                                   plot_type_waffle])

waffle = widgets.Output(layout=layout_output_wgt)

tab_waffle_content = v.Row(children=[
                                v.Card(style_=layout_card, children=[info.p5_doc_waffle]),
                                v.Col(col=12, sm=12, md=12,children=[
                                        menu_plant_waffle,
                                        waffle,
                                    ]),
                            ])

p5 = v.Tabs( 
            children=[
            v.Tab(children=['Waffle']),
            v.TabItem(children=[
                tab_waffle_content
            ]),
        ])


container_main = v.Container(fluid=True, 
                                   class_='grid-list-md box',
                                   children=[
                                       p5
                                   ])

# # ----------------------------------------------------------------
# # Link widgets - event
# # ----------------------------------------------------------------

genotypes_selection_waffle.on_event('change', on_change_node_waffle_genotype)
date_selection_waffle.on_event('change', on_change_node_waffle_date)
variable_selection_waffle.on_event('change', on_change_node_waffle_parameter)
plot_type_waffle.on_event('change', on_change_node_plot_type)
order_selection_waffle.on_event('change', on_change_node_order)






