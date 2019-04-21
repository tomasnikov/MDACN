from pdb import set_trace

with open ('../Data/RefugeeMatrices/RefugeeAdjacency2016.csv', 'r') as file:
  refugees = file.read().splitlines()
  num = len(refugees)
  refugee_str = '[|\n' + '|\n'.join(refugees) + '|]'
  print(refugee_str)

with open ('../Data/CountryAdjacency.csv', 'r') as file:
  langs = file.read().splitlines()
  lang_str = '[|\n' + '|\n'.join(langs) + '|]'
  print(lang_str)
  set_trace()


file = open('dzn2016.dzn', 'w')
file.write('num = %s;\nrefugees = %s;\nlanguages=%s;' % (num,refugee_str, lang_str))
file.close()