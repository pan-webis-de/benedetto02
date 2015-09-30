import json, os
import argparse

corpusdir = ""
OUT_FNAME = "out.json"
TRUTH_FNAME = "ground-truth.json"

def eval(corpusdir, outputdir):
    ofile = open(os.path.join(outputdir, OUT_FNAME), "r")
    tfile = open(os.path.join(corpusdir, TRUTH_FNAME), "r")
    ojson = json.load(ofile)
    tjson = json.load(tfile)
    ofile.close()
    tfile.close()

    succ = 0
    fail = 0
    sucscore = 0
    failscore = 0
    for i in range(len(tjson["ground-truth"])):
    #for i in range(len(ojson["answers"])):
        if tjson["ground-truth"][i]["true-author"] == ojson["answers"][i]["author"]:
            succ += 1
            sucscore += ojson["answers"][i]["score"]
        else:
            fail += 1
            failscore += ojson["answers"][i]["score"]
            
    print("Fail: "+str(fail))
    print("Success: "+str(succ))
    print("Accuracy: "+str(succ/(succ+fail)))
    print("Fail score mean: "+str(failscore/fail))
    print("Success score mean: "+str(sucscore/succ))

def main():
    parser = argparse.ArgumentParser(description='Tira evaluation')
    parser.add_argument('-i', 
                        action='store',
                        help='Path to input directory')
    parser.add_argument('-o', 
                        action='store',
                        help='Path to output directory')
    
    args = vars(parser.parse_args())
    
    corpusdir = args['i']
    outputdir = args['o']
    
    eval(corpusdir, outputdir)

if __name__ == "__main__":
    main()
