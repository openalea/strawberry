import pandas as pd
from collections import OrderedDict, defaultdict

from openalea.mtg import stat, algo


convert = dict(Stade='Stade',
               Fleurs_ouverte='FLWRNUMBER_OPEN',
               Fleurs_avorte='FLWRNUMBER_ABORTED',
               Fleurs_total='FLWRNUMBER',
               date='Sample_date',
               Plante='Plant_ID',
              )

def property(g, name):
    """ We can change the name of the MTG properties without changing the code"""
    return g.property(convert.get(name, name))


def extract_at_plant_scale(g, convert=convert):

    orders = algo.orders(g, scale=2)

    plant_variables = _plant_variables(g)
    plant_ids = g.vertices(scale=1)
    visible_modules(g)
    compute_leaf_area(g)

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

    plant_df['leaf_area'] = [mean_leaf_area(pid, g) * sum(nb_visible_leaves(v,g) for v in g.components(pid) if v in visibles) for pid in plant_ids]
    plant_df['order_max'] = [max(orders[v] for v in g.components(pid) if v in visibles) for pid in plant_ids]
    plant_df['nb_ramifications'] = [sum(1 for v in g.components(pid) if (type_of_crown(v, g)==3 and v in visibles)) for pid in plant_ids]
    plant_df['vid'] = plant_ids

    #rajouter par Marc


    df = pd.DataFrame(plant_df)
    return df


def extract_at_module_scale(g, convert=convert):

    orders = algo.orders(g, scale=2)

    module_variables = _module_variables(g)
    visible_modules(g)

    module_ids =  list(g.property('visible'))
    #modules_ids.sort()

    module_df = OrderedDict()
    # for name in ('Genotype', 'date', 'plant'):
    #     plant_df[name] = [plant_variables[name](pid) for pid in plant_ids]
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


def _plant_variables(g):
    plant_variables = OrderedDict()
    plant_variables['nb_total_leaves'] = nb_total_leaves #Nombre total de feuille
    plant_variables['nb_total_flowers'] = nb_total_flowers #Nombre total de Fleurs
    plant_variables['nb_stolons'] = nb_stolons

    return plant_variables



###############################################################################


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
    return module_variables


################################################################################
def visible_modules(g):
    modules =  [v for v in g.vertices_iter(scale=2)
                  if g.label(g.component_roots_iter(v).next()) == 'F']
    _visible = {}
    for m in modules:
        _visible[m] = True
    g.properties()['visible'] = _visible



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


"""Return the No vegetative bud

Algorithm:
if labet is bt then stage is 17,18,19 or None
count number of bt and attach at the parent order
    """
# function return number of vegetative buds
def nb_vegetative_buds(vid, g):
    stages= property(g, 'Stade')

    def nb_vegetative(v):
        cid = g.component_roots(v)[0]

        return sum(1 for cid in g.components(v) if g.label(cid)=='bt' and stages.get(cid) in (None,'17','18','19'))

    return sum(nb_vegetative(ch) for ch in g.children(vid))


""" Return the No initiated bud"""

def nb_initiated_buds(vid, g):

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
        cid = g.component_roots_iter(vid).next()
        pid = g.parent(cid)
        sid = g.Successor(pid)
        #print sid
        if g.label(sid) in ('F', 'f'):
            return 3
        elif g.label(sid) in ('bt', 'ht', 'HT'):
            return 2
        else:
            # ERROR !!!
            print g[cid], g[g.complex_at_scale(cid, scale=1)]
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

def compute_leaf_area(g):
    _central= g.property("LFTLG_CENTRAL")
    _left= g.property("LFTLG_LEFT")
    _mean_leaf_area= g.property("LFAR")

    for v in _central:
        central = _central.get(v)
        left = _left.get(v)
        if (central is None) or (left is None):
            print("DATA is missing on vertex %d for line %d"%(v, g.node(v)._line))
            continue

        pid = g.complex_at_scale(v, scale=1)
        _mean_leaf_area[pid]= round(1.89 + (2.145 * central * left),2)


def mean_leaf_area(vid,g):
    pid = g.complex_at_scale(vid, scale=1)
    area = g.property("LFAR").get(pid, 0.)

    return area

