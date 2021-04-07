# 1. Pakages import
from __future__ import absolute_import

from openalea.deploy.shared_data import shared_data
from openalea.mtg import *
from openalea.mtg.algo import orders
from openalea.plantgl import all as pgl
from math import radians

from six.moves import map
from six.moves import range
from six.moves import zip


#Properties
VISIBLE = False
WITHOUT_LEAF = False
position = (0,0,0)

# Rules of production for 3D visualisation

## 1. Phyllotaxie
roll_angle = 360.*2./5.

## 2.phytomer
def leaflet(length=1., width=1.):
    """
    return 
    ------
    a strawberry leaf composed of three discs
    """
    disc = pgl.Translated((-0.5,0,0), pgl.Disc())
    disc = pgl.Scaled((length, width,1), disc)
    disc = pgl.AxisRotated(axis=(0,1,0), angle=radians(90.), geometry=disc)

    d1 = pgl.AxisRotated(axis=(1,0,0), angle=-radians(60.), geometry=disc)
    d2 = pgl.AxisRotated(axis=(1,0,0), angle=-radians(-60.), geometry=disc)
    d3 = pgl.AxisRotated(axis=(1,0,0), angle=0., geometry=disc)

    shape = pgl.Group([d1, d2, d3])
    return shape

def phytomer(g, vid, turtle):
    """ F: Petiol + 3 lobes.
    cylinder + 3 ellipse/surface
    
    parameters:
    -----------
    g: is a current MTG
    vid: vertex id in the mtg
    turtle: openalea.
    
    return:
    ---------
    for each F in mtg return an object compose of petiol (2 cylinder) and 3 lobes (leaflet)
    """
    t = turtle
    nid = g.node(vid)
    order = nid.order
    t.setColor(2+order)
    t.setWidth(0.01)

    len_petiole = 1.
    len_internode = 0.1
    leaflet_length = 0.7/2.
    leaflet_wdth = 0.3/2.

    t.F(0.1)
    #if order != 1:
    #    return
    t.push()
    t.down(45.)
    t.F(len_petiole)
    if not WITHOUT_LEAF:
        t.customGeometry(leaflet(leaflet_length, leaflet_wdth))
    t.pop()

def phytomer_primordia(g, vid, turtle):
    """ f: Petiol + 3 lobes.
    cylinder + 3 ellipse/surface
    
    parameters:
    -----------
    g: is a current MTG
    vid: vertex id in the mtg
    turtle: openalea.pltgl.turtle
    
    return:
    ---------
    for each f in mtg return an object compose of petiol (2 cylinder) and 3 lobes (leaflet)
    
    """
    scale = 1./5
    t = turtle
    nid = g.node(vid)
    order = nid.order
    t.setColor(6+order)
    t.setWidth(0.01*scale)

    len_petiole = 1.
    len_internode = 0.1
    leaflet_length = 0.7/2.
    leaflet_wdth = 0.3/2.
    if VISIBLE:
        t.F(0.1*scale)
        t.push()
        t.down(45.)
        t.F(len_petiole*scale)
        t.pop()


## 3. inflorescence

def inflorescence(g, vid, turtle):
    """ HT: inflorescence
    Box (may change)
    
    parameters:
    -----------
    g: is a current MTG
    vid: vertex id in the mtg
    turtle: openalea.pltgl.turtle
    
    return:
    ----------
    for each HT in mtg return an object compose of cylender and a blue box. 
    Shape of the box is dependent of the number of total flower and number of open flowers.
    """
    t = turtle
    nid = g.node(vid)
    order = nid.order
    nb_flower = nid.FLWRNUMBER
    nb_flower_open = nid.FLWRNUMBER_OPEN

    t.setColor(2+order)
    turtle.F(0.2)
    if nb_flower is None:
        nb_flower = 0.5
    if nb_flower_open is None or nb_flower_open == 0:
        nb_flower_open = 0.5

    cube = pgl.Box(0.05*pgl.Vector3(1,1,nb_flower_open/4.))
    tap = pgl.Tapered(3./20*nb_flower, 3./20*nb_flower_open, cube)
    turtle.customGeometry(tap)

def inflo_primordia(g, vid, turtle):
    """ ht: Primordia inflorescence
    
    parameters:
    -----------
    g: is a current MTG
    vid: vertex id in the mtg
    turtle: openalea.pltgl.turtle
    
    return:
    -------
    for each ht in mtg return an object compose of a cylinder and a of orange cube 
    """
    t = turtle
    nid = g.node(vid)
    order = nid.order
    t.setColor(8+order)
    turtle.F(0.1)
    cube = pgl.Box(0.02*pgl.Vector3(1,1,1))
    turtle.customGeometry(cube)


## 5. stolon

def stolon_curve(scale=1.):
    """
    return a curve to for symbolise a stolon
    """
    v2 = pgl.Vector3
    ctrls = pgl.Point3Array([v2(x*scale, y*scale) for x,y in [(0,0), (1,3), (3,5), (4,2), (5,4)]])
    crv = pgl.BezierCurve2D(ctrls)
    return crv

_stolon = stolon_curve(scale=.25)


def stolon(g, vid, turtle):
    """ s: stolon
    
    """
    t = turtle
    nid = g.node(vid)
    order = nid.order
    t.setColor(2+order)
    turtle.customGeometry(_stolon)


# 6. bud

def bud(g, vid, turtle):
    """ bt: Terminal bud.
    sphere
    """
    t = turtle
    #turtle.setColor(1)
    nid = g.node(vid)
    order = nid.order
    t.setColor(2+order)
    turtle.F(0.05)
    sphere = pgl.Sphere(radius=0.02)
    turtle.customGeometry(sphere)



def get_symbols():
    """
    return:
    --------
    
    a dictionnary which associate each geometrical fonction phytomer, inflorescence, TerminalBud, phytomer_primordia, inflo_primordia,stolon to F, HT, bt, ht, s
    """
    geoms = dict(F=phytomer,
                 HT=inflorescence,
                 bt=bud,
                 f=phytomer_primordia,
                 ht=inflo_primordia,
                 s=stolon,
                #  Cotyledon= unifoliate, 
                #  Unifoliate= unifoliate, 
                #  Trifoliate= trifoliate, 
                #  Bud= bud, 
                #  TerminalBud= bud
                ) # dictionnary for all rules production
    return geoms

# 6.phytomer for plantule
## 6.1 Leaflet

def trileaflet(length=1., width=1.):
    disc = pgl.Translated((-0.5,0,0), pgl.Disc())
    disc = pgl.Scaled((length, width,1), disc)
    disc = pgl.AxisRotated(axis=(0,1,0), angle=radians(90.), geometry=disc)

    d1 = pgl.AxisRotated(axis=(1,0,0), angle=-radians(60.), geometry=disc)
    d2 = pgl.AxisRotated(axis=(1,0,0), angle=-radians(-60.), geometry=disc)
    d3 = pgl.AxisRotated(axis=(1,0,0), angle=0., geometry=disc)

    shape = pgl.Group([d1, d2, d3])
    return shape

def unileaflet(length=1., width=1.):
    disc = pgl.Translated((-0.5,0,0), pgl.Disc())
    disc = pgl.Scaled((length, width,1), disc)
    disc = pgl.AxisRotated(axis=(0,1,0), angle=radians(90.), geometry=disc)

    d3 = pgl.AxisRotated(axis=(1,0,0), angle=0., geometry=disc)

    shape = pgl.Group([d3])
    return shape

## 6.2 trifoliate
def trifoliate(g, vid, turtle):
    """ F: Petiol + 3 lobes.
    cylinder + 3 ellipse/surface
    """
    t = turtle
    nid = g.node(vid)
    order = nid.order
    t.setColor(2+order)
    t.setWidth(0.01)

    len_petiole = 1.
    len_internode = 0.1
    leaflet_length = 0.7/2.
    leaflet_wdth = 0.3/2.

    t.F(0.1)
    #if order != 1:
    #    return
    t.push()
    t.down(45.)
    t.F(len_petiole)
    if not WITHOUT_LEAF:
        t.customGeometry(Trileaflet(leaflet_length, leaflet_wdth))
    t.pop()

## 6.3 unifoliate
def unifoliate(g, vid, turtle):
    """ F: Petiol + 3 lobes.
    cylinder + 3 ellipse/surface
    """
    t = turtle
    nid = g.node(vid)
    order = nid.order
    t.setColor(2+order)
    t.setWidth(0.01)

    len_petiole = 1.
    len_internode = 0.1
    leaflet_length = 0.7/2.
    leaflet_wdth = 0.3/2.

    t.F(0.1)
    #if order != 1:
    #    return
    t.push()
    t.down(45.)
    t.F(len_petiole)
    if not WITHOUT_LEAF:
        t.customGeometry(Unileaflet(leaflet_length, leaflet_wdth))
    t.pop()

