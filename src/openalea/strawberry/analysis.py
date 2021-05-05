
from __future__ import absolute_import
from __future__ import print_function

import pandas as pd
from collections import OrderedDict, defaultdict
import matplotlib.pyplot as plt
from itertools import chain

from openalea.mtg.algo import orders
from openalea.mtg import stat, algo, traversal

import numpy as np
from matplotlib.colors import to_rgb
import matplotlib.patches as mpatches
import plotly.express as px
import plotly.graph_objs as go


import six
from six.moves import map
from six.moves import range


convert = dict(Stade='Stade',
               Fleurs_ouverte='FLWRNUMBER_OPEN',
               Fleurs_avorte='FLWRNUMBER_ABORTED',
               Fleurs_total='FLWRNUMBER',
               date='Sample_date',
               Plante='Plant_ID',
              )


def to_dataframe(g, vertices=[], f=None):
    """ Convert an MTG into a full dataframe.

    Properties:
      - vertices: define the vertices you want to export
      - f : v -> dict : function that returns a set of properties for any vertex.

    """

    # Recompute the properties for each vertices
    if not vertices:
        vertices = g.vertices()

    if f is None:
        f = lambda v : g[v]

    d = dict()
    for v in vertices:
        props_v = f(v)
        for k, value in props_v.items():
            d.setdefault(k,{})[v] = value

    parents = g._parent
    complexes = {vid: g.complex(vid) for vid in g if g.complex(vid) is not None}
    scales = g._scale
    _orders = orders(g)

    d['parent'] = {v: parents.get(v) for v in vertices}
    d['complex'] = {v: complexes.get(v) for v in vertices}
    d['scale'] = {v: scales.get(v) for v in vertices}
    d['order'] = {v: _orders.get(v) for v in vertices}


    dataframe = pd.DataFrame.from_dict(d)
    return dataframe

def strawberry_dataframe(g):
    vertices = [v for v in g.vertices_iter() if v !=0]

    props = g.properties()

    def my_f(v):
        d = dict()
        pid = g.complex_at_scale(v, scale=1)
        pnid = g.node(pid)
        nid = g.node(v)

        # Set plant properties to each node
        d['Genotype'] = pnid.Genotype
        d['Plante'] = pnid.Plante
        d['date'] = pnid.Sample_date
        d['label'] = g.label(v)

        # At all scale
        d['Stage'] = nid.Stade
        d['Foliar_type'] = nid.Foliar_type
        #d['prelevement'] = nid.prelevement
        #d['Fleurs_total']= nid.Fleurs_total
        #d['Fleurs_ouverte'] = nid.Fleurs_ouverte
        #d['Fleurs_avorte'] = nid.Fleurs_avorte



        return d


    return to_dataframe(g, vertices, my_f)


def write_sequences(seqs, variables, VertexIdentifiers):
    """ Write Sequences into a txt file.

    """
    sep = '\t'
    txts = []

    # header
    header = "INDEX_PARAMETER : TIME   # vertex_id"
    txts.append(header)
    txts.append('')

    n = len(variables)
    header = "%d VARIABLES"%n
    txts.append(header)
    txts.append('')

    for i in range(1, n+1):
        txts.append('VARIABLE %d: INT  # %s'%(i, variables[i-1]))

    txts.append('')
    txts.append('')
    txts.append('#Index'+sep+sep.join(variables))

    for i, seq in enumerate(seqs):
        n = len(seq)
        for j, value in enumerate(seq):
            vid = VertexIdentifiers[i][j]
            record = [str(vid)] + list(map(str,value))
            if j < n-1:
                record.append('\\')
            else:
                # end of the sequence
                record.append('')

            record.append('#')

            txt = sep.join(record)
            txts.append(txt)
        txts.append('')

    return '\n'.join(txts)


def median_individuals(df):
    indices = []
    for gd, dataf in df.groupby(["Genotype","date","modality"]):
        geno, date, mod = gd
        dg = dataf[df.columns[4:-1]]
        s=((dg-dg.median()).abs()/(dg-dg.median()).abs().mean()).sum(axis=1)
        indices.append(s.idxmin())

        # _min = s.min()
        # minimum_inds= s[s==_min]
    return df.iloc[indices]

def occurence_module_order_along_time(data, frequency_type):
    """
    parameters:
    -----------
        data = data at module scale 
        frequency_type = type of distribution frequency distribution (freq), probability distribution frequency (pbf) or cumulative frequency distribution (cdf)

    return:
    --------
        A dataframe with frequency, probability or cumulative frequency distribution for each module order along time
    """
    if frequency_type == "freq":
        res = pd.crosstab(index= data["order"], columns= data["date"], margins = True)
    if frequency_type == "pdf":
        res = pd.crosstab(index= data["order"], columns= data["date"], normalize = "columns")
    if frequency_type == "cdf":
        res = pd.crosstab(index= data["order"], columns= data["date"], normalize = "columns").cumsum()
    return res

def pointwisemean_plot(data_mean,data_sd,varieties, variable,title,ylab, expand=0):
    """
    parameters:
    -----------
        data_mean: panda dataframe containg mean values
        data_sd: panda dataframe containing standars error values
        varieties: names of varieties which are plot
        title: plot title
        ylab:  y axis label
        expand: allows to change xlim

    return:
    ---------
        line plot with mean value of each varieties selected 
    """

    fig, pointwise_mean = plt.subplots()
    cmap = plt.get_cmap('rainbow', len(varieties))
    for i, varietie in enumerate(varieties):
        pointwise_mean.errorbar(x=data_mean.loc[varietie].index, 
                     y=data_mean.loc[varietie][variable],
                     yerr=data_sd.loc[varietie][variable],
                     color=cmap(i), marker="p")
    pointwise_mean.legend(labels=varieties,loc='center left', bbox_to_anchor=(1, 0.5))
    pointwise_mean.set_title(title)
    pointwise_mean.set_ylabel(ylab)
    pointwise_mean.set_xlim(left=-expand, right= max(data_mean.loc[varietie].index)+expand)

    plt.show()

def crowntype_distribution(data, varieties, crown_type, plot=True,expand=0):
    """
    parameters:
    -----------
    data: panda dataframe issue from extraction of data at module scale
    varieties: names of varieties which are plot
    variable: type of branch crown (extension_crown or branch_crown)
    plot: booleen variable True or False

    return:
    -------
    a dataframe containing relative frequency values by genotype and order for extension and branch crown
    and a relative frequency distribution plot

    """
    df= pd.crosstab(index= [data.Genotype, data.order],
                    columns= data.type_of_crown,
                    normalize="index")
    
    df.columns=["Main", "extension_crown", "branch_crown"]
    
    if plot:
        cmap = plt.get_cmap('rainbow', len(varieties))
        print(cmap)
        
        for i, variety in enumerate(varieties): 
            
            df = df[df.index.get_level_values('order')!=0]
            
            plt.plot(df.loc[variety][crown_type],
                     marker="p", 
                     color = cmap(i))
            plt.ylabel("relative frequency")
            plt.xlabel("order")
            plt.title("Relative frequency of " + crown_type)
            plt.legend(labels=varieties,loc='center left', bbox_to_anchor=(1, 0.5))
            plt.xlim(left=1-expand, right= max(df.loc[variety].index)+expand)
            plt.ylim(bottom=0.1, top= 1.1)


    return df


# from variables
# 

def property(g, name):
    """ We can change the name of the MTG properties without changing the code"""
    return g.property(convert.get(name, name))

######################################## Extraction at plant scale ###########################################################
def extract_at_plant_scale(g, vids=[], convert=convert):
    """
    Return computed properties at plant scale

    Parameters
    ----------
    - g: MTG
    - vids : a subset of vertex ids at scale 1

    Returns
    -------
    - a Dataframe
    """
    #TODO: compute this only one. It would be nice if we can compute this in the init of a class Extractor.
    orders = algo.orders(g, scale=2)

    plant_variables = _plant_variables(g)

    # plant_ids is a list of plants we wat to process.
    if not vids:
        plant_ids = g.vertices(scale=1)
    else: 
        plant_ids = [pid for pid in g.vertices(scale=1) if pid in vids]

    visible_modules(g, vids=plant_ids)
    compute_leaf_area(g, vids=plant_ids)

    plant_df = OrderedDict()
    # for name in ('Genotype', 'date', 'plant'):
    #     plant_df[name] = [plant_variables[name](pid) for pid in plant_ids]
    plant_df['Genotype'] = [genotype(pid, g) for pid in plant_ids]
    plant_df['date'] = [date(pid, g) for pid in plant_ids]
    plant_df['modality'] = [modality(pid, g) for pid in plant_ids]
    plant_df['plant'] = [plant(pid, g) for pid in plant_ids]

    visibles = property(g, 'visible')

    for name in (plant_variables):
        f = plant_variables[name]
        plant_df[name] = [sum(f(v, g) for v in g.components(pid) if v in visibles) for pid in plant_ids]

    #plant_df['Total_leaf_area'] = [mean_leaf_area(pid, g) * (sum(nb_visible_leaves(v,g) for v in g.components(pid) if v in visibles) for pid in plant_ids]
    plant_df['leaf_area'] = [mean_leaf_area(pid, g)  for pid in plant_ids]
    plant_df['order_max'] = [max(orders[v] for v in g.components(pid) if v in visibles) for pid in plant_ids]
    plant_df['nb_ramifications'] = [sum(1 for v in g.components(pid) if (type_of_crown(v, g)==3 and v in visibles)) for pid in plant_ids]
    plant_df['vid'] = plant_ids

    df = pd.DataFrame(plant_df)
    return df

def _plant_variables(g):
    plant_variables = OrderedDict()
    plant_variables['nb_total_leaves'] = nb_total_leaves #Nombre total de feuille
    plant_variables['nb_total_flowers'] = nb_total_flowers #Nombre total de Fleurs
    plant_variables['nb_stolons'] = nb_stolons # Nombre de stolons
    plant_variables['nb_visible_leaves'] = nb_visible_leaves # Nombre de feuille visible
    plant_variables['nb_missing_leaves'] = missing_leaves #Nombre de feuille manquante
    plant_variables['nb_vegetative_bud'] = nb_vegetative_buds
    plant_variables['nb_initiated_bud'] = nb_initiated_buds
    plant_variables['nb_floral_bud'] = nb_floral_buds
    plant_variables['nb_inflorescence'] = nb_inflorescence
    #plant_variables['type_of_crown'] = type_of_crown
    #plant_variables['crown_status'] = crown_status

    return plant_variables

####################### Extraction at the module scale ##################################################################
def extract_at_module_scale(g, vids=[], convert=convert):

    if not vids:
        vids = g.vertices(scale=1)

    orders = algo.orders(g, scale=2)

    module_variables = _module_variables(g)
    visible_modules(g, vids=vids)
    complete_module(g, vids=vids)

    module_ids =  [v for v in g.property('visible') if g.complex_at_scale(v, scale=1) in vids]

    module_df = OrderedDict()
    module_df['Genotype'] = [genotype(mid, g) for mid in module_ids]
    module_df['date'] = [date(mid, g) for mid in module_ids]
    module_df['modality'] = [modality(mid, g) for mid in module_ids]
    module_df['plant'] = [plant(mid, g) for mid in module_ids]
    module_df['order'] = [orders[mid]  for mid in module_ids]

    visibles = property(g, 'visible')

    for name in (module_variables):
        f = module_variables[name]
        module_df[name] = [f(mid, g) for mid in module_ids]
    #plant_df['nb_ramifications'] = [sum(1 for v in g.components(pid) if (type_of_crown(v, g)==3 and v in visibles)) for pid in plant_ids]
    module_df['vid'] = module_ids
    module_df['plant_vid'] = [g.complex(v) for v in module_ids]

    df = pd.DataFrame(module_df)
    return df


def _module_variables(g):
    module_variables = OrderedDict()
    module_variables['nb_visible_leaves'] = nb_visible_leaves # Nombre de feuille developpe
    module_variables['nb_foliar_primordia'] = nb_foliar_primordia #Nombre de primordia foliaire
    module_variables['nb_total_leaves'] = nb_total_leaves #Nombre total de feuille
    module_variables['nb_open_flowers'] = nb_open_flowers #Nombre de fleurs ouverte
    module_variables['nb_aborted_flowers'] = nb_aborted_flowers #Nombre de fleurs avorte
    module_variables['nb_total_flowers'] = nb_total_flowers #Nombre total de Fleurs
    module_variables['nb_vegetative_bud'] = nb_vegetative_buds
    module_variables['nb_initiated_bud']= nb_initiated_buds
    module_variables['nb_floral_bud']= nb_floral_buds
    module_variables['nb_stolons']= nb_stolons
    module_variables['type_of_crown'] = type_of_crown # Type de crowns (Primary Crown:1, Branch crown:2 extension crown:3)
    module_variables['crown_status'] = Crown_status
    module_variables['complete_module'] = complete #(True: complete, False: incomplete)
    module_variables['stage']= stage

    return module_variables


def visible_modules(g, vids=[]):
    modules =  [v for v in g.vertices_iter(scale=2) 
                if (g.complex(v) in vids)
                and g.label(next(g.component_roots_iter(v))) == 'F']
    _visible = {}
    for m in modules:
        _visible[m] = True
    g.properties()['visible'] = _visible


def complete_module(g, vids=[]):
    """Return properties incomplete or complete module
    
    Algorithm: 
     module are complete:
       if module are visible and terminated by an Inflorescence (HT) (propertie=True)
       else module are incomplete (all module terminated by ht or bt) (property=False)
       
    """
    complete = {}
    visible = g.property('visible')
    for vid in visible:
        if g.complex_at_scale(vid, scale=1) not in vids:
            continue
        comp = g.components(vid)
        c = comp[0]
        axis = [v for v in g.Axis(c) if v in comp]
        last = axis[-1]
        if g.label(last) == 'HT': 
            complete[vid] = True 
            
    g.properties()['complete'] = complete
    

def nb_visible_leaves(vid, g):
    return sum(1 for cid in g.components(vid) if g.label(cid)=='F')

#function which count all f
def nb_foliar_primordia(vid, g):
    return sum(1 for cid in g.components(vid) if g.label(cid)=='f')

#function which count all f+F
def nb_total_leaves(vid, g):
    return sum(1 for cid in g.components(vid) if g.label(cid) in ('f', 'F'))

""" nb_stolon"""
#function count stolon
def nb_stolons(v, g):
    def nb_stolon(vid, g=g):
        return sum(1 for cid in g.components(vid) if g.label(cid)=='s')
    return sum(nb_stolon(ch) for ch in g.children(v))

#function return number of open flower
def nb_open_flowers(vid, g):
    flowers = property(g, 'Fleurs_ouverte')
    return sum( flowers.get(cid,0) for cid in g.components(vid) if g.label(cid) in ('ht', 'HT'))

# function return number of aborted flower
def nb_aborted_flowers(vid, g):
    flowers = property(g, 'Fleurs_aborted')
    return sum( flowers.get(cid,0) for cid in g.components(vid) if g.label(cid) in ('ht', 'HT'))

# function return number of total flower
def nb_total_flowers(vid, g):
    flowers = property(g, 'Fleurs_total')
    return sum( flowers.get(cid,0) for cid in g.components(vid) if g.label(cid) in ('ht', 'HT'))

def missing_leaves(vid,g):
    missing= property(g, 'Missing')
    return sum(1 for cid in g.components(vid) if missing.get(cid)=="yes")


# function return number of vegetative buds
def nb_vegetative_buds(vid, g):
    """Return the No vegetative bud

Algorithm:
if label is bt then stage is 17,18,19 or None
count number of bt and attach at the parent order
    """
    stages= property(g, 'Stade')

    def nb_vegetative(v):
        cid = g.component_roots(v)[0]

        return sum(1 for cid in g.components(v) if g.label(cid)=='bt' and stages.get(cid) in (None,'17','18','19'))

    return sum(nb_vegetative(ch) for ch in g.children(vid))




def nb_initiated_buds(vid, g):
    """ Return the No initiated bud"""
    stages= property(g, 'Stade')

    def nb_init(v):
        return sum(1 for cid in g.components(v) if (g.label(cid)=='bt') and (stages.get(cid)=='A'))

    return sum(nb_init(ch) for ch in g.children(vid))


""" Return the No Floral bud"""
def nb_floral_buds (vid, g):
    visibles = property(g, 'visible')
    def nb_floral(v):
        return sum(1 for cid in g.components(v) if g.label(cid)=="ht" )
    return sum(nb_floral(ch) for ch in g.children(vid) if ch not in visibles)


""" Qualitative variables"""
def type_of_crown(vid, g):
    """ Returns the type of crown.

    Definition of type of crown (1, 2, 3):
     - principal crown (1): label == T
     - branch_crown (3)
         parent(component_roots()[0]) : if successor() == F
     - extension_crown (2): contains(HT, ht, bt)
     - error (4)

    """
    if g.label(vid) == 'T':
        return 1
    else:
        cid = next(g.component_roots_iter(vid))
        pid = g.parent(cid)
        sid = g.Successor(pid)
        #print(sid)
        if g.label(sid) in ('F', 'f'):
            return 3
        elif g.label(sid) in ('bt', 'ht', 'HT'):
            return 2
        else:
            # ERROR !!!
            # print((g[cid], g[g.complex_at_scale(cid, scale=1)]))
            return 4

def Crown_status(vid, g):
    """ Returns the type of inflorescence

    :Algorithms:
    if label is bt then
        - if stage is 17, 18, 19 or None, => vegetative (1)
        - if stage is A => initiated (2)
        - if stage is other => non defined (pourri, avorte, coupe) (-1)
     - Terminal vegetative bud (1): label==bt g.property(Stade)== none or 17 or 18 or 19
     - Terminal initiated bud (2): label== bt if g.property(Stade) == A
     - Terminal Floral bud (3): label==ht
     - Inflorescence Terminal (4): label== HT
     - runner (5): label = s

    """
    stages = property(g,'Stade')
    # select s, ht, HT et bt
    for cid in g.components(vid):
        if g.label(cid) in ('s', 'ht', 'HT', 'bt'):
            label = g.label(cid)
            if label == 'ht':
                return 3
            elif label == 'HT':
                return 4
            elif label == 'bt':
                stage = stages.get(cid)
                if stage == 'A':
                    return 2
                elif stage in (None, '17', '18', '19'):
                    return 1
            elif label == 's':
                return 5
            return -1

def nb_inflorescence (Vid, g):
    return sum(1 for cid in g.components(Vid) if g.label(cid)=='HT')

#TODO: Remove
def genotype(vid, g):
    #d = {'Capriss':4, 'Ciflorette':2, 'Cir107':6, 'Clery':3, 'Darselect':5, 'Gariguette':1,
    #     'Nils': 1, }

    cpx = g.complex_at_scale(vid, scale=1)
    _genotype = property(g, 'Genotype')[cpx]
    return _genotype


def plant(vid, g):
    cpx = g.complex_at_scale(vid, scale=1)
    return property(g, 'Plante')[cpx]

def date(vid, g):
    #d = dates()

    cpx = g.complex_at_scale(vid, scale=1)
    _date = property(g, 'date')[cpx]
    return(_date)

def modality(vid, g):
    cpx = g.complex_at_scale(vid, scale=1)
    _modality = property(g, 'Modality')[cpx]
    return(_modality)

# add by marc

def compute_leaf_area(g, vids=[]):
    _central= g.property("LFTLG_CENTRAL")
    _left= g.property("LFTLG_LEFT")
    _mean_leaf_area= g.property("LFAR")

    for v in _central:
        pid = g.complex_at_scale(v, scale=1)
        if pid not in vids:
            continue

        central = _central.get(v)
        left = _left.get(v)
        if (central is None) or (left is None):
            print(("DATA is missing on vertex %d for line %d"%(v, g.node(v)._line)))
            continue

        _mean_leaf_area[pid]= round(1.89 + (2.145 * (central/10) * (left/10)),2)


def mean_leaf_area(vid,g):
    pid = g.complex_at_scale(vid, scale=1)
    area = g.property("LFAR").get(pid, 0.)

    return area

def complete(vid, g):
    return g.property("complete").get(vid, False)


def stage(vid, g):
    _stage = g.property('Stade')
    return next(iter(list(_stage[cid] for cid in g.components(vid) if cid in _stage)), None)


########################## Extraction on node scale ############################################

def extract_at_node_scale(g, vids=[], convert=convert):

    if not vids:
        vids = g.vertices(scale=1)
    
    node_df = OrderedDict()
    visible_modules(g, vids=vids)
    complete_module(g, vids=vids)
    orders = algo.orders(g,scale=2)

    # Define all the rows
    props = ['node_id', 'rank', 'branching_type', 'complete','nb_modules_branching','nb_branch_crown_branching','nb_extension_crown_branching','branching_length', 'stage', 'Genotype', 'order',  'date','plant']
    for prop in props:
        node_df[prop] = []

    roots = [rid for pid in vids for rid in g.component_roots_at_scale(pid, scale=2)]
    trunks = [ list(chain(*[(v for v in algo.axis(g,m, scale=3) if g.label(v) in ('F', 'f')) 
                            for m in apparent_axis(g, r)])) for r in roots]
            
    for trunk in trunks:
        # Define your schema
        for i, vid in enumerate(trunk):
            node_df['node_id'].append(vid) #scale=3
            node_df['rank'].append(i+1) #scale=3
            node_df['branching_type'].append(my_bt(vid,g)) #scale=2
            node_df['complete'].append(my_complete(vid, g)) #scale=2
            node_df['nb_modules_branching'].append(nb_total_module_tree(vid,g))#scale=2
            node_df['nb_branch_crown_branching'].append(nb_branching_tree(vid,g))#scale=2
            node_df['nb_extension_crown_branching'].append(nb_extension_tree(vid,g))#scale=2
            node_df['branching_length'].append(nb_visible_leaves_tree(vid,g))
            node_df['Genotype'].append(genotype(vid, g)) #scale=1
            node_df['order'].append(orders[g.complex(vid)]) #scale=2
            node_df['plant'].append(plant(vid, g)) #scale=1
            node_df['date'].append(date(vid, g)) #scale=1
            node_df['stage'].append(stage(vid, g)) # scale=3
            
    df = pd.DataFrame(node_df)

    return df



def my_bt(vid, g):
    """
    Return branching type on parent if branch crown correspond to Son vertex
    """
    for cid in g.Sons(vid, EdgeType='+'):
        return str(branching_type(cid,g))


def complete(vid, g):
    """
    Add property complete or not on mtg
    """
    return g.property("complete").get(vid, False)

    
def my_complete(vid, g):
    """
    Return complete module, incomplete module or other (if not branch crown)
    """
    # scale = 2
    _complete = g.property('complete')
    if not complete:
        complete_module(g)
        _complete = g.property('complete')
        # print(_complete)
    
    res = 'other'
    for cid in g.Sons(vid, EdgeType='+'):
        cpx = g.complex(cid)
        bt = branching_type(cid,g)
        if bt == 6: 
            res = 'complete' if complete(cpx,g) else 'incomplete'
            break
    return res

def apparent_axis(g, vid):
    """
    Return apparent axis if module are visible
    """
    visibles = g.property('visible')
    v = vid
    while v is not None:
        yield v
        vtx = v; v = None
        for vid in g.children(vtx):
            if (vid in visibles) and (not is_axis_root(g, vid)):
                v = vid


def is_axis_root(g, vid):
    cid = next(g.component_roots_iter(vid))
    pid = g.parent(cid)
    sid = g.Successor(pid)
    if g.label(sid) not in ('bt', 'ht', 'HT'):
        return True
    else:
        return False

def branching_type(vid, g):
    """ Returns the type of branching
    
    :Algorithms:
    
    if module is visible:
        - branch crown (complex ramification):6
        - inflorescence : 7

    if module is invisible:
        - stolon (s): 1,
        - vegetative bud(bt, at stage None, 17,18,19):2,
        - initiated bud, (bt, at stage A):3,
        - aborted or roten or dried bud: 4
        - floral bud(ht):5

     
    """

    cpx = g.complex(vid)
    nid = g.node(cpx) 
    if nid.visible:
        if g.label(vid) == 'HT':
            return 7
        else:
            return 6
    
    # select s, ht, et bt
    for cid in nid.components():
        label = cid.label
        if label in ('s', 'ht', 'bt'):
            if label == 's':
                return 1
            elif label == 'bt':
                stage = cid.Stade
                if stage in (None, '17', '18', '19'):
                    return 2
                elif stage == 'A':
                    return 3
                elif stage in ('pourri', 'aborted', 'dried'):
                    return 4
            elif label  == 'ht':
                return 5
    else:
        return -1
        print(('ERROR: ', cpx, nid.complex().Genotype, nid.properties()))

DEBUG = True
def module_tree(v, g):
#     _complete = g.property('complete')
#     if not complete:
#         complete_module(g)
#         _complete = g.property('complete')
    
    for cid in g.Sons(v, EdgeType='+'):
        cpx = g.complex(cid)
        visibles = g.property('visible')
        if DEBUG:
            if cpx in visibles and (is_axis_root(g, cpx)):
                return [m for m in traversal.pre_order2(g, cpx) if m in visibles]
        else:
            bt = branching_type(cid,g)
            if bt == 6:
                return [m for m in traversal.pre_order2(g, cpx) if m in visibles]

def nb_total_module_tree(v, g):
    if not module_tree(v,g):
        return 0
    else:
        return len(module_tree(v, g))

def nb_branching_tree(v, g):
    if not module_tree(v, g):
        return 0
    else:
        return sum(1 for m in module_tree(v, g) if is_axis_root(g, m))

def nb_branching_tree_weight(v, g):
    if not module_tree(v, g):
        return 0
    else:
        return sum(g.nb_components(m) for m in module_tree(v, g) if is_axis_root(g, m))

def nb_extension_tree(v, g):
    if not module_tree(v, g):
        return 0
    else:
        return sum(1 for m in module_tree(v, g) if not is_axis_root(g, m))

def nb_visible_leaves_tree(v, g):
    if not module_tree(v, g):
        return 0
    else:
        return sum(nb_visible_leaves(m,g) for m in module_tree(v, g))


def stage_tree(vid, g):
    return list(stage(m,g) for m in module_tree(v, g))


######################### Transformation of dataframe ######################################
def df2waffle(df, date, index, variable, aggfunc=None, crosstab=None, *args, **kwargs):
    '''
        Transpose dataframe by variable with plant in columns and rank or order in index
        This function are available for extraction at node scale (index='rank') and 
        extraction at module scale (index= 'order')
        Parameters:
        -----------
            df: dataframe from extract function at differente scale (modules and nodes scale)
            date_selected: date which must be processed
            variable: variable which must be processed
        
        Returns:
        --------
            a dataframe in "waffle" shape: index=date, & columns=variable
    '''

    data=df[df['date']==date]
    
    if index=='rank':
        res = data.pivot(index='rank',columns='plant',values=variable)
    elif index=='order':
        if crosstab:
            res = pd.crosstab(index=data['order'], columns=data[variable], normalize='index')
            res=res*100 # percentage (0-100)
            res = res.round(2)
        else:
            # Catch data error: when values are string and aggfunc compute numbers
            try:
                res= data.pivot_table(index='order',columns='plant',values=variable, aggfunc=aggfunc)
            except DataError:
                print("ERROR, the aggregate function does not handle the data type (float func on str?)")
                return pd.DataFrame()
            
    else:
        res = data.pivot(index=index,columns='plant',values=variable)
    
    # If use plotly heatmap -> comment "res = res.fillna('')"
    if res.isnull().values.any():
        res = res.fillna('')
    res = res.sort_index(ascending=False)
    return res


def plot_waffle_plotly_heatmap(df, layout={}, legend_name={}):
    
    def df_to_plotly(df):
        return {'z': df.values.tolist(),
                'x': df.columns.tolist(),
                'y': df.index.tolist()}
    
    height = layout.get('height', 500)
    width = layout.get('width', 500)
    xlabel = layout.get('xlabel', 'Plant')
    xticks = layout.get('xticks', range(0,len(df.columns)))
    xticks_label = layout.get('xticks_label', range(1,len(df.columns)+1))
    ylabel = layout.get('ylabel', '')
    yticks = layout.get('yticks', range(0,len(df.index)))
    yticks_label = layout.get('yticks_label', list(range(0,len(df.index))))
    title = layout.get('title', '')    

    hm_layout = go.Layout(plot_bgcolor='rgba(0,0,0,0)',
    #                    xaxis=dict(zeroline=False),
    #                    yaxis=dict(zeroline=False, ), 
                       autosize=False,
                       width=width, height=height
                      )

    data = go.Heatmap(df_to_plotly(df),
                       xgap=1,
                       ygap=1,
                       colorscale="aggrnyl"
                       )

    fig = go.Figure(data=data, layout=hm_layout)

    return fig


def plot_waffle_plotly_imshow(df, layout={}, legend_name={}):
    colormap_used = plt.cm.coolwarm

    values = list(set(df.values.flatten()))
    if '' in values:
        values.remove('')
    try:
        values.sort()
    except TypeError:
        values = [str(i) for i in values]
        values.sort()
    values.insert(0,'')

    color_map = {val: colormap_used(i/len(values)) for i, val in enumerate(values)}

    # Add the "empty" variable - and set its color as white
    color_map[''] = (1., 1., 1., 1.)

    data = np.array(df)

    # Create an array where each cell is a colormap value RGBA 
    data_3d = np.ndarray(shape=(data.shape[0], data.shape[1], 4), dtype=float)
    for i in range(0, data.shape[0]):
        for j in range(0, data.shape[1]):
            data_3d[i][j] = color_map[data[i][j]]

    # drop the A
    data_3d_rgb = np.array([[to_rgb([v for v in row]) for row in col] for col in data_3d], dtype=np.float64)

    yticks = list(range(0,data.shape[0]))
    yticks.reverse()

    fig = px.imshow(data,
                    labels={'x':'Plant', 'y':'Node'},
                    x=list(range(1,data.shape[1]+1)),
                    y=yticks,
                    origin='lower',
                    color_continuous_scale='aggrnyl',
    #                 colorbar={}
                    )
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                      )
    return fig


def plot_waffle_matplotlib(df, layout={}, legend_name={}):
    height = layout.get('height', 18.5)
    width = layout.get('width', 10.5)
    xlabel = layout.get('xlabel', 'Plant')
    xticks = layout.get('xticks', range(0,len(df.columns)))
    xticks_label = layout.get('xticks_label', range(1,len(df.columns)+1))
    ylabel = layout.get('ylabel', '')
    yticks = layout.get('yticks', range(0,len(df.index)))
    yticks_label = layout.get('yticks_label', list(range(0,len(df.index))))
    title = layout.get('title', '')    
    
    colormap_used = plt.cm.coolwarm
    
    # Sort the variables. When variables are int or float, remove the str('') (that replaced the NaN) before sorting
    values = list(set(df.values.flatten()))
    if '' in values:
        values.remove('')
    try:
        values.sort()
    except TypeError:
        values = [str(i) for i in values]
        values.sort()
    values.insert(0,'')
    
    w_height = len(df.index)
    w_width = len(df.columns)
    color_map = {val: colormap_used(i/len(values)) for i, val in enumerate(values)}
    
    # Add the "empty" variable - and set its color as white
    color_map[''] = (1., 1., 1., 1.)
    
    data = np.array(df)
    
    # Create an array where each cell is a colormap value RGBA 
    data_3d = np.ndarray(shape=(data.shape[0], data.shape[1], 4), dtype=float)
    for i in range(0, data.shape[0]):
        for j in range(0, data.shape[1]):
            data_3d[i][j] = color_map[data[i][j]]
    
#     display the plot 
    fig, ax = plt.subplots(1,1)
    fig.set_size_inches(height, width)
    fig = ax.imshow(data_3d)

    # Get the axis.
    ax = plt.gca()

    # Minor ticks
    ax.set_xticks(np.arange(-.5, (w_width), 1), minor=True);
    ax.set_yticks(np.arange(-.5, (w_height), 1), minor=True);

    # Gridlines based on minor ticks
    ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

    # Manually constructing a legend solves your "catagorical" problem.
    legend_handles = []

    for i, val in enumerate(values):
        if val!= "":
            color_val = color_map[val]
            legend_handles.append(mpatches.Patch(color=color_val, label=legend_name.get(val, val)))

    # Add the legend. 
    plt.legend(handles=legend_handles, loc=(1,0))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.xticks(ticks=xticks, labels=xticks_label)
    plt.yticks(ticks=yticks, labels=yticks_label)
    
    plt.title(title)

    return fig


def plot_waffle(df, layout={}, legend_name={}, savepath=None, plot_func='matplotlib'):
    """
    Plot a dataframe in "waffle" shape

    layout: dict of layout parameters:
            height/width: size of the picture in inch
            x/ylabel: label of the x/y axis
            x/yticks: ticks of the x/y axis
            x/yticks_labels: labels of the ticks on the x/y axis
            title: title
    plot_func: library used for the ploting:
            matplotlib: matplotlib.pyplot.subplot.imshow
            plotly.imshow: plotly.express.imshow
            plotly.heatmap: plotly.graph_objs.heatmap
    """

    ## Axes not working - Plotly heatmap
    if plot_func=='plotly.heatmap':
        fig= plot_waffle_plotly_heatmap(df=df, layout=layout, legend_name=legend_name)

    # Plotly imshow
    elif plot_func=='plotly.imshow':
        fig= plot_waffle_plotly_imshow(df=df, layout=layout, legend_name=legend_name)

    # With matplotlib
    elif plot_func=='matplotlib':
        fig= plot_waffle_matplotlib(df=df, layout=layout, legend_name=legend_name)

    if savepath:
        plt.savefig(savepath)
    
    return fig


def plot_pie(df):
    return px.pie(df, values=df.mean(axis=0), names=df.columns)
