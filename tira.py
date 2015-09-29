# Usage:
# loadJson(corpusname), with corpusname from commandline
# OPTIONAL: loadTraining()
# OPTIONAL: getTrainingText(jsonhandler.candidate[i], jsonhandler.trainings[jsonhandler.candidates[i]][j]), gets trainingtext j from candidate i as a string
# getUnknownText(jsonhandler.unknowns[i]), gets unknown text i as a string
# storeJson(candidates, texts, scores), with list of candidates as candidates (jsonhandler.candidates can be used), list of texts as texts and list of scores as scores, last argument can be ommitted

import jsonhandler
import sys

from relativzip import (create_simple_ranking, create_author_ranking, relative_zlib_entropy, dict_entropy)

candidates = jsonhandler.candidates
unknowns = jsonhandler.unknowns
corpus = sys.argv[1]
jsonhandler.loadJson(corpus)

# If you want to do training:
jsonhandler.loadTraining()

# Create lists for your answers (and scores)
authors = []
scores = []

for filename in unknowns:
    # Get content of unknown file 'file' as a string with:
    # jsonhandler.getUnknownText(file)
    # Determine author of the file, and score (optional)
    ranking = create_author_ranking(candidates, filename,
            method=dict_entropy)
    author = ranking[0][0]
    score = 0.5
    authors.append(author)
    scores.append(score)

# Save results to json-file out.json (passing 'scores' is optional)
jsonhandler.storeJson(unknowns, authors, scores)
