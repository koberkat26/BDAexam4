def validate_sequence(sequence, k):
    if len(sequence) < k:
        return False
    for nucleotide in sequence:
        if nucleotide.isdigit():
            return False
    return True

#tests
print(validate_sequence("ATCG", 3))   # should print True
print(validate_sequence("AT1G", 3))   # should print False
print(validate_sequence("ATG", 4))    #should print False


def update_kmer_count(kmer_data, kmer, next_char):
    if kmer not in kmer_data:
        kmer_data[kmer] = {'count': 0, 'next_chars': {}}

    kmer_data[kmer]['count'] += 1

    if next_char not in kmer_data[kmer]['next_chars']:
        kmer_data[kmer]['next_chars'][next_char] = 0

    kmer_data[kmer]['next_chars'][next_char] += 1

    return kmer_data
#test
if __name__ == "__main__":
    kmer_data = {}

    # simulate a DNA sequence split into k-mers and next chars
    kmer_data = update_kmer_count(kmer_data, "ATG", "C")
    kmer_data = update_kmer_count(kmer_data, "ATG", "C")
    kmer_data = update_kmer_count(kmer_data, "ATG", "A")
    kmer_data = update_kmer_count(kmer_data, "TGC", "A")

    print("Final k-mer data:")
    print(kmer_data)
