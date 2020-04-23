import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import information_content

# procedure takes in two words as synset


ic_file = sys.argv[1]
wsd_test_file = open(sys.argv[2], "r+")
results_out = open(sys.argv[3], "r+")

## this needs to compute the most similar sense pair between the words and output
## their similarity--> so we loop through each of them and grab the ones with the

# wn.synsets('dog') returns a list of synsets
def resnik_similarity(word1, word2):

    brown_ic = wordnet_ic.ic('ic-brown-resnik-add1.dat')
    max_subsumer_ic = 0
    for w1_synset in wn.sysnets(word1):
        for w2_sysnet in wn.synsets(word2):
            subsumers = w1_synset.common_hypernyms(w2_sysnet)

            if len(subsumers) == 0:
                subsumer_ic = 0
            else:
                # get the information content value for the most specific/informative subsumer
                subsumer_ic = max(information_content(sub, brown_ic) for sub in subsumers)

            if max_subsumer_ic < subsumer_ic:
                max_subsumer_ic = subsumer_ic
                most_similar_syn_w1 = w1_synset
                most_similar_syn_w2 = w2_sysnet

    return max_subsumer_ic, most_similar_syn_w1, most_similar_syn_w2





# dog = wn.synset('dog.n.01')
# cat = wn.synset('cat.n.01')
# hit = wn.synset('hit.v.01')
# slap = wn.synset('slap.v.01')

# print(resnik_similarity(dog, cat))
# print(resnik_similarity(hit, slap))

# grab test lines
wtf_lines = wsd_test_file.readlines()

# want to grab the first word and compute the similarity of each of the ones
# thereafter, printing as we go (on the same line) as

for line in wtf_lines:
    probe_word = line.split("\t")[0]
    context_list = line.split("\t")[1].split(",")
    result_line = ""
    max_rs = 0
    for context_word in context_list:
        ## pick the sense based on which sense its chosen with the word
        ## that its most similar to, or the synset that is chosen the most
        rs, probe_syn, context_syn = resnik_similarity(probe_word, context_word)
        result_line += '{},{},{}\t'.format(probe_word, context_word, rs)
        if rs > max_rs:
            max_rs = rs
            preferred_sense = probe_syn
    result_line += "\t{}".format(preferred_sense)
    results_out.write(result_line)





# find most similar word and then how do we pick which sense we want?