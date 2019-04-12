from bs4 import BeautifulSoup as Soup, Comment
import numpy as np
from numpy import genfromtxt

file = open('../Data/supplementalData.xml').read()
soup = Soup(file, 'lxml')
countries = []
for territory in soup.find_all('territory'):
  comments = territory.find_all(text=lambda text: isinstance(text, Comment))
  country = {
    'gdp': int(territory.get('gdp')),
    'literacyPercent': float(territory.get('literacypercent')),
    'population': int(territory.get('population')),
    'type': territory.get('type'),
    'name': comments[0],
    'languages': []
  }
  for i,lang in enumerate(territory.find_all('languagepopulation')):
    country['languages'].append({
        'type': lang.get('type'),
        'percent': float(lang.get('populationpercent')),
        'officialStatus': lang.get('officialstatus'),
        'name': comments[i+1]
      })
  # Remove the one country called 'Unkown region' with no data
  if len(country['languages']) > 0:
    countries.append(country)

numCountries = len(countries)

adjacency = np.zeros((numCountries,numCountries))
languageSimilarities = genfromtxt('../Data/LanguageSimilarities.csv', delimiter=',')
with open ('../Data/LanguageNames.csv', 'r') as file:
  languageNames = file.read().splitlines()

for i,country in enumerate(countries):
  for j,otherCountry in enumerate(countries):
    if i != j:
      totalAdjacency = 0
      normalization = 0
      for lang1 in country['languages']:
        for lang2 in otherCountry['languages']:
          if lang1['name'] in languageNames and lang2['name'] in languageNames:
            if (lang1['officialStatus'] == 'official' and lang2['officialStatus'] == 'official') or \
                    (lang1['officialStatus'] == 'de_facto_official' and lang2['officialStatus'] == 'de_facto_official') or \
                    (lang1['officialStatus'] == 'official' and lang2['officialStatus'] == 'de_facto_official') or \
                    (lang1['officialStatus'] == 'de_facto_official' and lang2['officialStatus'] == 'official'):

              adjacencyValue = languageSimilarities.item((languageNames.index(lang1['name']),languageNames.index(lang2['name'])))
              adjacencyValue = adjacencyValue * (lang1['percent']/100) * (lang2['percent']/100)
              totalAdjacency += adjacencyValue
              normalization += (lang1['percent'] / 100) * (lang2['percent'] / 100)
      if normalization != 0:
        totalAdjacency /= normalization
      adjacency[i, j] = totalAdjacency
    else:
      adjacency[i, j] = 1

print(adjacency)

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

oldAdjacency = adjacency
adjacency = np.zeros((len(refNames),len(refNames)))

for i in range(0, len(refNames)):
    found = False
    for j in range(0, len(refNames)):
        if indices[i] is not None and indices[j] is not None:
            old = oldAdjacency[indices[i], indices[j]]
            adjacency[i, j] = old
        else:
            adjacency[i, j] = 0

print(adjacency)
np.savetxt("../Data/CountryAdjacency.csv", adjacency, delimiter=',')
