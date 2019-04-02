import xml.etree.ElementTree as ET
from pdb import set_trace
import numpy as np
import pandas

tree = ET.parse('../data/RefugeeData.xml')
RefugeeXML = tree.getroot()
np.set_printoptions(suppress=True)


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

adjacency = np.zeros((numCountries,numCountries))
#counter =0
#for country in nodes:
#        counter +1
#        adjacency[1,counter] = country
#        adjacency[counter,1] = country

countinsert = 0
for year in years:
        countyear+=1
        relevantYear =list(filter(lambda x:x['Year']==year,dataObject)))
        for data in relevantYear:
                adjacency[nodes.index(data['Residence']),nodes.index(data['Origin'])] = data['Count']

   
        filename = "RefugeeAdjacency"+str(year)+".csv"                             
        np.savetxt(filename, adjacency, fmt='%.0f',delimiter=",")