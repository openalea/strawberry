
import pandas as pd
from openalea.mtg.algo import orders
import matplotlib.pyplot as plt

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

    props = g.properties()

    def my_f(v):
        d = dict()
        pid = g.complex_at_scale(v, scale=1)
        pnid = g.node(pid)
        nid = g.node(v)

        # Set plant properties to each node
        d['Genotype'] = pnid.Genotype
        d['Plante'] = pnid.Plante
        d['date'] = pnid.Sample_date
        d['label'] = g.label(v)

        # At all scale
        d['Stage'] = nid.Stade
        d['Foliar_type'] = nid.Foliar_type
        #d['prelevement'] = nid.prelevement
        #d['Fleurs_total']= nid.Fleurs_total
        #d['Fleurs_ouverte'] = nid.Fleurs_ouverte
        #d['Fleurs_avorte'] = nid.Fleurs_avorte



        return d


    return to_dataframe(g, vertices, my_f)


def write_sequences(seqs, variables, VertexIdentifiers):
    """ Write Sequences into a txt file.

    """
    sep = '\t'
    txts = []

    # header
    header = "INDEX_PARAMETER : TIME   # vertex_id"
    txts.append(header)
    txts.append('')

    n = len(variables)
    header = "%d VARIABLES"%n
    txts.append(header)
    txts.append('')

    for i in range(1, n+1):
        txts.append('VARIABLE %d: INT  # %s'%(i, variables[i-1]))

    txts.append('')
    txts.append('')
    txts.append('#Index'+sep+sep.join(variables))

    for i, seq in enumerate(seqs):
        n = len(seq)
        for j, value in enumerate(seq):
            vid = VertexIdentifiers[i][j]
            record = [str(vid)] + map(str,value)
            if j < n-1:
                record.append('\\')
            else:
                # end of the sequence
                record.append('')

            record.append('#')

            txt = sep.join(record)
            txts.append(txt)
        txts.append('')

    return '\n'.join(txts)


def median_individuals(df):
    indices = []
    for gd, dataf in df.groupby(["Genotype","date","modality"]):
        geno, date, mod = gd
        dg = dataf[df.columns[4:-1]]
        s=((dg-dg.median()).abs()/(dg-dg.median()).abs().mean()).sum(axis=1)
        indices.append(s.idxmin())

        # _min = s.min()
        # minimum_inds= s[s==_min]
    return df.iloc[indices]

def occurence_module_order_along_time(data, frequency_type):
    """
    parameters:
    -----------
        data = data at module scale 
        frequency_type = type of distribution frequency distribution (freq), probability distribution frequency (pbf) or cumulative frequency distribution (cdf)

    return:
    --------
        A dataframe with frequency, probability or cumulative frequency distribution for each module order along time
    """
    if frequency_type == "freq":
        res = pd.crosstab(index= data["order"], columns= data["date"], margins = True)
    if frequency_type == "pdf":
        res = pd.crosstab(index= data["order"], columns= data["date"], normalize = "columns")
    if frequency_type == "cdf":
        res = pd.crosstab(index= data["order"], columns= data["date"], normalize = "columns").cumsum()
    return res

def pointwisemean_plot(data_mean,data_sd,varieties, variable,title,ylab, expand=0):
    """
    parameters:
    -----------
        data_mean: panda dataframe containg mean values
        data_sd: panda dataframe containing standars error values
        varieties: names of varieties which are plot
        title: plot title
        ylab:  y axis label
        expand: allows to change xlim

    return:
    ---------
        line plot with mean value of each varieties selected 
    """

    fig, pointwise_mean = plt.subplots()
    cmap = plt.get_cmap('rainbow', len(varieties))
    for i, varietie in enumerate(varieties):
        pointwise_mean.errorbar(x=data_mean.loc[varietie].index, 
                     y=data_mean.loc[varietie][variable],
                     yerr=data_sd.loc[varietie][variable],
                     color=cmap(i), marker="p")
    pointwise_mean.legend(labels=varieties,loc='center left', bbox_to_anchor=(1, 0.5))
    pointwise_mean.set_title(title)
    pointwise_mean.set_ylabel(ylab)
    pointwise_mean.set_xlim(left=-expand, right= max(data_mean.loc[varietie].index)+expand)

    plt.show()

def crowntype_distribution(data, varieties, crown_type, plot=True,expand=0):
    """
    parameters:
    -----------
    data: panda dataframe issue from extraction of data at module scale
    varieties: names of varieties which are plot
    variable: type of branch crown (extension_crown or branch_crown)
    plot: booleen variable True or False

    return:
    -------
    a dataframe containing relative frequency values by genotype and order for extension and branch crown
    and a relative frequency distribution plot

    """
    df= pd.crosstab(index= [data.Genotype, data.order],
                    columns= data.type_of_crown,
                    normalize="index")
    
    df.columns=["Main", "extension_crown", "branch_crown"]
    
    if plot:
        cmap = plt.get_cmap('rainbow', len(varieties))
        print cmap
        
        for i, variety in enumerate(varieties): 
            
            df = df[df.index.get_level_values('order')!=0]
            
            plt.plot(df.loc[variety][crown_type],
                     marker="p", 
                     color = cmap(i))
            plt.ylabel("relative frequency")
            plt.xlabel("order")
            plt.title("Relative frequency of " + crown_type)
            plt.legend(labels=varieties,loc='center left', bbox_to_anchor=(1, 0.5))
            plt.xlim(left=1-expand, right= max(df.loc[variety].index)+expand)
            plt.ylim(bottom=0.1, top= 1.1)


    return df