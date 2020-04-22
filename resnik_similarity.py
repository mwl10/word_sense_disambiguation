import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import information_content

# procedure takes in two words as synsets

def resnik_similarity(word1, word2):
    # should also make sure both words are the same part of speech type
    if word1.pos != word2.pos:
        raise Exception("Need both words to be the same part of speech")

    brown_ic = wordnet_ic.ic('ic-brown-resnik-add1.dat')

    subsumers = word1.common_hypernyms(word2)

    if len(subsumers) == 0:
        subsumer_ic = 0
    else:
        # get the information content value for the most specific/informative subsumer
        subsumer_ic = max(information_content(sub, brown_ic) for sub in subsumers)

    return subsumer_ic

dog = wn.synset('dog.n.01')
cat = wn.synset('cat.n.01')
hit = wn.synset('hit.v.01')
slap = wn.synset('slap.v.01')

print(resnik_similarity(dog, cat))
print(resnik_similarity(hit, slap))









