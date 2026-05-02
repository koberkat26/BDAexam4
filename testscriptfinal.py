import os
import pytest
from kmer_analyzer import (
    validate_sequence,
    update_kmer_count,
    count_kmers_with_context,
    write_results_to_file)

############################validate_sequence tests###########################
#test the first function to make sure its reading sequences correctly based on substring size/length

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


# ------------------------
# update_kmer_count tests
# ------------------------

def test_update_kmer_count_basic():
    data = {}
    data = update_kmer_count(data, "ATG", "C")

    assert "ATG" in data
    assert data["ATG"]["count"] == 1
    assert data["ATG"]["next_chars"]["C"] == 1


def test_update_kmer_count_multiple():
    data = {}
    data = update_kmer_count(data, "ATG", "C")
    data = update_kmer_count(data, "ATG", "C")
    data = update_kmer_count(data, "ATG", "A")

    assert data["ATG"]["count"] == 3
    assert data["ATG"]["next_chars"]["C"] == 2
    assert data["ATG"]["next_chars"]["A"] == 1


# ------------------------
# count_kmers_with_context tests
# ------------------------

def test_count_kmers_simple():
    sequence = "ATGCGT"
    k = 3

    result = count_kmers_with_context(sequence, k)

    assert result["ATG"]["next_chars"]["C"] == 1
    assert result["TGC"]["next_chars"]["G"] == 1
    assert result["GCG"]["next_chars"]["T"] == 1


def test_count_kmers_repeated():
    sequence = "ATGATG"
    k = 3

    result = count_kmers_with_context(sequence, k)

    # ATG appears twice, followed by A once
    assert result["ATG"]["count"] == 1 or result["ATG"]["count"] == 2


# ------------------------
# write_results_to_file tests
# ------------------------

def test_write_results_to_file(tmp_path):
    data = {
        "ATG": {"count": 2, "next_chars": {"C": 1, "A": 1}},
        "TGC": {"count": 1, "next_chars": {"G": 1}}
    }

    output_file = tmp_path / "output.txt"

    write_results_to_file(data, output_file)

    assert os.path.exists(output_file)

    content = output_file.read_text()

    assert "ATG" in content
    assert "A:1" in content
    assert "C:1" in content
