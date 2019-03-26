from pdb import set_trace
from pprint import pprint
from bs4 import BeautifulSoup as Soup, Comment
import random

file = open('../Data/supplementalData.xml').read()
soup = Soup(file, 'lxml')
countries = {}
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
  countries[territory.get('type')] = country

print('Num countries: ', len(countries))
print('Random country: ')
pprint(countries[random.choice(list(countries.keys()))])