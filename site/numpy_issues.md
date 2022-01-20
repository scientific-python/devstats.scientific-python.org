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
tags: [remove-cell]
---

import json
import functools
import datetime
import warnings

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from myst_nb import glue

glue = functools.partial(glue, display=False)

warnings.filterwarnings(
    "ignore", category=DeprecationWarning, message="parsing timezone"
)
```
```{code-cell} ipython3
# For interactive plots
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import TeX
output_notebook()
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

glue("query_date", str(query_date.astype("M8[D]")))
```

### New issues

%TODO: should probably use pandas for this

```{code-cell} ipython3
---
tags: [hide-input]
---

newly_created = [
    iss for iss in issues if np.datetime64(iss["createdAt"]) > query_date
]
new_issues_closed = [iss for iss in newly_created if iss["state"] == "CLOSED"]

new_issue_lifetime = np.array(
    [
        np.datetime64(iss["closedAt"]) - np.datetime64(iss["createdAt"])
        for iss in new_issues_closed
    ],
).astype("m8[h]")  # in hours

glue("num_new_issues", len(newly_created))
glue(
    "num_new_issues_closed",
    f"{len(new_issues_closed)} ({100 * len(new_issues_closed) / len(newly_created)}%)"
)
glue("new_issue_avg_lifetime", f"{np.mean(new_issue_lifetime)}")
```

{glue:text}`num_new_issues` new issues have been opened since
{glue:text}`query_date`, of which {glue:text}`num_new_issues_closed` have been
closed.

The average lifetime of new issues that were created and closed in this period
is {glue:text}`new_issue_avg_lifetime`.

% TODO: replace with bokeh or some other live-plot
% TODO: for any remaining static/mpl plots, set default params for things
% like fontsize in a mplstyle file.

```{code-cell} ipython3
---
tags: [hide-input]
---
title = (
    f"Lifetime of issues created and closed in the last "
    f"{(np.datetime64(datetime.datetime.now()) - query_date).astype('m8[D]')}"
)
h, bedges = np.histogram(
    new_issue_lifetime.astype("m8[D]").astype(int), bins=np.arange(30)
)

p = figure(width=670, height=400, title=title, tooltips=[("value", "@top")])
p.quad(top=h, bottom=0, left=bedges[:-1], right=bedges[1:])
p.xaxis.axis_label = "Issue lifetime (days)"
p.yaxis.axis_label = TeX(r"\frac{issues}{day}")
show(p)
```

% TODO: add distribution of labels

### First responders

```{code-cell} ipython3
---
tags: [hide-input]
---
# Remove issues that are less than a day old for the following analysis
newly_created_day_old = [
    iss for iss in newly_created
    if np.datetime64(datetime.datetime.now()) - np.datetime64(iss["createdAt"])
    > np.timedelta64(1, "D")
]

# TODO: really need pandas here
first_commenters = []
for iss in newly_created_day_old:
    for e in iss["timelineItems"]["edges"]:
        if e["node"]["__typename"] == "IssueComment":
            first_commenters.append(e["node"]["author"]["login"])
            break  # Only want the first commenter

# TODO: Update IssueComment query to include:
#  - whether the commenter is a maintainer
#  - datetime of comment
# This will allow analysis of what fraction of issues are addressed by
# maintainers vs. non-maintainer, and the distribution of how long an issue
# usually sits before it's at least commented on

glue("new_issues_at_least_1_day_old", len(newly_created_day_old))
glue(
    "num_new_issues_responded",
    f"{len(first_commenters)} ({100 * len(first_commenters) / len(newly_created_day_old)}%)"
)
```

Of the {glue:text}`new_issues_at_least_1_day_old` issues that are at least 24
hours old, {glue:text}`num_new_issues_responded` of them have been commented
on.

```{code-cell} ipython3
---
tags: [hide-input]
---
first_commenter_tab = pd.DataFrame(
    {
        k: v
        for k, v in zip(
            ("Contributor", "# of times commented first"),
            np.unique(first_commenters, return_counts=True),
        )
    }
)
first_commenter_tab.sort_values(
    "# of times commented first", ascending=False
).head(10)
```
