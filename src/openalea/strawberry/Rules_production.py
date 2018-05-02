# 1. Pakages import
from openalea.deploy.shared_data import shared_data
from openalea.mtg import *
from openalea.mtg.algo import orders
from openalea.plantgl import all as pgl
from math import radians

#Properties
VISIBLE = False
WITHOUT_LEAF = False
position = (0,0,0)

## Rules of production

# 1. Phyllotaxie
roll_angle = 360.*2./5.

# 2.Phytomer
def leaflet(length=1., width=1.):
    disc = pgl.Translated((-0.5,0,0), pgl.Disc())
    disc = pgl.Scaled((length, width,1), disc)
    disc = pgl.AxisRotated(axis=(0,1,0), angle=radians(90.), geometry=disc)

    d1 = pgl.AxisRotated(axis=(1,0,0), angle=-radians(60.), geometry=disc)
    d2 = pgl.AxisRotated(axis=(1,0,0), angle=-radians(-60.), geometry=disc)
    d3 = pgl.AxisRotated(axis=(1,0,0), angle=0., geometry=disc)

    shape = pgl.Group([d1, d2, d3])
    return shape

def Phytomer(g, vid, turtle):
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
        t.customGeometry(leaflet(leaflet_length, leaflet_wdth))
    t.pop()

def Phytomer_Primordia(g, vid, turtle):
    """ F: Petiol + 3 lobes.
    cylinder + 3 ellipse/surface
    """
    scale = 1./5
    t = turtle
    nid = g.node(vid)
    order = nid.order
    t.setColor(6+order)
    t.setWidth(0.01*scale)
    # set color

    len_petiole = 1.
    len_internode = 0.1
    leaflet_length = 0.7/2.
    leaflet_wdth = 0.3/2.
    if VISIBLE:
        t.F(0.1*scale)
        t.push()
        t.down(45.)
        t.F(len_petiole*scale)
        #t.customGeometry(leaflet(leaflet_length*scale, leaflet_wdth*scale))
        t.pop()


# 3. Inflorescence

def Inflorescence(g, vid, turtle):
    """ HT: Inflorescence
    Box (may change)
    """
    t = turtle
    nid = g.node(vid)
    order = nid.order
    #turtle.setColor(3)
    nb_flower = nid.Fleurs_total
    nb_flower_open = nid.Fleurs_ouverte

    t.setColor(2+order)
    turtle.F(0.2)
    if nb_flower is None:
        nb_flower = 0.5
    if nb_flower_open is None or nb_flower_open == 0:
        nb_flower_open = 0.5

    cube = pgl.Box(0.05*pgl.Vector3(1,1,nb_flower_open/4.))
    tap = pgl.Tapered(3./20*nb_flower, 3./20*nb_flower_open, cube)
    turtle.customGeometry(tap)

def Inflo_Primordia(g, vid, turtle):
    """ ht: Primordia inflorescence
    """
    t = turtle
    #turtle.setColor(1)
    nid = g.node(vid)
    order = nid.order
    t.setColor(8+order)
    turtle.F(0.1)
    cube = pgl.Box(0.02*pgl.Vector3(1,1,1))
    turtle.customGeometry(cube)

# 4. Terminal Bud

def TerminalBud(g, vid, turtle):
    """ bt: Terminal Bud.
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

# 5. Stolon

def stolon_curve(scale=1.):
    v2 = pgl.Vector3
    ctrls = pgl.Point3Array([v2(x*scale, y*scale) for x,y in [(0,0), (1,3), (3,5), (4,2), (5,4)]])
    crv = pgl.BezierCurve2D(ctrls)
    return crv

stolon = stolon_curve(scale=.25)


def Stolon(g, vid, turtle):
	""" s: Stolon
    """
        t = turtle
    #t.setGuide(stolon, 1)
        nid = g.node(vid)
        order = nid.order
    #turtle.setColor(3)
        t.setColor(2+order)
        turtle.customGeometry(stolon)

def get_symbols():
    geoms = dict(F=Phytomer, HT=Inflorescence, bt=TerminalBud, f=Phytomer_Primordia, ht=Inflo_Primordia, s=Stolon) # dictionnary for all rules production
    return geoms

## Colors rules
def color_code(g):
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
                d = dict(zip('BCDEFGH', range(1, len('BCDEFGH')+1)))
                i = d[stade]
                nid.color = (255, 127+127/7*(i-1),0)
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
                d = dict(zip('BCDEFGH', range(1, len('BCDEFGH')+1)))
                i = d[stade]
                nid.color = (255, 127+127/7*(i-1),0)
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
                stades = map(str, range(55,88))
                if stade in stades:
                    d = dict(zip(stades, range(len(stades))))
                    i = d[stade]
                    nid.color = (0, 127+127/(len(stades)-1)*(i),255)
                else:
                    nid.color = (153, 102, 51)

