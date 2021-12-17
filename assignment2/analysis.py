import argparse
import json

def upscaleValues(data,fixedMult,dynamicMod,memorized = []):
    for idx in range(len(data['static'])):
        run = data['static'][idx]
        data['static'][idx] = {key:value*fixedMult for key,value in run.items()}

    for idx in range(len(data['dynamic'])):
        run = data['dynamic'][idx]
        for key,value in run.items():
            try:
                run[key] = memorized[value]
            except:
                memorized+=[dynamicMod(x) for x in range(len(memorized),value+21)] #advance memorization
                run[key] = memorized[value]
    return data


def inverseDynamicMod(value):
    #my factor is 1/(sqrt(2)**k)
    #equivalent to 1/(2 **1/2 **k) = 1/(2 **k/2)
    #meaning 2**(k/2)-1 events until expected value is k
    #from slides: k = log2( n/2 + 1 ) = floor(log2(n/2))+1 = floor(log2(n)-1+1) = floor(log(2))
    # k = floor(log2(n)) -> 2**k = n ?
    return 2 ** value  #TODO: ASK TEACHER ABOUT THIS

if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--source",help="input data json file", default="results.json")
    args = parser.parse_args()
    f = open(args.source,"r")
    data = json.load(f)
    f.close()
    for info in data.values():
        upscaleValues(info,16,inverseDynamicMod,[inverseDynamicMod(x) for x in range(101)])
        