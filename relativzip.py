import warnings
import random
import os
import zlib


def extract_sample(filename,size_sample):
    with open(filename,'rb') as f:
        size_file = os.path.getsize(filename)
        if size_file < size_sample:
            warnings.warn( filename + " too short to take a sample of full size")
            return bytearray(f.read())
        offset = random.randint(0,size_file-size_sample)
        f.seek(offset)
        return bytearray(f.read(size_sample))

def relative_zlib_entropy(corpus, unknown, level=6):
    size_corpus = len(zlib.compress(corpus, level))
    size_together = len(zlib.compress(corpus+unknown, level))
    return size_together - size_corpus

def dict_entropy(corpus, unknown, level=6):
    obj = zlib.compressobj(zdict=corpus,level=level)
    result = len(obj.compress(unknown))
    result += len(obj.flush())
    return result

def create_simple_ranking(corpus_info, unknown_filename,
        method=relative_zlib_entropy):
    unknown_sample = extract_sample(unknown_filename, 8*1024)
    results = []
    for entry in corpus_info:
        author = entry["author"]
        for filename in entry["files"]:
            corpus_sample = extract_sample(filename,48*1024)
            entropy = method(corpus_sample,unknown_sample)
            results.append((author,filename,entropy))
    return sorted(results,key=lambda r:r[2])

def compare_methods(corpus_info, unknown_filename):
    unknown_sample = extract_sample(unknown_filename, 8*1024)
    results = []
    for entry in corpus_info:
        author = entry["author"]
        for filename in entry["files"]:
            corpus_sample = extract_sample(filename,48*1024)
            a = relative_zlib_entropy(corpus_sample,unknown_sample)
            b = dict_entropy(corpus_sample,unknown_sample)
