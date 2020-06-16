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
from issues import to_ndata, generate_top_issues_summary
from myst_nb import glue
```

The {doc}`previous page <edge_counting>` demonstrated how we could derive some
information about the *issue graph* based on the structure of the query
itself.
Let's build a basic issue graph using `networkx` to see if we can derive any
insight with a slightly more detailed analysis.

```{code-block}
import networkx as nx
```

## Building the graph

Let's model the issues as an unweighted, bidirectional graph with issues as
nodes and cross-references representing the edges.

```{code-block}
with open(../../_data/issues.json) as fh:
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

```{code-block}
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

We then instantiate the graph with an enumeration of the nodes and edges from
the raw data.

```{code-block}
issue_graph = nx.Graph()
issue_graph.add_nodes_from(nodes)
issue_graph.add_edges_from(edges)
```
