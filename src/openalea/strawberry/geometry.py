''' Geometric rule of production for strawberry MTG Vizualisation '''

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


def colors_turtle(turtle):
    """Set the color pallette to the turtle

    :param turtle: Turtle 
    :type turtle: Turtle
    :return: return the turtle with initiated colors
    :rtype: Turtle
    """    
    colors = [
        (80, 80, 80),
        (65,45,15),
        (30,60,10),
        (60,0,0),
        (60,60,15),
        (0,0,60),
        (60,0,60),
        (0, 128, 0),
        (127, 255, 0),
        (102, 205, 170),
        (128, 128, 0),
        (0, 255, 127),
        (34, 139, 34),
        (173, 255, 47),
        (151, 255, 151),
        (0, 128, 128)
    ]
    
    if turtle.getColorListSize() != len(colors):
        colors = [pgl.Material(ambient=c,diffuse=3) for c in colors]
        turtle.setColorList(colors)

    return turtle


# Rules of production for 3D visualisation

## 1. Phyllotaxie
roll_angle = 360.*2./5.

## 2.phytomer
def leaflet(length=1., width=1.):
    """Generate a strawberry leaf

    :param length: length of the leaflet, defaults to 1.
    :type length: float, optional
    :param width: width of the leaflet, defaults to 1.
    :type width: float, optional
    :return: A strawberry leaf composed of three discs
    :rtype: pgl.Group
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
    """Generates a phytomer 
        F: Petiol + 3 lobes.
        cylinder + 3 ellipse/surface

    :param g: MTG
    :type g: MTG
    :param vid: selected vid
    :type vid: int
    :param turtle: the turtle that travel
    :type turtle: Trutle
    :return: for each F in mtg return an object compose of petiol (2 cylinder) and 3 lobes (leaflet)
    :rtype: [type]
    """    
    t = colors_turtle(turtle)
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
    """Generates the phytomer primordia
        f: Petiol + 3 lobes.
        cylinder + 3 ellipse/surface

    :param g: MTG
    :type g: MTG
    :param vid: vid selected
    :type vid: int
    :param turtle: the Turtle that travel
    :type turtle: openalea.pltgl.turtle
    :return: for each f in mtg return an object compose of petiol (2 cylinder) and 3 lobes (leaflet)
    :rtype: [type]
    """    
    scale = 1./5
    t = colors_turtle(turtle)
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
    """Generates the inflorescences

    HT: inflorescence
    Box (may change)
    for each HT in mtg return an object compose of cylender and a blue box. 
    Shape of the box is dependent of the number of total flower and number of open flowers.

    :param g: MTG
    :type g: MTG
    :param vid: vid selected
    :type vid: int
    :param turtle: Turtle
    :type turtle: Turtle
    :return: for each HT in mtg return an object compose of cylender and a blue box. 
    :rtype: [type]
    """    
    t = colors_turtle(turtle)
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
    """Generates inflorescence primordia
        ht: Primordia inflorescence

    :param g: MTG
    :type g: MTG
    :param vid: vid selected 
    :type vid: int
    :param turtle: Turtle
    :type turtle: Turtle
    :return: for each ht in mtg return an object compose of a cylinder and a of orange cube 
    :rtype: [type]
    """    
    t = colors_turtle(turtle)
    nid = g.node(vid)
    order = nid.order
    t.setColor(8+order)
    turtle.F(0.1)
    cube = pgl.Box(0.02*pgl.Vector3(1,1,1))
    turtle.customGeometry(cube)


## 5. stolon

def stolon_curve(scale=1.):
    """Generates the stolon as curves

    :param scale: size of the stolon, defaults to 1.
    :type scale: float, optional
    :return: return a curve to for symbolise a stolon
    :rtype: plf.BezierCurve2D
    """    
    v2 = pgl.Vector3
    ctrls = pgl.Point3Array([v2(x*scale, y*scale) for x,y in [(0,0), (1,3), (3,5), (4,2), (5,4)]])
    crv = pgl.BezierCurve2D(ctrls)
    return crv




def stolon(g, vid, turtle):
    """Generates the stolons in the turtle

    :param g: MTG
    :type g: MTG
    :param vid: vid selected
    :type vid: int
    :param turtle: Turtle
    :type turtle: Turtle
    """    
    _stolon = stolon_curve(scale=.25)
    t = colors_turtle(turtle)
    nid = g.node(vid)
    order = nid.order
    t.setColor(2+order)
    turtle.customGeometry(_stolon)


# 6. bud

def bud(g, vid, turtle):
    """Generates the buds in the turtle

    :param g: MTG
    :type g: MTG
    :param vid: vid selected
    :type vid: int
    :param turtle: Turtle
    :type turtle: Turtle
    """    
    t = colors_turtle(turtle)
    #turtle.setColor(1)
    nid = g.node(vid)
    order = nid.order
    t.setColor(2+order)
    turtle.F(0.05)
    sphere = pgl.Sphere(radius=0.02)
    turtle.customGeometry(sphere)


def get_symbols():
    """Get the possible symbols to read the mtg

    :return: a dictionnary which associate each geometrical fonction phytomer, inflorescence, TerminalBud, phytomer_primordia, inflo_primordia,stolon to F, HT, bt, ht, s
    :rtype: dict
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
    """Generates a trileaflet shape

    :param length: length of the shape, defaults to 1.
    :type length: float, optional
    :param width: width of the shape, defaults to 1.
    :type width: float, optional
    :return: the shape
    :rtype: pgl.Group
    """    
    disc = pgl.Translated((-0.5,0,0), pgl.Disc())
    disc = pgl.Scaled((length, width,1), disc)
    disc = pgl.AxisRotated(axis=(0,1,0), angle=radians(90.), geometry=disc)

    d1 = pgl.AxisRotated(axis=(1,0,0), angle=-radians(60.), geometry=disc)
    d2 = pgl.AxisRotated(axis=(1,0,0), angle=-radians(-60.), geometry=disc)
    d3 = pgl.AxisRotated(axis=(1,0,0), angle=0., geometry=disc)

    shape = pgl.Group([d1, d2, d3])
    return shape


def unileaflet(length=1., width=1.):
    """Generates a unileaflet shape

    :param length: length of the shape, defaults to 1.
    :type length: float, optional
    :param width: width of the shape, defaults to 1.
    :type width: float, optional
    :return: the shape
    :rtype: pgl.Group
    """  
    disc = pgl.Translated((-0.5,0,0), pgl.Disc())
    disc = pgl.Scaled((length, width,1), disc)
    disc = pgl.AxisRotated(axis=(0,1,0), angle=radians(90.), geometry=disc)

    d3 = pgl.AxisRotated(axis=(1,0,0), angle=0., geometry=disc)

    shape = pgl.Group([d3])
    return shape


## 6.2 trifoliate
def trifoliate(g, vid, turtle):
    """Generates the trifoliate in the turtle
        F: Petiol + 3 lobes.
        cylinder + 3 ellipse/surface

    :param g: MTG
    :type g: MTG
    :param vid: vid selected
    :type vid: int
    :param turtle: Turtle
    :type turtle: Turtle
    """    
    t = colors_turtle(turtle)
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
    """Generates the unifoliate in the turtle
        F: Petiol + 3 lobes.
        cylinder + 3 ellipse/surface    

    :param g: MTG
    :type g: MTG
    :param vid: vid selected
    :type vid: int
    :param turtle: Turtle
    :type turtle: Turtle
    """    
    t = colors_turtle(turtle)
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

