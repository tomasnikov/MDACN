import csv
from pdb import set_trace
from pprint import pprint
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math

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
assert(math.isclose(clust_coeff,nx.average_clustering(G)))
print("clust_coeff", clust_coeff)

#5
hopmatrix = np.zeros((num_nodes,num_nodes))
calc_hops = False
if calc_hops:
  for i in nodes:
    for j in nodes:
      if j < i:
        hopmatrix[i-1,j-1] = hopmatrix[j-1,i-1]
        continue
      if i == j:
        hopmatrix[i-1,j-1] = 0
        continue
      hopcount = 1
      neighbors = set(map(lambda y: y[1], filter(lambda x: x[0] == i, links)))
      neighbors = neighbors.union(set(map(lambda y: y[0], filter(lambda x: x[1] == i, links))))
      
      neighbor_found = False
      while not neighbor_found:
        if j in neighbors:
          hopmatrix[i-1,j-1] = hopcount
          neighbor_found = True
        tmp_neighbors = neighbors.union(set(map(lambda y: y[1], filter(lambda x: x[0] in neighbors, links))))
        neighbors = tmp_neighbors.union(set(map(lambda y: y[0], filter(lambda x: x[1] in neighbors, links))))
        hopcount += 1
      #print(i,j,hopcount,hopmatrix[i-1,j-1], nx.shortest_path_length(G,source=i,target=j))
      assert(hopmatrix[i-1,j-1] == nx.shortest_path_length(G,source=i,target=j))
    print(i)
  print('hopmatrix ready')

  avg_hop = np.sum(hopmatrix)/(167*166)
  assert(avg_hop == nx.average_shortest_path_length(G))
  print("avg_hop", avg_hop)
  diameter = np.max(hopmatrix)
  print("diameter", diameter)

rand_clust_coeffs = []
rand_shortest_paths = []

#6
calc_small_world = False
if calc_small_world:
  sigma = nx.sigma(G,1,1) # == 0.99017 ~ 1
  print("sigma", sigma)

  omega = nx.omega(G,1,1) # == -0.07 ~ SO NOT SMALL WORLD?
  print("omega", omega)

#7
largest_eigen = max(np.linalg.eig(adjacency)[0])
print("largest_eigen", largest_eigen)
assert(math.isclose(largest_eigen, max(nx.adjacency_spectrum(G))))

#8
degrees_diagonal = np.zeros((num_nodes,num_nodes))
np.fill_diagonal(degrees_diagonal, degrees)
laplacian = degrees_diagonal - adjacency
laplacian_eigens = np.linalg.eig(laplacian)[0]
second_biggest = sorted(laplacian_eigens)[-2]
print("second_biggest", second_biggest)
assert(math.isclose(second_biggest,sorted(nx.laplacian_spectrum(G))[-2]))


# 13: timestamps that every node gets infected by i for the first 80%
# 