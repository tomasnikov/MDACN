import numpy as np
from numpy import genfromtxt

with open('../Data/CountryNames.csv', 'r') as file:
    oldNames = file.read().splitlines()

with open('../Data/RefugeeCountries.csv', 'r') as file:
    refNames = file.read().splitlines()

indices = [None] * len(refNames)

for i in range(0, len(refNames)):
    found = False
    for j in range(0, len(oldNames)):
        refCountry = refNames[i]
        oldCountry = oldNames[j]
        if refNames[i] == oldNames[j]:
            indices[i] = j
            found = True

    if not found:
        print(refNames[i])

print(indices)

oldAdjacency = genfromtxt('../Data/CountryAdjacency.csv', delimiter=' ')
adjacency = np.zeros((len(refNames),len(refNames)))
print(oldAdjacency)

for i in range(0, len(refNames)):
    found = False
    for j in range(0, len(refNames)):
        if indices[i] is not None and indices[j] is not None:
            old = oldAdjacency[indices[i], indices[j]]
            adjacency[i, j] = old
        else:
            adjacency[i, j] = 0

print(adjacency)
np.savetxt("../Data/CountryAdjacencyNew.csv", adjacency, delimiter=',')
