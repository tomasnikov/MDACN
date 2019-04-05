from pdb import set_trace
from pprint import pprint
from bs4 import BeautifulSoup as Soup, Comment
import random
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
print('Num countries: ', len(countries))
print('Random country: ')
pprint(random.choice(countries))

nodes = [(x['type'],x['name'],i) for i,x in enumerate(countries)]
linkIndices = []
linkNames = []
adjacency = np.zeros((numCountries,numCountries))
languageSimilarities = genfromtxt('../Data/LanguageSimilarities.csv', delimiter=',')
with open ('../Data/LanguageNames.csv', 'r') as file:
  languageNames = file.read().splitlines()
notFoundLanguages = []

for i,country in enumerate(countries):
  for j,otherCountry in enumerate(countries):
    if i != j:
      totalAdjacency = 0

      for lang1 in country['languages']:
        for lang2 in otherCountry['languages']:
          if lang1['name'] in languageNames and lang2['name'] in languageNames:
            adjacencyValue = languageSimilarities.item((languageNames.index(lang1['name']),languageNames.index(lang2['name'])))
            adjacencyValue = adjacencyValue * (lang1['percent']/100) * (lang2['percent']/100)
            totalAdjacency += adjacencyValue
      if totalAdjacency > 1:
        totalAdjacency = 1

      adjacency[i, j] = totalAdjacency
      linkIndices.append((i, j))
      linkNames.append((country['name'], otherCountry['name'], totalAdjacency))
    else:
      adjacency[i, j] = 1
      linkIndices.append((i, j))
      linkNames.append((country['name'], otherCountry['name'], 1))

np.savetxt("../Data/CountryAdjacency.csv", adjacency)
print(adjacency)

print('Num links: ', len(linkNames))
print('Random link: ', random.choice(linkNames))
print('Random link: ', random.choice(linkNames))
print('Random link: ', random.choice(linkNames))
print('Random link: ', random.choice(linkNames))
print('Random link: ', random.choice(linkNames))
