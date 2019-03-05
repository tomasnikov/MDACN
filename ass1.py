import csv
from pdb import set_trace
from pprint import pprint

data = []
nodes = set()
links = set()

with open('manufacturing_emails_temporal_network.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    if line_count != 0:
      n1 = int(row[0])
      n2 = int(row[1])
      t = int(row[2])
      data.append({'node1': n1, 'node2': n2, 'timestamp': t})
      nodes.add(n1)
      nodes.add(n2)
      #links.add('-'.join([row[0],row[1]]))
      links.add((n1,n2))
    line_count += 1
set_trace()


# 13: timestamps that every node gets infected by i for the first 80%