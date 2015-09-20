from relativzip import create_ranking, compare_methods
import json
import os.path

def import_corpus_info(filename):
    with open(filename) as f:
        result = json.load(f)
    return result

def test_corpus(letter, num_tests):
    corpus_info = import_corpus_info("corpus" + letter+".json")
    for i in range(1, num_tests+1):
        unknown_file = "12" + letter + "test" + str(i).zfill(2)
        ranking = create_ranking(corpus_info, unknown_file + ".txt")
        print("file " + unknown_file + " = " + ranking[0][0])
        if ranking[0][0] != ranking[1][0]:
            print("maybe = " + ranking[1][0])

def test_all_corpora():
    tests = [('A',6),('C',8),('I',14)]
    for letter, num in tests:
        test_corpus(letter, num)


def compare_impl():
    corpus_info = import_corpus_info("corpusI.json")
    for i in range(1,15):
        unknown_file = "12Itest" + str(i).zfill(2)
        compare_methods(corpus_info, unknown_file + ".txt")

test_all_corpora()
