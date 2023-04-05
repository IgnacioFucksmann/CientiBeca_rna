import os 
import numpy as np
import torch as tr 
import pandas as pd 

def seq_to_pair(seq):
    seq_np=list(seq)
    seq_open=[]
    pairs=[]
    for it,char in enumerate(seq_np):
        if (char=='('):
            seq_open.append(it+1)
        if (char==')'):
            pairs.append([seq_open[-1],it+1])
            seq_open=seq_open[:-1]
    pairs=pairs[::-1]
    # pairs=', '.join(str(e) for e in pairs)
    # pairs='['+pairs+']'
    return pairs


def replace_E(seq):
    str=list(seq)
    for it in range(len(str)):
        print(str[it])
        if(str[it]=='('):
            break    
        else:
            str[it]='-'
    print('SALIO')
    for it in range(len(str)-1,0,-1):
        if(str[it]==')'):
            break   
        else:
            str[it]='-'
    return str
    
    
def dot_to_motif(seq, struct):
    """Get motifs from dot-bracket notation structure. Requieres bpRNA.pl script"""

    with open('tmp.dbn', 'w') as fout:
        fout.write('>id\n')
        fout.write(f'{seq}\n')
        fout.write(f'{struct}\n')
        
    os.system('perl extras/bpRNA.pl tmp.dbn')
    with open('tmp.st') as fin:
        k = 0
        for line in fin:
            if line[0] == '#':
                continue
            if k == 2:
                motif = line.strip()
                break
            else:
                k += 1
    os.remove('tmp.dbn')
    os.remove('tmp.st')
    return motif

def seq_len(seq):
   lenght=len(list(seq))
   return lenght

def make_data_set(data_set):
    data=[['id','sequence','structure','base_pairs','len']]
    for i in data_set[1:]:
        if seq_len(i[3]) < 800:
            data.append([i[1],i[3],i[4],seq_to_pair(i[4]),seq_len(i[3])])
      

        # data=data+i[0]+',SOLUTION NMR,'+i[1]+','+i[2]+','+'"'+pair+'"'+','+str(lenght)+'\n'
    writer=pd.DataFrame(data)
    writer.to_csv('dist03.csv',sep=',',header=False,index=False)
    return data

def valid_mask(seq):
    """Create a NxN mask with valid canonic pairings."""
    valid_pairs = [{"G", "C"}, {"A", "U"}, {"G", "U"}]
    mask = tr.zeros((len(seq), len(seq)), dtype=tr.float32)
    for i in range(len(seq)):
        for j in range(len(seq)):
            if i != j:
                if {seq[i], seq[j]} in valid_pairs:
                    mask[i, j] = 1
                    mask[j, i] = 1
    return mask

def fam_oneHot (fam):
    families = np.array(['5s', 'tmRNA', 'tRNA', 'srp', 'grp1', 'RNaseP', '23s','telomerase', '16s'])
    index = np.where(families==fam)
    onehot= np.zeros(families.shape)
    onehot[index]=1
    return onehot