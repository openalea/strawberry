""" Visualisation code for strawberry on MTG. """
from __future__ import absolute_import
from __future__ import print_function

from collections import OrderedDict, defaultdict
from math import radians

from openalea.strawberry import geometry
from openalea.mtg import *
from openalea.mtg.turtle import *
from openalea.plantgl import all as pgl
from openalea.plantgl.all import *

import six
from six.moves import range


def strawberry_visitor(g, v, turtle, time=0):
    """ Function that draw geometry for a given vertex. """
    geoms = geometry.get_symbols()
    turtle.setWidth(0.01)
    nid = g.node(v)
    label = g.label(v)


    if g.edge_type(v) == '+':
        turtle.down(30)
    elif label in ('F','f', 'Cotyledon', 'Unifoliate', 'Trifoliate', 'LeafPrimordia'):
        turtle.rollL(geometry.roll_angle)

    turtle.setId(v)
    geoms.get(label)(g, v, turtle)

#Vizalisation by genotype and by date

def visualise_plants(g, vids=[], positions=[], no_plant=[], hide_leaves=False):
    geometry.WITHOUT_LEAF = hide_leaves

    max_scale = g.max_scale()
    t = pgl.PglTurtle()
    if not vids:
        vids = g.component_roots_at_scale(g.root, scale=max_scale)
        x = - no_plant
        y = -12
        dx = 2.
        dy = 4.
        positions = [(x+(count%no_plant)*dx,y+(count/no_plant)*dy,0) for count in range(len(vids))]
    else:
        #vids = [cid for vid in vids for cid in g.component_roots_at_scale_iter(vid, scale=max_scale)]
        vids = vids

    assert len(vids) == len(positions)
    n= len(vids)

    scenes = pgl.Scene()
    for i, vid in enumerate(vids):
        #position = (x+(count%9)*dx,y+(count/9)*dy,0)
        position = positions[i]
        t = pgl.PglTurtle()
        #t.move(position)
        scene = turtle.traverse_with_turtle(g, vid, visitor=strawberry_visitor, turtle=t, gc=False)

        ds = scene.todict()

        for shid in ds:
            for sh in ds[shid]:
                sh.geometry = pgl.Translated(position, sh.geometry)
                scenes.add(sh)
    return scenes


def plant_positions(g, by=['Genotype'], vids=[]):
    prop = by[0]
    nb_by = 1
    if len(by) > 1:
        nb_by = len(by)
        if len(by) > 2:
            # print("Not implemented for more than 2 properties ", by)
            pass

    # TODO: Check if the property is in the MTG

    mod = g.property(prop)
    if nb_by > 1:
        mod2 = g.property(by[1])
    my_property = OrderedDict()
    
    for k, v in mod.items():
        if vids and (k not in vids):
            continue
        if nb_by == 1:
            my_property.setdefault(v, []).append(k)
        else:
            my_property.setdefault(v, OrderedDict()).setdefault(mod2[k], []).append(k)

    my_property = OrderedDict(sorted(my_property.items(), key=lambda x: x[0]))    
    for k in my_property:
        if nb_by == 1:
            my_property[k].sort()
        else:
            old_dict = my_property[k]
            new_dict = OrderedDict(sorted(old_dict.items(), key=lambda x: x[0]))
            my_property[k] = new_dict
            for k2, v2 in new_dict.items():
                v2.sort()

    max_scale = g.max_scale()
    dx = 4.
    dy = 4.

    nb_col = len(my_property)
    max_plants = max(len(x) for x in my_property.values())

    x0 = -max_plants * dx // 2
    y0 = - nb_col * dy // 2

    x0, y0 = 0,0

    if nb_by == 1:
        vids = [next(g.component_roots_at_scale_iter(vid, scale=max_scale)) for k, v in my_property.items() for vid in v]
    else:
        vids = [next(g.component_roots_at_scale_iter(vid, scale=max_scale)) for k, d in my_property.items() for k2, v in d.items() for vid in v]


    positions = []
    x, y = x0, y0
    for genotype in my_property:
        if nb_by == 1:
            for vid in my_property[genotype]:
                position = x, y, 0.
                y += dy
                positions.append(position)
            x += dx
            y = y0
        else:
            for name2 in my_property[genotype]:
                for vid in my_property[genotype][name2]:
                    position = x, y, 0.
                    y += dy
                    positions.append(position)
                x += dx
                y = y0
            x += dx
    return vids, positions


def plot3d(g, by=['Genotype'], hide_leaves=False,display=True):

    vids, positions = plant_positions(g, by=by)
    color_code(g)
    scene = visualise_plants(g, vids=vids, positions=positions, hide_leaves=hide_leaves)
    
    if display:
        pgl.Viewer.display(scene)
    else:
        return scene


## Colors rules
def color_code(g):
    """
    Parameter:
    g: a current MTG
    
    return:
    -------
    Colloration rule of each object phytomer, inflorescence, bud, phytomer_primordia, inflo_primordia,stolon
    according to orders and stage
    """
    cleaf = (0,125,0)
    cfleaf = (255, 0, 255)
    cstolon= (0,20,0)
    labels = g.property('label')
    for v in g.vertices(scale=g.max_scale()):
        nid = g.node(v)
        if nid.label == 'F':
            nid.color = cleaf
            if nid.order == 1:
                nid.color=(255,0,0)
            elif nid.order == 2:
                nid.color=(0,0,255)
            elif nid.order == 3:
                nid.color=(255,255,0)
            elif nid.order == 4:
                nid.color=(255,0,255)
            elif nid.order == 5:
                nid.color=(0,255,255)
            elif nid.order == 6:
                nid.color=(255,255,255)
            elif nid.order >6:
                nid.color=(0, 0, 0)
        if nid.label =='f':
            nid.color = cfleaf
        elif nid.label == 's':
            nid.color = cstolon
        elif nid.label == 'bt':
            stade = nid.Stade
            if stade is None:
                nid.color = (155, 155, 155)
            elif stade in ('17', '18', '19'):
                nid.color=(0, 255,0)
            elif stade == 'A':
                nid.color = (255,0,0)
            elif stade in 'BCDEFGH':
                d = dict(zip('BCDEFGH', list(range(1, len('BCDEFGH')+1))))
                i = d[stade]
                nid.color = (255, int(127+127/7*(i-1)),0)
            else:
                nid.color = (153, 102, 51)
        elif nid.label == 'ht':
            stade = nid.Stade

            if stade is None:
                nid.color = (155, 155, 155)
            elif stade in ('17', '18', '19'):
                nid.color= (0, 255,0)
            elif stade == 'A':
                nid.color = (255,0,0)
            elif stade in 'BCDEFGH':
                d = dict(zip('BCDEFGH', list(range(1, len('BCDEFGH')+1))))
                i = d[stade]
                nid.color = (255, int(127+127/7*(i-1)),0)
            else:
                nid.color = (153, 102, 51)
        elif nid.label == 'HT':
            stade = nid.Stade
            if stade is None:
                nid.color = (155, 155, 155)
            elif stade in ('17', '18', '19'):
                nid.color=(0,0,255)
            elif stade == 'I':
                nid.color = (255,0,0)
            else:
                stades = list(map(str, list(range(55,88))))
                if stade in stades:
                    d = dict(zip(stades, list(range(len(stades)))))
                    i = d[stade]
                    nid.color = (0, int(127+127/(len(stades)-1)*(i)),255)
                else:
                    nid.color = (153, 102, 51)


# 2D visualization
#############################################################################
# TODO: add visualization functions