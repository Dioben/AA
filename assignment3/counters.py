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
   
    results = {fp.removesuffix(".txt"):{"sketch":[],"real":{}} for fp in filepaths}
    for filepath in filepaths:
        keyname = filepath.removesuffix(".txt")
        with  open(filepath,"r") as f:
            words = f.read().split(" ")
        real = Counter(words)
        for hashes in range(3,11):
            for hashsize in range (1,21):
                sketch = CountMinSketch(d=hashes, m= int(len(real.keys()) *hashsize/10) )
                for word in words:
                    sketch.update(word)
                results[keyname]['sketch'].append({"hashes":hashes,"size":hashsize/10,"values": {x:int(sketch.query(x)) for x in real.keys()} } ) #converting is necessary because of JSON 
        results[keyname]['real'] = real
        
    if args.output:
        f = open(args.output,"w")
        json.dump(results,f)
        f.close()
    else:
        print(results)  

