import os
import requests
import json
import click

token = os.environ['GRAPH_API_KEY']
endpoint = r'https://api.github.com/graphql'
headers = {'Authorization': 'bearer {}'.format(token)}

def send_query(query_fname, cursor=None):
    """
    Helper function to use the graphql query example in `query_examples`
    to retrieve open numpy issues and all cross references
    """
    # Load request from examples
    with open(query_fname, 'r') as ff:
        req_data = ff.read()
    # Modifications to request template
    # TODO: Unhack this
    # WARNING: This hack relies on specific structure of issues query
    if cursor is not None:
        cursor_ind = req_data.find('OPEN') + len('OPEN')
        req_data = req_data[:cursor_ind] + ' after:"{}"'.format(cursor) + req_data[cursor_ind:]
    # Build request payload
    payload = {'query' : ''.join(req_data.split('\n'))}
    response = requests.post(endpoint, json=payload, headers=headers)
    return json.loads(response.content)

def get_all_responses(query_fname):
    """
    Helper function to bypass GitHub GraphQL API node limit.
    """
    # Get data from a single response
    inital_data = send_query(query_fname)
    data, last_cursor, total_num_issues = parse_single_issue_query(inital_data)
    print("Retrieving {} out of {} values...".format(len(data), total_num_issues))
    # Continue requesting issues (with pagination) until all are acquired
    while len(data) < total_num_issues:
        rdata = send_query(query_fname, cursor=last_cursor)
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

@click.command()
def cli():
    pass
