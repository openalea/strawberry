""" Visualisation code for strawberry on MTG. """
from strawberry import Rules_production
from openalea.mtg import *
from turtle import *
from openalea.core import *
from openalea.plantgl import all as pgl


#Visualization  by plante
# Je souhaiterai l'avoir une entre plutot de type Visualise_plant( Genotype_name, Date, plant number)


def strawberry_visitor(g, v, turtle, time=0):
    """ Function that draw geometry for a given vertex. """
    geoms = Rules_production.get_symbols()
    turtle.setWidth(0.01)
    nid = g.node(v)
    label = g.label(v)

    if label in ('F','f'): 
        turtle.rollL(Rules_production.roll_angle)
    if g.edge_type(v) == '+':
        turtle.down(30)

    turtle.setId(v)
    geoms.get(label)(g, v, turtle)

#Vizalisation by genotype et par de la date
#fonction visualisation(Genotype, nb_date, nb_plante)

def visualise_plants(g, vids=[], positions=[]):
    max_scale = g.max_scale()
    t = pgl.PglTurtle()
    if not vids:
        vids = g.component_roots_at_scale(g.root, scale=max_scale)
        x = -9
        y = -12
        dx = 2.
        dy = 4.
        positions = [(x+(count%9)*dx,y+(count/9)*dy,0) for count in range(len(vids))]
    else:
        vids = [cid for vid in vids for cid in g.component_roots_at_scale_iter(vid, scale=max_scale)]

    assert len(vids) == len(positions)
    n= len(vids)

    scenes = pgl.Scene()
    for i, vid in enumerate(vids):
        #position = (x+(count%9)*dx,y+(count/9)*dy,0)
        position = positions[i]
        t = pgl.PglTurtle()
        #t.move(position)
        scene = turtle.traverse_with_turtle(g, vid, visitor=strawberry_visitor, turtle=t)

        ds = scene.todict()

        for shid in ds:
            for sh in ds[shid]:
                sh.geometry = pgl.Translated(position, sh.geometry)
                scenes.add(sh)
    return scenes
