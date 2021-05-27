import ipyvuetify as v
import ipywidgets as widgets

import pandas as pd
import qgrid
import plotly.graph_objs as go

import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

from openalea.strawberry.analysis import (extract_at_module_scale, occurence_module_order_along_time, df2waffle, plot_waffle)

import openalea.strawberry.application.misc as misc
from openalea.strawberry.application.misc import (get_vid_of_genotype, transfert_figure, transfert_figure_pie, create_download_link)
from openalea.strawberry.application.layout import layout_output_wgt, layout_gofigure



# # ----------------------------------------------------------------
# # Print on widget function
# # ----------------------------------------------------------------

def plot_module_occurence_module_order_along_time(df, genotype):
    geno_frequency = occurence_module_order_along_time(data= df,frequency_type= "cdf")
    p=geno_frequency.iplot(kind = "line", 
                          mode='lines+markers', 
                          xTitle="order",
                          yTitle="cdf",
                          title="Occurence of successive module order for {}".format(genotype),
                          asFigure=True
                         )
    return p 

def plot_module_distribution_complete_incomplete_module_order(df, genotype):
    res=pd.crosstab(index= df["order"], columns= df["complete_module"],normalize="index")
    res.columns = ["incomplete","complete"]
    
    p=res.iplot(kind = "line", 
                      mode='lines+markers', 
                      xTitle="Order",
                      yTitle="Probability",
                      title="Relative distrivution of complete (True) and incomplete (False) module as function of module order for {}".format(genotype),
                      asFigure=True
                     )
    return p 

def plot_module_distribution_complete_incomplete_date(df, genotype):
    res=pd.crosstab(index=df["date"], columns= df["complete_module"],normalize="index")
    res.columns = ["incomplete","complete"]    

    p=res.iplot(kind = "line", 
                  mode='lines+markers', 
                  xTitle="Dates",
                  yTitle="Probability",
                  title="Relative distribution of complete (True) and incomplete (False) module as function of date for {}".format(genotype),
                  asFigure=True
                 )
    return p 


def print_single_genotype_plots():
    genotype=p4_wgt_genotypes_selection_t2.v_model
    vids=get_vid_of_genotype(misc.all_mtg, [genotype])
    df=extract_at_module_scale(misc.all_mtg, vids=vids)
    if genotype:
        # plot occurence module order
        fig = plot_module_occurence_module_order_along_time(df, genotype)
        transfert_figure(fig, p4_wgt_occurence)
        # plot occurence module order
        fig = plot_module_distribution_complete_incomplete_module_order(df, genotype)
        transfert_figure(fig, p4_wgt_distribution_module_order)
        # plot occurence module order
        fig = plot_module_distribution_complete_incomplete_date(df, genotype)
        transfert_figure(fig, p4_wgt_distribution_date)
    else:
        with p4_wgt_occurence:
            p4_wgt_occurence.clear_output()
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


def crowntype_plotly(data, crown_type, title, ylab,):
    fig=go.Figure()
    for genotype in list(data.unstack(level=0)[crown_type].columns):
        fig.add_trace(go.Scatter(
                x=list(data.unstack(level=0).index),
                y=list(data.unstack(level=0)[crown_type][genotype]),
                name=genotype,
                ))

    fig.update_layout(yaxis_title=ylab,
                      xaxis_title="Order",
                      title=title,
                      )
    return go.FigureWidget(fig)

def pointwisemean_plotly(data_mean, data_sd, variable,title,ylab,):
    fig=go.Figure()
    for genotype in list(data_mean.unstack(level=0)[variable].columns):
        sd_error = list(data_sd.unstack(level=0)[variable][genotype])
        fig.add_trace(go.Scatter(
                x=list(data_mean.unstack(level=0).index),
                y=data_mean.unstack(level=0)[variable][genotype],
                name=genotype,
                error_y=dict(type='data', 
                             array=sd_error, 
                             thickness=1,
                             visible=True)
                     ))

    fig.update_layout(yaxis_title=ylab,
                      xaxis_title="Order",
                      title=title,
                      )
    return go.FigureWidget(fig)



def plot_module_pointwisemean(df, var):
    Mean= df.groupby(["Genotype", "order"]).mean()
    sd= df.groupby(["Genotype", "order"]).std()
#     variable = "nb_total_{}".format(var)
    fig = pointwisemean_plotly(data_mean=Mean,
                   data_sd=sd,
                   variable=var,
                   title= "Pointwisemean of {}".format(var),
                   ylab="Mean {}".format(var),)

    return fig

def plot_module_crown(df, var):
    ctd = crowntype_distribution(data= df, crown_type=var)
    ctd = ctd[ctd.index.get_level_values('order')!=0]
    fig= crowntype_plotly(data=ctd,
                 crown_type=var, 
                 title="Relative frequency of {}".format(var),
                 ylab="Relative frequency")
    return fig


def print_multiple_genotypes_plots():
    if misc.all_mtg.property('Genotype'):
        df=extract_at_module_scale(misc.all_mtg)
        # plot pointwisemean leaves
        fig = plot_module_pointwisemean(df, "nb_total_leaves")
        transfert_figure(fig, p4_wgt_pointwisemean_leaves)
        # plot pointwisemean flowers
        fig = plot_module_pointwisemean(df, "nb_total_flowers")
        transfert_figure(fig, p4_wgt_pointwisemean_flowers)
        # plot pointwisemean stolons
        fig = plot_module_pointwisemean(df, "nb_stolons")
        transfert_figure(fig, p4_wgt_pointwisemean_stolons)
        # crowntype branch
        fig = plot_module_crown(df, "branch_crown")
        transfert_figure(fig, p4_wgt_branch_crown)
        # crowntype extension
        fig = plot_module_crown(df, "extension_crown")
        transfert_figure(fig, p4_wgt_extension_crown)
        


# # ----------------------------------------------------------------
# # On event trigger
# # ----------------------------------------------------------------

def on_change_genotype_p4(widget, event, data):
    # update table
    df=pd.DataFrame()
    if misc.all_mtg:
        vids=get_vid_of_genotype(misc.all_mtg, genotypes=data)
        df = extract_at_module_scale(misc.all_mtg, vids=vids)
    p4_wgt_df_modulescale.df = df
    
    # update descriptors
    with p4_wgt_descriptors:
        p4_wgt_descriptors.clear_output()
        display(df.describe())

def on_change_single_genotype(widget, event, data):
    print_single_genotype_plots()

def on_click_export_411(widget, event, data):
    genotype=p4_wgt_genotypes_selection_t2.v_model
    if genotype:
        vids=get_vid_of_genotype(misc.all_mtg, [genotype])
        df=extract_at_module_scale(misc.all_mtg, vids=vids)
        geno_frequency = occurence_module_order_along_time(data= df,frequency_type= "cdf")
        with p4_link_export_t11:
            p4_link_export_t11.clear_output()
            display(create_download_link(geno_frequency))
        
        
def on_click_export_412(widget, event, data):
    genotype=p4_wgt_genotypes_selection_t2.v_model
    if genotype:
        vids=get_vid_of_genotype(misc.all_mtg, [genotype])
        df=extract_at_module_scale(misc.all_mtg, vids=vids)
        res=pd.crosstab(index= df["order"], columns= df["complete_module"],normalize="index")
        res.columns = ["incomplete","complete"]
        with p4_link_export_t12:
            p4_link_export_t12.clear_output()
            display(create_download_link(res))
        
def on_click_export_413(widget, event, data):
    genotype=p4_wgt_genotypes_selection_t2.v_model
    if genotype:
        vids=get_vid_of_genotype(misc.all_mtg, [genotype])
        df=extract_at_module_scale(misc.all_mtg, vids=vids)
        res=pd.crosstab(index=df["date"], columns= df["complete_module"],normalize="index")
        res.columns = ["incomplete","complete"]    
        with p4_link_export_t13:
            p4_link_export_t13.clear_output()
            display(create_download_link(res))
            
def on_click_export_421(widget, event, data):
    if misc.all_mtg:
        df=extract_at_module_scale(misc.all_mtg)
        Mean= df.groupby(["Genotype", "order"]).mean()
        with p4_link_export_t21:
            p4_link_export_t21.clear_output()
            display(create_download_link(Mean))

            
def on_click_export_422(widget, event, data):
    if misc.all_mtg:
        df=extract_at_module_scale(misc.all_mtg)
        Mean= df.groupby(["Genotype", "order"]).mean()
        with p4_link_export_t22:
            p4_link_export_t22.clear_output()
            display(create_download_link(Mean))
            
def on_click_export_423(widget, event, data):
    if misc.all_mtg:
        df=extract_at_module_scale(misc.all_mtg)
        Mean= df.groupby(["Genotype", "order"]).mean()
        with p4_link_export_t23:
            p4_link_export_t23.clear_output()
            display(create_download_link(Mean))
            
def on_click_export_424(widget, event, data):
    if misc.all_mtg:
        df=extract_at_module_scale(misc.all_mtg)
        ctd = crowntype_distribution(data= df, crown_type="branch_crown")
        ctd = ctd[ctd.index.get_level_values('order')!=0]
        with p4_link_export_t24:
            p4_link_export_t24.clear_output()
            display(create_download_link(ctd))
            
def on_click_export_425(widget, event, data):
    if misc.all_mtg:
        df=extract_at_module_scale(misc.all_mtg)
        ctd = crowntype_distribution(data= df, crown_type="extension_crown")
        ctd = ctd[ctd.index.get_level_values('order')!=0]
        with p4_link_export_t25:
            p4_link_export_t25.clear_output()
            display(create_download_link(ctd))


def on_change_module_waffle_genotype(widget, event, data):
    genotype=p4_wgt_genotypes_selection_t4.v_model
    vids=get_vid_of_genotype(misc.all_mtg, [genotype])
    df=extract_at_module_scale(misc.all_mtg, vids=vids)
    param = list(df.columns)
    param.remove("Genotype")
    param.remove('date')
    p4_wgt_date_selection.items=list(df.date.unique())
    p4_wgt_date_selection.v_model=""
    p4_wgt_parameter_selection.items=param
    
def on_change_module_waffle_date(widget, event, data):
    if not p4_wgt_parameter_selection.v_model:
        pass
    else:
        with p4_waffle:
            p4_waffle.clear_output()
            genotype=p4_wgt_genotypes_selection_t4.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_module_scale(misc.all_mtg, vids=vids)

            if p4_wgt_aggfunc_selection.v_model == 'concat_string':
                tmp=df2waffle(df, index='order', 
                          date=data, 
                          variable=p4_wgt_parameter_selection.v_model, 
                          aggfunc=lambda x: ' '.join(x),
                          crosstab=False)
            else:
                tmp=df2waffle(df, index='order', 
                          date=data, 
                          variable=p4_wgt_parameter_selection.v_model, 
                          aggfunc=p4_wgt_aggfunc_selection.v_model,
                          crosstab=False)

            fig = plot_waffle(tmp,
#                               layout=layout,
                              plot_func=p4_wgt_plot_type.v_model)
            display(fig)


    
def on_change_module_waffle_parameter(widget, event, data):
    if not p4_wgt_date_selection.v_model:
        pass
    else:
        with p4_waffle:
            p4_waffle.clear_output()
            genotype=p4_wgt_genotypes_selection_t4.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_module_scale(misc.all_mtg, vids=vids)

            if p4_wgt_aggfunc_selection.v_model == 'concat_string':
                tmp=df2waffle(df, index='order', 
                          date=p4_wgt_date_selection.v_model, 
                          variable=data, 
                          aggfunc=lambda x: ' '.join(x),
                          crosstab=False)
            else:
                tmp=df2waffle(df, index='order', 
                          date=p4_wgt_date_selection.v_model, 
                          variable=data, 
                          aggfunc=p4_wgt_aggfunc_selection.v_model,
                          crosstab=False)


            fig = plot_waffle(tmp,
#                               layout=layout,
                              plot_func=p4_wgt_plot_type.v_model)
            display(fig)

            
def on_change_module_aggfunc(widget, event, data):
    if p4_wgt_date_selection.v_model and p4_wgt_parameter_selection.v_model:
        with p4_waffle:
            p4_waffle.clear_output()
            genotype=p4_wgt_genotypes_selection_t4.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_module_scale(misc.all_mtg, vids=vids)

            
            if p4_wgt_aggfunc_selection.v_model == 'concat_string':
                tmp=df2waffle(df, index='order', 
                          date=p4_wgt_date_selection.v_model, 
                          variable=p4_wgt_parameter_selection.v_model, 
                          aggfunc=lambda x: ' '.join(x),
                          crosstab=False)
            else:
                tmp=df2waffle(df, index='order', 
                          date=p4_wgt_date_selection.v_model, 
                          variable=p4_wgt_parameter_selection.v_model, 
                          aggfunc=data,
                          crosstab=False)

            fig = plot_waffle(tmp,
#                               layout=layout,
                              plot_func=p4_wgt_plot_type.v_model)
            display(fig)

            
# def on_change_module_crosstab(widget, event, data):
#     if p4_wgt_date_selection.v_model and p4_wgt_parameter_selection.v_model:
#         with p4_waffle:
#             p4_waffle.clear_output()
#             genotype=p4_wgt_genotypes_selection_t4.v_model
#             vids=get_vid_of_genotype(misc.all_mtg, [genotype])
#             df=extract_at_module_scale(misc.all_mtg, vids=vids)

#             tmp=df2waffle(df, index='order', 
#                           date=p4_wgt_date_selection.v_model, 
#                           variable=p4_wgt_parameter_selection.v_model, 
#                           aggfunc=p4_wgt_aggfunc_selection.v_model,
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
#                                   plot_func=p4_wgt_plot_type.v_model)
#             display(fig)

            
            
def on_change_module_plot_type(widget, event, data):
    if p4_wgt_date_selection.v_model and p4_wgt_parameter_selection.v_model:
        with p4_waffle:
            p4_waffle.clear_output()
            genotype=p4_wgt_genotypes_selection_t4.v_model
            vids=get_vid_of_genotype(misc.all_mtg, [genotype])
            df=extract_at_module_scale(misc.all_mtg, vids=vids)

            if p4_wgt_aggfunc_selection.v_model == 'concat_string':
                tmp=df2waffle(df, index='order', 
                          date=p4_wgt_date_selection.v_model, 
                          variable=p4_wgt_parameter_selection.v_model, 
                          aggfunc=lambda x: ' '.join(x),
                          crosstab=False
                         )
            else:
                tmp=df2waffle(df, index='order', 
                          date=p4_wgt_date_selection.v_model, 
                          variable=p4_wgt_parameter_selection.v_model, 
                          aggfunc=p4_wgt_aggfunc_selection.v_model,
                          crosstab=False
                         )

            fig = plot_waffle(tmp,
#                               layout=layout,
                              plot_func=data)

            display(fig)


def on_click_changetab(widget, event, data):
    print_multiple_genotypes_plots()


# # ----------------------------------------------------------------
# # Widgets
# # ----------------------------------------------------------------

p4_wgt_export = v.Btn(children=['Export table'])

p4_wgt_genotypes_selection_t1 = v.Select(items=[],
            chips=True, 
            multiple=True,
            counter=True,
            v_model="",
            label="Select Genotypes",
            truncate_length=22)

p4_col1 = v.Col(cols=12, sm=3, md=3,
                children=[
                          p4_wgt_genotypes_selection_t1,
                          p4_wgt_export
                      ])

p4_wgt_df_modulescale = qgrid.show_grid(pd.DataFrame(), show_toolbar=False, 
                                  grid_options={'forceFitColumns': False, 'editable':True, 'defaultColumnWidth':50})


p4_panel_table = v.Container(
                              fluid=True,
                              children=[
                                    p4_wgt_df_modulescale    
                            ])

p4_wgt_descriptors = widgets.Output(layout=layout_output_wgt)

p4_panel_descriptors =v.Container(fluid=True,
                              children=[
                                    p4_wgt_descriptors    
                                ])

p4_col2 = v.Col(cols=12, sm=7, md=9,
                children=[
                          p4_panel_table,
                          p4_panel_descriptors,
                      ])

p4_wgt_genotypes_selection_t1.on_event('change', on_change_genotype_p4)



p4_tab1 = v.Row(children=[p4_col1,
                          p4_col2,
                          ])

p4_wgt_genotypes_selection_t2 = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Genotype",
            truncate_length=22)

p4_wgt_occurence = go.FigureWidget(layout=layout_gofigure)
p4_wgt_distribution_module_order = go.FigureWidget(layout=layout_gofigure)
p4_wgt_distribution_date = go.FigureWidget(layout=layout_gofigure)

p4_link_export_t11 = widgets.Output(layout=layout_output_wgt)
p4_link_export_t12 = widgets.Output(layout=layout_output_wgt)
p4_link_export_t13 = widgets.Output(layout=layout_output_wgt)

p4_wgt_export_t11 = v.Btn(children=['Export table'])
p4_wgt_export_t12 = v.Btn(children=['Export table'])
p4_wgt_export_t13 = v.Btn(children=['Export table'])


p4_panel_single_genotype = v.Container(fluid=True,
                              children=[
                                    p4_wgt_occurence,
                                    v.Row(children=[p4_wgt_export_t11,p4_link_export_t11]),
                                    p4_wgt_distribution_module_order,
                                    v.Row(children=[p4_wgt_export_t12,p4_link_export_t12]),
                                    p4_wgt_distribution_date,
                                    v.Row(children=[p4_wgt_export_t13,p4_link_export_t13]),
                                ])


p4_col3 = v.Col(col=12, sm=11, md=11,
                children=[
                    p4_wgt_genotypes_selection_t2,
                    p4_panel_single_genotype
                  ])

p4_tab2 = v.Row(children=[p4_col3
                          ])


p4_wgt_pointwisemean_leaves = go.FigureWidget(layout=layout_gofigure)
p4_wgt_pointwisemean_flowers = go.FigureWidget(layout=layout_gofigure)
p4_wgt_pointwisemean_stolons = go.FigureWidget(layout=layout_gofigure)
p4_wgt_branch_crown = go.FigureWidget(layout=layout_gofigure)
p4_wgt_extension_crown = go.FigureWidget(layout=layout_gofigure)


p4_link_export_t21 = widgets.Output(layout=layout_output_wgt)
p4_link_export_t22 = widgets.Output(layout=layout_output_wgt)
p4_link_export_t23 = widgets.Output(layout=layout_output_wgt)
p4_link_export_t24 = widgets.Output(layout=layout_output_wgt)
p4_link_export_t25 = widgets.Output(layout=layout_output_wgt)

p4_wgt_export_t21 = v.Btn(children=['Export table'])
p4_wgt_export_t22 = v.Btn(children=['Export table'])
p4_wgt_export_t23 = v.Btn(children=['Export table'])
p4_wgt_export_t24 = v.Btn(children=['Export table'])
p4_wgt_export_t25 = v.Btn(children=['Export table'])

p4_panel_multiple_genotypes = v.Container(fluid=True,
                              children=[
                                    p4_wgt_pointwisemean_leaves,
                                    v.Row(children=[p4_wgt_export_t21,p4_link_export_t21]),
                                    p4_wgt_pointwisemean_flowers,
                                    v.Row(children=[p4_wgt_export_t22,p4_link_export_t22]),
                                    p4_wgt_pointwisemean_stolons,
                                    v.Row(children=[p4_wgt_export_t23,p4_link_export_t23]),
                                    p4_wgt_branch_crown,
                                    v.Row(children=[p4_wgt_export_t24,p4_link_export_t24]),
                                    p4_wgt_extension_crown,
                                    v.Row(children=[p4_wgt_export_t25,p4_link_export_t25]),
                                ])

p4_col4 = v.Col(col=12, sm=11, md=11,
                children=[
#                     p1_wgt_genotypes_selection,
                    p4_panel_multiple_genotypes
                  ])

p4_tab3 = v.Row(children=[p4_col4
                          ])

p4_wgt_genotypes_selection_t4 = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Genotype",
            truncate_length=22)

p4_wgt_date_selection = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Date",
            truncate_length=22)

p4_wgt_parameter_selection = v.Select(items=[],
            chips=True, 
            multiple=False,
            v_model="",
            label="Select Parameter",
            truncate_length=22)
    
p4_wgt_aggfunc_selection = v.Select(items=[{'text': 'Mean', 'value': 'mean'}, 
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

p4_wgt_plot_type = v.Select(items=["matplotlib", 'plotly.imshow', 'plotly.heatmap'],
            chips=True, 
            multiple=False,
            v_model="matplotlib",
            label="Select a plot library",
            truncate_length=22)


p4_select_waffle = v.Row(children=[p4_wgt_genotypes_selection_t4,
                                   p4_wgt_date_selection,
                                   p4_wgt_parameter_selection,
                                   p4_wgt_aggfunc_selection,
#                                    p4_wgt_crosstab,
                                   p4_wgt_plot_type])

p4_waffle = widgets.Output(layout=layout_output_wgt)


p4_tab4 = v.Row(children=[v.Col(
                            children=[
                                p4_select_waffle,
                                p4_waffle,
                              ]),
                        ])

p4 = v.Tabs( 
            children=[
            v.Tab(children=['Data extraction']),
            v.Tab(children=['Single genotype']),
            v.Tab(children=['Multiple genotypes']),
            v.Tab(children=['Waffle']),
            v.TabItem(children=[
                p4_tab1
            ]),
            v.TabItem(children=[
                p4_tab2
            ]),
            v.TabItem(children=[
                p4_tab3
            ]),
            v.TabItem(children=[
                p4_tab4
            ]),  
        ])


p4_container_main = v.Container(fluid=True, 
                                   class_='grid-list-md box',
                                   children=[
                                       p4
                                   ])

# # ----------------------------------------------------------------
# # Link widgets - event
# # ----------------------------------------------------------------

p4_wgt_genotypes_selection_t2.on_event("change", on_change_single_genotype)

p4_wgt_export_t11.on_event('click', on_click_export_411)
p4_wgt_export_t12.on_event('click', on_click_export_412)
p4_wgt_export_t13.on_event('click', on_click_export_413)

p4_wgt_export_t21.on_event('click', on_click_export_421)
p4_wgt_export_t22.on_event('click', on_click_export_422)
p4_wgt_export_t23.on_event('click', on_click_export_423)
p4_wgt_export_t24.on_event('click', on_click_export_424)
p4_wgt_export_t25.on_event('click', on_click_export_425)

p4_wgt_genotypes_selection_t4.on_event('change', on_change_module_waffle_genotype)
p4_wgt_date_selection.on_event('change', on_change_module_waffle_date)
p4_wgt_parameter_selection.on_event('change', on_change_module_waffle_parameter)
p4_wgt_aggfunc_selection.on_event('change', on_change_module_aggfunc)
# p4_wgt_crosstab.on_event('change', on_change_module_crosstab)
p4_wgt_plot_type.on_event('change', on_change_module_plot_type)

p4.on_event("change", on_click_changetab)

