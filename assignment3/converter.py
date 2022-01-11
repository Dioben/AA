import re
from nltk.corpus import stopwords

def convertFile(filename,output,stopwords = set()):
    with open(filename,"r") as f:
        contents = f.read()
        words = re.split(r"[^a-zA-Z]",contents)
        words = [x.lower() for x in words if x and x.lower() not in stopwords]
    with open(output,"w") as f:
        f.write(" ".join(words))

if __name__=="__main__":
    convertFile("englishText.txt","english.txt",set(stopwords.words('english')))
    convertFile("frenchText.txt","french.txt",set(stopwords.words('french')))
    convertFile("germanText.txt","german.txt",set(stopwords.words('german')))