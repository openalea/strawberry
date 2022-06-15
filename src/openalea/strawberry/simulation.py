''' Module containing used functions waiting to be integrated into a module 

example:
    import  openalea.plantgl.all as pgl
    import openalea.strawberry.simulation as sim
    %gui qt
    
    g=sim.import_csv_to_mtg(filename=["figure0_paper"],sheet_name="Feuil1", first_property="experimental_name",symbol_at_scale={'P':1,'T':2,'F':3,'f':3,'bt':3,'ht':3,'HT':3,'s':3})
    sim.plot2d_with_time(g,dist=[0],time_end=80,display=True)
'''
               
                
############### Readers ##################
from importlib.resources import path
import pandas as pd
import numpy as np
from pathlib import Path

import openalea.plantgl.all as pgl
from openalea.mtg import io
from openalea.mtg.algo import orders
import openalea.lpy as lpy
from openalea.deploy.shared_data import shared_data

import openalea.strawberry
from openalea.strawberry import visu3d

def name(f):
    """return base name without extension

    :param f: the file path
    :type f: string
    :return: basename
    :rtype: string
    """    
    return f.basename().splitext()[0]

def read_file(file,sheet_name):
    xls= pd.ExcelFile(file)
    df=pd.read_excel(xls,sheet_name=sheet_name)
    return df


def topology(df, first_property):
    # select topological part of file
    start_prop=df.columns.get_loc(first_property)
    df = df.loc[:,list(df.columns[:start_prop])]
    
    # convert in string
    array = df.fillna(-1).to_numpy() #replace na value by -1 and convert to numpy array
    
    # convert array to string
    row_index = list(range(0,array.shape[0]))
    column_index = list(range(0,array.shape[1]))
    column_start = 0
    string=[]
    
    for row in row_index:
        for column in column_index:
            if array[row,column]!=-1:
                break
        if column == column_start:
            string.append(array[row,column])
        elif column < column_start:
            string.extend([']',array[row,column]])
        else:
            string.extend(['[',array[row,column]])
        column_start = column
    
    # print(string) 
       
    string = "".join(string)
   
    # test string is correct
    def test_string_convertion(string):
        count=0
        for x in string:
            if x == "[":
                count+=1
            elif x == "]":
                count-=1

        return count
    
    if test_string_convertion(string)==0:
        return string
    else:
        print("Error in convertion dataframe to string")

def add_properties(g, df, first_property):
        start_prop=df.columns.get_loc(first_property)
        df = df.loc[:,list(df.columns[start_prop:])].replace({np.nan:None})
        df.index = np.arange(1, len(df) + 1)

        property_dict=df.to_dict()
        
        for key,value in property_dict.items():
                g.properties()[key]=value
                
        return g

def import_csv_to_mtg(filename=[], sheet_name="Feuil0", first_property="experimental_name",symbol_at_scale={'P':1,'T':2,'F':3,'f':3,'bt':3,'ht':3,'HT':3,'s':3}):
    files= shared_data(openalea.strawberry).glob('*.xlsx')
    file_path = dict((name(f),f) for f in files)
    file = dict((k,f) for k,f in file_path.items() if k in filename)
    
    if len(filename)==1:
        df= read_file(file[filename[0]],sheet_name)
        s= topology(df, first_property)
        scene = pgl.Scene()
    
        l = lpy.LsysContext()
        l.makeCurrent()
        for module in symbol_at_scale:
            l.declare(module)
    
        axialtree = lpy.AxialTree(s)
        g = io.axialtree2mtg(tree=axialtree, scale=symbol_at_scale, scene=scene)
        l.done()
    
        g= add_properties(g, df,first_property)
        g.properties()["order"]= orders(g)
        g.properties()["Stade"]= {k:str(v) for k,v in g.property("Stade").items()}

        return g
    else:
        print("multiple file is not implemented TODO")




################# Simulation ######################
import openalea.mtg.traversal as trans
from openalea.mtg.turtle import *

import openalea.strawberry.visu2d as visu2d
import openalea.strawberry.geometry as geom  
import openalea.strawberry.visu3d as viu3d


def thermal_time(g, phyllochron=5):
    """add start_tt and end_tt properties on MTG according to phyllochrone
       The aim is to determine from the phyllochron a number of leaves that have appeared on the final MTG 
       and to calculate a delta that fixes the step of appearance delta_t= phyllochron / number of leaves present 
       in order to include a dynamic of appearance 
       
       Pb: phyllochrone give the number of leaves displays
       
    Parameters
    ----------
    g : Object
        An MTG
    phyllochrone : int or float,
        the intervening period between the sequential emergence of leaves

    Returns
    -------
    Object
        An MTG containing start_tt and end_tt properties
    """
    plants= g.vertices(scale=1) # plantids
    #module_scale = 2 #module scale
    max_scale = g.max_scale() # echelle la plus elevé
    my_scale = max_scale
    
    for plant in plants: 
        
        root_id = next(g.component_roots_at_scale_iter(plant, scale=my_scale)) #vid of the first module (Trunk)
        #time=0 # init a count variable
        #last_time = time + phyllochrone # last time determine the vid of the last components
        
        for vid in trans.pre_order2(g, root_id):
            pid = g.parent(vid)
            if pid is not None:
                time = g.node(pid).end_tt
            else:
                time = 0 # to improve
            
            #time_end = time + phyllochron
            n= g.node(vid)
            n.start_tt=time
            n.end_tt=time + phyllochron
            
    return g

def strawberry_visitor3d(g,v,turtle, time):
    nid= g.node(v)
    geoms = geom.get_symbols()
    label= nid.label
    turtle=turtle
    turtle.setWidth(0.01)

    if nid.start_tt<=time<nid.end_tt:
        if g.edge_type(v)== "+":
            turtle.down(30)
        elif label in ("F","f"):
            turtle.rollL(geom.roll_angle)
    else:
        if g.edge_type(v)== "+":
            turtle.down(30)
        elif label in ("F","f"):
            turtle.rollL(geom.roll_angle)
    
    v,turtle.setId(v)
    geoms.get(label)(g, v, turtle)

def strawberry_visitor2d(g, v, turtle, time):
    geoms = geom.get_symbols2d()
    turtle.setWidth(0.01)
    nid = g.node(v)
    label = g.label(v)
    draw_it = nid.drawable
    branch_ratio = nid.branch_ratio

    if nid.start_tt<=time<nid.end_tt:
        if label in ('F','f'):
            turtle.rollL(180)

        turtle.setId(v)

        if not draw_it:
            pass
        elif (label == 'F'):
            if visu2d.is_visible(g, v):
                if visu2d.type_of_crown(v, g) == 3:
                    angle = 30.
                    length = 0.5
                else:
                    angle = 90.
                    length = 1.5 * branch_ratio

                turtle.down(angle)
                turtle.F(length)
                turtle.down(-angle)
                

        elif label in ('HT',"ht"):
            turtle.F(0.1)

        elif label == 's':
            turtle.rollL(180)
            turtle.f(0.05)
    else:
        if label in ('F','f'):
            turtle.rollL(180)

        turtle.setId(v)

        if not draw_it:
            pass
        elif (label == 'F'):
            if visu2d.is_visible(g, v):
                if visu2d.type_of_crown(v, g) == 3:
                    angle = 30.
                    length = 0.5
                else:
                    angle = 90.
                    length = 1.5 * branch_ratio

                turtle.down(angle)
                turtle.F(length)
                turtle.down(-angle)
                
        elif label =='bt':
            turtle.down(30.)
            turtle.f(0.05)
            
        elif label in ('HT',"ht"):
            turtle.F(0.1)

        elif label == 's':
            turtle.rollL(180)
            turtle.f(0.05)
        turtle.setId(v)
        geoms.get(label)(g, v, turtle)
        
def traverse_with_turtle_time(g, vid, time, visitor):
    
    turtle = pgl.PglTurtle()
    
    def push_turtle(v):
        n = g.node(v)
        try:
            start_tt = n.start_tt
            if start_tt > time:
                return False
        except: 
            pass
        if g.edge_type(v) == '+':
            turtle.push()
        return True

    def pop_turtle(v):
        n = g.node(v)
        try:
            start_tt = n.start_tt
            if start_tt > time:
                return False
        except: 
            pass
        if g.edge_type(v) == '+':
            turtle.pop()

    if g.node(vid).start_tt <= time:
        visitor(g,vid,turtle,time)

    for v in trans.pre_order2_with_filter(g, vid, None, push_turtle, pop_turtle):
        if v == vid: continue
        # Done for the leaves
        if g.node(v).start_tt > time:
            print('Do not consider ', v, time)
            continue
        visitor(g,v,turtle,time)
        
    scene=turtle.getScene()
    
    return scene



#### plot ######
def plot2d_with_time(g, vids=[],time_start=0,time_end=180,step=1 ,by=[], dist=[], complete=False, display=False):
    scene = pgl.Scene()
    position = pgl.Vector3()
    max_scale = g.max_scale()
    times=[x for x in range(time_start,time_end,step)]
        
    if not vids:
        vids= g.vertices(scale=1)
    
    positions=[]
    
    if by:
        _, positions = visu3d.plant_positions(g, by=by, vids=vids)
        
    thermal_time(g)
    visu2d.visible_modules(g)
    visu2d.complete_module(g)
    visu2d.color_code(g,complete=complete)
    visu2d.drawable(g)
    visu2d.graph_layout(g)
    
    for time in times:    
        for i, rid in enumerate(vids):
            t = pgl.PglTurtle()

            vid = next(g.component_roots_at_scale_iter(rid, scale=max_scale))
            _scene = traverse_with_turtle_time(g,vid,time,visitor=strawberry_visitor2d)

            ds = _scene.todict()
            if positions:
                position = positions[i]
            else:
                position.x += dist[i]

            for shid in ds:
                for sh in ds[shid]:
                    sh.geometry = pgl.Translated(position, sh.geometry)
                    scene.add(sh)
                    
        if display:
            pgl.Viewer.display(scene)
        else:
            return scene


def plot3d(g, by=['Sample_date'], display=True, dist=[], vids=[],time_start=0,time_end=180,step=1):
    
    scene = pgl.Scene()
    position = pgl.Vector3()
    max_scale = g.max_scale()
    times=[x for x in range(time_start,time_end,step)]
    
    if not vids:
        vids = g.vertices(scale=1)
    
    positions=[]
    
    if by:
        _, positions = visu3d.plant_positions(g, by=by, vids=vids)
        
    thermal_time(g)
    visu3d.color_code(g)
    
    for time in times:    
        for i, rid in enumerate(vids):
            t = pgl.PglTurtle()

            vid = next(g.component_roots_at_scale_iter(rid, scale=max_scale))
            _scene = traverse_with_turtle_time(g,vid,time,visitor=strawberry_visitor3d)

            ds = _scene.todict()
            if positions:
                position = positions[i]
            else:
                position.x += dist[i]

            for shid in ds:
                for sh in ds[shid]:
                    sh.geometry = pgl.Translated(position, sh.geometry)
                    scene.add(sh)
                    
    

    if display:
        pgl.Viewer.display(scene)
    else:
        return scene

