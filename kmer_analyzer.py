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
