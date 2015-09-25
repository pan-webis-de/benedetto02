from collections import Counter
from functools import partial
import json
import logging
import os.path
import sys
import warnings

from relativzip import (create_simple_ranking, relative_zlib_entropy,
                       dict_entropy, compare_methods)

def import_json(filename):
    with open(filename) as f:
        result = json.load(f)
    return result

def create_author_ranking(corpus_info, unknown_filename, method, runs = 20):
    author_score = Counter()
    for i in range(runs):
        simple_ranking = create_simple_ranking(corpus_info,
                unknown_filename, method = method)
        best_author = simple_ranking[0][0]
        second_author = simple_ranking[1][0]
        author_score[best_author] += 1
    return author_score.most_common()

def test_corpus(letter, ranking_method):
    ground_truth = import_json("ground-truth.json")[letter]
    corpus_info = import_json(ground_truth["corpus"])
    num_first = 0
    num_second = 0
    total = 0
    for entry in ground_truth["files"]:
        unknown_file = entry["name"]
        author = entry["author"]
        if author == "None":
            continue
        total += 1
        ranking = ranking_method(corpus_info, unknown_file + ".txt")
        #best match is the real author
        if ranking[0][0] == author:
            num_first  += 1
            num_second += 1
            logging.info("file " + unknown_file + " correctly recognized as " +
                    author)
        #we have only one guess (which is wrong)
        elif len(ranking) == 1:
            logging.info("file " + unknown_file + " not recognized as " +
                    author + " (guess was " + ranking[0][0] + ")")
        #second best match is the real author
        elif ranking[1][0] == author:
            num_second += 1
            logging.info("file " + unknown_file + " almost recognized as " +
                    author + " (first guess was " + ranking[0][0] + ")")
        else:
            logging.info("file " + unknown_file + " not recognized as " +
                    author + " (guesses were " + ranking[0][0] + ", " +
                    ranking[1][0] + ")")
    print("N. of texts:", total)
    print("N. of successes 1: ", num_first)
    print("N. of successes 2: ", num_second)
    print("")

def test_all_corpora():
    for i in range(10):
        print ("Compression level:", i)
        relative = partial(relative_zlib_entropy, level=i)
        dictionary = partial(dict_entropy, level=i)
        methods = [
            ("relative, single run",
            partial(create_simple_ranking, method=relative)),
            ("dictionary, single run",
            partial(create_simple_ranking, method=dictionary)),
            ("relative, 10 runs",
            partial(create_author_ranking, method=relative,
                runs=10)),
            ("dictionary, 10 runs",
            partial(create_author_ranking, method=dictionary,
                runs=10)),
            ("relative, 20 runs",
            partial(create_author_ranking, method=relative,
                runs=20)),
            ("dictionary, 20 runs",
            partial(create_author_ranking, method=dictionary,
                runs=20))]
        for letter in ['A', 'B', 'C', 'D', 'I', 'J']:
            print (letter)
            for name, func in methods:
                print (name)
                test_corpus(letter, func)
            sys.stdout.flush()

def test_table():
    for i in range(10):
        print ("Compression level:", i)
        relative = partial(relative_zlib_entropy, level=i)
        dictionary = partial(dict_entropy, level=i)
        methods = [
            ("relative, single run",
            partial(create_simple_ranking, method=relative)),
            ("relative, 10 runs",
            partial(create_author_ranking, method=relative,
                runs=10)),
            ("relative, 20 runs",
            partial(create_author_ranking, method=relative,
                runs=20)),
            ("dictionary, single run",
            partial(create_simple_ranking, method=dictionary)),
            ("dictionary, 10 runs",
            partial(create_author_ranking, method=dictionary,
                runs=10)),
            ("dictionary, 20 runs",
            partial(create_author_ranking, method=dictionary,
                runs=20))]
        for name, func in methods:
            print (name)
            test_corpus("I+J", func)
        sys.stdout.flush()


def compare_impl():
    corpus_info = import_corpus_info("corpusI.json")
    for i in range(1,15):
        unknown_file = "12Itest" + str(i).zfill(2)
        compare_methods(corpus_info, unknown_file + ".txt")

warnings.simplefilter("ignore")
#logging.basicConfig(level=logging.INFO)

test_table()
