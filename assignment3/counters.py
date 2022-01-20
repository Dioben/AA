import argparse
import json
from collections import Counter
from minSketch import CountMinSketch
from heapq import heapify,heappushpop


if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--files",help="comma separated input files", default="english.txt,french.txt,german.txt")
    parser.add_argument("--output",help="file to dump information into")
    args = parser.parse_args()
    filepaths = args.files.split(",")
   
    results = {fp.removesuffix(".txt"):{"sketch":[],"snapshot":[],"real":{}} for fp in filepaths}
    for filepath in filepaths:
        keyname = filepath.removesuffix(".txt")
        with  open(filepath,"r") as f:
            words = f.read().split(" ")
        real = Counter(words)
        for hashes in range(3,11):
            for hashsize in range (1,21):
                sketch = CountMinSketch(d=hashes, m= int(len(real.keys()) *hashsize/10) )
                heap = [(0,"") for _ in range(100)]
                heapify(heap)
                for word in words:
                    sketch.update(word)
                    val = sketch.query(word)
                    wordseen = [i for i,s in enumerate(heap) if s[1] == word] #only supposed to have one element at most
                    if wordseen:
                        heap[wordseen[0]] = (val,word)
                        heapify(heap)
                    else:    
                        heappushpop(heap,(val,word)) #attempt to add this to heap

                results[keyname]['snapshot'].append({"hashes":hashes,"size":hashsize/10, "values":[y for x,y in sorted(heap, reverse=True, key=lambda x: x[0]) ] }) #top 100 sketch values when the words actually appeared (therefore equal or smaller)
                results[keyname]['sketch'].append({"hashes":hashes,"size":hashsize/10,"values": {x:int(sketch.query(x)) for x in real.keys()} } ) #converting is necessary because of JSON 
        results[keyname]['real'] = real
        
        
    if args.output:
        f = open(args.output,"w")
        json.dump(results,f)
        f.close()
    else:
        print(results)  

