def convertFile(filename):
    f = open(filename,"rw")
    contents = f.read()
    contents = [ x.upper() for x in contents if x.isalpha()]
    f.write(contents)
    f.close()

if __name__=="__main__":
    convertFile("english.txt")
    convertFile("french.txt")
    convertFile("german.txt")