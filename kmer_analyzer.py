#Reese Kober
#BIO-539
#Exam 4

import sys

#creates a function to validate the seq using input values of a certain seq and the length of a substring 'k'
#if the length of the seq is less than k, then stops= false
#if a nucleotide in the seq is anything besides the 4 bases (upper/lowercase), then stops= false
##this prevents incorrect letters/spaces/digits/etc from getting counted
#if passes these = true
import sys

def validate_sequence(sequence, k):
    """Description: Validate DNA sequence before kmer analysis
        Ensures correct length and made up of nucleotides
      Parameters:
        argument 1= sequence (str): DNA sequence to validate
        argument 2= k (int): Minimum k-mer size
      Returns:
        bool: True if sequence is valid/pass, false if fails"""

    if len(sequence) < k:
        return False

    valid_chars = set("ATCGatcg")

    for nucleotide in sequence:
        if nucleotide not in valid_chars:
            return False

    return True


#creates function to update the count of substrings in a dictionary of kmers
#input values are the kmer data, a substring, and the next character
#if a substring/kmer isnt in the data, then it intiates it into the dictionary of kmers (starts the count at 1, need to change to start at 0)
#if the next character has never been seen after that kmer, then it gets intiated too (starts at zero)
#kmer data is the dictionary w/ all this info stored
def update_kmer_count(kmer_data, kmer, next_char):
    """Description: Update substrings in kmer dictionary
       Parameters: 
          argument 1= kmer_data (dict): Dictionary storing k-mer counts and next-character frequencies
          argument 2= kmer (str): Substring of length k from sequence
          argument 3= next_char (str): Single character following the k-mer in the sequence
       Returns:
         Dict: dictionary of substrings and characters from sequence"""

    if kmer not in kmer_data:
        kmer_data[kmer] = {'count': 0, 'next_chars': {}}

    kmer_data[kmer]['count'] += 1

    if next_char not in kmer_data[kmer]['next_chars']:
        kmer_data[kmer]['next_chars'][next_char] = 0

    kmer_data[kmer]['next_chars'][next_char] += 1

    return kmer_data


#creates function to show the freq of a substring in context of the characters following it
#creates dictionary of kmers
#counts how often each kmer occurs & the characters that follow it
#kmer_data creates an empty dictionary that will get filled
def count_kmers_with_context(sequence, k):
    """Description: Frequency of substrings in context of next-characters
       Parameters:
         argument 1: sequence (str): DNA sequence to analyze.
         argument 2: k (int): Length of k-mers to extract.
       Returns:
         dict: Nested dictionary where each k-mer maps to:
                - count: number of times the k-mer appears
                - next_chars: dictionary of following characters & freq"""

    kmer_data = {}

    #loops through the sequence to get all possible substrings & following characters
    for i in range(len(sequence) - k):

        #extract the kmer
        kmer = sequence[i:i+k]

        #get next character after the sequence
        next_char = sequence[i+k]

        #update the dictionary with the new kmers and characters
        kmer_data = update_kmer_count(kmer_data, kmer, next_char)

    return kmer_data


#printing the dictionary into an output file
def write_results_to_file(kmer_data, output_filename):
    """Description: Print kmer dictionary into text file
       Parameters:
         argument 1= kmer_data (dict): Nested dictionary with k-mer counts and
                            next-character freq data
         argument 2= output_filename (str): Name of the output file to write results in
       Returns:
         none"""

    #sorts the kmers in the dictionary alphabetically
    sorted_kmers = sorted(kmer_data.keys())

    #open the new output file to write in new info
    with open(output_filename, 'w') as f:

        #loop through each kmer in the sorted list
        for kmer in sorted_kmers:

            #get next characters
            next_chars = kmer_data[kmer]['next_chars']

            #format next characters into string
            next_char_str = " ".join(
                f"{char}:{freq}"
                for char, freq in sorted(next_chars.items())
            )

            #write to file: kmer count, char count
            f.write(f"{kmer} {kmer_data[kmer]['count']} {next_char_str}\n")


#tie everything together into this main function
def main():
    """Description: Run the entire kmer analysis pipeline
       Parameters:
         None (uses command line arguments using sys.argv)
       Returns:
         none"""
#what to input to run this function
    #the sequence file, kmer size, output file name
    sequence_file = sys.argv[1]
    k = int(sys.argv[2])
    output_file = sys.argv[3]
#prints a warning message if it doesnt pass
    print(f"Reading sequences from {sequence_file}...")
 #empty dictionary moved here so it doesnt overwrite past entries into the dictionary
    kmer_data = {}
#opens the file and reads it 
    with open(sequence_file, 'r') as f:
#loops through the sequences
        for sequence in f:
#strip gets rid of blanks
            sequence = sequence.strip()
#validates the seq to make sure it is the correct length or has incorrect characters
            if not validate_sequence(sequence, k):
                print(f"  Warning: Skipping sequence")
                continue
#loop through the positions in the sequence
            #subtract k to include the next character
            #set how to read each kmer
            #set how to read/position itself to read each next character
#update the dictionary w/ accumulated counts
            for i in range(len(sequence) - k):
                kmer = sequence[i:i+k]
                next_char = sequence[i+k]

                kmer_data = update_kmer_count(kmer_data, kmer, next_char)
#creates output file with kmder dictionary
    write_results_to_file(kmer_data, output_file)

#can only run this function directly, not just whenever script is run
if __name__ == '__main__':
    main()
