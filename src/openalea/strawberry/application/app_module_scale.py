import ipyvuetify as v
import ipywidgets as widgets

import pandas as pd
import plotly.graph_objs as go

import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

from openalea.strawberry.analysis import (extract_at_module_scale, occurence_module_order_along_time, df2waffle, plot_waffle)

import openalea.strawberry.application.misc as misc
from openalea.strawberry.application.misc import (get_vid_of_genotype, transfert_figure, create_download_link, create_grid, update_grid, update_btn_export)
from openalea.strawberry.application.layout import layout_output_wgt, layout_gofigure
import openalea.strawberry.application.info


# # ----------------------------------------------------------------
# # Print on widget function
# # ----------------------------------------------------------------

def update_btn_extract():
    genotype=genotypes_selection_extraction.v_model
    if genotype:
        vids=get_vid_of_genotype(misc.all_mtg, genotype)
        df=extract_at_module_scale(misc.all_mtg, vids=vids)
        update_btn_export(export_extraction, df)


def update_btn_single():
    genotype=genotypes_selection_single_genotype.v_model
    if genotype:
        vids=get_vid_of_genotype(misc.all_mtg, [genotype])
        df=extract_at_module_scale(misc.all_mtg, vids=vids)
        geno_frequency = occurence_module_order_along_time(data= df,frequency_type= "cdf")
    update_btn_export(link_export_t11,geno_frequency)

    if genotype:
        vids=get_vid_of_genotype(misc.all_mtg, [genotype])
        df=extract_at_module_scale(misc.all_mtg, vids=vids)
        res=pd.crosstab(index= df["order"], columns= df["complete_module"],normalize="index")
        res.columns = ["incomplete","complete"]
    update_btn_export(link_export_t12,res)

    if genotype:
        vids=get_vid_of_genotype(misc.all_mtg, [genotype])
        df=extract_at_module_scale(misc.all_mtg, vids=vids)
        res=pd.crosstab(index=df["date"], columns= df["complete_module"],normalize="index")
        res.columns = ["incomplete","complete"]    
    update_btn_export(link_export_t13,res)


def update_btn_multiple():
    if misc.all_mtg:
        df=extract_at_module_scale(misc.all_mtg)
        Mean= df.groupby(["Genotype", "order"]).mean()
    update_btn_export(link_export_t21,Mean)

    if misc.all_mtg:
        df=extract_at_module_scale(misc.all_mtg)
        Mean= df.groupby(["Genotype", "order"]).mean()
    update_btn_export(link_export_t22,Mean)

    if misc.all_mtg:
        df=extract_at_module_scale(misc.all_mtg)
        Mean= df.groupby(["Genotype", "order"]).mean()
    update_btn_export(link_export_t23,Mean)

    if misc.all_mtg:
        df=extract_at_module_scale(misc.all_mtg)
        ctd = crowntype_distribution(data= df, crown_type="branch_crown")
        ctd = ctd[ctd.index.get_level_values('order')!=0]
    update_btn_export(link_export_t24,ctd)

    if misc.all_mtg:
        df=extract_at_module_scale(misc.all_mtg)
        ctd = crowntype_distribution(data= df, crown_type="extension_crown")
        ctd = ctd[ctd.index.get_level_values('order')!=0]  
    update_btn_export(link_export_t25,ctd)        


def plot_module_occurence_module_order_along_time(df, genotype, layout={}):
    kind = layout.get('kind', "line")
    mode = layout.get('mode', 'lines+markers')
    xlabel = layout.get('xlabel', "Order")
    ylabel = layout.get('ylabel', "cdf")
    title = layout.get('title', "Occurence of successive module order for {}".format(genotype))   
    
    geno_frequency = occurence_module_order_along_time(data= df,frequency_type= "cdf")
    p=geno_frequency.iplot(kind = kind, 
                          mode=mode, 
                          xTitle=xlabel,
                          yTitle=ylabel,
                          title=title,
                          asFigure=True
                         )
    return p 

def plot_module_distribution_complete_incomplete_module_order(df, genotype, layout={}):
    kind = layout.get('kind', "line")
    mode = layout.get('mode', 'lines+markers')
    xlabel = layout.get('xlabel', "Order")
    ylabel = layout.get('ylabel', "Probability")
    title = layout.get('title', "Relative distrivution of complete (True) and incomplete (False) module as function of module order for {}".format(genotype))   
   
    res=pd.crosstab(index= df["order"], columns= df["complete_module"],normalize="index")
    res.columns = ["incomplete","complete"]
    
    p=res.iplot(kind =kind, 
                  mode=mode, 
                  xTitle=xlabel,
                  yTitle=ylabel,
                  title=title,
              asFigure=True
                     )
    return p 

def plot_module_distribution_complete_incomplete_date(df, genotype, layout={}):
    kind = layout.get('kind', "line")
    mode = layout.get('mode', 'lines+markers')
    xlabel = layout.get('xlabel', "Dates")
    ylabel = layout.get('ylabel', "Probability")
    title = layout.get('title', "Relative distribution of complete (True) and incomplete (False) module as function of date for {}".format(genotype))   
   
    res=pd.crosstab(index=df["date"], columns= df["complete_module"],normalize="index")
    res.columns = ["incomplete","complete"]    

    p=res.iplot(kind =kind, 
                  mode=mode, 
                  xTitle=xlabel,
                  yTitle=ylabel,
                  title=title,
              asFigure=True
                 )
    return p 


def print_single_genotype_plots():
    genotype=genotypes_selection_single_genotype.v_model
    vids=get_vid_of_genotype(misc.all_mtg, [genotype])
    df=extract_at_module_scale(misc.all_mtg, vids=vids)
    if genotype:
        # plot occurence module order
        fig = plot_module_occurence_module_order_along_time(df, genotype)
        transfert_figure(fig, plot_occurence)
        # plot occurence module order
        fig = plot_module_distribution_complete_incomplete_module_order(df, genotype)
        transfert_figure(fig, plot_distribution_module_order)
        # plot occurence module order
        fig = plot_module_distribution_complete_incomplete_date(df, genotype)
        transfert_figure(fig, plot_distribution_date)
    else:
        with plot_occurence:
            plot_occurence.clear_output()
            print('Select a Genotype')

def crowntype_distribution(data, crown_type,):
    """
    parameters:
    -----------
    data: panda dataframe issue from extraction of data at module scale
    variable: type of branch crown (extension_crown or branch_crown)

    return:
    -------
    a dataframe containing relative frequency values by genotype and order for extension and branch crown
    and a relative frequency distribution plot

    """
    df= pd.crosstab(index= [data.Genotype, data.order],
                    columns= data.type_of_crown,
                    normalize="index")   
    df.columns=["Main", "extension_crown", "branch_crown"]

    return df


def crowntype_plotly(data, crown_type, layout={}):
    xlabel = layout.get('xlabel', "Order")
    ylabel = layout.get('ylabel', "Relative frequency")
    title = layout.get('title',"Relative frequency of {}".format(crown_type))   
   
    fig=go.Figure()
    for genotype in list(data.unstack(level=0)[crown_type].columns):
        fig.add_trace(go.Scatter(
                x=list(data.unstack(level=0).index),
                y=list(data.unstack(level=0)[crown_type][genotype]),
                name=genotype,
                ))

    fig.update_layout(yaxis_title=ylabel,
                      xaxis_title=xlabel,
                      title=title,
                      )
    return go.FigureWidget(fig)

                       
def pointwisemean_plotly(data_mean, data_sd, variable, layout={}):
    xlabel = layout.get('xlabel', "Order")
    ylabel = layout.get('ylabel', "Mean {}".format(variable))
    title = layout.get('title', "Pointwisemean of {}".format(variable))   
   
    fig=go.Figure()
    for genotype in list(data_mean.unstack(level=0)[variable].columns):
        sd_error = list(data_sd.unstack(level=0)[variable][genotype])
        fig.add_trace(go.Scatter(
                x=list(data_mean.unstack(level=0).index),
                y=data_mean.unstack(level=0)[variable][genotype],
                name=genotype,
                mode='lines',
                error_y=dict(type='data', 
                             array=sd_error, 
                             thickness=1,
                             visible=True)
                     ))

    fig.update_layout(yaxis_title=ylabel,
                      xaxis_title=xlabel,
                      title=title,
                      )
    return go.FigureWidget(fig)



def plot_module_pointwisemean(df, var, layout={}):
    Mean= df.groupby(["Genotype", "order"]).mean()
    sd= df.groupby(["Genotype", "order"]).std()
#     variable = "nb_total_{}".format(var)
    fig = pointwisemean_plotly(data_mean=Mean,
                   data_sd=sd,
                   variable=var,
                   layout=layout)

    return fig

def plot_module_crown(df, var, layout={}):
    ctd = crowntype_distribution(data= df, crown_type=var)
    ctd = ctd[ctd.index.get_level_values('order')!=0]
    fig= crowntype_plotly(data=ctd,
                 crown_type=var, 
                 layout=layout)
    return fig


def print_multiple_genotypes_plots():
    if misc.all_mtg.property('Genotype'):
        df=extract_at_module_scale(misc.all_mtg)
        # plot pointwisemean leaves
        fig = plot_module_pointwisemean(df, "nb_total_leaves")
        transfert_figure(fig, plot_pointwisemean_leaves)
        # plot pointwisemean flowers
        fig = plot_module_pointwisemean(df, "nb_total_flowers")
        transfert_figure(fig, plot_pointwisemean_flowers)
        # plot pointwisemean stolons
        fig = plot_module_pointwisemean(df, "nb_stolons")
        transfert_figure(fig, plot_pointwisemean_stolons)
        # crowntype branch
        fig = plot_module_crown(df, "branch_crown")
        transfert_figure(fig, plot_branch_crown)
        # crowntype extension
        fig = plot_module_crown(df, "extension_crown")
        transfert_figure(fig, plot_extension_crown)
        


# # ----------------------------------------------------------------
# # On event trigger
# # ----------------------------------------------------------------

def on_change_genotype_p4(widget, event, data):
    # update table
    df=pd.DataFrame()
    if misc.all_mtg:
        vids=get_vid_of_genotype(misc.all_mtg, genotypes=data)
        df = extract_at_module_scale(misc.all_mtg, vids=vids)
    update_grid(df, df_modulescale)
    
    # update descriptors
    update_grid(df.describe(), df_description)

    # update the extraction button
    update_btn_extract()


def on_change_single_genotype(widget, event, data):
    print_single_genotype_plots()
    update_btn_single()

def on_change_module_waffle_genotype(widget, event, data):
    genotype=genotypes_selection_waffle.v_model
    vids=get_vid_of_genotype(misc.all_mtg, [genotype])
    df=extract_at_module_scale(misc.all_mtg, vids=vids)
    param = list(df.columns)
    param.remove("Genotype")
    param.remove('date')
    param.remove('order')
    param.remove('plant')
    date_selection_waffle.items=list(df.date.unique())
    date_selection_waffle.v_model=""
    parameter_selection_waffle.items=param
    
def on_change_module_waffle_date(widget, event, data):
    if not parameter_selection_waffle.v_model:
        pass
    else:
        with waffle:
            waffle.clear_output()
            genotype=genotypes_selection_waffle.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_module_scale(misc.all_mtg, vids=vids)

            if aggfunc_selection_waffle.v_model == 'concat_string':
                tmp=df2waffle(df, index='order', 
                          date=data, 
                          variable=parameter_selection_waffle.v_model, 
                          aggfunc=lambda x: ' '.join(x),
                          crosstab=False)
            else:
                tmp=df2waffle(df, index='order', 
                          date=data, 
                          variable=parameter_selection_waffle.v_model, 
                          aggfunc=aggfunc_selection_waffle.v_model,
                          crosstab=False)

            fig = plot_waffle(tmp,
#                               layout=layout,
                              plot_func=plot_type_waffle.v_model)
            display(fig)


    
def on_change_module_waffle_parameter(widget, event, data):
    if not date_selection_waffle.v_model:
        pass
    else:
        with waffle:
            waffle.clear_output()
            genotype=genotypes_selection_waffle.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_module_scale(misc.all_mtg, vids=vids)

            if aggfunc_selection_waffle.v_model == 'concat_string':
                tmp=df2waffle(df, index='order', 
                          date=date_selection_waffle.v_model, 
                          variable=data, 
                          aggfunc=lambda x: ' '.join(x),
                          crosstab=False)
            else:
                tmp=df2waffle(df, index='order', 
                          date=date_selection_waffle.v_model, 
                          variable=data, 
                          aggfunc=aggfunc_selection_waffle.v_model,
                          crosstab=False)


            fig = plot_waffle(tmp,
#                               layout=layout,
                              plot_func=plot_type_waffle.v_model)
            display(fig)

            
def on_change_module_aggfunc(widget, event, data):
    if date_selection_waffle.v_model and parameter_selection_waffle.v_model:
        with waffle:
            waffle.clear_output()
            genotype=genotypes_selection_waffle.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_module_scale(misc.all_mtg, vids=vids)

            
            if aggfunc_selection_waffle.v_model == 'concat_string':
                tmp=df2waffle(df, index='order', 
                          date=date_selection_waffle.v_model, 
                          variable=parameter_selection_waffle.v_model, 
                          aggfunc=lambda x: ' '.join(x),
                          crosstab=False)
            else:
                tmp=df2waffle(df, index='order', 
                          date=date_selection_waffle.v_model, 
                          variable=parameter_selection_waffle.v_model, 
                          aggfunc=data,
                          crosstab=False)

            fig = plot_waffle(tmp,
#                               layout=layout,
                              plot_func=plot_type_waffle.v_model)
            display(fig)

            
# def on_change_module_crosstab(widget, event, data):
#     if date_selection_waffle.v_model and parameter_selection_waffle.v_model:
#         with waffle:
#             waffle.clear_output()
#             genotype=genotypes_selection_waffle.v_model
#             vids=get_vid_of_genotype(misc.all_mtg, [genotype])
#             df=extract_at_module_scale(misc.all_mtg, vids=vids)

#             tmp=df2waffle(df, index='order', 
#                           date=date_selection_waffle.v_model, 
#                           variable=parameter_selection_waffle.v_model, 
#                           aggfunc=aggfunc_selection_waffle.v_model,
#                           crosstab=data)
            
#             yticks_l =list(range(0,len(tmp.index)))
#             yticks_l.reverse()

#             layout={
#                 'xlabel': 'Plant',
#                 'xticks': range(0,len(tmp.columns)),
#                 'xticks_label': tmp.columns,
#                 'ylabel': 'Module',
#                 'yticks': range(0,len(tmp.index)),
#                 'yticks_label': yticks_l,
#             }



#                 fig = plot_waffle(tmp,
#                                   layout=layout,
#                                   plot_func=plot_type_waffle.v_model)
#             display(fig)

            
            
def on_change_module_plot_type(widget, event, data):
    if date_selection_waffle.v_model and parameter_selection_waffle.v_model:
        with waffle:
            waffle.clear_output()
            genotype=genotypes_selection_waffle.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_module_scale(misc.all_mtg, vids=vids)

            if aggfunc_selection_waffle.v_model == 'concat_string':
                tmp=df2waffle(df, index='order', 
                          date=date_selection_waffle.v_model, 
                          variable=parameter_selection_waffle.v_model, 
                          aggfunc=lambda x: ' '.join(x),
                          crosstab=False
                         )
            else:
                tmp=df2waffle(df, index='order', 
                          date=date_selection_waffle.v_model, 
                          variable=parameter_selection_waffle.v_model, 
                          aggfunc=aggfunc_selection_waffle.v_model,
                          crosstab=False
                         )

            fig = plot_waffle(tmp,
#                               layout=layout,
                              plot_func=data)

            display(fig)


def on_click_changetab(widget, event, data):
    print_multiple_genotypes_plots()
    update_btn_multiple()


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

df_modulescale = create_grid()

panel_df = v.Container(
                    fluid=True,
                    children=[
                        df_modulescale    
                ])

df_description = create_grid()

panel_description =v.Container(fluid=True,
                              children=[
                                    df_description    
                                ])

tab_extraction_content = v.Row(children=[menu_plant_extraction,
                          v.Col(cols=12, sm=7, md=9,children=[panel_df,
                                            panel_description,
                                        ]),
                          ])

genotypes_selection_single_genotype = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Genotype",
            truncate_length=22)

plot_occurence = go.FigureWidget(layout=layout_gofigure)
plot_distribution_module_order = go.FigureWidget(layout=layout_gofigure)
plot_distribution_date = go.FigureWidget(layout=layout_gofigure)

link_export_t11 = widgets.Output(layout=layout_output_wgt)
link_export_t12 = widgets.Output(layout=layout_output_wgt)
link_export_t13 = widgets.Output(layout=layout_output_wgt)


panel_single_genotype = v.Container(fluid=True,
                              children=[
                                    plot_occurence,
                                    v.Row(children=[link_export_t11]),
                                    plot_distribution_module_order,
                                    v.Row(children=[link_export_t12]),
                                    plot_distribution_date,
                                    v.Row(children=[link_export_t13]),
                                ])

tab_single_genotype_content = v.Row(children=[v.Col(col=12, sm=11, md=11, children=[
                                                        genotypes_selection_single_genotype,
                                                        panel_single_genotype
                                                    ])
                          ])


plot_pointwisemean_leaves = go.FigureWidget(layout=layout_gofigure)
plot_pointwisemean_flowers = go.FigureWidget(layout=layout_gofigure)
plot_pointwisemean_stolons = go.FigureWidget(layout=layout_gofigure)
plot_branch_crown = go.FigureWidget(layout=layout_gofigure)
plot_extension_crown = go.FigureWidget(layout=layout_gofigure)


link_export_t21 = widgets.Output(layout=layout_output_wgt)
link_export_t22 = widgets.Output(layout=layout_output_wgt)
link_export_t23 = widgets.Output(layout=layout_output_wgt)
link_export_t24 = widgets.Output(layout=layout_output_wgt)
link_export_t25 = widgets.Output(layout=layout_output_wgt)


panel_multiple_genotypes = v.Container(fluid=True,
                              children=[
                                    plot_pointwisemean_leaves,
                                    v.Row(children=[link_export_t21]),
                                    plot_pointwisemean_flowers,
                                    v.Row(children=[link_export_t22]),
                                    plot_pointwisemean_stolons,
                                    v.Row(children=[link_export_t23]),
                                    plot_branch_crown,
                                    v.Row(children=[link_export_t24]),
                                    plot_extension_crown,
                                    v.Row(children=[link_export_t25]),
                                ])

tab_multiple_genotype_content = v.Row(children=[v.Col(col=12, sm=11, md=11, children=[panel_multiple_genotypes])])

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

parameter_selection_waffle = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Parameter",
            truncate_length=22)
    
aggfunc_selection_waffle = v.Select(items=[{'text': 'Mean', 'value': 'mean'}, 
                                           {'text': 'Median', 'value': 'median'}, 
                                           {'text': 'Concatenate string', 'value': 'concat_string'}],
                                    chips=True, 
                                    multiple=False,
                                    v_model='mean',
                                    label="Select a function",
                                    truncate_length=22)

# p4_wgt_crosstab = v.Select(items=[True, False],
#             chips=True, 
#             multiple=False,
#             v_model=False,
#             label="Crosstab",
#             truncate_length=22)

plot_type_waffle = v.Select(items=["matplotlib", 'plotly.imshow', 'plotly.heatmap'],
            chips=True, 
            multiple=False,
            v_model="matplotlib",
            label="Select a plot library",
            truncate_length=22)


menu_plant_waffle = v.Row(children=[genotypes_selection_waffle,
                                   date_selection_waffle,
                                   parameter_selection_waffle,
                                   aggfunc_selection_waffle,
#                                    p4_wgt_crosstab,
                                   plot_type_waffle])

waffle = widgets.Output(layout=layout_output_wgt)


tab_waffle_content = v.Row(children=[v.Col(children=[
                                menu_plant_waffle,
                                waffle,
                              ]),
                        ])

tab_3 = v.Tab(children=['Multiple genotypes'])

container_main = v.Container(fluid=True, 
                                   class_='grid-list-md box',
                                   children=[
                                       v.Tabs( children=[
                                            v.Tab(children=['Data extraction']),
                                            v.Tab(children=['Single genotype']),
                                            tab_3,
                                            v.Tab(children=['Waffle']),
                                            v.TabItem(children=[
                                                tab_extraction_content
                                            ]),
                                            v.TabItem(children=[
                                                tab_single_genotype_content
                                            ]),
                                            v.TabItem(children=[
                                                tab_multiple_genotype_content
                                            ]),
                                            v.TabItem(children=[
                                                tab_waffle_content
                                            ]),  
                                        ])
                                   ])

# # ----------------------------------------------------------------
# # Link widgets - event
# # ----------------------------------------------------------------

genotypes_selection_extraction.on_event('change', on_change_genotype_p4)
genotypes_selection_single_genotype.on_event("change", on_change_single_genotype)

genotypes_selection_waffle.on_event('change', on_change_module_waffle_genotype)
date_selection_waffle.on_event('change', on_change_module_waffle_date)
parameter_selection_waffle.on_event('change', on_change_module_waffle_parameter)
aggfunc_selection_waffle.on_event('change', on_change_module_aggfunc)
# p4_wgt_crosstab.on_event('change', on_change_module_crosstab)
plot_type_waffle.on_event('change', on_change_module_plot_type)

tab_3.on_event("change", on_click_changetab)

