import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

b_dir = './stack-overflow-tag-network/'

G = nx.Graph(day="Stackoverflow")
df_nodes = pd.read_csv(b_dir + 'stack_network_nodes.csv')
df_edges = pd.read_csv(b_dir + 'stack_network_links.csv')


for index, row in df_nodes.iterrows():
    G.add_node(row['name'], group=row['group'], nodesize=row['nodesize'])

for index, row in df_edges.iterrows():
    G.add_weighted_edges_from([(row['source'], row['target'], row['value'])])

color_map = {1: '#f09494', 2: '#eebcbc', 3: '#72bbd0', 4: '#91f0a1', 5: '#629fff', 6: '#bcc2f2',
             7: '#eebcbc', 8: '#f1f0c0', 9: '#d2ffe7', 10: '#caf3a6', 11: '#ffdf55', 12: '#ef77aa',
             13: '#d6dcff', 14: '#d2f5f0'}
df_nodes['c'] = pd.Categorical.from_array(df_nodes.group).labels
plt.figure(figsize=(25, 25))
group_len = len(df_nodes['group'].value_counts())


import seaborn as sns
colors = sns.mpl_palette("tab20", group_len)

options = {
    'nodelist': df_nodes['name'].tolist(),
    'node_size': [nodesize * 1.1 for nodesize in df_nodes['nodesize'].tolist()],
    #'node_color': [colors[group - 1] for group in df_nodes['group'].tolist()],
    'node_color': [colors[c] for c in df_nodes['c'].tolist()],
    'edgelist': list(zip(df_edges['source'], df_edges['target'])),
    'width': [value * 0.1 for value in df_edges['value'].tolist()],
    'edge_color': 'gray',
    'with_labels': True,
    'alpha': 1,
    'font_weight': 'regular',
}

"""
Using the spring layout : 
- k controls the distance between the nodes and varies between 0 and 1
- iterations is the number of times simulated annealing is run
default k=0.1 and iterations=50
"""
from networkx.drawing.nx_agraph import graphviz_layout
#nx.draw(G, pos=nx.spring_layout(G, k=0.25, iterations=50), **options)
#nx.draw(G, pos=graphviz_layout(G, prog='neato'), **options)
pos = graphviz_layout(G, prog='neato')
nx.draw_networkx_nodes(G, pos, nodelist=options['nodelist'], node_size=options['node_size'],
                       node_color=options['node_color'], with_labels=True)
nx.draw_networkx_edges(G, pos, edgelist=options['edgelist'],
                       width=options['width'], alpha=0.2)
nx.draw_networkx_labels(G, pos)
ax = plt.gca()
ax.collections[0].set_edgecolor("#555555")
# plt.show()
plt.savefig('tag_network_in_SO.png', dpi=200)
plt.clf()
plt.cla()
plt.close()
