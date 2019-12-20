import os
import requests
import json

token = os.environ['GRAPH_API_KEY']
endpoint = r'https://api.github.com/graphql'
headers = {'Authorization': 'bearer {}'.format(token)}

def get_open_numpy_issues_with_crossrefs():
    """
    Helper function to use the graphql query example in `query_examples`
    to retrieve open numpy issues and all cross references
    """
    # Load request from examples
    with open('query_examples/open_issue_crossrefs.gql', 'r') as ff:
        req_data = ff.read()
    # Build request payload
    payload = {'query' : ''.join(req_data.split('\n'))}
    response = requests.post(endpoint, json=payload, headers=headers)
    return json.loads(response.content)

if __name__ == "__main__":
    client = QueryClient()
