# IPython log file

import os
import requests
token = os.environ['GRAPH_API_KEY']
token
endpoint = r'https://api.github.com/graphql'
headers = {'Authorization': 'bearer {}'.format(token)}
get_ipython().run_line_magic('pinfo', 'requests.post')
with open('query_examples/total_num_open_issues.json', 'r') as ff:
    req_data = ff.read()
    
req_data
print(req_data)
response = requests.post(endpoint, data=req_data, headers=headers)
response
response.data
response.headers
response.content
response = requests.post(endpoint, json=req_data, headers=headers)
response.status
response.content
req_data
import json
with open('query_examples/total_num_open_issues.json', 'r') as ff:
    req_data = json.load(ff)
    
with open('query_examples/total_num_open_issues.json', 'r') as ff:
    
    req_data = json.load(ff)
    
with open('query_examples/hello.json', 'r') as ff:
    req_data = json.load(ff)
    
req_data
response = requests.post(endpoint, data=req_data, headers=headers)
respone
response
response.content
response.headers['status']
response = requests.post(endpoint, json=req_data, headers=headers)
response.headers['status']
response.content
with open('query_examples/total_num_open_issues.json', 'r') as ff:
    req_data = json.load(ff)
    
with open('query_examples/total_num_open_issues.json', 'r') as ff:
    req_data = json.load(ff)
    
with open('query_examples/total_num_open_issues.json', 'r') as ff:
    req_data = json.load(ff)
    
req_data
with open('query_examples/total_num_open_issues.json', 'r') as ff:
    req_data = json.load(ff)
    
response = requests.post(endpoint, json=req_data, headers=headers)
response.status_code
response.content
with open('query_examples/total_num_open_issues.json', 'r') as ff:
    req_data = ff.read()
    
req_dat
req_data
with open('query_examples/num_crossreferences_in_first_100_issues.json'', 'r') as ff:
    req_data = ff.read()
    
with open('query_examples/num_crossreferences_in_first_100_issues.json', 'r') as ff:
    req_data = ff.read()
    
req_data
req_data.strip("\n")
req_data.replace("\n", "")
req_data = "{ \"query\" : " + req_data.replace("\n", "") + "}"
req_data
with open('query_examples/num_crossreferences_in_first_100_issues.json', 'r') as ff:
    req_data = json.load(ff)
    
with open('query_examples/num_crossreferences_in_first_100_issues.json', 'r') as ff:
    req_data = ff.read()
    
print(req_data)
print(req_data.replace("\n", ""))
req_data = "{ \"query\" : \"" + req_data.replace("\n", "") + "\"}"
print(req_data)
req_data = "{ \"query\" : \"" + req_data.replace("\n", "").replace(" ", "") + "\"}"
print(req_data)
with open('query_examples/num_crossreferences_in_first_100_issues.json', 'r') as ff:
    req_data = ff.read()
    
req_data = "{ \"query\" : \"" + req_data.replace("\n", "") + "\"}"
req_data
response = requests.post(endpoint, json=req_data, headers=headers)
response.status_code
response = requests.post(endpoint, data=req_data, headers=headers)
response.status_code
with open('query_examples/num_crossreferences_in_first_100_issues.json', 'r') as ff:
    req_data = ff.read()
    
print(req_data)
req_data.split('\n')
sum(req_data.split('\n'))
''.join(req_data.split('\n'))
''.join(req_data.split('\n').lstrip())
''.join([line.lstrip() for line in req_data.split('/')])
''.join(req_data.split('\n').lstrip())
''.join(req_data.split('\n'))
req_data.split('\n')
rd = _75
for line in rd:
    rd.lstrip()
    
rd
rd[0]
rd[0].lstrip()
for line in rd:
    line.lstrip()
    
rd
str.lstrip)(
map(str.lstrip, req_data.split('\n'))
''.join(map(str.lstrip, req_data.split('\n')))
payload = {'query' : ''.join(map(str.lstrip, req_data.split('\n')))}
response = requests.post(endpoint, json=json.dumps(payload), headers=headers)
response.status_code
with open('query_examples/total_num_open_issues.json', 'r') as ff:
    req_data = json.load(ff)
    
req_data
response = requests.post(endpoint, data=req_data, headers=headers)
response.status_code
response = requests.post(endpoint, json=req_data, headers=headers)
response.status_code
json.dumps(payload)
payload
response = requests.post(endpoint, json=payload, headers=headers)
response.status_code
response.content
data = json.load(response.content)
get_ipython().run_line_magic('pinfo', 'json.loads')
data = json.loads(response.content)
data
data[0]
data.keys()
data = data['data']
data.keys()
data = data['data']['repository']
data = data['repository']
data.keys()
data = data['issues']
data.keys()
data = data['edges']
data
import numpy as np
refcounts = np.array([line['node']['timelineItems']['totalCount'] for line in data], dtype=int)
np.bincount(refcounts)
np.sum(_117)
get_ipython().run_line_magic('logstart', 'gql_query.log')
exit()
