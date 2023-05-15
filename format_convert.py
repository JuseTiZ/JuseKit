# format_convert.py
# Author: Juse
# Description: Used to transform format of fasta files.

def add_newlines(sequence, line_length=60):
    return "\n".join(sequence[i:i+line_length] for i in range(0, len(sequence), line_length))

def check_sequence_type(sequences_dict):
    dna_alphabet = set("ACGTNacgtn-?")
    protein_alphabet = set("ACDEFGHIKLMNPQRSTVWYXacdefghiklmnpqrstvwyx-?")

    dna_count = 0
    protein_count = 0

    for sequence in sequences_dict.values():
        seq_set = set(sequence)
        if seq_set.issubset(dna_alphabet):
            dna_count += 1
        elif seq_set.issubset(protein_alphabet):
            protein_count += 1

    if dna_count > protein_count:
        return "DNA"
    elif protein_count > dna_count:
        return "Protein"
    else:
        return "Unknown"

def write_phylip(output_file, records_dict):
    num_sequences = len(records_dict)
    sequence_length = len(next(iter(records_dict.values())))
    max_id_length = max(len(header) for header in records_dict.keys())

    with open(output_file, 'w') as f:
        f.write(f"{num_sequences} {sequence_length}\n")
        for header, sequence in records_dict.items():
            f.write(f"{header.ljust(max_id_length)} {sequence}\n")

def write_paml(output_file, records_dict):
    num_sequences = len(records_dict)
    sequence_length = len(next(iter(records_dict.values())))

    with open(output_file, 'w') as f:
        f.write(f"{num_sequences}  {sequence_length}\n")
        for header, sequence in records_dict.items():
            f.write(f"\n{header}\n{add_newlines(sequence)}\n")

def write_nexus(output_file, records_dict, typeofseq):
    num_sequences = len(records_dict)
    sequence_length = len(next(iter(records_dict.values())))
    max_id_length = max(len(header) for header in records_dict.keys())

    with open(output_file, 'w') as f:
        f.write('#NEXUS\n')
        f.write('BEGIN DATA;\n')
        f.write(f'dimensions ntax={num_sequences} nchar={sequence_length};\n')
        f.write(f'format datatype={typeofseq} interleave=no gap=-;\n')
        f.write('\nmatrix\n')

        for header, sequence in records_dict.items():
            f.write(f"{header.ljust(max_id_length)} {sequence}\n")

        f.write(';\nend;')

def write_nexus_interleaved(output_file, records_dict, typeofseq, line_length=60):
    num_sequences = len(records_dict)
    sequence_length = len(next(iter(records_dict.values())))
    max_id_length = max(len(header) for header in records_dict.keys())

    with open(output_file, 'w') as f:
        f.write('#NEXUS\n')
        f.write('begin data;\n')
        f.write(f'dimensions ntax={num_sequences} nchar={sequence_length};\n')
        f.write(f'format datatype={typeofseq} interleave=yes gap=-;\n')
        f.write('\nmatrix\n')

        for i in range(0, sequence_length, line_length):
            for header, sequence in records_dict.items():
                subsequence = sequence[i:i+line_length]
                f.write(f"{header.ljust(max_id_length)} {subsequence}\n")
            f.write('\n')

        f.write(';\nend;')


def write_axt(output_file, records_dict):
    axt_name = '-'.join(records_dict.keys())
    with open(output_file, 'w') as f:
        f.write(axt_name+'\n')
        for seq in records_dict.values():
            f.write(seq+'\n')
