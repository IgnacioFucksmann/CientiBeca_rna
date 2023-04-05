import torch as tr   

class OneHot():
    def __init__(self):
        self.pad_token = "-"
        self.vocabulary = ['A', 'U', 'G', 'C'] 
        self.emb_size = 4
        
    def seq2onehot(self, seq):
        emb = tr.zeros((self.emb_size, len(seq)), dtype=tr.float)
        for k, nt in enumerate(seq):
            # print(f'letra = {nt} indice = {k}')
            if nt == self.pad_token:
                continue
            if nt in self.vocabulary:
                emb[self.vocabulary.index(nt), k] = 1
            else:
                emb[:, k] = 1/self.emb_size
            # print(f'embedding = {emb}')
        return emb