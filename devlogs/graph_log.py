# IPython log file

get_ipython().run_line_magic('run', 'gql_query_log.py')
data = [item['node'] for item in data]
data
nodes = [node['number'] for node in data]
nodes
data[0]
edges = []
import itertools
itertools.repeat(1)
edges = [(itertools.repeat(node['number']), edge['node']['number']) for edge in node['edges'] for node in data]
edges = []
for node in data:
    for edge in node['edges']:
        crnode = edge['node']
        if not crnode['isCrossRepository']:
            edges.append(node['number'], crnode['number'])
            
edges = []
for node in data:
    for edge in node['timelineItems']['edges']:
        crnode = edge['node']
        if not crnode['isCrossRepository']:
            edges.append(node['number'], crnode['number'])
            
node = data[0]
node['number']
crnode = node['timelineItems']['edges'][0]
edge = node['timelineItems']['edges'][0]
edge
edges = []
for node in data:
    for edge in node['timelineItems']['edges']:
        crnode = edge['node']
        if not crnode['isCrossRepository']:
            edges.append(node['number'], crnode['source']['number'])
            
            
edges = []
for node in data:
    for edge in node['timelineItems']['edges']:
        crnode = edge['node']
        if not crnode['isCrossRepository']:
            edges.append((node['number'], crnode['source']['number']))
            
edges
refcounts
refcounts.sum()
len(edges)
nodes
G = nx.graph()
import networkx as nx
G = nx.graph()
G = nx.Graph()
G
G.add_nodes(nodes)
G.add_nodes_from(nodes)
G.nodes
G.add_edges_from(edges)
G.nodes
nx.draw(G)
plt.show()
import matplotlib.pyplot as plt
plt.show()
nx.draw(G, node_size=100)
plt.show()
G
G.edges
centrality = nx.betweenness_centrality(G)
central = sorted(centrality, key=centrality.get, reverse=True)
central
data
get_ipython().run_line_magic('hist', '')
with open('res.json', 'r') as ff:
    data = json.load(ff)
    
data
len(data)
get_ipython().run_line_magic('hist', '')
data = [item['node'] for item in data]
data
len(data)
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('hist', '')
nodes = [node['number'] for node in data]
nodes
nodes = np.array([node['number'] for node in data])
nodes
nodes.shape
get_ipython().run_line_magic('hist', '')
edges = []
for node in data:
    for edge in node['timelineItems']['edges']:
        crnode = edge['node']
        if not crnode['isCrossRepository']:
            edges.append((node['number'], crnode['source']['number']))
            
len(edges)
np.array(edges)
G = nx.graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
nx.draw(G)
plt.show()
plt.show()
get_ipython().run_line_magic('pinfo', 'nx.draw')
get_ipython().run_line_magic('pinfo', 'nx.draw_networkx')
nx.draw(G, with_labels=True)
plt.show()
centrality = nx.betweenness_centrality(G)
central = sorted(centrality, key=centrality.get, reverse=True)
type(central)
centra[:10]
central[:10]
type(central[0])
central = np.array(sorted(centrality, key=centrality.get, reverse=True))
G.nodes
G.nodes.get(central[0])
central
get_ipython().run_line_magic('pinfo', 'G.nodes')
get_ipython().run_line_magic('pinfo', 'G.edges')
G.edges(nbunch=central[0])
len(G.edges(nbunch=central[0]))
len(G.edges(nbunch=central[1]))
len(G.edges(nbunch=central[2]))
len(G.edges(nbunch=central[3]))
len(G.edges(nbunch=central[4]))
nx.draw(G, nodelist=central[:100])
plt.show()
G.edges()
len(G.edges)
len(edges)
G.edges
type(G.edges)
get_ipython().run_line_magic('pinfo', 'nx.classes.reportviews.EdgeView')
edges = np.array(G.edges)
edges.shape
edges
edges[0:100]
np.sort(edges, axis=1)
np.sort(edges, axis=1)[0:100]
np.unique(edges[:,0])
np.unique(edges[:,0], return_counts=True)
np.unique(edges[:,1], return_counts=True)
np.unique(edges.flat, return_counts=True)
get_ipython().run_line_magic('pinfo', 'G.degree')
G.degree()
degree = G.degree()
degree = sorted(degree, key=degree.get, reverse=True)
degree
centrality
type(centrality)
type(degree)
degree = dict(G.degree())
degree = sorted(degree, key=degree.get, reverse=True)
degree
degree[0]
G.degree(12525)
get_ipython().run_line_magic('logstart', 'graph_log.py')
exit()
