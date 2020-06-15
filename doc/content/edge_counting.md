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

%```{code-cell}
%import json
%from issues import to_ndata
%```
%
%
%The number of times a particular issue has been cross-referenced can serve as
%a rudimentary measure for how "important" the issue is.
%
%```{code-cell}
%with open('../../_data/issues.json', 'r') as fh:
%    data = to_ndata(json.load(fh))
%```
%
