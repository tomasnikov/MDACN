import xml.etree.ElementTree as ET
from pdb import set_trace

tree = ET.parse('..\data\RefugeeData.xml')
RefugeeXML = tree.getroot()


data = []
countRoot = 1
for root in RefugeeXML:
    if countRoot<2:
        for  info in root:
            row =[]
            count = 0
            for field in info:
                if count <4:    
                    row.append(field.text)
                    count+=1
            data.append(row) 
        countRoot+=1 

print(count)
set_trace()
