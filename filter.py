# filter.py
# Author: Juse
# Description: Used to filter fasta file based on length and number of species.

import re
import os
from fasta import readfa

def remove_n(string, char):

    return len(re.sub(char, '', string))

def fa_filter(fasta, outputdir, spesym = '@', gap = '-', min_ali_len = 80, min_seq_len = 80, min_spe_num = 1):

    id_seq, _, _ = readfa(file=fasta,symbol=' ')
    fasta = os.path.basename(fasta)
    with open(f'{outputdir}/filter.log', 'a') as log:

        # 序列短于要求则直接返回
        if remove_n(list(id_seq.values())[0], '\n') < min_ali_len:
            log.write(f'{fasta} is shorter than {min_ali_len} and be removed.\n')
            return
        # 新建序列字典，保存除去gap后长度大于一定值的序列
        newid_seq = {}
        for i in id_seq.keys():
            if remove_n(id_seq[i], f'[{gap}\n]') >= min_seq_len:
                newid_seq[i] = id_seq[i]
            else:
                log.write(f'{fasta} {i} is shorter than {min_seq_len} without gap and be removed.\n')
        # 对新字典所包含的物种进行计数，若物种剩余数低于一定值则直接返回
        species_list = []
        for i in newid_seq.keys():
            species = i.split(spesym)[0]
            # 统计物种名单
            if species not in species_list:
                species_list.append(species)
        if len(species_list) < min_spe_num:
            log.write(f'{fasta} tax is less than {min_spe_num} and be removed.\n')
            return
        # 最后输出文件
        with open(f'{outputdir}/{fasta}', 'w') as opfa:
            for i in newid_seq.keys():
                opfa.write(f'>{i}' + '\n')
                opfa.write(newid_seq[i])
        log.write(f'{fasta} has been filtered and saved.\n')
