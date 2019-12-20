import os
import requests
import json

token = os.environ['GRAPH_API_KEY']
endpoint = r'https://api.github.com/graphql'
headers = {'Authorization': 'bearer {}'.format(token)}

def get_open_numpy_issues_with_crossrefs(cursor=None):
    """
    Helper function to use the graphql query example in `query_examples`
    to retrieve open numpy issues and all cross references
    """
    # Load request from examples
    with open('query_examples/open_issue_crossrefs.gql', 'r') as ff:
        req_data = ff.read()
    # Modifications to request template
    # TODO: Unhack this
    if cursor is not None:
        cursor_ind = req_data.find('OPEN') + len('OPEN')
        req_data = req_data[:cursor_ind] + ' after:"{}"'.format(cursor) + req_data[cursor_ind:]
    # Build request payload
    payload = {'query' : ''.join(req_data.split('\n'))}
    response = requests.post(endpoint, json=payload, headers=headers)
    return json.loads(response.content)

def get_all_open_issues():
    """
    Helper function to bypass GitHub GraphQL API node limit.
    """
    # Get data from a single response
    inital_data = get_open_numpy_issues_with_crossrefs()
    data, last_cursor, total_num_issues = parse_single_issue_query(inital_data)
    # Continue requesting issues (with pagination) until all are acquired
    while len(data) < total_num_issues:
        rdata = get_open_numpy_issues_with_crossrefs(cursor=last_cursor)
        pdata, last_cursor, _ = parse_single_issue_query(rdata)
        data.extend(pdata)
    return data

def parse_single_issue_query(data):
    """
    Parse the raw json returned by get_open_numpy_issues_with_crossrefs.
    """
    total_num_issues = data['data']['repository']['issues']['totalCount']
    data = data['data']['repository']['issues']['edges']
    last_cursor = data[-1]['cursor']
    return data, last_cursor, total_num_issues

if __name__ == "__main__":
    client = QueryClient()
