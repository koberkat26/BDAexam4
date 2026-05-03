#Reese Kober
#BIO-539
#Exam 4

import sys

#creates a function to validate the seq using input values of a certain seq and the length of a substring 'k'
#if the length of the seq is less than k, then stops= false
#if a nucleotide in the seq is anything besides the 4 bases (upper/lowercase), then stops= false
##this prevents incorrect letters/spaces/digits/etc from getting counted
#if passes these = true
def validate_sequence(sequence, k):
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
    kmer_data = {}
    #loops through the sequence to get all possible substrings & following characters
    for i in range(len(sequence) - k):
        #extract the kmer, depending on where you start in the sequence (at position "i" which could be 0, 1, etc)
        kmer = sequence[i:i+k]
        #get next character after the sequence
        next_char = sequence[i+k]
        #update the dictionary with the new kmers and characters
        kmer_data = update_kmer_count(kmer_data, kmer, next_char)
    #print out the dictionary
    return kmer_data


#printing the dictionary into an output file
def write_results_to_file(kmer_data, output_filename):
  #sorts the kmers in the dictionary alphabetically
    sorted_kmers = sorted(kmer_data.keys())
    #open the new output file to write in new info
    with open(output_filename, 'w') as f:
      #loop through each kmer in the sorted list
        for kmer in sorted_kmers:
          #and get the next character after each kmer
            next_chars = kmer_data[kmer]['next_chars']
            #the next characters get joined together into a string
            next_char_str = " ".join(
                f"{char}:{freq}" 
                #loop through each character/freq pair & formats them the same^
                #sorts alphabetically
                for char, freq in sorted(next_chars.items())
            )
            #writes into the file the kmer and following character string and the count, changed to include total kmer count
            f.write(f"{kmer} {next_char_str}\n")

#tie everything together into this main function
def main():
  #what to input to run this function
    #the sequence file, kmer size, output file name
    sequence_file = sys.argv[1]
    k = int(sys.argv[2])
    output_file = sys.argv[3]
#check that shows where the seq are being read from to confirm correct file
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
              #prints a warning message if it doesnt pass that
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
