# -*- python -*-
#
#       MTG Reader of StrawBerry architecture
#
#       StrawBerry: 3D Architectural and developmental model
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.pradal@cirad.fr>
#
#       File contributor(s):
#         - Marc Labadie
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

"""
MTG strawberry Reader: Module to configurate read data informationq 
"""
from __future__ import absolute_import
from __future__ import print_function

import datetime

from openalea.mtg import MTG, fat_mtg
from openalea.mtg.algo import orders

import six
from six.moves import range
from six.moves import zip


###############################################################################
# Class Reader corresponds to the MTG.Reader interface
# TODO: Define the MTG Reader interface

class Reader(object):
    sep = ';'

    labels = {'C': (2, 'Crown'),
              'F': (3, 'Phytomer'),
              's': (2, 'Runner'),
              'b': (),
              'BT': (3, 'TerminalBud'),
              'HT': (3, 'Inflorescence'),
              }

    def __init__(self, filename):
        self.fn = filename
        self.props = []  # property names in a specific order
        self.types = []
        self.line_no = -1
        self.prop_no = -1

    def read(self):
        f = open(self.fn)
        content = f.read()
        f.close()
        self.content = [line.strip() for line in content.split('\n')]

    def header(self):
        """ Read the properties """

        sep = self.sep
        line_no = 0
        for l in self.content:
            line = [item.strip() for item in l.split(sep)]
            if line[0].startswith('Axis_') and line[1].startswith('Axis_'):
                print('\t'.join(line))
                break
            line_no += 1

        self.line_no = line_no
        self.prop_no = self.line_no

        self.props = [item.strip() for item in self.content[line_no].split(';')]

        # Rename
        props = []
        com_rank = 0
        for i, prop in enumerate(self.props):
            if prop.startswith('Axe_'):
                prop = prop.replace('Axe_', 'Axis_')
            if prop.lower().startswith('com'):
                com_rank += 1
                prop = prop.lower()[:3]+'_'+str(com_rank)
                prop = prop.capitalize()
            props.append(prop)
        self.props = props

        self.prop_index = sum(1 for p in self.props if p.startswith('Axis_')) - 1
        self.props = self.props[self.prop_index:]

    def __update_axis(self, first):
        n = len(self._axis_vid)
        if n == first:
            self._axis_vid.append(self._vid)
        elif n == first+1:
            self._axis_vid[first] = self._vid
        else:
            print(("ERROR", first, n, self._axis_vid))


    def read_line(self):
        """
        Read one line
        """

        g = self.g
        self.line_no += 1
        n = len(self.content)
        if self.line_no >= n:
            return

        l = self.content[self.line_no]
        line = [item.strip() for item in l.split(self.sep)]
        if not line:
            return

        code = line[:self.prop_index]
        props = line[self.prop_index:]

        # TODO : convert properties to their own type
        current_props = dict(zip(self.props, props))

        if not [_f for _f in code if _f]:
            return

        first = 0
        for item in code:
            if not item:
                first += 1
            else:
                break

        if first >= self.prop_index:
            return

        label = code[first]
        info = self.labels.get(label, None)

        if info is None:
            raise 'Line %d: Label %s is not managed'%(self.line_no, label)
        elif not info:
            pass
        else:
            scale, label = self.labels[label]

        prev_scale = self._scale
        prev_order = self._order

        cur_order = first

        if self._vid is None:
            assert (cur_order == 0)
            self._vid = g.add_component(g.root, label=label, **current_props)
            self._axis_vid.append(self._vid)
        elif cur_order == prev_order:
            if scale == prev_scale:
                pid = self._axis_vid[cur_order]
                self._vid = g.add_child(pid, label=label, edge_type='<', **current_props)
                self.__update_axis(first)
            else:
                # TODO
                # pid = self._axis_vid[cur_order-1]
                pass
        elif cur_order > prev_order:
            if scale == prev_scale:
                pid = self._axis_vid[prev_order]
                self._vid = g.add_child(pid, label=label, edge_type='+', **current_props)
                self.__update_axis(first)
            else:
                # TODO
                # pid = self._axis_vid[cur_order-1]
                pass
        else:
            pid = self._axis_vid[cur_order]
            self._vid = g.add_child(pid, label=label, edge_type='<', **current_props)
            self._axis_vid[cur_order] = self._vid
            if len(self._axis_vid) > cur_order:
                del self._axis_vid[cur_order+1:]

        self._order = cur_order

    def build_mtg(self):
        """ Build an MTG structure from data.

        The MTG is composed of 3 scales: Plant, Crown, Phytomer

        """
        self._axis_vid = []

        self.g = MTG()
        g = self.g

        # build 2 elements: P plante and C crown
        #self._vid = plant_id = g.add_component(g.root, label='Plant')
        # add crown
        #self._vid = g.add_component(self._vid, label='Crown')
        self._order = 0
        self._scale = 3
        self._vid = None
        #self._axis_vid.append(self._vid)

        nb_lines = len(self.content) - self.prop_no
        for i in range(nb_lines):
            #print (self._vid)
            self.read_line()

        self.g = fat_mtg(g)

    def parse(self):
        """ Read the file and build the MTG """
        self.read()
        self.header()
        self.build_mtg()
        return self.g


###############################################################################


def strawberry2mtg(fn):
    """ csv to MTG converter """
    reader = Reader(fn)
    g = reader.parse()
    return g

###############################################################################

def transform_date(g, pattern = 'date'):
    date_properties = [name for name in g.property_names_iter() if pattern in name]
    for date_property in date_properties:
        prop = g.property(date_property)
        if prop:
            myd = next(g.property(date_property).values())
            date_format = '%d-%m-%Y' if '-' in myd else '%d/%m/%Y'
            g.properties()[date_property] = dict((v, datetime.datetime.strptime(d, date_format))
                                             for v, d in g.property(date_property).items())
    return g


def load_mtg(fn):
    g = MTG(fn)
    g = transform_date(g)
    g.properties()['order'] = orders(g)

    return g
