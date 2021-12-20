def convertFile(filename,output):
    f = open(filename,"r")
    contents = f.read()
    contents = [x.upper() for x in contents if x.isalpha()]
    f.close()
    f = open(output,"w")
    f.write("".join(contents))
    f.close()

if __name__=="__main__":
    convertFile("englishText.txt","english.txt")
    convertFile("frenchText.txt","french.txt")
    convertFile("germanText.txt","german.txt")