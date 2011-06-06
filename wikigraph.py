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
    """ Get list of filepaths from path with given extension
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

        validate_page_paths()

        update_links()

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
        >>> WG.validate_page_paths()
        0

    """
    #

    #
    def __init__(self):
        """ Constructor """
        import networkx as nx
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
        # add node
        self._graph.add_node(filename, {'path': filepath})
        # extract links
        linked_filenames = get_links_from_page(filepath)
        # add edges
        self._graph.add_edges_from(zip([filename]*len(linked_filenames), linked_filenames))
        return self.num_pages()>N0, len(linked_filenames)
        #


    #
    def validate_page_paths(self, keepunknown=True):
        """ Adds 'unknown' as the 'path' for nodes when attribute is missing """
        N0 = len(self._graph)
        if keepunknown:
            self._graph.add_nodes_from([ppdat[0] for ppdat in self._graph.nodes(data=True) if 'path' not in ppdat[1]], **{'path': "unknown"})
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

    #
    def draw(self):
        """ Draw the graph """
        import networkx as nx
        #import matplotlib.pyplot as plt
        #plt.figure(1,figsize=(8,8))
        #
        #nx.drawing.nx_pylab.draw_networkx(self._graph, pos=nx.spring_layout(self._graph), with_labels=True)
        #nx.drawing.nx_pylab.draw_networkx(self._graph, pos=nx.spectral_layout(self._graph), with_labels=False)
        #nx.drawing.nx_pylab.draw_networkx(self._graph, pos=nx.graphviz_layout(self._graph,prog="neato"), with_labels=False)
        nx.drawing.nx_pylab.draw_networkx(self._graph, pos=nx.circular_layout(self._graph), with_labels=False)
        #
        #plt.savefig("atlas.png",dpi=75)
        return True
        #

#
if __name__ == "__main__":
    #
    #import doctest
    #doctest.testmod()
    #
    directory = '/Users/stu/TrunkNotes/Notes'
    extension = 'txt'
    filenames = get_files_from_path_with_ext(directory, extension)
    WG = WikiGraph()
    WG.add_pages(filenames)
    WG.validate_page_paths(keepunknown=False)
    WG.draw()



