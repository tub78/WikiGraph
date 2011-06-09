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
        >>> WG.prune_unknown_paths()
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

        self._default_node_attributes = {"path": "unknown", "tags": []}
        #

    #
    def __repr__(self):
        """ Page names and adjacency structure """
        import numpy as np
        import networkx as nx
        import scipy as sp

        if self.num_pages() == 0:
            return "Empty WikiGraph"
        elif self.num_pages() <= 10:
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
            boolean: whether page was previously unknown
        """
        N0 = self.num_pages()
        nodename = get_basename_without_extension(filepath)
        self._graph.add_node(nodename, {'path': filepath})
        self.validate_page_attributes(nodename)
        return self.num_pages()>N0
        #

    #
    def add_tags(self):
        """ Extract tags and add as a node attribute """
        N = 0
        for nodename in self._graph.nodes(): N += self.add_page_tags(nodename)
        return N
        #

    #
    def add_page_tags(self, nodename):
        """ Extract tags and add as a node attribute """
        assert self._graph.node[nodename].has_key('path'), "Was expecting node attribute named 'path'"
        tags = get_tags_from_page(self._graph.node[nodename]['path'])
        self._graph.node[nodename]['tags'] = tags
        return len(self._graph.node[nodename]['tags'])
        #

    #
    def rm_links(self):
        """ Remove links """
        N = self._graph.number_of_edges()
        self._graph.remove_edges_from(self._graph.edges)
        return N
        #

    #
    def add_links(self):
        """ Extract links and add as edges """
        N0 = self._graph.number_of_edges()
        for nodename in self._graph.nodes(): self.add_page_links(nodename)
        N1 = self._graph.number_of_edges()
        return N1 - N0
        #

    #
    def add_page_links(self, nodename):
        """ Extract links and add as edges """
        assert self._graph.node[nodename].has_key('path'), "Was expecting node attribute named 'path'"
        linked_filenames = get_links_from_page(self._graph.node[nodename]['path'])
        # add to graph
        N = len(linked_filenames)
        self._graph.add_edges_from(zip([nodename]*N, linked_filenames))
        self.validate_attributes(linked_filenames)
        return N
        #

    #
    def validate_attributes(self, nodenames):
        """ Validate attributes from named nodes """
        for nodename in nodenames: self.validate_page_attributes(nodename)
        return True
        #

    #
    def validate_page_attributes(self, nodename):
        """ Validate attributes from node """
        defaultKeys = set(self._default_node_attributes.keys())
        nodeKeys = set(self._graph.node[nodename].keys())
        addKeys = defaultKeys.difference(nodeKeys)
        self._graph.node[nodename].update(map(lambda kk: (kk, self._default_node_attributes[kk]), addKeys))
        return True
        #




    #
    def get_node_attributes(self, name):
        """ get node attributes """
        return get_node_attributes(self._graph, name)
        #

    #
    def set_node_attributes(self, name, values):
        """ set node attributes """
        set_node_attributes(self._graph, name, values)
        return True
        #



    #
    def prune_unknown_paths(self):
        """ Remove nodes with default path attribute """
        N0 = len(self._graph)
        self._graph.remove_nodes_from([ppdat[0] for ppdat in self._graph.nodes(data=True) if ppdat[1]['path']==self._default_node_attributes['path'] ])
        N1 = len(self._graph)
        return N0 - N1
        #




    #
    def prune_ccomponents(self, N):
        """ Remove all but N largest weakly connected components from the graph """
        import networkx as nx
        N0 = len(self._graph)
        listoflistsofnodes = nx.algorithms.components.weakly_connected.weakly_connected_components(self._graph)
        Nccomps = len(listoflistsofnodes)
        Nkeep = min(N, Nccomps)
        nodes2rm = flatten_list_of_lists(listoflistsofnodes[Nkeep:Nccomps])
        self._graph.remove_nodes_from(nodes2rm)
        N1 = len(self._graph)
        return N0 - N1, Nccomps-Nkeep
        #

    #
    def prune_isolates(self):
        """ Remove isolated nodes from graph """
        import networkx as nx
        N0 = len(self._graph)
        self._graph.remove_nodes_from(nx.isolates(self._graph))
        N1 = len(self._graph)
        return N0 - N1
        #

    #
    def select_pages_by_tags(self, alltags, tagset):
        """ Return a list of pages selected by tags
        """
        if alltags:
            nodelist = [ppdat[0] for ppdat in self._graph.nodes(data=True) if tagset.issubset(set(ppdat[1]['tags']))]
        else:
            nodelist = [ppdat[0] for ppdat in self._graph.nodes(data=True) if tagset.intersection(set(ppdat[1]['tags']))]
        return nodelist
        #

    #
    def filter_by_tag(self, alltags, tagset):
        """ Filter graph using tags
        """
        N0 = len(self._graph)
        nodelist = self.select_pages_by_tags(alltags, tagset)
        self._graph = self._graph.subgraph(nodelist)
        N1 = len(self._graph)
        return N0 - N1
        #

    #
    def extract_by_tag(self, alltags, tagset):
        """ Extract subgraph using tags
        """
        if len(tagset) == 0:
            return self
        nodelist = self.select_pages_by_tags(alltags, tagset)
        return WikiGraph(self._graph.subgraph(nodelist))
        #

    #
    def draw(self, design=None, labels=False, **kwargs):
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
            nx.drawing.nx_pylab.draw_networkx(self._graph, nx.circular_layout(self._graph), labels, **kwargs)

        #
        elif design=='mpl':
            nx.drawing.nx_pylab.draw_networkx(self._graph, nx.spring_layout(self._graph), labels, **kwargs)

        #
        elif design=='spec':
            nx.drawing.nx_pylab.draw_networkx(self._graph, nx.spectral_layout(self._graph), labels, **kwargs)

        #
        elif design=='neato':
            nx.drawing.nx_pylab.draw_networkx(self._graph, nx.pydot_layout(self._graph,prog="neato"), labels, **kwargs)

        #
        elif design=='twopi':
            nx.drawing.nx_pylab.draw_networkx(self._graph, nx.pydot_layout(self._graph,prog="twopi"), labels, **kwargs)

        #
        elif design=='fdp':
            nx.drawing.nx_pylab.draw_networkx(self._graph, nx.pydot_layout(self._graph,prog="fdp"), labels, **kwargs)

        #
        elif design=='sfdp':
            nx.drawing.nx_pylab.draw_networkx(self._graph, nx.pydot_layout(self._graph,prog="sfdp"), labels, **kwargs)

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

#
def whole_number(string):
    import argparse
    value = int(string)
    if value < 0:
        msg = "Error: {} is not a whole number".format(string)
        raise argparse.ArgumentTypeError(msg)
    return value
    #

#
if __name__ == "__main__":

    #import doctest
    #doctest.testmod()

    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Analyze and visualize semantics and link structure of wiki')

    parser.add_argument('--verbosity'    , default=0                             , type=int            , help='Level of verbosity for logging')
    parser.add_argument('--directory'    , default='/Users/stu/TrunkNotes/Notes' , type=str            , help='Directory where files containing wiki pages are stored (flat)')
    parser.add_argument('--extension'    , default='.txt'                        , type=str            , help='Extension of files containing wiki pages')
    parser.add_argument('--keepunknown'  , default=False                         , action='store_true' , help='Whether to keep linked pages if no corresponding file is found')
    parser.add_argument('--keepisolates' , default=False                         , action='store_true' , help='Whether to keep isolated pages')
    parser.add_argument('--numcomponents', default=0                             , type=whole_number   , help='Number of largest connected components to keep (0 selects all)')
    parser.add_argument('--tags'         , default=[], nargs='*'                 , type=str            , help='Tags to filter')
    parser.add_argument('--alltags'      , default=False                         , action='store_true' , help='If true, only returns pages that contain ALL tags')
    parser.add_argument('--design'       , default='circ'                        , type=str            , help='The type of display to generate', \
            choices=['mpl', 'circ', 'spec', 'neato', 'twopi', 'fdp', 'sfdp'])
    parser.add_argument('--labels'       , default=False                         , action='store_true' , help='Whether to show labels in displays')

    ARGS, EXTRA_ARGS = parser.parse_known_args()

    # HACK!
    kwargs = {}
    kwargs.update(zip(EXTRA_ARGS[0:len(EXTRA_ARGS):2], map(lambda ee: float(ee), EXTRA_ARGS[1:len(EXTRA_ARGS):2])))


    print "\n\n\nTESTING>\n\n\n" + str(ARGS) + "\n\n\n"
    #print "."*30 + " PROCEEDING TO SYS.EXIT()\n\n\n"; sys.exit()

    WG = WikiGraph()
    WG.add_pages(get_files_from_path_with_ext(ARGS.directory, ARGS.extension))
    WG.add_links()

    if not(ARGS.keepunknown):
        Nrm_nodes = WG.prune_unknown_paths()
        print "Removed {} nodes with unknown paths".format(Nrm_nodes)

    WG.add_tags()

    if len(ARGS.tags) > 0:
        tagset = set(ARGS.tags)
        Nrm_nodes = WG.filter_by_tag(ARGS.alltags, tagset)
        print "Removed {} nodes not related to tags: '{}'".format(Nrm_nodes, str(ARGS.tags))

    if ARGS.numcomponents>0:
        Nrm_nodes, Nrm_comp = WG.prune_ccomponents(ARGS.numcomponents)
        print "Removed {} nodes from {} smallest components".format(Nrm_nodes, Nrm_comp)

    if not(ARGS.keepisolates):
        Nrm_nodes = WG.prune_isolates()
        print "Removed {} isolated nodes".format(Nrm_nodes)


    WG.draw(design=ARGS.design, labels=ARGS.labels, **kwargs)





