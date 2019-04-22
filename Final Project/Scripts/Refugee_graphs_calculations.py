import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import community
from pdb import set_trace
import matplotlib.cm as cm

country_names = pd.read_csv('../Data/RefugeeCountries.csv', header=None, names=['Country'])
country_adjacency = pd.read_csv('../Data/CountryAdjacency.csv', header=None, names=country_names.Country)
country_adjacency.set_index(country_names.Country, inplace=True)
country_adjacency_without_names = pd.read_csv('../Data/CountryAdjacency.csv', header=None)
country_adjacency.head()


country_gdp = pd.read_csv('../Data/CountriesGDP.csv', header=None)
country_array_gdp = np.genfromtxt('../Data/CountriesGDP.csv', delimiter=',')

country_array_population = np.genfromtxt('../Data/Population.csv', delimiter=',')
namesArray = np.genfromtxt('../Data/RefugeeCountries.csv', delimiter=',')


G = nx.from_pandas_adjacency(country_adjacency.T)
G.name = 'Language similarity between countries'


refugee_data_folder = '../Data/RefugeeMatrices/'
years =range(1975,2017)
yearInfo = dict()
for i in years:
    yearMatrix_no_name = pd.read_csv(refugee_data_folder + 'RefugeeAdjacency'+str(i)+'.csv', header=None,dtype=int)   
    
    yearMatrix = pd.read_csv(refugee_data_folder + 'RefugeeAdjacency'+str(i)+'.csv', header=None, names=country_names.Country, dtype=int)
    yearMatrix.set_index(country_names.Country, inplace=True)
    yearMatrix.head()
    
    normalizedMatrix = yearMatrix.div(yearMatrix.sum(axis=0), axis=1)
    normalizedMatrix.fillna(0, inplace=True)
    
    threshold = 0.85
    refugee_masked = yearMatrix.mask(normalizedMatrix < threshold, 0)
    
    Graph = nx.from_pandas_adjacency(refugee_masked.T, create_using=nx.DiGraph())
    Graph.name = 'Refugee '+ str(i)
    Graph_no_index = nx.from_pandas_adjacency(yearMatrix.T, create_using=nx.DiGraph())
    Graph_no_index.name = 'Refugee '+ str(i)
    
    entry={'year':str(i),'matrix_without_names':yearMatrix_no_name,'matrix_with_names':yearMatrix,'normalized_with_names':normalizedMatrix,'graph':Graph ,'graph_no_index':Graph_no_index , 'countRefugees': 0,'Origin_Countpercountry':{},'Asylum_Countpercountry':{}}
   
    yearInfo[str(i)]=entry
    
for year in years:
    matrix = yearInfo[str(year)]['matrix_without_names']
    names = country_names.Country
    countAll =0
    for i in range(0,len(matrix)):
            Origin_count=0
            Asylum_count=0
            for j in range(0,len(matrix)):
                Origin_count+=matrix[i][j]
                Asylum_count +=matrix[j][i]
                countAll += matrix[i][j]
            yearInfo[str(year)]['Origin_Countpercountry'][names[i]]=Origin_count
            yearInfo[str(year)]['Asylum_Countpercountry'][names[i]]=Asylum_count
    yearInfo[str(year)]['countRefugees'] =countAll
    

    CountryNameArray = [i for i in country_names['Country']]

#yearInfo['2016']['relation_to_languageData']
year = '2016'
#test = nx.from_pandas_adjacency(yearInfo[year]['relation_to_languageData'], create_using=nx.DiGraph())

refugee_year_no_name=yearInfo[year]['matrix_without_names']
#print(refugee_2016)

refugee_year=yearInfo[year]['matrix_with_names']
#print(refugee_2016['Afghanistan'])

 
refugee_year = refugee_year.div(refugee_year.sum(axis=0), axis=1)
#print(refugee_2016['Afghanistan'])
refugee_year.fillna(0, inplace=True)
refugee_year.head()
asylumArray =[]
for i in yearInfo[year]['Asylum_Countpercountry']:
    asylumArray.append(yearInfo[year]['Asylum_Countpercountry'][i])
AccumulatedAsylumArray=[]
count=0
for j in years: 
    index = 0
    for k in yearInfo[str(j)]['Asylum_Countpercountry']:   
        if count == 0:
            AccumulatedAsylumArray.append(yearInfo[str(j)]['Asylum_Countpercountry'][k])
           
        else:
            #set_trace()
            AccumulatedAsylumArray[index]+=yearInfo[str(j)]['Asylum_Countpercountry'][k]
            index+=1
        
    count+=1
    #set_trace()
AylumNorm = [i/sum(asylumArray) for i in asylumArray]
AccAylumNorm = [i/sum(AccumulatedAsylumArray) for i in AccumulatedAsylumArray]
country_array_gdp_p_population= country_array_gdp/country_array_population

country_array_gdp_p_population_norm = [i/sum(country_array_gdp_p_population) for i in country_array_gdp_p_population]
country_gdp_norm = [i/sum(country_array_gdp) for i in country_array_gdp]
country_population_norm = [i/sum(country_array_population) for i in country_array_population]


c = [i for i in country_names['Country']]

fig=plt.figure(figsize=(10,7))
for i,type in enumerate(CountryNameArray):
    
    x = AccAylumNorm[i]
    y = country_population_norm[i]
    #if not ((x>0.15) or (y>0.15)):
    plt.scatter(x, y, marker='x', color='blue')
    plt.text(x+0.0002, y+0.0002, type, fontsize=8)
plt.xlabel('Refugees Received')
plt.ylabel('Population')
plt.show()

fig=plt.figure(figsize=(10,7))
for i,type in enumerate(CountryNameArray):
    
    x = AccAylumNorm[i]
    y = country_gdp_norm[i]
    #if not ((x>0.15) or (y>0.15)):
    plt.scatter(x, y, marker='x', color='blue')
    plt.text(x+0.0002, y+0.0002, type, fontsize=8)
plt.xlabel('Refugees Received')
plt.ylabel('GDP')
plt.show()

fig=plt.figure(figsize=(10,7))
for i,type in enumerate(CountryNameArray):
    
    x = AccAylumNorm[i]
    y = country_array_gdp_p_population_norm[i]
    if not ((x>0.15) or (y>0.075)):
        plt.scatter(x, y, marker='x', color='blue')
        plt.text(x+0.0002, y+0.0002, type, fontsize=8)
plt.xlabel('Refugees Received')
plt.ylabel('GDP p population')
plt.show()
    

#yearInfo[str(year)]['Origin_Countpercountry'][names[i]]=Origin_count

AccumulatedAsylumArray=dict()
AccumulatedOriginArray=dict()
count=0
#for j in range(2012,2017): 
for j in range(1975,2017): 
    index = 0
    for k in yearInfo[str(j)]['Asylum_Countpercountry']:   
        if count == 0:
            #AccumulatedAsylumArray.append([yearInfo[str(j)]['Asylum_Countpercountry'][k]]['test'])
            AccumulatedAsylumArray[k]=yearInfo[str(j)]['Asylum_Countpercountry'][k]
            #AccumulatedAsylumArray['k']=5
           
        else:
            #set_trace()
            #AccumulatedAsylumArray[index]+=yearInfo[str(j)]['Asylum_Countpercountry'][k]
            AccumulatedAsylumArray[k]+=yearInfo[str(j)]['Asylum_Countpercountry'][k]

    for k in yearInfo[str(j)]['Origin_Countpercountry']:   
        if count == 0:
            #set_trace()
            #AccumulatedOriginArray.append(yearInfo[str(j)]['Origin_Countpercountry'][k])
            AccumulatedOriginArray[k]=yearInfo[str(j)]['Origin_Countpercountry'][k]
        else:
            #set_trace()
            #AccumulatedOriginArray[index]+=yearInfo[str(j)]['Origin_Countpercountry'][k]
            AccumulatedOriginArray[k]+=yearInfo[str(j)]['Origin_Countpercountry'][k]
            index+=1
    count+=1

biggestReceivingCountriesIndex=[]

Recieving = sorted(AccumulatedAsylumArray.items(), key=lambda item: item[1],reverse=True)

#Recieving = sorted(AccumulatedAsylumArray,reverse=True)
counter =0
for country,type in enumerate(Recieving): 
    if counter <16:
        biggestReceivingCountriesIndex.append(type)        
        counter+=1
        
biggestSendingCountriesIndex=[]

Sending = sorted(AccumulatedOriginArray.items(), key=lambda item: item[1],reverse=True)
#Sending = sorted(AccumulatedOriginArray,reverse=True)
counter =0

for country,type in enumerate(Sending): 
    if counter <16:
        biggestSendingCountriesIndex.append(type)        
        counter+=1




yearsToTest =[1976,1978,1980,1982,1984,1986,1988,1990,1992,1994,1996,1998,2000,2002,2004,2006,2008,2010,2012,2014,2016]

highestRecieving=[]
for country,type in enumerate(biggestReceivingCountriesIndex):
    bla=[]
    for yearTotest in yearsToTest:  
        bla.append(yearInfo[str(yearTotest)]['Asylum_Countpercountry'][type[0]]) 
        
    highestRecieving.append(bla)
    
    
highestSending=[]
for country,type in enumerate(biggestSendingCountriesIndex):
    bla=[]
    for yearTotest in yearsToTest:  
        bla.append(yearInfo[str(yearTotest)]['Origin_Countpercountry'][type[0]]) 
    highestSending.append(bla)


colors = cm.rainbow(np.linspace(0, 1, 16))

counter=0
fig=plt.figure(figsize=(10,10))
legend=[]
for bla in highestRecieving:
    df=pd.DataFrame({'xx':yearsToTest , 'yy':bla,'z':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,biggestReceivingCountriesIndex[counter][0]]})
    plt.plot( 'xx', 'yy', data=df, marker='o', color=colors[counter])

    plt.text(df['xx'][20]+0.2, df['yy'][20]+100, df['z'][20], fontsize=8)
    legend.append(df['z'][20])
    counter+=1
   
plt.ylabel('Most refugees given asylum')
plt.xlabel('Year')
plt.legend(legend,loc='upper left')
plt.show()


counter=0
fig=plt.figure(figsize=(10,10))
legend=[]
for bla in highestSending:
    df=pd.DataFrame({'xx':yearsToTest , 'yy':bla,'z':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,biggestSendingCountriesIndex[counter][0]]})
    plt.plot( 'xx', 'yy', data=df, marker='o', color=colors[counter])
    plt.text(df['xx'][20]+0.2, df['yy'][20]+100, df['z'][20], fontsize=8)
    legend.append(df['z'][20])
    counter+=1
plt.ylabel('Most  refugees originated from country')
plt.xlabel('Year')    
plt.legend(legend,loc='upper left')
plt.show()






     
    