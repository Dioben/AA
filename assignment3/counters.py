import argparse
import json
from collections import Counter
from minSketch import CountMinSketch



if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--files",help="comma separated input files", default="english.txt,french.txt,german.txt")
    parser.add_argument("--output",help="file to dump information into")
    args = parser.parse_args()
    filepaths = args.files.split(",")
   
    results = {fp.removesuffix(".txt"):{} for fp in filepaths}
    for filepath in filepaths:
        keyname = filepath.removesuffix(".txt")
        with  open(filepath,"r") as f:
            words = f.read().split(" ")
        real = Counter(words)
        sketch = CountMinSketch(d=7, m=len(real.keys()) ) #7 functions, as many rows as there are words
        for word in words:
            sketch.update(word)
        results[keyname]['real'] = real
        results[keyname]['sketch'] = {x:int(sketch.query(x)) for x in real.keys()} #converting is necessary because of JSON
    if args.output:
        f = open(args.output,"w")
        json.dump(results,f)
        f.close()
    else:
        print(results)  

