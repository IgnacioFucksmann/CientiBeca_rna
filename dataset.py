import pandas as pd
import numpy as np
from torch.utils.data import Dataset
import torch as tr
import os
import json
import pickle
from utils import fam_oneHot
from embeddings import OneHot


class DatasetSeq(Dataset):

    def __init__(self,dataset_path, embedding=None, min_len=0, max_len=1000,padding=True,random_pad=False,
                 mask=False, cache="cache/"):
        self.max_len=max_len
        self.min_len=min_len
        self.embedding = embedding
        self.padding = padding
        self.mask = mask


        if not os.path.isdir(cache):
            os.mkdir(cache)
        self.cache = cache
        dat=pd.read_csv(dataset_path,index_col=None)
        dat.insert(loc=len(dat.columns), column='oneHot', value=[fam_oneHot(id.split("_")[0]) for id in dat.id])    
        dat = dat[(dat.len > min_len) & (dat.len < max_len)]
        dat = dat.reset_index(drop=True)
        self.id=dat.id
        self.cluster=dat.cluster
        self.seq=dat.sequence.tolist()
        self.struct=dat.structure
        self.pair=[json.loads(dat.base_pairs.iloc[i]) for i in range(len(dat))]

        if self.embedding is None: # one-hot embedding by default
            self.embedding = OneHot()
        self.embedding_size = self.embedding.emb_size

        
        self.pad_token = '-'
        self.random_pad = random_pad

        self.famHot=dat.oneHot
    def __len__(self): 
       return len(self.seq)

    def __getitem__(self,index):
        
        id = self.id[index]
        cache = f"{self.cache}/{id}.pk"
        
        if os.path.isfile(cache):
            seq_emb, Mc, L, id,fhot  = pickle.load(open(cache, "rb"))
        else:
            connections = tr.tensor(self.pair[index])-1
            sequence,Mc = self.pad_sequence(self.seq[index],connections)
            seq_emb=self.embedding.seq2onehot(sequence)
            L = len(self.seq[index])
            fhot=tr.tensor(self.famHot[index])
            # mask = valid_mask(sequence)
        return seq_emb,Mc,L,id,fhot

        
    def pad_sequence(self, sequence, connections):
        """Pad sequence and create connection matrix to max length"""
        left_pad, right_pad = 0, 0 
        if self.padding:
            left_pad = 0
            right_pad = self.max_len - len(sequence)
            if self.random_pad:
                left_pad = np.random.randint(right_pad)
                right_pad -= left_pad
        sequence = self.pad_token*left_pad + sequence + self.pad_token*right_pad
        # Conection matrix: -1 padding, 0 is not connected, 1 is connected
        Mc = -tr.ones((len(sequence), len(sequence)), dtype=tr.float32)      
        if right_pad > 0:
            Mc[left_pad:-right_pad, left_pad:-right_pad] = 0
        else:
            Mc[left_pad:, left_pad:] = 0
        if len(connections)>0:
            # for i in range(len(connections)):
            #     Mc[connections[][0] + left_pad, connections[i][1] + left_pad] = 1
            Mc[connections[:,0] + left_pad, connections[:,1] + left_pad] = 1
            Mc[connections[:,1] + left_pad, connections[:,0] + left_pad] = 1
        # else:
            # print(f"Warning: sequence {sequence} do not have any connections")
        return sequence, Mc.long()
