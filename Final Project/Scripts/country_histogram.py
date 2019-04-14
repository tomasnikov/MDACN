import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from pprint import pprint

country_adj = pd.read_csv('../Data/CountryAdjacency.csv', header=None)
country_names = pd.read_csv('../Data/RefugeeCountries.csv', header=None)
refugee_adj = pd.read_csv('../Data/RefugeeMatrices/RefugeeAdjacency2016.csv', header=None,dtype=int)   
country_adj = pd.DataFrame(country_adj).to_numpy()
refugee_adj = pd.DataFrame(refugee_adj).to_numpy()
refugee_adj_copy = refugee_adj.copy()

# Create 20 bins of language similarities and refugee numbers
def create_bins(ref_matrix):
  x = np.linspace(0.05,1.0,20)
  y = np.zeros(20)

  for i in range(0,len(country_adj)):
    for j in range(0,len(country_adj)): 
      if ref_matrix[i][j] > 0:
        lang_sim = country_adj[i][j]
        if lang_sim == 1.0:
          lang_sim = 0.999
        y[int(np.floor(lang_sim/0.05))] += ref_matrix[i][j]
  return x,y

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
x,y = create_bins(refugee_adj)
x,y_r = create_bins(refugee_adj_copy)

fig = plt.figure(1)
plt.xlabel('Language Similarity')
plt.ylabel('Total refugee count')
plt.title('Original Data')
plt.bar(x,y,width=-0.05,align='edge',edgecolor='r')

fig = plt.figure(2)
plt.xlabel('Language Similarity')
plt.ylabel('Total refugee count')
plt.title('Shuffled Data')
plt.bar(x, y_r,width=-0.05,align='edge',edgecolor='r')
plt.show()
