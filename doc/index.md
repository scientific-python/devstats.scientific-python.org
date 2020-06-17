# Analyzing GitHub Issues

Using the [GitHub GraphQL API](https://developer.github.com/v4/) to analyze
the issue tracker for open source projects.

## Summary

### Most cross-referenced issues

The {glue:text}`num_issues` most cross-referenced issues.
Note this includes all cross-references including those from other
repositories.
See {doc}`content/edge_counting` for details.

````{admonition} Click to show/hide table
:class: toggle

```{include} content/_generated/issues_table_sortedByNumrefs
```
````

### Most cross-referenced issues (intra-repository)

The {glue:text}`num_issues` most cross-referenced issues, limited to references
originating in the same repository. See {ref}`sec:degree` for details.

````{admonition} Click to show/hide table
:class: toggle

```{include} content/_generated/degree_table.md
```
````

### Most *central* issues

A listing of issues sorted by *betweenness centrality*.
See {ref}`sec:centrality` for details.

````{admonition} Click to show/hide table
:class: toggle

```{include} content/_generated/centrality_table.md
```
````

## Details

```{toctree}
---
maxdepth: 1
---

content/edge_counting
content/basic_graph_analysis
```
