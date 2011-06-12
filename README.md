
# Introduction

_WikiGraph_ is a tool that I wrote in Python to extract and visualize the link structure from a collection of wiki pages.  It scans a wiki, extracts links and tags, filters and prunes the resulting graph, and displays the resulting graph in an attractive manner.

Several examples generated using _WikiGraph_ are included in the results directory, e.g. ![this figure][]

[this figure]: https://github.com/tub78/WikiGraph/blob/hg/results/wg-family-bicycle-work-rev2_2011-06-10_23-23-35.png
<!-- http://lh3.ggpht.com/-tlIKybACStc/TfLlhFKoh7I/AAAAAAAABHM/nVseuLoi6Lw/wg-family-bicycle-work-rev2_2011-06-10_23-23-35.jpg -->

# Assumptions

_WikiGraph_ makes several assumptions:

 1. Pages are stored at the top level of a directory with a common extension.

 1. Wiki-links are encoded using a `[[name]]` syntax, where `name` matches the linked file's basename

 1. Pages may include optional keyword metadata encoded on a header line with syntax:
    
    `^Tags: tag1 [, tag2 [, ..., tagN]]$`
    
    Tags may be used to filter the wiki to produce subgraphs of a manageable size.


# Usage

WikiGraph has many configurable parameters which are listed in uppercase in the display above.  Further details are included in the program's help text, shown below

``` text
usage: wikigraph.py [-h] [--verbosity VERBOSITY] [--directory DIRECTORY]
                    [--extension EXTENSION] [--keepunknown] [--keepisolates]
                    [--numcomponents NUMCOMPONENTS] [--tags [TAGS [TAGS ...]]]
                    [--alltags]
                    [--design {mpl,circ,spec,neato,twopi,fdp,sfdp}] [--labels]
                    [--figalpha FIGALPHA] [--figdpi {72,100,200,300}]
                    [--figtype {png,pdf,ps,eps,svg}] [--output OUTPUT]

Extract and visualize the link structure of a wiki

optional arguments:
  -h, --help            show this help message and exit
  --verbosity VERBOSITY
                        Level of verbosity for logging
  --directory DIRECTORY
                        Directory where files containing wiki pages are stored
                        (flat)
  --extension EXTENSION
                        Extension of files containing wiki pages
  --keepunknown         Whether to keep linked pages if no corresponding file
                        is found
  --keepisolates        Whether to keep isolated pages
  --numcomponents NUMCOMPONENTS
                        Number of largest connected components to keep (0
                        selects all)
  --tags [TAGS [TAGS ...]]
                        Tags to filter
  --alltags             If true, only returns pages that contain ALL tags
  --design {mpl,circ,spec,neato,twopi,fdp,sfdp}
                        The layout algorithm to use (from graphviz, etc.)
  --labels              Whether to show labels in displays
  --figalpha FIGALPHA   Transparency level for figure background
  --figdpi {72,100,200,300}
                        DPI for saved figure
  --figtype {png,pdf,ps,eps,svg}
                        Type of saved figure
  --output OUTPUT       Prefix of saved figure

Additional arguments pairs are passed to the drawing routine as keyword-values
(floats assumed).
```


# Example

The example linked above was generated with the following command:

``` bash
wikigraph.py --directory $NOTES \
             --extension txt \
             --design sfdp \
             --labels \
             --tags Fun Family Events Exercise Health TrunkNotes Python Javascript \
             --numcomponents 1 \
             --figdpi 200 \
             node_size 80 font_size 5 width 0.5 alpha 0.7
```


<!-- vim: set ft=vimwiki: -->
