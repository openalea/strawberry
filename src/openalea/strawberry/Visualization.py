# """ Visualisation code for strawberry on MTG. """
# from __future__ import absolute_import
# from __future__ import print_function

# from collections import OrderedDict, defaultdict

# from openalea.strawberry import geometry
# from openalea.mtg import *
# from openalea.core import *
# from openalea.plantgl import all as pgl

# import six
# from six.moves import range



# #Visualization  by plante
# # Je souhaiterai l'avoir une entre plutot de type Visualise_plant( Genotype_name, Date, plant number)



# def strawberry_visitor(g, v, turtle, time=0):
#     """ Function that draw geometry for a given vertex. """
#     geoms = geometry.get_symbols()
#     turtle.setWidth(0.01)
#     nid = g.node(v)
#     label = g.label(v)


#     if g.edge_type(v) == '+':
#         turtle.down(30)
#     elif label in ('F','f'):
#         turtle.rollL(geometry.roll_angle)

#     turtle.setId(v)
#     geoms.get(label)(g, v, turtle)

# #Vizalisation by genotype et par de la date
# #fonction visualisation(Genotype, nb_date, nb_plante)

# def visualise_plants(g, vids=[], positions=[], no_plant=[], hide_leaves=False):
#     geometry.WITHOUT_LEAF = hide_leaves

#     max_scale = g.max_scale()
#     t = pgl.PglTurtle()
#     if not vids:
#         vids = g.component_roots_at_scale(g.root, scale=max_scale)
#         x = - no_plant
#         y = -12
#         dx = 2.
#         dy = 4.
#         positions = [(x+(count%no_plant)*dx,y+(count/no_plant)*dy,0) for count in range(len(vids))]
#     else:
#         #vids = [cid for vid in vids for cid in g.component_roots_at_scale_iter(vid, scale=max_scale)]
#         vids = vids

#     assert len(vids) == len(positions)
#     n= len(vids)

#     scenes = pgl.Scene()
#     for i, vid in enumerate(vids):
#         #position = (x+(count%9)*dx,y+(count/9)*dy,0)
#         position = positions[i]
#         t = pgl.PglTurtle()
#         #t.move(position)
#         scene = turtle.traverse_with_turtle(g, vid, visitor=strawberry_visitor, turtle=t, gc=False)

#         ds = scene.todict()

#         for shid in ds:
#             for sh in ds[shid]:
#                 sh.geometry = pgl.Translated(position, sh.geometry)
#                 scenes.add(sh)
#     return scenes


# def plant_positions(g, by=['Genotype'], vids=[]):
#     prop = by[0]
#     nb_by = 1
#     if len(by) > 1:
#         nb_by = len(by)
#         if len(by) > 2:
#             # print("Not implemented for more than 2 properties ", by)
#             pass

#     # TODO: Check if the property is in the MTG

#     mod = g.property(prop)
#     if nb_by > 1:
#         mod2 = g.property(by[1])
#     my_property = OrderedDict()
    
#     for k, v in mod.items():
#         if vids and (k not in vids):
#             continue
#         if nb_by == 1:
#             my_property.setdefault(v, []).append(k)
#         else:
#             my_property.setdefault(v, OrderedDict()).setdefault(mod2[k], []).append(k)

#     my_property = OrderedDict(sorted(my_property.items(), key=lambda x: x[0]))    
#     for k in my_property:
#         if nb_by == 1:
#             my_property[k].sort()
#         else:
#             old_dict = my_property[k]
#             new_dict = OrderedDict(sorted(old_dict.items(), key=lambda x: x[0]))
#             my_property[k] = new_dict
#             for k2, v2 in new_dict.items():
#                 v2.sort()

#     max_scale = g.max_scale()
#     dx = 4.
#     dy = 4.

#     nb_col = len(my_property)
#     max_plants = max(len(x) for x in my_property.values())

#     x0 = -max_plants * dx // 2
#     y0 = - nb_col * dy // 2

#     x0, y0 = 0,0

#     if nb_by == 1:
#         vids = [next(g.component_roots_at_scale_iter(vid, scale=max_scale)) for k, v in my_property.items() for vid in v]
#     else:
#         vids = [next(g.component_roots_at_scale_iter(vid, scale=max_scale)) for k, d in my_property.items() for k2, v in d.items() for vid in v]


#     positions = []
#     x, y = x0, y0
#     for genotype in my_property:
#         # print(genotype)
#         if nb_by == 1:
#             for vid in my_property[genotype]:
#                 position = x, y, 0.
#                 y += dy
#                 positions.append(position)
#             x += dx
#             y = y0
#         else:
#             for name2 in my_property[genotype]:
#                 # print(name2)
#                 for vid in my_property[genotype][name2]:
#                     position = x, y, 0.
#                     y += dy
#                     positions.append(position)
#                 x += dx
#                 y = y0
#             x += dx
#     return vids, positions


# def plot3d(g, by=['Genotype'], hide_leaves=False,display=True):

#     vids, positions = plant_positions(g, by=by)
#     geometry.color_code(g)
#     scene = visualise_plants(g, vids=vids, positions=positions, hide_leaves=hide_leaves)
    
#     if display:
#         pgl.Viewer.display(scene)
#     else:
#         return scene
