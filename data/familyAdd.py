import pandas as pd
data = pd.read_csv("data/archiveII_220808.csv")
data.insert(loc=len(data.columns), column='family', value=[id.split("_")[0] for id in data.id])
pd.DataFrame(data).to_csv('archiveII_220808.csv',index=False) 
data = pd.read_csv('data/archiveII_220808.csv')
print(data)