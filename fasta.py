# fasta.py
# Author: Juse
# Description: Used to read and modify fasta file.

import os

#第一个返回id_seq，第三个返回最长转录本
def readfa(file, symbol, txt = False, longest = False, stripornot = False):

    id_seq = {}
    gene_id = {}
    gene_longest = {}
    fa = file

    if txt:
        with open('tmp.fa', 'w') as t:
            t.write(file)
            fa = 'tmp.fa'

    with open(fa, 'r') as f:
        for line in f:
            if line.startswith(">"):
                contig_id = line.split()[0][1:]
                if longest:
                    contig_gene = line.split(symbol)[0][1:]
                    if contig_gene in gene_id.keys():
                        gene_id[contig_gene].append(contig_id)
                    else:
                        gene_id[contig_gene] = []
                        gene_id[contig_gene].append(contig_id)
            else:
                if contig_id in id_seq.keys():
                    if stripornot:
                        id_seq[contig_id] += line.strip()
                    else:
                        id_seq[contig_id] += line
                else:
                    if stripornot:
                        id_seq[contig_id] = line.strip()
                    else:
                        id_seq[contig_id] = line

    if longest:
        for gene in gene_id.keys():
            contigs = []
            for contig in gene_id[gene]:
                contigs.append(id_seq[contig])
            longest_contig = max(contigs, key=len)
            gene_longest[gene] = longest_contig

    if txt:
        os.remove(fa)

    return id_seq, gene_id, gene_longest

#mod有['pre','suf','sim','spe']
def id_modify(inputfile, mod, string = ''):

    input_path = os.path.abspath(inputfile)
    outputfile = f'{input_path}.{mod}.fa'
    with open(outputfile, 'w') as output:
        with open(inputfile, 'r') as fasta:
            if mod == 'sim':
                for line in fasta:
                    if line.startswith(">"):
                        seqid = line.split()[0]
                        output.write(seqid + '\n')
                        continue
                    output.write(line)
            if mod == 'pre':
                prefix = string
                for line in fasta:
                    if line.startswith(">"):
                        seqid = line.split()[0][1:]
                        new_seqid = ">" + prefix + seqid
                        output.write(new_seqid + '\n')
                        continue
                    output.write(line)
            if mod == 'suf':
                suffix = string
                for line in fasta:
                    if line.startswith(">"):
                        seqid = line.split()[0][1:]
                        new_seqid = ">" + seqid + suffix
                        output.write(new_seqid + '\n')
                        continue
                    output.write(line)
            if mod == 'spe':
                spe_sym = string
                for line in fasta:
                    if line.startswith(">"):
                        seqid = line.split(spe_sym)[0][1:].strip()
                        new_seqid = ">" + seqid
                        output.write(new_seqid + '\n')
                        continue
                    output.write(line)

def peptocds(id_seq, pepfile, outputdir):

    pepname = os.path.basename(pepfile)
    outname = f'{outputdir}/{pepname}'

    with open(outname, 'w') as out:
        with open(pepfile, 'r') as pep:
            for line in pep:
                if line.startswith('>'):
                    id = line.split()[0][1:]
                    seq = id_seq[id]
                    out.write(f'>{id}\n{seq}')


def qc_calcu(id_seq):

    seq_len = sorted([len(seq) for seq in id_seq.values()], reverse=True)
    total_length = sum(seq_len)
    max_length = max(seq_len)
    min_length = min(seq_len)
    gene_count = len(id_seq.values())
    aver_length = round(total_length/gene_count, 2)

    proportions = [0.1, 0.2, 0.3, 0.4, 0.5]
    threshold_lengths = [total_length * prop for prop in proportions]
    contig_values = {prop: 0 for prop in proportions}

    now_length = 0

    for length in seq_len:
        now_length += length
        for prop, thresh in zip(proportions, threshold_lengths):
            if contig_values[prop] == 0 and now_length > thresh:
                contig_values[prop] = length
        if now_length >= threshold_lengths[-1]:
            break

    contign10, contign20, contign30, contign40, contign50 = contig_values.values()

    all_bases = ''.join(id_seq.values())
    GC_content = round((all_bases.count('G') + all_bases.count('C')) * 100/total_length, 2)

    return {'num_gene': gene_count,
            'max_leng': max_length,
            'min_leng': min_length,
            'ave_leng': aver_length,
            'N10': contign10,
            'N20': contign20,
            'N30': contign30,
            'N40': contign40,
            'N50': contign50,
            'GC': GC_content}