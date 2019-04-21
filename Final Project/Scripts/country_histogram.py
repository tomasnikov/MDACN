import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from pprint import pprint
from pdb import set_trace

year = '2016'

country_adj = pd.read_csv('../Data/CountryAdjacency.csv', header=None)
country_names = pd.read_csv('../Data/RefugeeCountries.csv', header=None)
refugee_adj = pd.read_csv('../Data/RefugeeMatrices/RefugeeAdjacency%s.csv' % year, header=None,dtype=int)   
#refugee_adj = pd.read_csv('../Data/IncreaseRefugeeMatrices/IncreaseRefugeeAdjacency%s.csv' % year, header=None,dtype=int)   
country_adj = pd.DataFrame(country_adj).to_numpy()
refugee_adj = pd.DataFrame(refugee_adj).to_numpy()
refugee_adj_copy = refugee_adj.copy()

# Create 20 bins of language similarities and refugee numbers
def create_bins(ref_matrix):
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

# Get total number of refugees in every country
refugee_nums = np.sum(refugee_adj,axis=1)
refugee_nums_by_country = [(refugee_nums[i],country_names[0][i],i) for i in range(0,len(country_adj))]
refugee_nums_by_country = sorted(refugee_nums_by_country)


tmp = [refugee_nums_by_country[0]]
last = [refugee_nums_by_country[0]]
index = 0
# Cluster together countries with similar refugee counts and shuffle their rows in matrix
for val in refugee_nums_by_country[1:]:
  ref_nums = [i[0] for i in tmp]
  last_nums = [i[0] for i in last]
  if val[0] <= np.mean(ref_nums) + np.std(last_nums + ref_nums):
    tmp.append(val)
  else:
    pprint(tmp)
    indices = [i[2] for i in tmp]
    indices_shuffle = indices.copy()
    random.shuffle(indices_shuffle)
    refugee_adj_copy[indices] = refugee_adj_copy[indices_shuffle]
    last = tmp
    tmp = [val]
  index += 1

# Finish the last value(s)
pprint(tmp)
indices = [i[2] for i in tmp]
indices_shuffle = indices.copy()
random.shuffle(indices_shuffle)
refugee_adj_copy[indices] = refugee_adj_copy[indices_shuffle]

# Plot both original historgram and shuffled histogram
x,y,mean = create_bins(refugee_adj)
x,y_shuff,mean_shuff = create_bins(refugee_adj_copy)
print('original mean', mean)
print('shuffled mean', mean_shuff)


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
plt.title('Shuffled Data, %s' % year)
plt.axvline(mean_shuff, color='g', linewidth=3, label='Mean = %.3f' % mean_shuff)
plt.bar(x, y_shuff,width=-0.05,align='edge',edgecolor='r')
plt.legend()
plt.show()
