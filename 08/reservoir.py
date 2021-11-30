import random

def samplingv1(array,K):
    in_sample=  [False for _ in array]
    N = len(array)
    for _ in range(K):
        r = random.randint(0, N-1 )
        in_sample[r] = True
    return [array[x] for x in range(N) if in_sample[x]]

def samplingv2(array,K):
    in_sample = [x for x in array[:K]]
    read = K
    for x in array[K:]:
        r = random.randint(0, read-1)
        if (r<=K):
            in_sample[r]=x
        read+=1
    return in_sample