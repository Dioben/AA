def convertFile(filename):
    f = open(filename,"r")
    contents = f.read()
    contents = [x.upper() for x in contents if x.isalpha()]
    f.close()
    f = open(filename,"w")
    f.write("".join(contents))
    f.close()

if __name__=="__main__":
    convertFile("english.txt")
    convertFile("french.txt")
    convertFile("german.txt")