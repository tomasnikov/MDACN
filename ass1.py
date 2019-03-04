import csv
from pdb import set_trace

data = []

with open('manufacturing_emails_temporal_network.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    if line_count != 0:
      data.append({'node1': row[0], 'node2': row[1], 'timestamp': row[2]})
    line_count += 1
set_trace()
