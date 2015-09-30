import argparse
import sys

import jsonhandler
from relativzip import (create_simple_ranking, create_author_ranking, relative_zlib_entropy, dict_entropy)

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
