import pandas as pd

refugee_data_folder = '../Data/RefugeeMatrices/'
increase_refugee_data_folder = '../Data/IncreaseRefugeeMatrices/'
years = range(1975, 2016)

# calculate increase in refugees between consecutive years (decrease in refugees is set to zero)
for i in years:
    j = i + 1

    yearMatrix = pd.read_csv(refugee_data_folder + 'RefugeeAdjacency' + str(i) + '.csv',
                             header=None, dtype=int)
    nextYearMatrix = pd.read_csv(refugee_data_folder + 'RefugeeAdjacency' + str(j) + '.csv',
                                 header=None, dtype=int)

    increaseYearMatrix = nextYearMatrix.sub(yearMatrix)
    increaseYearMatrix.mask(increaseYearMatrix < 0, 0, inplace=True)

    increaseYearMatrix.to_csv(increase_refugee_data_folder + 'IncreaseRefugeeAdjacency'+str(j)+'.csv',
                              header=False, index=False)