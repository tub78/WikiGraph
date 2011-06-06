
# approximate maximum file size in bytes
MAXFILESIZE = 30000

#
def get_files_from_path_with_ext(path, extension):
    """ Get list of filepaths from path with given extension """
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
    import re
    import itertools
    links = []
    try:
        with open(filepath) as fp:
            lines = fp.readlines(MAXFILESIZE)
        # links = flatten(map(re.findall("\[\[([^\]]*)\]\]"), lines))
        links = list(itertools.chain.from_iterable(map(lambda ll: re.findall("\[\[([^\]]*)\]\]", ll), lines)))

        # from itertools import chain 
        # l=[[1,2,3],[4,5,6], [7], [8,9]]*99
        # list(chain.from_iterable(l))

        # [item for sublist in l for item in sublist]

    except Exception:
        print "Error: Could not retrieve links."
    return links
    #


#
class WikiGraph:
    """ Blah

    _index - information about wiki pages
    _pages - ordering of pages in graph
    _graph - representation of graph


    Methods:

        num_pages()

        add_pages()
        add_page()

        update_links()

        draw_graph()

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


    Test
    >>> [0, 0, 0]
    [0, 0, 0]

    >>> A ('/Users/stu/Desktop/Dropbox/Documents/TrunkNotes/Notes', 'txt')
    [0, 0, 0]
    """
    #

    #
    def __init__(self):
        """
        """
        import scipy.sparse as scipysp
        import numpy

        # information about wiki pages
        ## self._index = {}
        # ordering of pages in graph
        ## self._pages = ()
        # representation of graph
        self._graph = nx.Graph()
        ## scipysp.coo_matrix((numpy.array([]),(numpy.array([]), numpy.array([]))),(1,1))
        #


    #
    def num_pages(self):
        """ Number of pages """
        ## return len(self._index)
        return len(self._graph)
        #

    #
    def add_pages(self, filepaths):
        """ Adds list of pages to the wiki graph

        Arguments
            filepaths: an array of filepaths
        Returns
            count_added: tuple listing number of files successfully added
        """
        count_before = self.num_pages()
        for fn in filepaths: self.add_page(fn)
        count_after = self.num_pages()
        return count_after - count_before
        #

    #
    def add_page(self, filepath):
        """ Adds a single page to the wiki graph

        Arguments
            filepath: path to a file
        Returns
            success: boolean, whether page was added successfully
        """
        import os
        filename = os.path.splitext(os.path.split(filepath)[1])[0]
        ##self._index[filename] = {'path': filepath}
        self._graph.add_node(filename, {'path': filepath})
        #
        linked_filenames = get_links_from_page(filepath)
        self._graph.add_edges_from(zip([filenames]*len(linked_filenames), linked_filenames))
        return True
        #

    #
    def update_links(self):
        """ (Re)creates the link structure by scanning all wiki pages
        Arguments
            none
        Returns
            N: number of links added
        """
        ## create frozen ordering of current pages
        ##self._pages = self._index.keys()
        ##for pp, ppdat in self._index.iteritems():
        ##    add_page_links(pp, get_links_from_page(ppdat['path']))
        #
        for pp, ppdat in self._graph.nodes(data=True).iteritems()
            linked_filenames = get_links_from_page(ppdat['path'])
            self._graph.add_edges_from(zip([pp]*len(linked_filenames), linked_filenames))
        #
        return True
        #

    #
    def __repr__(self):
        """ Page names and adjacency structure """
        ##spmat, node = nx.attr_sparse_matrix(self._graph, rc_order=range(self._graph.number_of_nodes()))
        import numpy
        return str(self._graph.nodes()) + "\n" + str(nx.convert.to_scipy_sparse_matrix(self._graph, dtype=numpy.int16))
        #

#
if __name__ == "__main__":
    #
    #import doctest
    #doctest.testmod()
    filenames = get_files_from_path_with_ext('/Users/stu/Desktop/Dropbox/Documents/TrunkNotes/Notes', 'txt')
    #
    links = get_links_from_page('/Users/stu/Desktop/Dropbox/Documents/TrunkNotes/Notes/Blog.txt')
    #
    WG = WikiGraph()
    WG.add_pages(filenames)
    #




