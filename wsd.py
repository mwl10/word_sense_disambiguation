import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import information_content
import os
import sys

# procedure takes in two words as synset

ic_file = sys.argv[1]
wsd_test_file = open(sys.argv[2], "r+")
results_out = open(sys.argv[3], "r+")

## this needs to compute the most similar sense pair between the words and output
## their similarity--> so we loop through each of them and grab the ones with the

# here we add the ic parameter instead of directly injecting the
# ic-brown-resnik-add1.dat file

# NOT LIKING THE FIRST LINE

def resnik_similarity(word1, word2, ic):
    _ic = wordnet_ic.ic(ic)
    max_subsumer_ic = 0
    most_similar_syn_w1 = wn.synsets(word1)[0]
    most_similar_syn_w2 = wn.synsets(word2)[0]
    for w1_synset in wn.synsets(word1):
        for w2_sysnet in wn.synsets(word2):
            subsumers = w1_synset.common_hypernyms(w2_sysnet)

            if len(subsumers) == 0:
                subsumer_ic = 0
            else:
                # get the information content value for the most specific/informative subsumer
                subsumer_ic = max(information_content(sub, _ic) for sub in subsumers)

            if max_subsumer_ic < subsumer_ic:
                max_subsumer_ic = subsumer_ic
                most_similar_syn_w1 = w1_synset
                most_similar_syn_w2 = w2_sysnet

    return max_subsumer_ic, most_similar_syn_w1, most_similar_syn_w2


# grab test lines
wtf_lines = wsd_test_file.readlines()

# make sure results file is empty so we can write to it
results_out.truncate(0)


# want to grab the first word and compute the similarity of each of the ones
# thereafter, printing as we go (on the same line) as

# sift through the lines in the wsd test lines
for line in wtf_lines:
    # get rid of the newline character
    line = line.split('\n')[0]
    # probe words and context words are separated by tab characters
    list = line.split("\t")
    # grab the probe word
    probe_word = list[0]
    # grab the context words and split them according to the commas that separate them
    context_list = line[1].split(",")

    result_line = ""
    max_rs = 0
    # sift through the context words in the context_list
    for context_word in context_list:
        # get the rs similarity, and the particular probe
        # synset relative to the probe word and the current context word
        rs, probe_syn, context_syn = resnik_similarity(probe_word, context_word, ic_file)

        result_line += '{},{},{}\t'.format(probe_word, context_word, rs)

        # pick the sense based on which sense its chosen with the word
        # that its most similar to, or the synset that is chosen the most
        if rs > max_rs:
            max_rs = rs
            preferred_sense = probe_syn
    result_line += "\t{}".format(preferred_sense)
    results_out.write(result_line)


# The intuition behind this algorithm is essentially the same intuition
# exploited by Lesk (1986), Sussna (1993), and others: the most plausible
# assignment of the senses to multiple co-occuring words is the
# one that maximizes relatedness of meaning among the senses chosen