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
tags: [remove-input]
---
# Num merged PRs per month
start_date = today - year
bedges = np.array(
    [start_date + i * np.timedelta64(30, "D") for i in range(13)], dtype=np.datetime64
)
# Proxy date for center of bin
x = bedges[:-1] + np.timedelta64(15, "D")

fig, ax = plt.subplots(figsize=(16, 12))
ax.set_title("Merged PRs", fontsize=24)

# NOTE: np.histogram doesn't work on datetimes
for proj, data in project_prs.items():
    merged_prs = data["merged_prs"]
    merge_dates = np.array([pr["mergedAt"] for pr in merged_prs], dtype="M8[D]")
    num_merged_per_month = []
    for lo, hi in itertools.pairwise(bedges):
        num_merged_per_month.append(
            sum(1 for md in merge_dates if md > lo and md < hi)
        )
    ax.plot(x, num_merged_per_month, label=proj)
ax.legend()
plt.show()
```
