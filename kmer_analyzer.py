def validate_sequence(sequence, k):
    if len(sequence) < k:
        return False
    
    valid_chars = set("ATCGatcg")
    for nucleotide in sequence:
        if nucleotide not in valid_chars:
            return False

    return True


def update_kmer_count(kmer_data, kmer, next_char):
    if kmer not in kmer_data:
        kmer_data[kmer] = {'count': 0, 'next_chars': {}}

    kmer_data[kmer]['count'] += 1

    if next_char not in kmer_data[kmer]['next_chars']:
        kmer_data[kmer]['next_chars'][next_char] = 0

    kmer_data[kmer]['next_chars'][next_char] += 1

    return kmer_data


def count_kmers_with_context(sequence, k):
    kmer_data = {}
    
    for i in range(len(sequence) - k):
        kmer = sequence[i:i+k]
        next_char = sequence[i+k]
        kmer_data = update_kmer_count(kmer_data, kmer, next_char)
    
    return kmer_data


def write_results_to_file(kmer_data, output_filename):
    sorted_kmers = sorted(kmer_data.keys())
    
    with open(output_filename, 'w') as f:
        for kmer in sorted_kmers:
            next_chars = kmer_data[kmer]['next_chars']
            
            next_char_str = " ".join(
                f"{char}:{freq}" 
                for char, freq in sorted(next_chars.items())
            )
            
            f.write(f"{kmer} {next_char_str}\n")
