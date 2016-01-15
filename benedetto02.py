import argparse
import sys
import jsonhandler
import warnings
import random
import os
import zlib
from collections import Counter


def extract_sample(text,size_sample):
    size_text = len(text)
    if size_text < size_sample:
        return text
    offset = random.randint(0,size_text-size_sample)
    return text[offset:offset+size_sample]

def relative_zlib_entropy(corpus, unknown, level=6):
    size_corpus = len(zlib.compress(corpus, level))
    size_together = len(zlib.compress(corpus+unknown, level))
    return size_together - size_corpus

def dict_entropy(corpus, unknown, level=6):
    obj = zlib.compressobj(zdict=corpus,level=level)
    result = len(obj.compress(unknown))
    result += len(obj.flush())
    return result

def create_simple_ranking(candidates, unknown,
        method=relative_zlib_entropy):
    unknown_text = jsonhandler.getUnknownBytes(unknown)
    unknown_sample = extract_sample(unknown_text, 8*1024)
    results = []
    for author in candidates:
        for filename in jsonhandler.trainings[author]:
            corpus_text = jsonhandler.getTrainingBytes(author,filename)
            corpus_sample = extract_sample(corpus_text,48*1024)
            entropy = method(corpus_sample,unknown_sample)
            results.append((author,filename,entropy))
    return sorted(results,key=lambda r:r[2])

def create_author_ranking(candidates, unknown, method, runs = 20):
    author_score = Counter()
    for i in range(runs):
        simple_ranking = create_simple_ranking(candidates,
                unknown, method = method)
        best_author = simple_ranking[0][0]
        second_author = simple_ranking[1][0]
        author_score[best_author] += 1
    return author_score.most_common()


def tira(corpusdir, outputdir):
    """
    Keyword arguments:
    corpusdir -- Path to a tira corpus
    outputdir -- Output directory
    """
    candidates = jsonhandler.candidates
    unknowns = jsonhandler.unknowns
    jsonhandler.loadJson(corpusdir)
    jsonhandler.loadTraining()
    authors = []
    scores = []

    for filename in unknowns:
        ranking = create_author_ranking(candidates, filename,
                method=dict_entropy)
#        ranking = create_simple_ranking(candidates, filename,
#                method=relative_zlib_entropy)
        author = ranking[0][0]
        score = 0.5
        authors.append(author)
        scores.append(score)
    jsonhandler.storeJson(outputdir, unknowns, authors, scores)
    

def main():
    parser = argparse.ArgumentParser(description='Tira submission for' +
            ' Language Trees and Zipping.')
    parser.add_argument('-i', 
                        action='store',
                        help='Path to input directory')
    parser.add_argument('-o', 
                        action='store',
                        help='Path to output directory')
    
    args = vars(parser.parse_args())
    
    corpusdir = args['i']
    outputdir = args['o']
    
    tira(corpusdir, outputdir)

if __name__ == "__main__":
    # execute only if run as a script
    # logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s: %(message)s')
    main()
