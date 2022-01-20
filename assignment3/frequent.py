#just a small example on how to keep track of heavy hitters with minheap and CountMinSketch
#this always stores the top X words regardless of estimated frequency, compares results to words that make up x 

import argparse
import json
from collections import Counter
from minSketch import CountMinSketch

from heapq import heapify,heappushpop,heappush


if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--file",help="input file", default="english.txt")
    parser.add_argument("--hashes",help="how many hash functions to use", type=int, default=5)
    parser.add_argument("--slots",help="size of each hash table", type=int, default=700)
    parser.add_argument("--heapsize",help="heap size", type=int, default=100)
    parser.add_argument("--cutoff",help="heavy hitters make up cutoff % of all words", type=float, default=50.0)
    args = parser.parse_args()

    with  open(args.file,"r") as f:
        words = f.read().split(" ")
    real = Counter(words)
    sketch = CountMinSketch(d=args.hashes, m= args.slots )
    heap = [(0,"") for _ in range(args.heapsize)]
    heapify(heap)
    for word in words: #let's pretend this is a stream and we don't know all the words
        sketch.update(word)
        val = sketch.query(word)
        wordseen = [i for i,s in enumerate(heap) if s[1] == word] #only supposed to have one element at most
        if wordseen:
            heap[wordseen[0]] = (val,word)
            heapify(heap)
        else:    
            heappushpop(heap,(val,word)) #attempt to add this to heap
    
    #feedback
    top = sorted(real.keys(), key=lambda x:real[x], reverse=True)
    cutoff = sum(real.values()) *args.cutoff/100
    curr = 0
    for i,x in enumerate(top):
        curr+=real[x]
        if curr>cutoff:
            break
    top =  set(top[:i+1])
    est = set ([x[1] for x in heap])

    

    prec = len(top.intersection(est))/len(top)
    rec = len(top.intersection(est))/len(est)
    fscore = 2*prec*rec /(rec+prec) 
    print("Precision is ",prec)
    print("Recall is ",rec)
    print("FScore is ",fscore)



    
