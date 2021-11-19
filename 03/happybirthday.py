
import random
from collections import Counter
SPOTS = 6
POSS = ["Q","W","E","R","T","Y"]
TURNS =15


def generate():
    answer = [random.choice(POSS) for x in range(SPOTS)]
    print("ANSWER HAS BEEN GENERATED ")
    print(f"LENGTH IS {SPOTS}")
    return answer

print("Valid Options are",POSS)


while 1:
    answer = generate()
    seen_ans = {}
    for x in answer:
        if x in seen_ans:
            seen_ans[x]+=1
        else:
            seen_ans[x]=1
    TURN=1
    while TURN<TURNS:
        TURN+=1
        inp = input()[:SPOTS].upper()
        rightpos=0
        same_idx = []
        inp_clone=inp
        ans_clone = answer
        for x in range(len(answer)):
            if answer[x]==inp[x]:
                rightpos+=1
                same_idx.append(x)
        
        while len(same_idx):
            x = same_idx[0]
            same_idx = [y-1 for y in same_idx[1:]]
            inp_clone = inp_clone[:x]+inp_clone[x+1:]
            ans_clone = ans_clone[:x]+ans_clone[x+1:]

        wrongpos = 0

        ans_counter = Counter(ans_clone)
        inp_counter = Counter(inp_clone)
        
        for x,y in ans_counter.items():
            if x in inp_counter:
                wrongpos+=min(inp_counter[x],y)

        print(f"{rightpos} RIGHT ,{wrongpos} MISPLACED")
        if rightpos==SPOTS:
            print("CONGRATION")
            break

