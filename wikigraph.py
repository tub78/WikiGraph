"""
WikiGraph
"""

# Globals

#
# approximate maximum file size in bytes
MAXFILESIZE = 30000


# Functions

#
def flatten_list_of_lists(list_of_lists):
    """ Flatten list of lists
    Tests:
        >>> flatten_list_of_lists([])
        []
        >>> flatten_list_of_lists(['a', 'b'])
        ['a', 'b']
        >>> flatten_list_of_lists(['a', 'b', 'c', ['a1', 'b1'], [['a2.1'], ['a2.2', 'b2.2'], ['a2.3', 'b2.3', 'c2.3']]])
        ['a', 'b', 'c', 'a1', 'b1', ['a2.1'], ['a2.2', 'b2.2'], ['a2.3', 'b2.3', 'c2.3']]
    """
    import itertools
    return list(itertools.chain.from_iterable(list_of_lists))
    #

#
def get_basename_without_extension(filepath):
    """ As described
    Tests:
        >>> get_basename_without_extension('test')
        'test'
        >>> get_basename_without_extension('test.txt')
        'test'
        >>> get_basename_without_extension('/this/is/a/more/involved/test.txt')
        'test'
        >>> get_basename_without_extension('../what/../..//about///test.txt')
        'test'
    """
    import os
    return os.path.splitext(os.path.split(filepath)[1])[0]
    #

#
def get_files_from_path_with_ext(path, extension):
    """ Get list of filepaths from path with given extension
    Tests:
        >>> import os, tempfile
        >>> tmpdir = tempfile.mkdtemp(suffix='', prefix='wikigraph')
        >>> fp1 = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix='.txt', prefix='tmp', dir=tmpdir, delete=True)
        >>> fp2 = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix='.txt', prefix='tmp', dir=tmpdir, delete=True)
        >>> fp1.writelines(['Title: ' + get_basename_without_extension(fp1.name) + '\\n'])
        >>> fp2.writelines(['Title: ' + get_basename_without_extension(fp2.name) + '\\n'])
        >>> fp1.flush()
        >>> fp2.flush()
        >>> get_files_from_path_with_ext(tmpdir, 'txt').sort() == [fp1.name, fp2.name].sort()
        True

    """
    import os, glob
    filepaths = []
    try:
        # get list of filepaths
        filepaths = glob.glob(os.path.join(path, '*' + os.path.splitext('junk.' + extension)[1]))
    except Exception:
        print "Error: Could not retrieve files."
    return filepaths
    #

#
def get_links_from_page(filepath):
    """ Get list of wikilinks ("[[link]]") on page
    Tests:
        >>> import os, tempfile
        >>> tmpdir = tempfile.mkdtemp(suffix='', prefix='wikigraph')
        >>> fp1 = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix='.txt', prefix='tmp', dir=tmpdir, delete=True)
        >>> fp2 = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix='.txt', prefix='tmp', dir=tmpdir, delete=True)
        >>> fp1.writelines(['Title: ' + get_basename_without_extension(fp1.name) + '\\n', '[[' + get_basename_without_extension(fp2.name) + ']]' + '\\n'])
        >>> fp2.writelines(['Title: ' + get_basename_without_extension(fp2.name) + '\\n', '[[' + get_basename_without_extension(fp1.name) + ']]' + '\\n'])
        >>> fp1.flush()
        >>> fp2.flush()
        >>> get_links_from_page(fp2.name) + get_links_from_page(fp1.name) == [get_basename_without_extension(fp1.name), get_basename_without_extension(fp2.name)]
        True

    """
    import re
    import itertools
    links = []
    try:
        with open(filepath) as fp:
            lines = fp.readlines(MAXFILESIZE)
        # extact links - removing braces and descriptions e.g. [[Special:Header|header]] -> Special:Header
        links = flatten_list_of_lists(map(lambda ll: re.findall("\[\[([^\]\|]*)(?:\|[^\]]*)?\]\]", ll), lines))
        # remove ":" characters e.g. Special:Header -> SpecialHeader
        links = map(lambda ll: re.sub(":","",ll), links)
    except Exception:
        print "Error: Could not retrieve links."
    return links
    #

#
def get_tags_from_page(filepath):
    """ Get list of tags ("^Tags: tag1, tag2, tag3") on page
    Tests:
        >>> import os, tempfile
        >>> tmpdir = tempfile.mkdtemp(suffix='', prefix='wikigraph')
        >>> fp1 = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix='.txt', prefix='tmp', dir=tmpdir, delete=True)
        >>> fp2 = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix='.txt', prefix='tmp', dir=tmpdir, delete=True)
        >>> fp1.writelines(['Title: ' + get_basename_without_extension(fp1.name) + '\\n', 'Tags: One, ' + get_basename_without_extension(fp2.name) + ', Three' + '\\n'])
        >>> fp2.writelines(['Title: ' + get_basename_without_extension(fp2.name) + '\\n', 'Tags: Two, ' + get_basename_without_extension(fp1.name) + ', Three' + '\\n'])
        >>> fp1.flush()
        >>> fp2.flush()
        >>> get_tags_from_page(fp2.name) + get_tags_from_page(fp1.name) == ['Two', get_basename_without_extension(fp1.name), 'Three', 'One', get_basename_without_extension(fp2.name), 'Three']
        True

    """
    import re
    tags = []
    ii = 0
    try:
        with open(filepath) as fp:
            while fp and ii<20:
                ii += 1
                line = fp.readline()
                # extact tags
                tagmatch = re.match("^Tags: (.*)$", line)
                if tagmatch:
                    break
        # split
        if tagmatch:
            tags = map(lambda tt: tt.strip(), tagmatch.groups()[0].strip().split(","))
    except Exception:
        print "Error: Could not retrieve tags."
    return tags
    #


# WikiGraph Class

#
class WikiGraph:
    """ Blah

    Attributes:

        _graph - representation of graph (NetworkX), with nodes storing
        information about wiki pages

    Methods:

        __init__()
        __repr__()
        num_pages()
        add_pages()
        add_page()
        validate_page_info()
        #update_links()
        filter_by_tag()
        extract_by_tag()

        draw()

        get_page_rank()
        get_hubs_and_authorities()
        page_similarity()
        predict_missing_tags()
        predict_related_pages()
        add_tags()
        add_related_pages()
        train_topics()
        label_topics()
        label_pages()

    Tests:

        >>> [0, 0, 0]
        [0, 0, 0]

        >>> import os, tempfile
        >>> tmpdir = tempfile.mkdtemp(suffix='', prefix='wikigraph')
        >>> fp1 = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix='.txt', prefix='tmp', dir=tmpdir, delete=True)
        >>> fp2 = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix='.txt', prefix='tmp', dir=tmpdir, delete=True)
        >>> fp1.writelines(['Title: ' + get_basename_without_extension(fp1.name) + '\\n'])
        >>> fp2.writelines(['Title: ' + get_basename_without_extension(fp2.name) + '\\n'])
        >>> fp1.flush()
        >>> fp2.flush()
        >>> filenames = get_files_from_path_with_ext(tmpdir, 'txt')
        >>> WG = WikiGraph()
        >>> WG.add_pages(filenames)
        2
        >>> WG.validate_page_info()
        0

    """
    #

    #
    def __init__(self, digraph=None):
        """ Constructor """
        import networkx as nx
        if digraph:
            self._graph = digraph
        else:
            self._graph = nx.DiGraph()
        #

    #
    def __repr__(self):
        """ Page names and adjacency structure """
        import numpy as np
        import networkx as nx
        import scipy as sp
        if self.num_pages() <= 10:
            return str(self._graph.nodes()) + "\n" + str(nx.convert.to_scipy_sparse_matrix(self._graph, dtype=np.int16))
        else:
            return "Nodes: {}, Edges: {}".format(self._graph.number_of_nodes(), self._graph.number_of_edges())
        #


    #
    def num_pages(self):
        """ Number of pages """
        return len(self._graph)
        #

    #
    def add_pages(self, filepaths):
        """ Adds list of pages to the wiki graph

        Arguments
            filepaths: an array of filepaths
        Returns
            N: number of files added
        """
        N0 = self.num_pages()
        for fn in filepaths: self.add_page(fn)
        N1 = self.num_pages()
        return N1 - N0
        #

    #
    def add_page(self, filepath):
        """ Adds a single page to the wiki graph

        Arguments
            filepath: path to a file
        Returns
            (boolean, N): whether page was previously unknown, number of edges added
        """
        filename = get_basename_without_extension(filepath)
        N0 = self.num_pages()
        # extract links
        linked_filenames = get_links_from_page(filepath)
        # extract tags
        tags = get_tags_from_page(filepath)
        # add node
        self._graph.add_node(filename, {'path': filepath, 'tags': tags})
        # add edges
        self._graph.add_edges_from(zip([filename]*len(linked_filenames), linked_filenames))
        return self.num_pages()>N0, len(linked_filenames)
        #

    #
    def prune_isolates(self):
        """ Remove isolated nodes from graph """
        import networkx as nx
        N0 = len(self._graph)
        self._graph.remove_nodes_from(nx.isolates(self._graph))
        N1 = len(self._graph)
        return N1 - N0
        #

    #
    def validate_page_info(self, keepunknown=True, defaultinfo={"path": "unknown", "tags": []}):
        """ Adds 'unknown' as the 'path' for nodes when attribute is missing """
        N0 = len(self._graph)
        if keepunknown:
            self._graph.add_nodes_from([ppdat[0] for ppdat in self._graph.nodes(data=True) if 'path' not in ppdat[1]], **defaultinfo)
        else:
            self._graph.remove_nodes_from([ppdat[0] for ppdat in self._graph.nodes(data=True) if 'path' not in ppdat[1]])
        N1 = len(self._graph)
        return N1 - N0
        #


    # def update_links(self):
    #     """ (Re)creates the link structure by scanning all wiki pages
    #     Arguments
    #         none
    #     Returns
    #         N: number of links added
    #     """
    #     N0 = self._graph.number_of_edges()
    #     for ppdat in self._graph.nodes(data=True):
    #         linked_filenames = get_links_from_page(ppdat[1]['path'])
    #         self._graph.add_edges_from(zip([ppdat[0]]*len(linked_filenames), linked_filenames))
    #     N1 = self._graph.number_of_edges()
    #     return N1 - N0

    def get_pages_by_tags(self, alltags, tagset):
        """ Return a list of pages selected by tags
        """
        if alltags:
            nodelist = [ppdat[0] for ppdat in self._graph.nodes(data=True) if tagset.issubset(set(ppdat[1]['tags']))]
        else:
            nodelist = [ppdat[0] for ppdat in self._graph.nodes(data=True) if tagset.intersection(set(ppdat[1]['tags']))]
        print "tagset: {}, subgraph: {}".format(str(tagset), len(nodelist))
        return nodelist
        #

    #
    def filter_by_tag(self, alltags, tagset):
        """ Filter graph using tags
        """
        if len(tagset) == 0:
            return True
        nodelist = self.get_pages_by_tags(alltags, tagset)
        self._graph = self._graph.subgraph(nodelist)
        return True
        #

    #
    def extract_by_tag(self, alltags, tagset):
        """ Extract subgraph using tags
        """
        if len(tagset) == 0:
            return self
        nodelist = self.get_pages_by_tags(alltags, tagset)
        return WikiGraph(self._graph.subgraph(nodelist))
        #

    #
    def draw(self, design=None, labels=False):
        """ Draw the graph """
        import networkx as nx
        import matplotlib.pyplot as plt
        fig = plt.figure(1,figsize=(8,8))
        fig.clear()
        fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)


        if not(design):
            design = 'circ'

        #
        if design=='circ':
            nx.drawing.nx_pylab.draw_networkx(self._graph, pos=nx.circular_layout(self._graph), with_labels=labels)

        #
        elif design=='mpl':
            nx.drawing.nx_pylab.draw_networkx(self._graph, pos=nx.spring_layout(self._graph), with_labels=labels)

        #
        elif design=='spec':
            nx.drawing.nx_pylab.draw_networkx(self._graph, pos=nx.spectral_layout(self._graph), with_labels=labels)

        #
        elif design=='neato':
            nx.drawing.nx_pylab.draw_networkx(self._graph, pos=nx.graphviz_layout(self._graph,prog="neato"), with_labels=labels)

        #
        elif design=='twopi':
            nx.drawing.nx_pylab.draw_networkx(self._graph, pos=nx.graphviz_layout(self._graph,prog="twopi"), with_labels=labels)

        #
        elif design=='sfdp':
            nx.drawing.nx_pylab.draw_networkx(self._graph, pos=nx.graphviz_layout(self._graph,prog="sfdp"), with_labels=labels)

        #
        else:
            print "Error: design not recognized"
            return True

        plt.axis('equal')
        #plt.axis('image')
        limits = plt.axis('off') # turn of axis 
        plt.show()

        #plt.savefig("atlas.png",dpi=75)
        return True
        #

    # G : graph
    #    A networkx graph 
    # 
    # pos : dictionary, optional
    #    A dictionary with nodes as keys and positions as values.
    #    If not specified a spring layout positioning will be computed.
    #    See networkx.layout for functions that compute node positions.
    # 
    # ax : Matplotlib Axes object, optional
    #    Draw the graph in the specified Matplotlib axes.  
    # 
    # with_labels:  bool, optional       
    #    Set to True (default) to draw labels on the nodes.
    # 
    # nodelist: list, optional
    #    Draw only specified nodes (default G.nodes())
    # 
    # edgelist: list
    #    Draw only specified edges(default=G.edges())
    # 
    # node_size: scalar or array
    #    Size of nodes (default=300).  If an array is specified it must be the
    #    same length as nodelist. 
    # 
    # node_color: color string, or array of floats
    #    Node color. Can be a single color format string (default='r'),
    #    or a  sequence of colors with the same length as nodelist.
    #    If numeric values are specified they will be mapped to
    #    colors using the cmap and vmin,vmax parameters.  See
    #    matplotlib.scatter for more details.
    # 
    # node_shape:  string
    #    The shape of the node.  Specification is as matplotlib.scatter
    #    marker, one of 'so^>v<dph8' (default='o').
    # 
    # alpha: float
    #    The node transparency (default=1.0) 
    # 
    # cmap: Matplotlib colormap
    #    Colormap for mapping intensities of nodes (default=None)
    # 
    # vmin,vmax: floats
    #    Minimum and maximum for node colormap scaling (default=None)
    # 
    # width: float
    #    Line width of edges (default =1.0)
    # 
    # edge_color: color string, or array of floats
    #    Edge color. Can be a single color format string (default='r'),
    #    or a sequence of colors with the same length as edgelist.
    #    If numeric values are specified they will be mapped to
    #    colors using the edge_cmap and edge_vmin,edge_vmax parameters.
    # 
    # edge_cmap: Matplotlib colormap
    #    Colormap for mapping intensities of edges (default=None)
    # 
    # edge_vmin,edge_vmax: floats
    #    Minimum and maximum for edge colormap scaling (default=None)
    # 
    # style: string
    #    Edge line style (default='solid') (solid|dashed|dotted,dashdot)
    # 
    # labels: dictionary
    #    Node labels in a dictionary keyed by node of text labels (default=None)
    # 
    # font_size: int
    #    Font size for text labels (default=12)
    # 
    # font_color: string
    #    Font color string (default='k' black)
    # 
    # font_weight: string
    #    Font weight (default='normal')
    # 
    # font_family: string
    #    Font family (default='sans-serif')
    # 
    # Examples
    # --------
    # >>> G=nx.dodecahedral_graph()
    # >>> nx.draw(G)
    # >>> nx.draw(G,pos=nx.spring_layout(G)) # use spring layout
    # 
    # >>> import pylab
    # >>> limits=pylab.axis('off') # turn of axis 
    # 
    # Also see the NetworkX drawing examples at
    # http://networkx.lanl.gov/gallery.html
    # 
    # See Also
    # --------
    # draw()
    # draw_networkx_nodes()
    # draw_networkx_edges()
    # draw_networkx_labels()
    # draw_networkx_edge_labels()

#
if __name__ == "__main__":

    #import doctest
    #doctest.testmod()

    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Analyze and visualize semantics and link structure of wiki')

    parser.add_argument('--directory'   , default='/Users/stu/TrunkNotes/Notes' , type=str            , help='Directory where files containing wiki pages are stored (flat)')
    parser.add_argument('--extension'   , default='.txt'                        , type=str            , help='Extension of files containing wiki pages')
    parser.add_argument('--keepunknown' , default=False                         , action='store_true' , help='Whether to keep linked pages if no corresponding file is found')
    parser.add_argument('--keepisolates', default=False                         , action='store_true' , help='Whether to keep isolated pages')
    parser.add_argument('--tags'        , default=[], nargs='*'                 , type=str            , help='Tags to filter')
    parser.add_argument('--alltags'     , default=False                         , action='store_true' , help='If true, only returns pages that contain ALL tags')
    parser.add_argument('--design'      , default='circ'                        , type=str            , help='The type of display to generate', \
            choices=['mpl', 'circ', 'spec', 'neato', 'twopi', 'sfdp'])
    parser.add_argument('--labels'      , default=False                         , action='store_true' , help='Whether to show labels in displays')

    ARGS = parser.parse_args()

    print "\n\n\nTESTING>\n\n\n" + str(ARGS) + "\n\n\n............................... PROCEEDING TO SYS.EXIT()\n\n\n"
    #sys.exit()

    WG = WikiGraph()
    WG.add_pages(get_files_from_path_with_ext(ARGS.directory, ARGS.extension))
    WG.validate_page_info(keepunknown=ARGS.keepunknown)

    if len(sys.argv) > 1:
        tagset = set(ARGS.tags)
        WG.filter_by_tag(ARGS.alltags, tagset)
        #
        #WGdraw = WG.extract_by_tag(ARGS.alltags, tagset)

    if not(ARGS.keepisolates):
        print "Removed {} isolated nodes".format(-WG.prune_isolates())

    WG.draw(design=ARGS.design, labels=ARGS.labels)


# diffusion graph segmentation cuts
# pagerank, hubs and authorities, google matrix
# blockmodels
# isolates
# (strongly) connected-components
# k-NN: average degree connectivity
# degree, degree_histogram
# info
# get/set_attributes
# freeze

#
# Graphviz 
#
# bcomps   -
# ccomps   - 
# diffimg  - calculates difference between two images (by pixel) - http://www.graphviz.org/pdf/diffimg.1.pdf
# dijkstra - single source distance filter                       - http://www.graphviz.org/pdf/dijkstra.1.pdf
# gc       - analog to wc                                        - http://www.graphviz.org/pdf/gc.1.pdf
# gvcolor  - flow colors through a ranked digraph                - http://www.graphviz.org/pdf/gvcolor.1.pdf
# gvgen    - generate graphs                                     - http://www.graphviz.org/pdf/gvgen.1.pdf
# gvpack   - merge and pack disjoint graphs                      - http://www.graphviz.org/pdf/gvpack.1.pdf
# gvpr     - graph pattern scanning and processing language      - http://www.graphviz.org/pdf/gvpr.1.pdf
#
# smyrna   - viewing graphs tool
#



