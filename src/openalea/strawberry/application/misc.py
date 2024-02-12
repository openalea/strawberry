from pathlib import Path
import os
from io import StringIO
import pandas as pd
import base64

from ipywidgets import HTML
import ipywidgets as widgets

from oawidgets.plantgl import PlantGL

import openalea.strawberry
from openalea.mtg.io import write_mtg
from openalea.mtg import MTG

from openalea.strawberry.data import data_directory
from openalea.strawberry.application.layout import layout_dataframe, layout_output_wgt, layout_visu3d


if layout_dataframe == "qgrid":
    try:
        import qgrid
        qgrid.set_grid_option('maxVisibleRows', 10)
    except:
        layout_dataframe == "pandas"

if layout_visu3d == "pgljupyter":
    try:
        from pgljupyter import SceneWidget
    except:
        layout_visu3d="oawidgets"


def init_allmtg():
    global all_mtg
    all_mtg = MTG()


def get_vid_of_genotype(g, genotypes):
    if len(genotypes)==1:
        vids=[vid for vid in g.vertices(scale=1) if g.property('Genotype').get(vid) == genotypes[0]]
    else:
        vids=[]
        for genotype in genotypes:
            tmp=[vid for vid in g.vertices(scale=1) if g.property('Genotype').get(vid) == genotype]
            vids.extend(tmp)
    return vids


def get_genotypes(g):
    return list(set(g.property('Genotype').values()))


def get_vid_from_nbplant(g, genotype, p_nb):
    return get_vid_of_genotype(g, [genotype])[p_nb-1]


def get_files():

    files=[]
    # START BY LOADING ALL EXISTING MTG FILES IN /dashboard_files
    file_paths = {}
    if os.path.isdir(data_directory):
        for file in os.listdir(data_directory):
            if file.endswith('.mtg'):
                file_paths[file] = os.path.join(data_directory, file)
                files.append(file)
    return files, file_paths


def fix_inferior_character_for_qgrid(df):
    """ Return the dataframe with "<" character transformed as "&lt;"
    """
    return df.applymap(replace_inf_alt)

    
def replace_inf_alt(x):
    if isinstance(x, str):
        return x.replace('<','&lt;')
    else:
        return x


def get_table_mtg(g):
    
#     tmp_table_path = "mtg_table.csv"
    properties = [('Experiment_name','STRING'), ('Sample_date', 'STRING'),('Genotype', 'STRING'),('Modality', 'STRING'),
              ('Plant_ID', 'INT'),('Stade', 'STRING'),('DBI', 'REAL'),('INFLOLG', 'REAL'),('LFTLG_CENTRAL', 'REAL'),
              ('LFTLG_LEFT', 'REAL'),('FLWRNUMBER', 'REAL'),('FLWRNUMBER_OPEN', 'REAL'),('FLWRNUMBER_ABORTED', 'REAL'),
              ('FLWRNUMBER_CLOSED', 'REAL'),('SAMPLING', 'STRING'),]


    current_properties = [t for t in properties if t[0] in g.property_names()]
    mtg_string = write_mtg(g, current_properties)
    f = StringIO(mtg_string[mtg_string.find('ENTITY-CODE'):])
    df = pd.read_csv(f,
               sep="\t",
               header=0, 
               engine="python")
    df=df.fillna('')
    return df


def transfert_figure(source, cible):
    cible.data = []
    cible.layout = {}
    cible.update_layout(source.layout)
    for trace in source.data:
        cible.add_scatter(**trace.to_plotly_json())
        

def transfert_figure_pie(source, cible):
    cible.data = []
    cible.layout = {}
    cible.update_layout(source.layout)
    for trace in source.data:
        cible.add_pie(**trace.to_plotly_json())


def create_download_link( df, title = "Download CSV file", filename = "selected_mtg.csv"):
    csv = df.to_csv()
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
    html = html.format(payload=payload,title=title,filename=filename)
    return HTML(html)


def create_download_btn(df, title = "Download CSV file", filename = "selected_dataframe.csv"):
    csv = df.to_csv()
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    html_buttons = '''<html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
    <a download="{filename}" href="data:text/csv;base64,{payload}" download>
    <button class="p-Widget jupyter-widgets jupyter-button widget-button mod-warning">Download File</button>
    </a>
    </body>
    </html>
    '''
    html_button = html_buttons.format(payload=payload,filename=filename)
    return HTML(html_button)


def update_btn_export(wgt, payload):
    """The export buttons are widget.Output widget, that are updated when a genotype is selected to print a button with the associated link

    :param wgt: [description]
    :type wgt: [type]
    :param payload: [description]
    :type payload: [type]
    """
    with wgt:
        wgt.clear_output()
        display(create_download_btn(payload))


def update_grid(df, wgt):
    if layout_dataframe == "qgrid":
        df_fixed = fix_inferior_character_for_qgrid(df)
        wgt.df = df_fixed
    elif layout_dataframe == "pandas":
        with wgt:
            wgt.clear_output()
            display(df)


def create_grid():
    if layout_dataframe =="qgrid":
        return qgrid.show_grid(pd.DataFrame(), show_toolbar=False, 
                                  grid_options={'forceFitColumns': False, 'editable':True, 'defaultColumnWidth':50})
    elif layout_dataframe=="pandas":
        return widgets.Output(layout=layout_output_wgt)


def display3d(scene):
    if layout_visu3d=="pgljupyter":
        display(SceneWidget(scene))
    elif layout_visu3d=="oawidgets":
        display(PlantGL(scene,group_by_color=False))
