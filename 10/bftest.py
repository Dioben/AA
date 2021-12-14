from bloom_filter_V_1 import BloomFilter

bf = BloomFilter(1000,5,hash)

count = 0
for i in range(ord('a'), ord('z')+1):
    letter = chr(i)
    count+=bf.contains(letter)
    bf.insert(letter,letter)

print("FP:",count)