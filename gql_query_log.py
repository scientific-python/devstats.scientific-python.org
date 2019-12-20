# Get github api token
import os
token = os.environ['GRAPH_API_KEY']

# Necessary stuff for constructing valid requests
import requests
import json
endpoint = r'https://api.github.com/graphql'
headers = {'Authorization': 'bearer {}'.format(token)}
    
# Get a sample gql query
with open('query_examples/open_issue_crossrefs.gql', 'r') as ff:
    req_data = ff.read()
# Turn loaded query into a properly-formatted json payload
payload = {'query' : ''.join(req_data.split('\n'))}

# Send request
response = requests.post(endpoint, json=payload, headers=headers)
print(response.status_code)
data = json.loads(response.content)
data = data['data']['repository']['issues']['edges']

# Example analysis: look at distribution of number of connections per node
import numpy as np
refcounts = np.array([line['node']['timelineItems']['totalCount'] for line in data], dtype=int)
print(np.unique(refcounts, return_counts=True))
