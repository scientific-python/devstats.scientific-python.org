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

# NumPy Report

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

def percent_val(val, denom):
    return f"{val} ({100 * val / denom:1.0f}%)"

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

A snapshot of the development on the NumPy project since {glue:text}`query_date`

## Issues

%TODO: query_date should be synced up with the query that generates data, rather
%than specified manually

```{code-cell} ipython3
query_date = np.datetime64("2020-01-01 00:00:00")

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
glue("num_new_issues_closed", percent_val(len(new_issues_closed), len(newly_created)))
glue("new_issue_median_lifetime", f"{np.median(new_issue_lifetime)}")
```

{glue:text}`num_new_issues` new issues have been opened since
{glue:text}`query_date`, of which {glue:text}`num_new_issues_closed` have been
closed.

The median lifetime of new issues that were created and closed in this period
is {glue:text}`new_issue_median_lifetime`.

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

p = figure(
    width=670,
    height=400,
    title=title,
    tooltips=[("lifetime", "@right days"), (r"# issues", "@top")],
)
p.quad(top=h, bottom=0, left=bedges[:-1], right=bedges[1:])
p.xaxis.axis_label = "Issue lifetime (days)"
p.yaxis.axis_label = "# Issues"
show(p)
```

#### Time to response

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
commented_issues = [
    iss for iss in newly_created_day_old
    if any(
        e["node"]["__typename"] == "IssueComment" for e in iss["timelineItems"]["edges"]
    )
]
first_commenters, time_to_first_comment = [], []
for iss in commented_issues:
    for e in iss["timelineItems"]["edges"]:
        if e["node"]["__typename"] == "IssueComment":
            try:
                user = e["node"]["author"]["login"]
            except TypeError as err:
                # This can happen e.g. when a user deletes their GH acct
                user = "UNKNOWN"
            first_commenters.append(user)
            dt = np.datetime64(e["node"]["createdAt"]) - np.datetime64(iss["createdAt"])
            time_to_first_comment.append(dt.astype("m8[m]"))
            break  # Only want the first commenter
time_to_first_comment = np.array(time_to_first_comment)  # in minutes

median_time_til_first_response = np.median(time_to_first_comment.astype(int) / 60)

cutoffs = [
    np.timedelta64(1, "h"),
    np.timedelta64(12, "h"),
    np.timedelta64(24, "h"),
    np.timedelta64(3, "D"),
    np.timedelta64(7, "D"),
    np.timedelta64(14, "D"),
]
num_issues_commented_by_cutoff = np.array(
    [
        np.sum(time_to_first_comment < cutoff) for cutoff in cutoffs
    ]
)

# TODO: Update IssueComment query to include:
#  - whether the commenter is a maintainer
#  - datetime of comment
# This will allow analysis of what fraction of issues are addressed by
# maintainers vs. non-maintainer, and the distribution of how long an issue
# usually sits before it's at least commented on

glue(
    "num_new_issues_responded",
    percent_val(len(commented_issues), len(newly_created_day_old))
)

glue("new_issues_at_least_1_day_old", len(newly_created_day_old))
glue("median_response_time", f"{median_time_til_first_response:1.0f}")
```

Of the {glue:text}`new_issues_at_least_1_day_old` issues that are at least 24
hours old, {glue:text}`num_new_issues_responded` of them have been commented
on.
The median time until an issue is first responded to is
{glue:text}`median_response_time` hours.

```{code-cell} ipython3
---
tags: [hide-input]
---
from bokeh.transform import dodge

title = f"Percentage of issues opened since {query_date} that are commented on within..."

x = [str(c) for c in cutoffs]
y = 100 * num_issues_commented_by_cutoff / len(newly_created_day_old)

p = figure(
    x_range=x,
    y_range=(0, 100),
    width=670,
    height=400,
    title=title,
    tooltips=[(r"%", "@top")],
)
p.vbar(x=x, top=y, width=0.8)
p.xaxis.axis_label = "Time interval"
p.yaxis.axis_label = "Percentage of issues commented on within interval"
show(p)
```

#### First responders

```{code-cell} ipython3
---
tags: [hide-input]
---
```

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

## Pull Requests

```{code-cell} ipython3
---
tags: [hide-input]
---

with open("../_data/prs.json", "r") as fh:
    data = json.loads(fh.read())
```

A look at merged PRs over time.

% TODO: This data includes backports - in the future, should limit to PRs merged
% into main only (query needs update).

```{code-cell} ipython3
---
tags: [hide-input]
---
# All contributors

merged_prs = [d for d in data if d['node']['state'] == 'MERGED']
merge_dates = np.array([r['node']['mergedAt'] for r in merged_prs], dtype=np.datetime64)
binsize = np.timedelta64(30, "D")
date_bins = np.arange(merge_dates[0], merge_dates[-1], binsize)
h_all, bedges = np.histogram(merge_dates, date_bins)
bcenters = bedges[:-1] + binsize / 2
smoothing_interval = 4  # in units of bin-width

# First-time contributors
first_time_contributor = []
prev_contrib = set()
for record in merged_prs:
    try:
        author = record['node']['author']['login']
    except TypeError:  # Author no longer has GitHub account
        first_time_contributor.append(None)
        continue
    if author not in prev_contrib:
        first_time_contributor.append(True)
        prev_contrib.add(author)
    else:
        first_time_contributor.append(False)
# Object dtype for handling None
first_time_contributor = np.array(first_time_contributor, dtype=object)
# Focus on first time contributors
ftc_mask = first_time_contributor == True
ftc_dates = merge_dates[ftc_mask]

h_ftc, bedges = np.histogram(ftc_dates, date_bins)

fig, axes = plt.subplots(1, 2, figsize=(16, 8))
for ax, h, whom in zip(
    axes.ravel(), (h_all, h_ftc), ("all contributors", "first-time contributors")
):
    ax.bar(bcenters, h, width=binsize, label="Raw")
    ax.plot(
        bcenters,
        np.convolve(h, np.ones(smoothing_interval), 'same') / smoothing_interval,
        label=f"{binsize * smoothing_interval} moving average",
        color='tab:orange',
        linewidth=2.0,
    )
 
    ax.set_title(f'{whom}')
    ax.legend()

fig.suptitle("Merged PRs from:")
axes[0].set_xlabel('Time')
axes[0].set_ylabel(f'# Merged PRs / {binsize} interval')
axes[1].set_ylim(axes[0].get_ylim())
fig.autofmt_xdate()
plt.show()
```
