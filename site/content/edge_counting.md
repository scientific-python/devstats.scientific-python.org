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
:tags: [remove-cell]

import json
from issues import to_ndata, generate_top_issues_summary
from myst_nb import glue
```

The number of times a particular issue has been cross-referenced can serve as
a rudimentary measure of the "importance" of the issue.
The GraphQL API is nice in that it gives us the number of cross references
"for free" from the query itself.

The query used to acquire the data was structured in such a way that issues
themselves are treated as nodes in a graph, while the `numrefs` attribute
reflects the total number of times that each node is referenced.

```{code-cell}
:tags: [remove-cell]

with open('../../_data/issues.json', 'r') as fh:
    data = to_ndata(json.load(fh))
```

Thus reporting the most referenced issue is as simple as sorting the query
results by the `numrefs` attribute in reverse order:

```{code-block} python
---
name: code:numref_sort
caption: |
    Create a generator that returns the nodes (i.e. issues) ordered by the
    total number of times each issue is referenced.
---

# The numrefs attr is part of the data dictionary attached to each node
sorted(ndata.items(), key=lambda x: x[1]['numrefs'], reverse=True)
```

The following table is compiled using the strategy in 
{numref}`code:numref_sort`.

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

(tbl:edge_count)=
````{admonition} Click to show/hide table
:class: toggle

```{include} _generated/issues_table_sortedByNumrefs
```
````
