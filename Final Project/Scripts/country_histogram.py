import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import itertools
from pdb import set_trace

def get_data(year):
  country_adj = pd.read_csv('../Data/CountryAdjacency.csv', header=None)
  country_names = pd.read_csv('../Data/RefugeeCountries.csv', header=None)
  refugee_adj = pd.read_csv('../Data/RefugeeMatrices/RefugeeAdjacency%s.csv' % year, header=None,dtype=int)   
  #refugee_adj = pd.read_csv('../Data/IncreaseRefugeeMatrices/IncreaseRefugeeAdjacency%s.csv' % year, header=None,dtype=int)   
  country_adj = pd.DataFrame(country_adj).to_numpy()
  refugee_adj = pd.DataFrame(refugee_adj).to_numpy()
  refugee_adj_shuff = refugee_adj.copy()

  # Get total number of refugees in every country
  refugee_nums = np.sum(refugee_adj,axis=1)
  refugee_nums_by_country = [(refugee_nums[i],country_names[0][i],i) for i in range(0,len(country_adj))]
  refugee_nums_by_country = sorted(refugee_nums_by_country)

  return country_adj, refugee_adj, refugee_adj_shuff, refugee_nums_by_country

# Create 20 bins of language similarities and refugee numbers
def create_bins(country_adj, ref_matrix):
  x = np.linspace(0.05,1.0,20)
  y = np.zeros(20)
  total = 0

  for i in range(0,len(country_adj)):
    for j in range(0,len(country_adj)): 
      if ref_matrix[i][j] > 0:
        lang_sim = country_adj[i][j]
        total += lang_sim*ref_matrix[i][j]
        if lang_sim == 1.0:
          lang_sim = 0.999
        y[int(np.floor(lang_sim/0.05))] += ref_matrix[i][j]

  return x,y,total/sum(sum(ref_matrix))


def cluster_shuffle(refugee_nums_by_country,refugee_adj_shuff):
  tmp = [refugee_nums_by_country[0]]
  last = [refugee_nums_by_country[0]]
  index = 0
  clusters = []
  # Cluster together countries with similar refugee counts and shuffle their rows in matrix
  for val in refugee_nums_by_country[1:]:
    ref_nums = [i[0] for i in tmp]
    last_nums = [i[0] for i in last]
    if val[0] <= np.mean(ref_nums) + np.std(last_nums + ref_nums):
      tmp.append(val)
    else:
      indices = [i[2] for i in tmp]
      indices_shuffle = indices.copy()
      random.shuffle(indices_shuffle)
      refugee_adj_shuff[indices] = refugee_adj_shuff[indices_shuffle]
      last = tmp
      clusters.append(tmp)
      tmp = [val]
    index += 1
  clusters.append(tmp)
  # Finish the last value(s)
  indices = [i[2] for i in tmp]
  indices_shuffle = indices.copy()
  random.shuffle(indices_shuffle)
  refugee_adj_shuff[indices] = refugee_adj_shuff[indices_shuffle]

  return refugee_adj_shuff, clusters

def cluster_optimal(country_adj,refugee_adj, clusters):
  refugee_adj_opt = refugee_adj.copy()
  c_val = lambda c_ind, ref_adj: sum([ref_adj[c_ind,j]*country_adj[c_ind,j] for j in range(214)])
  for cluster in clusters[1:]:
    indices = [i[2] for i in cluster]
    cluster_val = sum([c_val(c_ind, refugee_adj) for c_ind in indices])
    opt_ind = indices
    for perm in itertools.permutations(indices):
      perm = list(perm)
      ref_tmp = refugee_adj.copy()
      ref_tmp[indices] = ref_tmp[perm]
      perm_val = sum([c_val(c_ind, ref_tmp) for c_ind in perm])
      if perm_val > cluster_val:
        cluster_val = perm_val
        opt_ind = perm
        if len(cluster) >= 7:
          break
    refugee_adj_opt[indices] = refugee_adj_opt[opt_ind]
  return refugee_adj_opt


def plot_histograms(country_adj, refugee_adj, refugee_adj_shuff, year, label, show_plot=True):
  # Plot both original historgram and shuffled histogram
  x,y,mean = create_bins(country_adj, refugee_adj)
  x,y_shuff,mean_shuff = create_bins(country_adj, refugee_adj_shuff)
  print('original mean %s' % year, mean)
  print('%s mean %s' % (label,year), mean_shuff)

  if show_plot:
    fig = plt.figure(1)
    plt.xlabel('Language Similarity')
    plt.ylabel('Total refugee count')
    plt.title('Original Data, %s' % year)
    plt.axvline(mean, color='g', linewidth=3, label='Mean = %.3f' % mean)
    plt.bar(x,y,width=-0.05,align='edge',edgecolor='r')
    plt.legend()

    fig = plt.figure(2)
    plt.xlabel('Language Similarity')
    plt.ylabel('Total refugee count')
    plt.title('%s Data, %s' % (label,year))
    plt.axvline(mean_shuff, color='g', linewidth=3, label='Mean = %.3f' % mean_shuff)
    plt.bar(x, y_shuff,width=-0.05,align='edge',edgecolor='r')
    plt.legend()
    plt.show()
  return mean, mean_shuff

year = '2016'

country_adj, refugee_adj, refugee_adj_shuff, refugee_nums_by_country = get_data(year)
refugee_adj_shuff, clusters = cluster_shuffle(refugee_nums_by_country, refugee_adj_shuff)
refugee_adj_opt = cluster_optimal(country_adj, refugee_adj, clusters)
plot_histograms(country_adj, refugee_adj, refugee_adj_shuff, year, 'Shuffled', False)
plot_histograms(country_adj, refugee_adj, refugee_adj_opt, year, 'Optimal', True)

years = range(1975,2017)
mean_x = []
mean_shuff_x = []
mean_opt_x = []
for year in years:
  print(year)
  country_adj, refugee_adj, refugee_adj_shuff, refugee_nums_by_country = get_data(year)
  mean_shuff = 0
  for i in range(10):
    refugee_adj_shuff, clusters = cluster_shuffle(refugee_nums_by_country, refugee_adj_shuff)
    mean, tmp_shuff = plot_histograms(country_adj, refugee_adj, refugee_adj_shuff, year, 'Shuffled', False)
    mean_shuff += tmp_shuff
  mean_shuff = mean_shuff/10

  refugee_adj_opt = cluster_optimal(country_adj, refugee_adj, clusters)
  _, mean_opt = plot_histograms(country_adj, refugee_adj, refugee_adj_opt, year, 'Optimal', False)
  mean_x.append(mean)
  mean_shuff_x.append(mean_shuff)
  mean_opt_x.append(mean_opt)

fig = plt.figure(3)
plt.plot(years, mean_x, label='Original data')
plt.plot(years, mean_shuff_x, label='Shuffled data')
plt.plot(years, mean_opt_x, label='Optimal data')
plt.xlabel('Years')
plt.ylabel('Mean')
plt.legend()
plt.show()
