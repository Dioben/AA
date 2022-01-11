import argparse
import json
from itertools import Counter
from minSketch import CountMinSketch



if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--files",help="comma separated input files", default="english.txt,french.txt,german.txt")
    parser.add_argument("--output",help="file to dump information into")
    args = parser.parse_args()
    filepaths = args.files.split(",")
   
    results = {}
    for filepath in filepaths:
        with  open(filepath,"r") as f:
            words = f.read().split(" ")
        results[filepath]['real'] = Counter(words)
        #TODO: GET,SAVE SKETCH RESULTS

    if args.output:
        f = open(args.output,"w")
        json.dump(results,f)
        f.close()
    else:
        print(results)  

