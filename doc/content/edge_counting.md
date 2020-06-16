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

# Counting cross-references

```{code-cell}
:tags: [hide-cell]

import json
from issues import to_ndata, generate_top_issues_summary
from myst_nb import glue
```

The number of times a particular issue has been cross-referenced can serve as
a rudimentary measure for how "important" the issue is.
One nice thing about using the GraphQL API for obtaining the issues is that
we get a rudimentary measure of the number of edges for free from the query
itself, without having to do any extra analysis!

First, we load the data and use `to_ndata` to make the raw JSON of the query
response a bit easier to navigate.

```{code-cell}
with open('../../_data/issues.json', 'r') as fh:
    data = to_ndata(json.load(fh))
```

The query itself was structured in such a way that issues themselves are
treated as nodes in a graph model, while the `numrefs` attribute reflects the
total number of times that each node is referenced.

Thus reporting the most referenced issue is as simple as sorting the query
results by the `numrefs` attribute in reverse order.

```{code-cell}
:tags: [hide-input]

num_issues_to_display = 25
table = generate_top_issues_summary(data, num_issues=25)
with open("_generated/issues_table_sortedByNumrefs", 'w') as of:
    of.write(table)

# For referencing in text
glue("num_issues", num_issues_to_display, display=False)
```

## Top {glue:text}`num_issues` issues by number of cross-references

````{admonition} Click to show/hide table
:class: toggle

```{include} _generated/issues_table_sortedByNumrefs
:class: toggle
```
````
