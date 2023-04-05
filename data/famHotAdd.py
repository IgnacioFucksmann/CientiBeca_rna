import pandas as pd
import torch as tr
import numpy as np 

def fam_oneHot (fam):
    families = np.array(['5s', 'tmRNA', 'tRNA', 'srp', 'grp1', 'RNaseP', '23s','telomerase', '16s'])
    index = np.where(families==fam)
    onehot= np.zeros(families.shape)
    onehot[index]=1
    return onehot


data = pd.read_csv("data/archiveII_220808.csv")
# data.insert(loc=len(data.columns), column='oneHot', value=[fam_oneHot(id.split("_")[0]) for id in data.id])

# pd.DataFrame(data).to_csv('archiveII_220808.csv',index=False,) 
data = pd.read_csv('data/archiveII_220808.csv')
print(data['oneHot'].apply(literal_eval))