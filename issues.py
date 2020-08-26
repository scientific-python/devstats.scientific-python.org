import os
import requests
import json
import click

token = os.environ["GRAPH_API_KEY"]
endpoint = r"https://api.github.com/graphql"
headers = {"Authorization": "bearer {}".format(token)}


def load_query_from_file(fname, repo_owner="numpy", repo_name="numpy"):
    """
    Load an 'issue' query from file and set the target repository, where
    the target repository has the format:
    
    https://github.com/<repo_owner>/<repo_name>
    
    Parameters
    ----------
    fname : str
        Path to a text file containing a valid issue query according to the 
        GitHub GraphQL schema.
    repo_owner : str
        Owner of target repository on GitHub. Default is 'numpy'.
    repo_name : str
        Name of target repository on GitHub. Default is 'numpy'.
    
    Returns
    -------
    query : str
        Query loaded from file in text form suitable for ``send_query``.

    Notes
    -----
    This function expects the query to have a specific form and will not work
    for general GitHub GraphQL queries. See ``examples/`` for some valid
    templated issue queries.
    """
    with open(fname, "r") as fh:
        query = fh.read()
        # Set target repo from template
        query = query.replace("_REPO_OWNER_", repo_owner)
        query = query.replace("_REPO_NAME_", repo_name)
    return query


def send_query(query, cursor=None):
    """
    Helper function to use the graphql query example in `query_examples`
    to retrieve open numpy issues and all cross references
    """
    # Modifications to request template
    # TODO: Unhack this
    # WARNING: This hack relies on specific structure of issues query
    if cursor is not None:
        cursor_ind = query.find('OPEN') + len('OPEN')
        query = query[:cursor_ind] + ' after:"{}"'.format(cursor) + query[cursor_ind:]
    # Build request payload
    payload = {'query' : ''.join(query.split('\n'))}
    response = requests.post(endpoint, json=payload, headers=headers)
    return json.loads(response.content)

def get_all_responses(query):
    """
    Helper function to bypass GitHub GraphQL API node limit.
    """
    # Get data from a single response
    initial_data = send_query(query)
    data, last_cursor, total_num_issues = parse_single_issue_query(initial_data)
    print("Retrieving {} out of {} values...".format(len(data), total_num_issues))
    # Continue requesting issues (with pagination) until all are acquired
    while len(data) < total_num_issues:
        rdata = send_query(query, cursor=last_cursor)
        pdata, last_cursor, _ = parse_single_issue_query(rdata)
        data.extend(pdata)
        print("Retrieving {} out of {} values...".format(len(data), total_num_issues))
    print("Done.")
    return data

def parse_single_issue_query(data):
    """
    Parse the raw json returned by get_open_numpy_issues_with_crossrefs.
    """
    total_num_issues = data['data']['repository']['issues']['totalCount']
    data = data['data']['repository']['issues']['edges']
    last_cursor = data[-1]['cursor']
    return data, last_cursor, total_num_issues

def to_ndata(data):
    """
    Parse the raw json returned by a GitHub GraphQL query into an issue
    dictionary.

    Parameters
    ----------
    data : dict
        The result of `get_all_responses` or `parse_single_issue_query`

    Returns
    -------
    ndata : dict
        A dictionary of issues where the keys are the issue numbers.
        This is the data format expected by subsequent filtering/summarizing
        functions.
    """
    # Dict & list comps to decompose json
    ndata = {
        n['node']['number'] : {
            'title' : n['node']['title'],
            'url'   : n['node']['url'],
            'numrefs' : n['node']['timelineItems']['totalCount'],
            'labels'  : [lbl['node']['name'] for lbl in n['node']['labels']['edges']]
        } for n in data
    }
    return ndata

def filter_issues_by_label(ndata, labels_to_filter=("Triaged",)):
    """
    Remove nodes from parsed node data if the node's labels contain any of
    the labels in labels_to_filter

    Parameters
    ----------
    ndata : dict
        Dictionary of node data parsed from query response.
        Result of to_ndata(query_response)

    labels_to_filter : tuple
        Tuple of strings containing the names of labels to filter by

    Returns
    -------
    filtered_ndata : dict
        Dictionary of node data with specified nodes filtered out.
    """
    if type(labels_to_filter) is not tuple:
        raise TypeError('labels_to_filter must be a tuple of strings')
    lbls = set(labels_to_filter)

    return { 
        k : v for k, v in ndata.items() if len(lbls.intersection(set(v['labels']))) == 0
    }

def filter_issues_apply_blacklist(ndata, blacklist):
    """
    Remove nodes from parsed node data if the node's number (i.e. the issue
    number) is on the blacklist.

    Parameters
    ----------
    ndata : dict
        Dictionary of node data parsed from query response.
        Result of to_ndata(query_response)

    blacklist: tuple
        Tuple of ints containing the issue IDs to filter.

    Returns
    -------
    filtered_ndata : dict
        Dictionary of node data with specified nodes filtered out.
    """
    if type(blacklist) is not tuple:
        raise TypeError('blacklist bust be a tuple of integers')
    blacklist = set(blacklist)

    return {
        k : v for k, v in ndata.items() if k not in blacklist
    }

def generate_table(ndata, idx, num_issues=10):
    """
    Generate a markdown-formatted table from the first `num_issues` nodes
    in `idx`.
    """
    # Initialize table
    mdtable =  '|Iss. \#| xrefs | Issue |\n'
    mdtable += '|:-----:|:------|:------|\n'

    for issue_num in idx[:num_issues]:
        node = ndata[issue_num]
        mdtable += '|{}|{}|[{}]({})\n'.format(
            issue_num,
            node['numrefs'],
            node['title'],
            node['url']
        )
    return mdtable


def generate_top_issues_summary(ndata, num_issues=10):
    """
    Generate a markdown-formatted table of GitHub issues sorted by 
    cross-reference count.

    Parameters
    ----------
    num_issues : int
        Number of issues to include in the summary table. Default = 10.
    ndata : dict
        Dictionary of node data parsed from query repsonse.
        Result of to_ndata(query_response)

    Returns
    -------
    table : str
        A string containing a markdown-formatted table with the issue number,
        number of cross-references, and issue title/url.
    """

    # Initialize table
    mdtable =  '|Iss. \#| xrefs | Issue |\n'
    mdtable += '|:-----:|:------|:------|\n'

    # Sort data by num xrefs and generate summary
    for node in sorted(ndata.items(), key=lambda x: x[1]['numrefs'], reverse=True)[:num_issues]:
        mdtable += '|{}|{}|[{}]({})\n'.format(
            node[0],
            node[1]['numrefs'],
            node[1]['title'],
            node[1]['url']
        )
    return mdtable


class GithubIssueGrabber:
    """
    Pull down data via the GitHub APIv.4 given a valid GraphQL query.
    """

    def __init__(self, query_fname, repo_owner="numpy", repo_name="numpy"):
        """
        Create an object to send/recv queries related to the issue tracker
        for the given repository via the GitHub API v.4.

        The repository to query against is given by:
        https://github.com/<repo_owner>/<repo_name>

        Parameters
        ----------
        query_fname : str
            Path to a valid GraphQL query conforming to the GitHub GraphQL
            schema
        repo_owner : str
            Repository owner. Default is "numpy"
        repo_name : str
            Repository name. Default is "numpy"
        """
        self.query_fname = query_fname
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.raw_data = None
        self.load_query()

    def load_query(self):
        self.query = load_query_from_file(
            self.query_fname, self.repo_owner, self.repo_name
        )

    def get(self):
        """
        Get JSON-formatted raw data from the query.
        """
        self.raw_data = get_all_responses(self.query)

    def dump(self, outfile):
        """
        Dump raw json to `outfile`.
        """
        if not self.raw_data:
            raise ValueError("raw_data is currently empty, nothing to dump")

        with open(outfile, "w") as outf:
            json.dump(self.raw_data, outf)


@click.command()
def cli():
    pass


if __name__ == "__main__":
    grabber = GithubIssueGrabber('query_examples/max_issue_data.gql')
    grabber.get()
    grabber.dump("_data/issues.json")
