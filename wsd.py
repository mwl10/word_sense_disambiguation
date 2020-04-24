import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import information_content
import sys

# grab command line arguments
ic_file = sys.argv[1]
wsd_test_file = open(sys.argv[2], "r")
results_out = open(sys.argv[3], "w")

# here we add the ic parameter instead of directly injecting the
# ic-brown-resnik-add1.dat file

# computes the resnik_similarity of the most similar sense pair of the two words given an input ic file
def resnik_similarity(word1, word2, ic):
    # initializing
    _ic = wordnet_ic.ic(ic)
    max_subsumer_ic = 0
    most_similar_syn_w1 = wn.synsets(word1)[0]

    # if the word isn't in wordnet, ignore it
    if len(wn.synsets(word2)) == 0:
        most_similar_syn_w2 = 0
    # double for loop to pick the most similar sense of each of the two words
    for w1_synset in wn.synsets(word1):
        for w2_sysnet in wn.synsets(word2):
            subsumers = w1_synset.common_hypernyms(w2_sysnet)

            if len(subsumers) == 0:
                subsumer_ic = 0
            else:
                # get the information content value for the most specific/informative subsumer
                subsumer_ic = max(information_content(sub, _ic) for sub in subsumers)
            # make sure we keep the most similar sense pair
            if max_subsumer_ic < subsumer_ic:
                max_subsumer_ic = subsumer_ic
                most_similar_syn_w1 = w1_synset
                most_similar_syn_w2 = w2_sysnet

    return max_subsumer_ic, most_similar_syn_w1, most_similar_syn_w2


# grab test lines
wtf_lines = wsd_test_file.readlines()

# make sure results file is empty so we can write to it
results_out.truncate(0)

# sift through the lines in the wsd test lines
for line in wtf_lines:
    # get rid of the newline character
    line = line.split('\n')[0]
    # probe words and context words are separated by tab characters
    list = line.split("  ")
    # grab the probe word
    probe_word = list[0]
    # grab the context words and split them according to the commas that separate them
    context_list = list[1].split(",")
   # print(context_list)

    result_line = ""
    max_rs = 0
    # sift through the context words in the context_list
    for context_word in context_list:
        # get the rs similarity, and the particular probe
        # synset relative to the probe word and the current context word
        rs, probe_syn, context_syn = resnik_similarity(probe_word, context_word, ic_file)

        # write to the line in the form word1,word2,similarity
        result_line += '{},{},{}\t'.format(probe_word, context_word, rs)

        # pick the sense based on which sense is chosen with the word
        # that its most similar to out of the context words
        if rs > max_rs:
            max_rs = rs
            preferred_sense = probe_syn
    # write out the synset we picked

    result_line += "{}\n".format(preferred_sense)
    results_out.write(result_line)


# computing accuracy

wsd_test_file.close()
results_out.close()

# The intuition behind this algorithm is essentially the same intuition
# exploited by Lesk (1986), Sussna (1993), and others: the most plausible
# assignment of the senses to multiple co-occuring words is the
# one that maximizes relatedness of meaning among the senses chosen