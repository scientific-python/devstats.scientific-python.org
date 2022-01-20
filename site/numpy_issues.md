---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.6
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# NumPy Monthly Report

```{code-cell} ipython3
---
:tags: [remove-cell]
---

import json
import functools
import numpy as np
from myst_nb import glue

glue = functools.partial(glue, display=False)
```

%TODO improve handling of datetimes (super annoying)

A snapshot of the development on the NumPy project in the past month

## Issues

%TODO: query_date should be synced up with the query that generates data, rather
%than specified manually

```{code-cell} ipython3
query_date = np.datetime64("2022-01-01 00:00:00")

# Load data
with open("../_data/issues.json", "r") as fh:
    issues = [item["node"] for item in json.loads(fh.read())]

glue("query_date", str(query_date))
```

### New issues

%TODO: should probably use pandas for this

```{code-cell} ipython3
---
:tags: [hide-input]
---

newly_created = [
    iss for iss in issues if np.datetime64(iss["createdAt"]) > query_date
]
num_closed = sum(iss["state"] == "CLOSED" for iss in newly_created)

glue("num_new_issues", len(newly_created))
glue("num_new_issues_closed", f"{num_closed} ({100 * num_closed / len(newly_created)}%)")
```

{glue:text}`num_new_issues` have been opened since {glue:text}`query_date`, of
which {glue:text}`num_new_issues_closed` have been closed.
