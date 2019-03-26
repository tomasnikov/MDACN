import xml.etree.ElementTree as ET
from pdb import set_trace

tree = ET.parse('..\data\RefugeeData.xml')
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


print(count)
set_trace()
