from relativzip import create_ranking, compare_methods
import json
import os.path

def import_json(filename):
    with open(filename) as f:
        result = json.load(f)
    return result


def test_corpus(letter):
    corpus_info = import_json("corpus" + letter+".json")
    ground_truth = import_json("ground-truth.json")
    num_first = 0
    num_second = 0
    for entry in ground_truth[letter]:
        unknown_file = entry["name"]
        ranking = create_ranking(corpus_info, unknown_file + ".txt")
        author = entry["author"]
        #best match is the real author
        if ranking[0][0] == author:
            num_first  += 1
            num_second += 1
            print("file " + unknown_file + " correctly recognized as " +
                    author)
        #second best match is the real author
        elif ranking[1][0] == author:
            num_second += 1
            print("file " + unknown_file + " almost recognized as " +
                    author + " (first guess was " + ranking[0][0] + ")")
        else:
            print("file " + unknown_file + " not recognized as " +
                    author + " (guesses were " + ranking[0][0] + ", " +
                    ranking[1][0] + ")")
    print("N. of texts:", len(ground_truth[letter]))
    print("N. of successes 1: ", num_first)
    print("N. of successes 2: ", num_second)

def test_all_corpora():
    for letter in ['A', 'C', 'I']:
        test_corpus(letter)


def compare_impl():
    corpus_info = import_corpus_info("corpusI.json")
    for i in range(1,15):
        unknown_file = "12Itest" + str(i).zfill(2)
        compare_methods(corpus_info, unknown_file + ".txt")

test_all_corpora()
