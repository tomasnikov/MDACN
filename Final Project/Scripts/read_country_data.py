from pdb import set_trace
from pprint import pprint
from bs4 import BeautifulSoup as Soup, Comment
import random
import numpy as np

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

for i,country in enumerate(countries):
  for j,otherCountry in enumerate(countries):
    if i != j:
      weight = 0
      langTexts = []
      for lang in [x for x in country['languages'] if x['type'] in [y['type'] for y in otherCountry['languages']]]:
        percent = lang['percent']/100
        weight += percent
        langTexts.append('%s-%s' % (lang['name'],percent))
      adjacency[i,j] = weight
      if weight > 0:
        linkIndices.append((i,j))
        linkNames.append((country['name'],otherCountry['name'], weight, '|'.join(langTexts)))


print('Num links: ', len(linkNames))
print('Random link: ', random.choice(linkNames))
