
import pandas as pd
from openalea.mtg.algo import orders


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
        for k, value in props_v.iteritems():
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

    def my_f(v):
        d = dict()
        pid = g.complex_at_scale(v, scale=1)
        pnid = g.node(pid)
        d['Genotype'] = pnid.Genotype
        d['Plante'] = pnid.Plante
        d['date'] = pnid.date
        d['label'] = g.label(v)
        
        return d


    return to_dataframe(g, vertices, my_f)

