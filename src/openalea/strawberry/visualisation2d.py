from __future__ import absolute_import
from __future__ import print_function

from math import radians

from openalea.core import path
from openalea.plantgl.all import *
from openalea.mtg import *
from openalea.mtg.turtle import *

from .Visualization import plant_positions

def colors():
    """ Returns a set of predefined colors"""
    shoot_color=Material("green",Color3(0,255,0))
    vegbud_color=Material("green",Color3(0,40,0))
    initbud_color = Material("orange",Color3(255,128,0))
    floral_color= Material("red",Color3(255,0,0))

    d=dict()
    d['shoot'] = shoot_color
    d['vegbud'] = vegbud_color
    d['initbud'] = initbud_color
    d['floral'] = floral_color

    return d



###############################################################################
#                                                                             #
#                           Graphic alphabet                                  #
#                   leaf, bud, stolon, inflorescence                          #
#                                                                             #
############################################################################### 

def leaf():
    cyl = Cylinder(0.01,0.5)
    cyl2 =  AxisRotated(axis=(0,1,0), angle= radians(60.), geometry= cyl)
    cyl3 = Translated(0,0,0.5,cyl2)
    cl4= Group(cyl,cyl3)

    disc= Disc()
    disc = Translated((-.5,0,0), disc)
    disc= AxisRotated(axis=(0,1,0), angle= radians(90.), geometry= disc)

    d1 = AxisRotated(axis=(1,0,0), angle=-radians(60.), geometry=disc)
    d2 = AxisRotated(axis=(1,0,0), angle=-radians(-60.), geometry=disc)
    d3 = AxisRotated(axis=(1,0,0), angle=0., geometry=disc)
    d1= Translated(0,0,1.6,d1)
    d3= Translated(0,0,1,d3)
    d2= Translated(0,0,1.6,d2)
    d1=Scaled((0.01,0.3,0.15), d1)
    d2=Scaled((0.01,0.3,0.15), d2)
    d3=Scaled((0.01,0.15,0.3), d3)

    leaflet= Group(d1,d2,d3)
    leaflet = AxisRotated(axis=(0,1,0),angle=radians(0),geometry=leaflet)
    leaflet = AxisRotated(axis=(1,0,0),angle=radians(60),geometry=leaflet)
    leaflet = AxisRotated(axis=(0,0,1),angle=radians(90),geometry=leaflet)

    leaflet = Translated((0.2,0,0.60),leaflet)
    shape=Group(cl4,leaflet)

    return(shape)


def bud():
    sphere = Sphere(.1)
    return sphere

initiated_bud = bud


def stolon():
    cyl = Cylinder(0.01,0.5)
    cyl2 = Cylinder(0.01,0.2)
    cyl3 = Cylinder(0.01,0.2)
    cyl = AxisRotated(axis=(0,1,0), angle= radians(30.), geometry= cyl)
    cyl2 = AxisRotated(axis=(0,1,0), angle= -radians(120.), geometry= cyl2)
    cyl3 = AxisRotated(axis=(0,1,0), angle= -radians(180.), geometry= cyl3)
    cyl2= Translated((0.26,0,0.45),cyl2)
    cyl3= Translated((0.26,0,0.45),cyl3)
    sto= Group([cyl,cyl2,cyl3])

    return sto


def Inflorescence():
    box = Box(.1,0.1,0.15)
    box_axis = AxisRotated(axis=(0,1,0), angle =45.,geometry=box)
    box2 = Translated(.5,0,.8,box_axis)

    cyl = Cylinder(.01,0.5)
    cyl2 =  AxisRotated(axis=(0,1,0), angle= 45., geometry= cyl)
    cyl3 = Translated(0,0,0.5,cyl2)

    shape= Group([cyl,cyl3,box2])
    return shape

###############################################################################
#                                                                             #
#                              MTG functions                                  #
#                                                                             #
###############################################################################
def is_visible(g, v):
    """ Returns bolean value if module are visible or not
    Module are considered as visible when axis contains at least one F
    
    """
    if g.edge_type(v) == '+' and g.label(v) == 'F':
        return True
    else:
        return False


def type_of_crown(vid, g):
    """ Returns the type of crown.

    Definition of type of crown (1, 2, 3):
     - principal crown (1): label == T
     - branch_crown (2)
         parent(component_roots()[0]) : if successor() == F
     - extension_crown (3): contains(HT, ht, bt)
     - error (4)

    """
    if g.scale(vid) == 3:
        vid = g.complex(vid)

    if g.label(vid) == 'T':
        return 1
    else:
        cid = next(g.component_roots_iter(vid))
        pid = g.parent(cid)
        sid = g.Successor(pid)
        #print(sid)
        if g.label(sid) in ('F','f'):
            return 2
        elif g.label(sid) in ('bt', 'ht', 'HT'):
            return 3
        else:
            # ERROR !!!
           # print(g[cid], g[g.complex_at_scale(cid, scale=1)])
            return 4

def drawable(g):
    drawables = {}
    max_scale = g.max_scale()
    vids = g.component_roots_at_scale_iter(g.root, scale=max_scale)
    for root in vids:
        for v in traversal.pre_order2(g,root):
            pid = g.parent(v)

            if pid is not None and drawables[pid] is False:
                drawables[v] = False
            else:
                if g.edge_type(v) == '+' and g.label(pid) =='f':
                    drawables[v] = False
                else:
                    drawables[v] = True
    g.properties()['drawable'] = drawables

def visible_modules(g):
    modules =  [v for v in g.vertices_iter(scale=2) if g.label(next(g.component_roots_iter(v))) == 'F']
    _visible = {}

    for m in modules:
        _visible[m] = True
    g.properties()['visible'] = _visible

def complete_module (g):
    """Return properties incomplete or complete module
    
    Algorithm: 
     module are complete:
       if module are visible and terminated by an Inflorescence (HT) (propertie=True)
       else module are incomplete (all module terminated by ht or bt) (property=False)
       
    """
    complete = {}
    visible = g.property('visible')
    for vid in visible:
        comp = g.components(vid)
        c = comp[0]
        axis = [v for v in g.Axis(c) if v in comp]
        last = axis[-1]
        if g.label(last) == 'HT': 
            complete[vid] = True
        else:
            complete[vid] = False
            
    g.properties()['complete'] = complete


def color_code(g,complete, plantule=False):
    PLANTULE = plantule
    _complete = complete

    shoot_green = (0,255,0)
    vegetative = (0,128,0)
    initiated= (125,125,0)
    floral= (255,0,0)
    stolon= (255,255,255)

    labels = g.property('label')

# TODO: If module are incomplet module color (red) else (blue)
#       - complet module is a module finished by an inflorescence (HT)
#       - incomplet module is a module finished by terminal bud (bt) or floral bud (ht)
#  Warning: only drawing module must be take into account
    
    for v in g.vertices(scale=g.max_scale()):
        nid = g.node(v)
        if nid.label == 'F':
            if _complete:
                if nid.complex().complete:
                    nid.color= (0,0,255)
                else:
                    nid.color = (255,0,0)
 #           if PLANTULE:
 #               foliar_type= nid.Foliar_type
 #               if nid.Foliar_type =='Cotyledon':
 #                   nid.color=(0,0,255)
 #               elif nid.Foliar_type=='Unifoliate':
 #                   nid.color=(125,125,125)
            else:
                nid.color = shoot_green
        elif nid.label == 's':
            nid.color = stolon
        elif nid.label == 'bt':
            stade = nid.Stade
            if stade is None:
                nid.color = vegetative
            elif stade in ('17', '18', '19'):
                nid.color=vegetative
            elif stade == 'A':
                nid.color = initiated
            elif stade in 'BCDEFGH':
                nid.color = floral
        elif nid.label == 'ht':
            stade = nid.Stade
            if stade is None:
                nid.color = vegetative
            elif stade in ('17', '18', '19'):
                nid.color= vegetative
            elif stade == 'A':
                nid.color = initiated
            elif stade in 'BCDEFGH':
                nid.color = floral
            else:
                nid.color = (153, 102, 51)
        elif nid.label == 'HT':
            stade = nid.Stade
            if stade is None:
                nid.color = vegetative
            elif stade in ('17', '18', '19'):
                nid.color= vegetative
            else:
                nid.color = floral

# Compute the number of branch crown that are content in the upper tree
def graph_layout(g):
    """ Compute the distance between branch to minimize the overlaping between crowns. """
    branch_ratio = {}
    max_scale = g.max_scale()
    roots = [v for v in g.component_roots_at_scale(0,scale=max_scale)]
    for root in roots:
        for v in traversal.post_order2(g, root, complex=None):
            branch_ratio[v] =  sum(branch_ratio[cid] for cid in g.children(v) if g.node(cid).ramif)
            if g.label(v) =='F' and is_visible(g,v) and type_of_crown(v, g=g)!=3:
                branch_ratio[v] = 2*branch_ratio[v]+1
                g.node(v).ramif = 1
            else:
                g.node(v).ramif = max([g.node(cid).ramif for cid in g.children(v)]+[0])

    g.properties()['branch_ratio'] = branch_ratio


def my_visitor(g, v, turtle, time=0):
    turtle.setWidth(0.01)
    t = turtle
    nid = g.node(v)
    label = g.label(v)
    draw_it = nid.drawable
    branch_ratio = nid.branch_ratio

    if label in ('F','f'):
        turtle.rollL(180.)
    turtle.setId(v)

    advance = 0.5

    if not draw_it:
        pass
    elif label == 'F':
        if is_visible(g, v):
            if type_of_crown(v, g) == 3:
                turtle.rollL(180.)
                angle = 30.
                length = 0.5
            else:
                angle = 90.
                length = 1.5 * branch_ratio
             #   print('v:%d, length:%d'%(v, branch_ratio))

            turtle.down(angle)
            turtle.F(length)
            turtle.down(-angle)
        custom = leaf()
        t.customGeometry(custom)
        t.f(advance)
    elif label == 'f':
        pass
    elif label == 's':
        custom = stolon()
        t.customGeometry(custom)
    elif label == 'ht':
        # TODO: Do not draw elements
        custom = initiated_bud()
        t.customGeometry(custom)
    elif label == 'HT':
        custom = Inflorescence()
        t.customGeometry(custom)
        t.f(advance)
    elif label == 'bt':
        custom = initiated_bud()
        t.down(30.)
        t.f(0.05)
        t.customGeometry(custom)

        
###############################################################################
#                            Visualisation                                    #
###############################################################################

#TODO: add argument to choose complete/incomplet color for module

def plot2d(g, vids, dist=[5, 5, 6, 8, 8, 100], by=[], display=True, complete=False):

    scene = Scene()
    position = Vector3()
    max_scale = g.max_scale()
    visible_modules(g)
    complete_module(g)

    color_code(g,complete=complete)
    
    drawable(g)
    graph_layout(g)
    
    positions = []
    if by:
        _, positions = plant_positions(g, by=by, vids=vids)

    # print(vids)

    for i, rid in enumerate(vids):
        t = PglTurtle()

        vid = next(g.component_roots_at_scale_iter(rid, scale=max_scale))
        _scene = turtle.traverse_with_turtle(g, vid, visitor=my_visitor, turtle=t, gc=False)

        ds = _scene.todict()

        if positions:
            position = positions[i]
        else:
            position.x += dist[i]

        for shid in ds:

            for sh in ds[shid]:
                sh.geometry = Translated(position, sh.geometry)
                scene.add(sh)
                 

    if display:
        Viewer.display(scene)
    else:
        return scene

