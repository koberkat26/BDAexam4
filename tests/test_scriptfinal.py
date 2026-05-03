import os
import pytest
from kmer_analyzer import (
    validate_sequence,
    update_kmer_count,
    count_kmers_with_context,
    write_results_to_file)

############################validate_sequence tests###########################
#test the first function to make sure its reading sequences correctly based on substring size/length

#create a test function with pytest to run all these at once
@pytest.mark.parametrize("sequence,k,expected", [
    ("ATGCGT", 3, True),      #tests a normal seq
    ("AT1CGT", 3, False),     #tests digits in seq
    ("ATG CGT", 3, False),    #tests spaces in seq
    ("AT", 3, False),         #tests strings =too short
    ("", 3, False),           #tests strings =empty
    ("atgcgt", 3, True),      #tests if lowercase allowed
])
def test_validate_sequence(sequence, k, expected):
    assert validate_sequence(sequence, k) == expected



#####################################update_kmer_count tests##################################
#testing 2nd function that updates the dictionary with kmers/counts/characters

def test_update_kmer_count_basic():
    data = {}
    data = update_kmer_count(data, "ATG", "C")

    assert "ATG" in data
    assert data["ATG"]["count"] == 1
    assert data["ATG"]["next_chars"]["C"] == 1

#function to test that the counts are increasing properly
def test_update_kmer_count_multiple():
    #creates empty data dictionary for the results to go into
    data = {}
    data = update_kmer_count(data, "ATG", "C")
    data = update_kmer_count(data, "ATG", "C")
    data = update_kmer_count(data, "ATG", "A")

    assert data["ATG"]["count"] == 3
    assert data["ATG"]["next_chars"]["C"] == 2
    assert data["ATG"]["next_chars"]["A"] == 1



##############################################count_kmers_with_context tests###################################3

#function to test that characters are being counted/recognized correctly
##gives example seq & substring length
##writes what the next character after a substring should be & the proper freq/count
def test_count_kmers_simple():
    sequence = "ATGCGT"
    k = 3
    result = count_kmers_with_context(sequence, k)
    assert result["ATG"]["next_chars"]["C"] == 1
    assert result["TGC"]["next_chars"]["G"] == 1
    assert result["GCG"]["next_chars"]["T"] == 1
#confirms that seq gets sliced/indexed correctly & slides along to next string correctly

#test to check that kmers get counted correctly & accumulate when theres multiple
def test_count_kmers_full_structure():
    sequence = "ATGATG"
    k = 3

    result = count_kmers_with_context(sequence, k)

    expected = {
        "ATG": {
            "count": 1,
            "next_chars": {"A": 1}
        },
        "TGA": {
            "count": 1,
            "next_chars": {"T": 1}
        },
        "GAT": {
            "count": 1,
            "next_chars": {"G": 1}
        }
    }

    assert result == expected

##############write_results_to_file tests############################3

#creates temporary folder so files dont get overwritten
def test_write_results_to_file(tmp_path):
    #create fake data to read
    data = {
        "ATG": {"count": 2, "next_chars": {"C": 1, "A": 1}},
        "TGC": {"count": 1, "next_chars": {"G": 1}}}
    #create output file in the temporary folder
    output_file = tmp_path / "output.txt"
    #put the results into the output file
    write_results_to_file(data, output_file)
    #check the file exists
    assert os.path.exists(output_file)
    #reads the contents of the file
    content = output_file.read_text()
    #validate the output
    assert "ATG" in content
    assert "A:1" in content
    assert "C:1" in content
