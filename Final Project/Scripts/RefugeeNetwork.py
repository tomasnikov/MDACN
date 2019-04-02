import xml.etree.ElementTree as ET
from pdb import set_trace
import numpy as np
import pandas

tree = ET.parse('../data/RefugeeData.xml')
RefugeeXML = tree.getroot()


dataMatrix = []
for root in RefugeeXML:
    data =RefugeeXML.find('data')
    for  record in data:
        row =[]
        count = 0
        for field in record:
            if count <4:  
                row.append(field.text)
                count+=1
        dataMatrix.append(row) 

dataObject = []
allCountries= []
years =set()


for data in dataMatrix:
        entry = {
        'Residence':data[0],
        'Origin':data[1],
        'Year':data[2],
        'Count':data[3]
        }
        dataObject.append(entry)
        years.add(entry['Year'])
        if entry['Residence'] not in allCountries:
                allCountries.append(entry['Residence'])
        if entry['Origin'] not in allCountries:
                allCountries.append(entry['Origin'])
      

numCountries = len(allCountries)

allCountries.sort()
#df = pandas.DataFrame(data={"Countries": allCountries})
#df.to_csv("./RefugeeCountries.csv", sep=',',index=False)
nodes = allCountries
linkIndices = []
linkNames = []


countyear = -1
years =["2016"]
adjacency = np.zeros((numCountries,numCountries))
for year in years:
        countyear+=1
        '''
        onlyNew =list(filter(lambda x:x['Year']==year,dataObject))
        for i,country in enumerate(nodes):
                for j,otherCountry in enumerate(nodes):
                        if i !=j:
                                i_relevant =list(filter(lambda x:x['Residence']==nodes[i],onlyNew))
                                j_relevant =list(filter(lambda x:x['Origin']==nodes[j],i_relevant))
                                if j_relevant != []:
                                
                                        adjacency[i,j] = j_relevant[0]['Count']

        '''
        for i,country in enumerate(nodes):
                for j,otherCountry in enumerate(nodes):
                        if i !=j:
                                
                                #relevant = list(filter(lambda x:(x['Residence']==nodes[i])&(x['Residence']==nodes[j])&(x['Year']==year),dataObject))  
                                relevant = list(filter(lambda x:(x['Year']==year)&(x['Residence']==nodes[i])&(x['Origin']==nodes[j]),dataObject))
                                if relevant != []:
                                        adjacency[i,j] = relevant[0]['Count']
                                        
np.savetxt("RefugeeAdjacency.csv", adjacency, delimiter=",")