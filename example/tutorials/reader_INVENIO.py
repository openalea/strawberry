from collections import OrderedDict, defaultdict
import pandas as pd

from openalea.mtg.io import multiscale_edit


def add_component(s, symbol, children={}, *args, **kwargs):
    s+=symbol
    if len(kwargs)>0:
        s+='('
        i=0
        for arg, val in kwargs.items():
            if type(val)==str:
                s+=str(arg)+'="'+val+'"'
            else:
                s+=str(arg)+'='+str(val)
            i+=1
            if i<len(kwargs):
                s+=','
        s+=')'
    # if it is a leaf: add a complex too.
    if (symbol[-1:] == 'f') or (symbol[-1:] == 'F'):
        s=add_complex(s, children=children, **kwargs)
    return s

def add_complex(s, **kwargs):
    s+='[+A'
    # by default a complex end with a <bt
    children=kwargs.get('children',)
    if children == {}:
        children={'/bt':{'Stade':''}}
    s+=children.pop('caca',"")
    for comp, args in children.items():
        complex_s = ''
        complex_s=add_component(complex_s, comp, **args)
        s+=complex_s
    s+=']'
    return s

def create_mtg(s):
    symbol_at_scale=dict(P=1, T=2, A=2,F=3, f=3, bt=3, ht=3)
    class_type = {'Genotype':'STRING', 
                  'Experiment_name':'STRING', 
                  'Plant_ID': 'INT', 
                  'date': 'STRING',
                  'DBI':'REAL' ,
                  'PETLG':'REAL' ,
                  'LFTLG_CENTRAL':'REAL' ,
                  'LFTLG_LEFT':'REAL' ,
                  'Stade':'STRING',
                  'INFLOLG': 'REAL'}

    g=multiscale_edit(s, symbol_at_scale=symbol_at_scale, class_type=class_type)
    return g


def get_metadata_INVENIO(xls_path, row=1):
    
    metadata = {}

    xls = pd.ExcelFile(xls_path)
    df = xls.parse(1, header=1,).iloc[:11]
    
    # for a plant id:
    plant_id=df['plant'].iloc[row]

    genotype= xls.sheet_names[1]
    experiment_name = 'TEST INVENIO'
    # # get the date
    date=xls.parse(1, index_col=None, usecols = "B", header = 14, nrows=0)
    date = date.columns.values[0]
    ts = pd.to_datetime(str(date)) 
    date = ts.strftime('%Y/%m/%d')
    dbi=df.iloc[plant_id]['Diamètre\nmm']

    # Nb of leaves
    nb_leaves = df.iloc[plant_id]['Nombre \nVieilles feuilles\nétalées'] + df.iloc[plant_id]['Nombre \n feuilles\nétalées']
    nb_leaves_hidden=df.iloc[plant_id]['Détail Hampe terminale ']+df.iloc[plant_id]['Unnamed: 10']
    PETLG=df.iloc[plant_id]['Longueur pétiole']
    LFTLG_CENTRAL=df.iloc[plant_id]['LS']
    LFTLG_LEFT=df.iloc[plant_id]['LG']
    ht_stade=df.iloc[plant_id]['Unnamed: 11']
    INFLOLG=df.iloc[plant_id]['Unnamed: 12']

    # En dessous du HT -Niveau 1
    nb_bt_ni_HT_N1=df.iloc[plant_id]['Unnamed: 14']
    nb_bt_HT_N1=df.iloc[plant_id]['Unnamed: 15']
    # get a dict of the nb of bt under ht with stage {19:0, A:1, ...}
    col_bt_HT_N1=['Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18', 'Unnamed: 19', 'Unnamed: 20', 'Unnamed: 21', 'Unnamed: 22', 'Unnamed: 23', 'Unnamed: 24', 'Unnamed: 25',]
    l=df.iloc[plant_id][col_bt_HT_N1]
    stage_bt_HT_N1={}
    l=l.fillna(0)
    l=l.astype(int)
    for col_stage in col_bt_HT_N1:
        stage_bt_HT_N1[str(df.iloc[0][col_bt_HT_N1][col_stage])]=l[col_stage]
    list_stage_bt_HT_N1 = []
    for k,v in stage_bt_HT_N1.items():
        for i in range(v):
            list_stage_bt_HT_N1.append(k)

    # En dessous du HT -Niveau 2
    # TODO

    # A la base - Niveau 1
    nb_bt_ni_BASE_N1 = df.iloc[plant_id]['Détail niveau 1 - Nombre / stade']
    nb_bt_BASE_N1 = df.iloc[plant_id]['Unnamed: 87']
    col_bt_BASE_N1=[ 'Unnamed: 88', 'Unnamed: 89', 'Unnamed: 90', 'Unnamed: 91', 'Unnamed: 92', 'Unnamed: 93', 'Unnamed: 94', 'Unnamed: 95', 'Unnamed: 96', 'Unnamed: 97',]
    l=df.iloc[plant_id][col_bt_BASE_N1]
    stage_bt_BASE_N1={}
    l=l.fillna(0)
    l=l.astype(int)
    for col_stage in col_bt_BASE_N1:
        stage_bt_BASE_N1[str(df.iloc[0][col_bt_BASE_N1][col_stage])]=l[col_stage]
    list_stage_bt_BASE_N1 = []
    for k,v in stage_bt_BASE_N1.items():
        for i in range(v):
            list_stage_bt_BASE_N1.append(k)

    # A la base - Niveau 2 
    # TODO: et lv 3
    
    metadata['genotype']=genotype
    metadata['experiment_name']=experiment_name
    metadata['date']=date
    metadata['plant_id']=plant_id
    metadata['dbi']=dbi
    metadata['nb_leaves']=nb_leaves
    metadata['nb_leaves_hidden']=nb_leaves_hidden
    metadata['nb_bt_ni_BASE_N1']=nb_bt_ni_BASE_N1
    metadata['nb_bt_BASE_N1']=nb_bt_BASE_N1
    metadata['list_stage_bt_BASE_N1']=list_stage_bt_BASE_N1
    metadata['PETLG']=PETLG
    metadata['LFTLG_CENTRAL']=LFTLG_CENTRAL
    metadata['LFTLG_LEFT']=LFTLG_LEFT
    metadata['INFLOLG']=INFLOLG
    metadata['ht_stade']=ht_stade
    metadata['nb_bt_ni_HT_N1']=nb_bt_ni_HT_N1
    metadata['nb_bt_HT_N1']=nb_bt_HT_N1
    metadata['list_stage_bt_HT_N1']=list_stage_bt_HT_N1    
    return metadata


def mtg_string_from_INVENIO(genotype, experiment_name, date, plant_id, 
                            dbi, nb_leaves, nb_bt_ni_BASE_N1, nb_bt_BASE_N1, list_stage_bt_BASE_N1,
                            PETLG, LFTLG_CENTRAL, LFTLG_LEFT, INFLOLG, ht_stade,
                            nb_leaves_hidden, nb_bt_ni_HT_N1, nb_bt_HT_N1, list_stage_bt_HT_N1):
    
    s=""
    s=add_component(s, '/P', Genotype=genotype, 
                    date=date, 
                    Experiment_name=experiment_name,
                    Plant_ID=plant_id)
    s=add_component(s, '/T', DBI=dbi)
    # for each non initiated bt at base lv 1 - CREATE the leaves, then add them to each following /F
    # for big leaves - leaves to bases - last:
    remaining_leaves=nb_leaves
    first_leaf=True
    for leaves_base in range(nb_bt_ni_BASE_N1):
        if first_leaf==True:
            first_leaf=False
            s=add_component(s, '/F',)
        else:
            s=add_component(s, '<F',)
        remaining_leaves-=1

    for leaves_base in range(nb_bt_BASE_N1):
        # get the stage first the bigger ones:
        stage=list_stage_bt_BASE_N1.pop()
        if first_leaf==True:
            first_leaf=False
            s=add_component(s, '/F',children={'/ht':{'Stade':stage}})
        else:
            s=add_component(s, '<F', children={'/ht':{'Stade':stage}})
        remaining_leaves-=1

    # FOR each of the remaining leaves add a <F (/F if first)
    if remaining_leaves>1:
        for leaves_base in range(remaining_leaves-1):
            if first_leaf==True:
                first_leaf=False
                s=add_component(s, '/F',)
            else:
                s=add_component(s, '<F',)

    # add the last visible leaf with the petiol information
    s=add_component(s, '<F', PETLG=PETLG,LFTLG_CENTRAL=LFTLG_CENTRAL,LFTLG_LEFT=LFTLG_LEFT)

    # for hidden leaf before the HT
    remaining_leaves=nb_leaves_hidden
    # FOR each of the remaining (not bt) leaves add a <f 
    remaining_leaves= remaining_leaves - nb_bt_ni_HT_N1 - nb_bt_HT_N1
    if remaining_leaves>1:
        for leaves_base in range(remaining_leaves):
            s=add_component(s, '<f',)

    for leaves_ht in range(nb_bt_ni_HT_N1):
        s=add_component(s, '<f',)

    for leaves_ht in range(nb_bt_HT_N1):
        # get the stage first the bigger ones:
        stage=list_stage_bt_HT_N1.pop()
        s=add_component(s, '<f', children={'/ht':{'Stade':stage}})

    # ADD the final HT
    s=add_component(s, '<ht', Stade=ht_stade, INFLOLG=INFLOLG)
    return s