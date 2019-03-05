import csv
from pdb import set_trace
from pprint import pprint
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

data = []
nodes = set()
links = set()

with open('manufacturing_emails_temporal_network.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    if line_count != 0:
      n1 = int(row[0])
      n2 = int(row[1])
      t = int(row[2])
      data.append({'node1': n1, 'node2': n2, 'timestamp': t})
      nodes.add(n1)
      nodes.add(n2)
      #links.add('-'.join([row[0],row[1]]))
      links.add((n1,n2))
      
    line_count += 1
G = nx.Graph()
G.add_edges_from(links)

# ANSWERS HERE
# 1
num_nodes = len(nodes)
num_links = len(links)

assert(num_nodes == G.number_of_nodes())
assert(num_links == G.number_of_edges())
print('num nodes', len(nodes))
print('num links', len(links))
link_density = num_links/((num_nodes*(num_nodes-1)/2))
assert(link_density == nx.density(G))
print('link density', link_density)

degrees = [0]*(num_nodes + 1)
for i in links:
  degrees[i[0]] += 1
  degrees[i[1]] += 1
degrees = degrees[1:]
print('average degrees', np.mean(degrees))
print('standard dev degrees', np.var(degrees))

# 2
degree_x = np.arange(1,max(degrees)+1)
degree_y = [0]*(max(degrees))
for i in range(max(degrees)):
  degree_y[i] = degrees.count(i+1)
fig, ax = plt.subplots()
ax.plot(degree_x, degree_y)
ax.set(xlabel='degree k', ylabel='P[D=k]',
       title='Degree distribution')
ax.grid()
#plt.show()
# SCALE FREE since the degree distribution should follow a more normal distribution for ER.

#3
adjacency = np.zeros((num_nodes,num_nodes))
for i in links:
  adjacency[i[0]-1,i[1]-1] = 1
  adjacency[i[1]-1,i[0]-1] = 1
u = np.ones((num_nodes,1))
N0 = (np.transpose(u)@(np.linalg.matrix_power(adjacency, 0))@u)[0,0]
N1 = (np.transpose(u)@(np.linalg.matrix_power(adjacency, 1))@u)[0,0]
N2 = (np.transpose(u)@(np.linalg.matrix_power(adjacency, 2))@u)[0,0]
N3 = (np.transpose(u)@(np.linalg.matrix_power(adjacency, 3))@u)[0,0]
degree_cor = ((N1*N3) - N2*N2)/(N1*sum([i*i*i for i in degrees]) - N2*N2)
assert(degree_cor == nx.degree_pearson_correlation_coefficient(G))
print("degree_correlation", degree_cor)
# IT IS DISASSORTATIVE

#4
clust_coeffs = []
for i in nodes:
  neighbor_links = []
  neighbor_link_count = 0
  for j in filter(lambda x: x[0] == i or x[1] == i, links):
    if j[0] == i:
      neighbor_links.append(j[1])
    else:
      neighbor_links.append(j[0])
  for x in neighbor_links:
    for y in neighbor_links:
      neighbor_link_count += adjacency[x-1,y-1]
  neighbor_link_count = neighbor_link_count/2
  if degrees[i-1] == 1:
    clust_coeffs.append(0)
  else:
    clust_coeffs.append(neighbor_link_count/((degrees[i-1]*(degrees[i-1]-1))/2))
clust_coeff =  np.mean(clust_coeffs)
print("clust_coeff", clust_coeff)

#5
set_trace()
# 13: timestamps that every node gets infected by i for the first 80%