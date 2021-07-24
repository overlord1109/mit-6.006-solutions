#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.multi_dict = {}
        for pair in pairs:
            self.multi_dict.put(self, pair[0], pair[1])
    # Associates the value v with the key k.
    def put(self, k, v):
        if not self.get(k):
            self.multi_dict[k] = [v]
        else:
            self.multi_dict[k].append(v)

    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        try:
            return self.multi_dict[k]
        except KeyError:
            return []

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    try:
        subseq = ''
        i = 0
        while len(subseq) < k:
            subseq += seq.next()
        rhash = RollingHash(subseq)
        while True:
            yield (rhash.current_hash(), subseq, i)
            i = i + 1
            previtm = subseq[0] 
            nextitm = seq.next()
            rhash.slide(previtm, nextitm)
            subseq = subseq[1:] + nextitm 
    except StopIteration:
        return

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    try:
        subseq = ''
        i = 0
        while len(subseq) < k:
            subseq += seq.next()
        rhash = RollingHash(subseq)
        while True:
            yield (rhash.current_hash(), subseq, i)
            if (i % m == 0):
                #skip
                for skip in range(1, m - k + 1):
                    seq.next()
            previtm = subseq[0] 
            nextitm = seq.next()
            rhash.slide(previtm, nextitm)
            subseq = subseq[1:] + nextitm
            if(i % m == k-1):
                i = i + m - k + 1
            else:
                i = i + 1
    except StopIteration:
        return

def retardedIntervalSubsequenceHashes(seq, k, m):
    try:
        i=0
        for yield_val in subsequenceHashes(seq, k):
            yield (yield_val[0], yield_val[1], i)
            if (i % m == 0):
                #skip
                for skip in range(1, m - k + 1):
                    seq.next()
            if(i % m == k-1):
                i = i + m - k + 1
            else:
                i = i + 1
    except StopIteration:
        return


# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    multi_dict = Multidict()
    for subseq_hashes in retardedIntervalSubsequenceHashes(a, k, m):
        multi_dict.put(subseq_hashes[0], (subseq_hashes[1], subseq_hashes[2]))
    for subseq_hashes in subsequenceHashes(b, k):
        matching_hash_list = multi_dict.get(subseq_hashes[0])
        for possible_matches in matching_hash_list:
            if(possible_matches[0] == subseq_hashes[1]):
                yield (possible_matches[1], subseq_hashes[2])

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
