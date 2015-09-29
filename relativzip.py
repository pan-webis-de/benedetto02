import warnings
import random
import os
import zlib
from collections import Counter

import jsonhandler

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
