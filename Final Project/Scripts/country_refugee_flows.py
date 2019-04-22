import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import community # https://github.com/taynaud/python-louvain

# parameters
years = range(1976, 2017) # years to consider [1976, 2017]
threshold_incoming_labels = 0.1 # do not show label if country does not receive at least 10% of a country's refugees
threshold_outgoing_labels = 0.01 # do not show label if outgoing refugees do not account for 1% of a country's population

# read country datasets
country_names = pd.read_csv('../Data/RefugeeCountriesPopulationGDP.csv')
country_names.set_index('Country', inplace=True)
country_adjacency = pd.read_csv('../Data/CountryAdjacency.csv', header=None, names=country_names.index)
country_adjacency.set_index(country_names.index, inplace=True)

# initialize dataframe with all zeros
refugeeAdjacency = pd.DataFrame(0, index=country_names.index, columns=country_names.index)

# increase in refugees between consecutive years (rows denote country of asylum, columns denote country of origin):
increase_refugee_data_folder = '../Data/IncreaseRefugeeMatrices/'
for i in years:
    increaseYearMatrix = pd.read_csv(increase_refugee_data_folder + 'IncreaseRefugeeAdjacency' + str(i) + '.csv',
                                     header=None, names=country_names.index, dtype=int)
    increaseYearMatrix.set_index(country_names.index, inplace=True)
    refugeeAdjacency = refugeeAdjacency.add(increaseYearMatrix)

# normalize refugees by country population
refugeeAdjacencyNormPop = refugeeAdjacency.div(country_names.Population.T, axis=1)
refugeeAdjacencyNormPop.fillna(0, inplace=True)

# calculate outgoing and incoming flow for each country and determine if country is a source node
country_names['Outgoing flow'] = refugeeAdjacency.sum(axis=0)
country_names['Incoming flow'] = refugeeAdjacency.sum(axis=1)
country_names.loc[country_names['Outgoing flow'] >= country_names['Incoming flow'], 'Source'] = 1
country_names.loc[country_names['Outgoing flow'] < country_names['Incoming flow'], 'Source'] = 0

# normalize refugees to indicate the fraction of refugees from origin country that goes to a different country
refugeeAdjacency = refugeeAdjacency.div(refugeeAdjacency.sum(axis=0), axis=1)
refugeeAdjacency.fillna(0, inplace=True)

# determine which countries receive a large fraction of refugees from one country
country_names['Largest incoming fraction'] = refugeeAdjacency.max(axis = 1)
country_names['Outgoing flow normalized'] = refugeeAdjacencyNormPop.sum(axis = 0)
country_names['Label'] = country_names.index
country_names.loc[((country_names['Largest incoming fraction'] <= threshold_incoming_labels) & (country_names['Source'] == 0)) |
                  ((country_names['Outgoing flow normalized'] < threshold_outgoing_labels) & (country_names['Source'] == 1)), 'Label'] = ''
country_labels = country_names['Label'].to_dict()

# remove nodes without neighbors in refugees graph
merged = refugeeAdjacency
G = nx.from_pandas_adjacency(merged.T, create_using=nx.DiGraph())
nodes_to_remove = list(nx.isolates(G))
G.remove_nodes_from(nodes_to_remove)

# remove nodes that have no outgoing edge
outdeg = G.out_degree()
nodes_to_keep = [n for (n, deg) in outdeg if deg != 0]
merged = refugeeAdjacency
merged = pd.DataFrame(0, index=country_names.index, columns=country_names.index)[nodes_to_keep].add(merged)
merged.fillna(0, inplace=True)

# remove nodes without neighbors in refugees graph
G = nx.from_pandas_adjacency(merged.T, create_using=nx.DiGraph())
nodes_to_remove = list(nx.isolates(G))
G.remove_nodes_from(nodes_to_remove)
G2 = nx.from_pandas_adjacency(country_adjacency)
G2.remove_nodes_from(nodes_to_remove)
refugeeAdjacency.drop(nodes_to_remove, axis=0, inplace=True)
refugeeAdjacency.drop(nodes_to_remove, axis=1, inplace=True)
country_names.drop(nodes_to_remove, axis=0, inplace=True)
print('Number of nodes: %d' % len(country_names))

# find communities using Louvain
parts = community.best_partition(G2)
values = [parts.get(node) for node in G2.nodes()]
community_list = list(zip(G2.nodes, values))
df_community = pd.DataFrame(community_list, columns = ['Country', 'Community'])
df_community.set_index('Country', inplace=True)
country_names = country_names.join(df_community)

# plot language similarity graph with communities
plt.figure(figsize=(15, 15))
pos = nx.spring_layout(G2, k=1.0)
nx.draw_networkx_nodes(G2, pos, node_color=values, alpha=0.5)
nx.draw_networkx_labels(G2, pos, labels=country_labels)
nx.draw_networkx_edges(G2, pos, alpha=0.01)
plt.axis('off')
plt.savefig('../images/language_similarity_communities.png', dpi=300)
plt.show()

# plot language similarity graph for individual communities
for i in range(max(values) + 1):
    countries_in_community_i = country_names.loc[country_names['Community'] == i].index
    country_adjacency_community_i = country_adjacency.loc[countries_in_community_i]
    country_adjacency_community_i = country_adjacency_community_i[list(countries_in_community_i)]

    G3 = nx.from_pandas_adjacency(country_adjacency_community_i)
    print(nx.info(G3))
    average_degree = [val for (node, val) in G3.degree(weight='weight')]
    print('Average weighted degree: ', sum(average_degree) / len(G3.nodes))
    print('')

    plt.figure(figsize=(15, 15))
    pos = nx.spring_layout(G3)
    nx.draw_networkx_nodes(G3, pos, node_color=country_names.loc[country_names['Community'] == i].Community.tolist(),
                           alpha=0.5, cmap=plt.cm.viridis, vmin=0, vmax=max(values))
    nx.draw_networkx_labels(G3, pos)
    nx.draw_networkx_edges(G3, pos, alpha=0.05)
    plt.axis('off')
    plt.savefig('../images/language_similarity_communities_%d.png' % i, dpi=300, bbox_inches = 'tight')
    plt.show()

# rearrange bipartite positions
source_nodes = country_names.loc[country_names['Source'] == 1].index.tolist()
pos = nx.bipartite_layout(G, source_nodes)
df_pos = pd.DataFrame.from_dict(pos).T
df_pos.sort_values([0, 1], ascending=[True, True], inplace=True) # use [True, False] for vertical
country_names.sort_values(['Source', 'Community'], ascending=[False, True], inplace=True)
country_names[1] = df_pos[0].values # use country_names[0] for vertical
country_names[0] = df_pos[1].values # use country_names[1] for vertical
sorted_pos = country_names[[0, 1]].T.to_dict(orient='list')
edge_weights = nx.get_edge_attributes(G, 'weight')

# plot bipartite graph
plt.figure(figsize=(25, 10))
nx.draw_networkx_nodes(G, sorted_pos, node_color=country_names.sort_index().Community, alpha=0.5)
labels = nx.draw_networkx_labels(G, sorted_pos, labels=country_labels)
nx.draw_networkx_edges(G, sorted_pos, alpha=0.5, edge_color=list(edge_weights.values()), edge_cmap=plt.cm.binary,
                       edge_vmin=0.1, edge_vmax=refugeeAdjacency.values.max())
for _,t in labels.items():
    t.set_rotation(45)
plt.axis('off')
plt.savefig('../images/flow_between_countries.png', dpi=300, bbox_inches = 'tight')
plt.show()
