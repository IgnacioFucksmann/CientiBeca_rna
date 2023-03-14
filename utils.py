


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
    pairs=', '.join(str(e) for e in pairs)
    pairs='['+pairs+']'
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

def list_to_string(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1

def make_data_set(data_set):
    header= 'id,method,sequence,structure,motif,base_pairs,header,date,resolution,len\n'
    data=header
    for i in data_set[:]:
        pair=seq_to_pair(i[2])
        data=data+i[0]+',SOLUTION NMR,'+i[1]+','+i[2]+','+'"'+pair+'"'+'\n'
    return data