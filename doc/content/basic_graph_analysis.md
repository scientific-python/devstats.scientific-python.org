---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.8'
    jupytext_version: 1.4.2
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Basic graph analysis

```{code-cell}
:tags: [remove-cell]

import json
from issues import to_ndata, generate_table
from myst_nb import glue
```

The {doc}`previous page <edge_counting>` demonstrated how we could derive some
information about the *issue graph* based on the structure of the query
itself.
Let's build a basic issue graph using `networkx` to see if we can derive any
insight with a slightly more detailed analysis.

```{code-cell}
import networkx as nx
```

## Building the graph

Let's model the issues as an unweighted, bidirectional graph with issues as
nodes and cross-references representing the edges.

```{code-cell}
with open("../../_data/issues.json", "r") as fh:
    data = json.load(fh)
# Create "node data" from the raw json
ndata = to_ndata(data)
# And strip the top layer of nesting from the raw json
data = [item['node'] for item in data]
```

In the previous example, we made no attempt to distinguish edges by *the 
origin of the cross-reference* -- references from other repositories were
treated the same as intra-repository references.
In this analysis, we'll focus only on intra-repository references.

```{code-cell}
nodes = [n['number'] for n in data]
edges = []
for node in data:
    for edge in node['timelineItems']['edges']:
        xref_origin = edge['node']
        # Ignore xrefs originating from other repositories
        if not xref_origin['isCrossRepository']:
            edges.append(
                (node['number'], xref_origin['source']['number'])
            )
```

Note also that we did not discriminate against *closed issues* or 
*pull requests* when compiling the list of edges.
Thus the graph we're building may contain edges to nodes that are *not* in 
`ndata`, which only comprises open issues.
This is an important thing to keep in mind for the subsequent analysis.

```{code-cell}
issue_graph = nx.Graph()
issue_graph.add_nodes_from(nodes)
issue_graph.add_edges_from(edges)
```

## Number of cross-references, redux

We can get the number of cross-references for any issue by looking at the
*degree*[^degree] of each node.
At face value, one might expect the result to be identical to the 
{ref}`edge-counting table <tbl:edge_count>`.
However, this graph only counts intra-repository references, so any issues
that were commonly linked from external repositories won't show up here.

[^degree]: The degree of a node is given by the number of edges adjacent to it.

```{code-cell}
# Limit degree calculation to nodes representing open issues
degree = dict(issue_graph.degree(nbunch=ndata.keys()))
# Sort by degree
degree = sorted(degree, key=degree.get, reverse=True)
```

Now we can look at the open issues sorted by the number of intra-respository
cross-references:

% NOTE: Work-around until myst-nb supports formatted markdown in cell outputs
```{code-cell}
:tags: [remove-cell]

md_table = generate_table(ndata, degree, num_issues=25)
with open('_generated/degree_table.md', 'w') as of:
    of.write(md_table)
```

````{admonition} Click to show/hide table
:class: toggle

```{include} _generated/degree_table.md
```
````

## Centrality

Now that we have constructed the graph model of the issues, we can use the
`networkx` utilities to look at other properties of the graph. 
For example, we can compute the *centrality* for each node in the graph
model.

```{code-cell}
centrality = nx.betweenness_centrality(issue_graph)

# Sort the nodes by centrality and limit the summary to open issues
most_central = [
    n for n in sorted(centrality, key=centrality.get, reverse=True)
    if n in ndata.keys()
]
```

```{code-cell}
:tags: [remove-cell]

md_table = generate_table(ndata, most_central, num_issues=25)
with open('_generated/centrality_table.md', 'w') as of:
    of.write(md_table)
```

````{admonition} Click to show/hide table
:class: toggle

```{include} _generated/centrality_table.md
```
````
