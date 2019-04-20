import pandas as pd
from bs4 import BeautifulSoup as Soup, Comment

file = open('../Data/supplementalData.xml').read()
soup = Soup(file, 'lxml')
countries = []

for territory in soup.find_all('territory'):
    comments = territory.find_all(text=lambda text: isinstance(text, Comment))
    country = {
        'name': comments[0],
        'gdp': int(territory.get('gdp')),
        'population': int(territory.get('population')),
    }
    countries.append(country)

# create dataframe from data
df_population_gdp = pd.DataFrame(countries)
df_population_gdp.columns = ['GDP','Name','Population']

# read refugee country names
df_countries = pd.read_csv('../Data/RefugeeCountries.csv', header=None, names=['Country'])

# join both dataframes
df_merged = df_countries.set_index('Country').join(df_population_gdp.set_index('Name'))
df_merged = df_merged[['Population', 'GDP']]
df_merged.to_csv('../Data/RefugeeCountriesPopulationGDP.csv')