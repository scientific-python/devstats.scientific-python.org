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

Scientific Python Devstats
==========================

This website tracks the recent development history of the Scientific Python
ecosystem.

```{toctree}
:maxdepth: 1
:hidden: true

project_reports
```

% TODO: Figure out why bokeh won't render when output_notebook is in a hidden cell

```{code-cell} ipython3
---
tags: []
---
# For interactive plots
from bokeh.plotting import figure, show, output_notebook
from bokeh.palettes import Category10_10 as palette
from bokeh.models import Legend
output_notebook()
```

% TODO: automate project generation based on which data files are in devstats-data

```{code-cell} ipython3
---
tags: [remove-cell]
---
import json
import datetime
import itertools
from dateutil.parser import isoparse
import numpy as np
import matplotlib.pyplot as plt

projects = [
    "numpy", "scipy", "matplotlib", "pandas", "scikit-learn", "scikit-image", "networkx"
]

project_prs = dict()
for proj in projects:
    with open(f"../devstats-data/{proj}_prs.json") as fh:
        data = [item["node"] for item in json.loads(fh.read())]

    # Only consider prs to the main development branch
    default_branches = {"main", "master"}
    prs = [pr for pr in data if pr["baseRefName"] in default_branches]

    # Ignore PRs with unknown author
    prs = [pr for pr in prs if pr["author"]]  # Failed author query results in None

    # Ignore bots
    bot_filter = {"dependabot-preview"}
    prs = [pr for pr in prs if pr["author"]["login"] not in bot_filter]

    # Split into merged and open
    merged_prs = [pr for pr in prs if pr["state"] == "MERGED"]
    open_prs = [pr for pr in prs if pr["state"] == "OPEN"]

    # Only look at PRs that have been created or merged in the last year
    today = np.datetime64(datetime.datetime.now(), "D")
    year = np.timedelta64(365, "D")
    merged_prs = [
        pr for pr in merged_prs
        if (today - np.datetime64(pr["mergedAt"], "D")) < year
    ]
    open_prs = [
        pr for pr in open_prs
        if (today - np.datetime64(pr["createdAt"], "D")) < year
    ]
    
    project_prs[proj] = {
        "open_prs" : open_prs,
        "merged_prs" : merged_prs,
    }
```

```{code-cell} ipython3
---
tags: [remove-cell]
---
# Num merged PRs per month
start_date = today - year
bedges = np.array(
    [start_date + i * np.timedelta64(30, "D") for i in range(13)], dtype=np.datetime64
)
# Proxy date for center of bin
x = bedges[:-1] + np.timedelta64(15, "D")

# NOTE: np.histogram doesn't work on datetimes
merged_prs_per_month = dict()
uniq_mergers_per_month = dict()
for proj, data in project_prs.items():
    # Num merged PRs per month
    merged_prs = np.array(data["merged_prs"], dtype=object)
    merge_dates = np.array([pr["mergedAt"] for pr in merged_prs], dtype="M8[D]")
    num_merged_per_month = []
    uniq_mergers = []
    for lo, hi in zip(bedges[:-1], bedges[1:]):
        month_mask = (merge_dates < hi) & (merge_dates > lo)

        # Number of PRs merged per month
        num_merged_per_month.append(month_mask.sum())

        # Number of unique maintainers who merged a PR in a given month
        mergers = {pr["mergedBy"]["login"] for pr in merged_prs[month_mask]}
        uniq_mergers.append(len(mergers))

    merged_prs_per_month[proj] = np.array(num_merged_per_month)
    uniq_mergers_per_month[proj] = np.array(uniq_mergers)
```

```{code-cell} ipython3
---
tags: [remove-input]
---
p = figure(
    width=650,
    height=400,
    title="Merged PRs per month",
    x_axis_type="datetime",
)

legend_items = []
for (label, y), color in zip(merged_prs_per_month.items(), itertools.cycle(palette)):
    l = p.line(x, y, line_width=2, color=color, muted_alpha=0.2)
    legend_items.append((label, [l]))

legend = Legend(items=legend_items, orientation="horizontal")
legend.click_policy = "mute"
p.add_layout(legend, "below")
show(p)
```

```{code-cell} ipython3
---
tags: [remove-input]
---
p = figure(
    width=650,
    height=400,
    title="Number of unique maintainers who merged at least 1 PR",
    x_axis_type="datetime",
)

legend_items = []
for (label, y), color in zip(uniq_mergers_per_month.items(), itertools.cycle(palette)):
    l = p.line(x, y, line_width=2, color=color, muted_alpha=0.2)
    legend_items.append((label, [l]))

legend = Legend(items=legend_items, orientation="horizontal")
legend.click_policy = "mute"
p.add_layout(legend, "below")
show(p)
```

```{code-cell} ipython3
---
tags: [remove-input]
---
p = figure(
    width=650,
    height=400,
    title="Avg # PRs merged per maintainer",
    x_axis_type="datetime",
)

legend_items = []
for (label, y), (_, n), color in zip(merged_prs_per_month.items(), uniq_mergers_per_month.items(), itertools.cycle(palette)):
    l = p.line(x, y / n, line_width=2, color=color, muted_alpha=0.2)
    legend_items.append((label, [l]))

legend = Legend(items=legend_items, orientation="horizontal")
legend.click_policy = "mute"
p.add_layout(legend, "below")
show(p)
```
