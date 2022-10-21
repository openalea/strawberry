import ipyvuetify as v
import ipywidgets as widgets
from matplotlib.pyplot import plot
import plotly.graph_objs as go
import pandas as pd
import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

from openalea.strawberry.analysis import (extract_at_node_scale, df2waffle, plot_waffle)
import openalea.strawberry.application.misc as misc
from openalea.strawberry.application.misc import (get_vid_of_genotype, transfert_figure,update_btn_export, create_grid, update_grid)
from openalea.strawberry.application.layout import layout_output_wgt, layout_card,layout_gofigure
import openalea.strawberry.application.info as info


# # ----------------------------------------------------------------
# # Print on widget function
# # ----------------------------------------------------------------

def update_btn_extract():
    genotype=genotypes_selection_extraction.v_model
    if genotype:
        vids=get_vid_of_genotype(misc.all_mtg, genotype)
        df=extract_at_node_scale(misc.all_mtg, vids=vids)
        df["branching_type"]=df["branching_type"].replace(["1","2","3","4","5","6",'7'], ["stolon","vegetative bud", "initiated bud", "aborted/dried bud", "floral bud", "branch crown",'Inflorescence'])
        update_btn_export(export_extraction, df)

def update_btn_single():
    genotype=genotypes_selection_single_genotype.v_model
    if genotype:
        vids=get_vid_of_genotype(misc.all_mtg, [genotype])
        df=extract_at_node_scale(misc.all_mtg, vids=vids)
        pad = prob_axillary_production(df,order=None,frequency=True)
    update_btn_export(link_export_t21,pad)
    if genotype:
        vids=get_vid_of_genotype(misc.all_mtg, [genotype])
        df=extract_at_node_scale(misc.all_mtg, vids=vids)
        pad = prob_axillary_production(df,order=None,frequency=False)
    update_btn_export(link_export_t22,pad)

def prob_axillary_production(df, order=None, frequency=True):
    if order is not None:
        df=df[df["order"]==order]
        
    # Value conversion
    df["branching_type"]= df["branching_type"].replace(["1","2","3","4","5","6","7"],["S","VB","IB","AB","FB","BC","Inflorescence"])

    # pandas crosstab data
    if frequency==True:  
        data= pd.crosstab(df["rank"],df["branching_type"])
    else:
        data=pd.crosstab(df["rank"],df["branching_type"],normalize="index")
        print(data)
    return data

def axillary_production_plotly(data, order,frequency, layout={}):
    kind = layout.get('kind', "line")
    mode = layout.get('mode', 'lines+markers')
    xlabel = layout.get('xlabel', "Node rank")
    if frequency==True:
        ylabel = layout.get('ylabel', "Frequency")
        title = layout.get('title', "Frequency of axillary production")   
    else:
        ylabel = layout.get('ylabel', "Relative frequency")
        title = layout.get('title','Relative frequency of axillary production')
    
    res = prob_axillary_production(data, order, frequency)
    
    p=res.iplot(kind =kind, 
                mode=mode, 
                xTitle=xlabel,
                yTitle=ylabel,
                title=title,
                asFigure=True)
    p.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    
    return p
    


def print_single_genotype_plots():
    if misc.all_mtg.property('Genotype'):
        df=extract_at_node_scale(misc.all_mtg)
        # plot axillary production distri frequency
        fig= axillary_production_plotly(data=df,order=0,frequency=True)
        transfert_figure(fig, plot_axillary_production_frequency)
        #plot axillary production distri relative frequency
        fig= axillary_production_plotly(data=df,order=0,frequency=False)
        transfert_figure(fig, plot_axillary_production_relative_frequency)
        
# # ----------------------------------------------------------------
# # On event trigger
# # ----------------------------------------------------------------

def on_change_genotype_p5(widget, event, data):
    #update table
    df= pd.DataFrame()
    if misc.all_mtg:
        vids= get_vid_of_genotype(misc.all_mtg, genotypes=data)
        df = extract_at_node_scale(misc.all_mtg,vids=vids)
        df["branching_type"]=df["branching_type"].replace(["1","2","3","4","5","6","7"], ["stolon","vegetative bud", "initiated bud", "aborted/dried bud", "floral bud", "branch crown","Inflorescence"])
        update_grid(df,df_nodescale)
        update_btn_extract()

def on_change_single_genotype(widget, event, data):
    print_single_genotype_plots()
    update_btn_single()

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
               "6":"Branch crown",
                "7":"Inflorescence"}

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
               "6":"Branch crown",
                "7":"Inflorescence"}

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
               "6":"Branch crown",
                "7": "Inflorescence"}

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
               "6":"Branch crown",
               "7":"Inflorescence"}

            fig=plot_waffle(tmp, 
#                             layout=layout,
                            legend_name=l_names,
                            plot_func=plot_type_waffle.v_model)
            display(fig)

# # ----------------------------------------------------------------
# # Widgets
# # ----------------------------------------------------------------
export_extraction = widgets.Output(layout=layout_output_wgt)

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

df_nodescale = create_grid()

panel_df = v.Container(
                    fluid=True,
                    children=[
                        df_nodescale    
                ])

tab_extraction_content = v.Row(children=[
                            v.Card(style_=layout_card, children=[info.p5_doc_extraction]),
                            v.Col(cols=12, sm=12, md=12,children=[
                                            menu_plant_extraction,
                                            panel_df,
                                        ]),
                          ])

genotypes_selection_single_genotype = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Genotype",
            truncate_length=22)


# plot
plot_axillary_production_frequency= go.FigureWidget(layout=layout_gofigure)
plot_axillary_production_relative_frequency= go.FigureWidget(layout=layout_gofigure)

#link button export
link_export_t21 = widgets.Output(layout=layout_output_wgt)
link_export_t22 = widgets.Output(layout=layout_output_wgt)

#panel
panel_single_genotype= v.Container(fluid=True,
                                   children=[
                                       plot_axillary_production_frequency,
                                       v.Row(col=12,sm=12,md=12,
                                            children= [v.Row(children=[link_export_t21])]),
                                       plot_axillary_production_relative_frequency,
                                       v.Row(col=12,sm=12,md=12,
                                             children= [v.Row(children=[link_export_t22])]),
                                   ])

#tab
tab_single_genotype_content = v.Row(children=[v.Card(style_=layout_card, children=[info.p5_doc_single_genotype]),
                                            v.Col(col=12, sm=12, md=12, children=[
                                                genotypes_selection_single_genotype,
                                                panel_single_genotype
                                            ])
                          ])

##########
# Waffle tab
##########
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

# p5 = v.Tabs( 
#             children=[
#             v.Tab(children=['Waffle']),
#             v.TabItem(children=[
#                 tab_waffle_content
#             ]),
#         ])


# container_main = v.Container(fluid=True, 
#                                    class_='grid-list-md box',
#                                    children=[
#                                        p5
#                                    ])

container_main = v.Container(fluid=True, 
                                   class_='grid-list-md box',
                                   children=[
                                       v.Tabs(children=[
                                           v.Tab(children=['Data extraction']),
                                           v.TabItem(children=[tab_extraction_content]),
                                           v.Tab(children=['Single genotype']),
                                           v.TabItem(children=[tab_single_genotype_content]),
                                           v.Tab(children=['Waffle']),
                                           v.TabItem(children=[tab_waffle_content])
                                       ])
                                   ])
# # ----------------------------------------------------------------
# # Link widgets - event
# # ----------------------------------------------------------------

genotypes_selection_extraction.on_event('change', on_change_genotype_p5)
genotypes_selection_single_genotype.on_event("change", on_change_single_genotype)

genotypes_selection_waffle.on_event('change', on_change_node_waffle_genotype)
date_selection_waffle.on_event('change', on_change_node_waffle_date)
variable_selection_waffle.on_event('change', on_change_node_waffle_parameter)
plot_type_waffle.on_event('change', on_change_node_plot_type)
order_selection_waffle.on_event('change', on_change_node_order)






