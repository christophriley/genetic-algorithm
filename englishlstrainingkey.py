import os, sys,random, re
#go through the words individually and make them a new key file
def main():
    directory = os.getcwd()+"/data_WSD/word files/"
    if not os.path.exists("key_files/"):#it shouldn't
        os.makedirs("key_files/")
    for word in os.listdir(directory):
        f = open(directory+word)
        try:
            g = open(os.getcwd()+"/key_files/EnglishLS.train."+word[:-4]+".key","a")
        except:
            g = open(os.getcwd()+"/EnglishLS.train."+word[:-4]+".key","w")
        writetog = ""
        foundContextYet = "no"
        for line in f:
            if line.startswith("<context>"):
                foundContextYet = "yes"
                if len(writetog) != 0:
                    g.write(writetog+"\n")
                    writetog = ""
                               
            #<answer instance="activate.v.bnc.00044852" senseid="38201">
            if line.startswith("<answer instance="):
                m = re.search("\"(.+?)\"",line)
                n = m.group(1)
                if len(writetog) == 0:
                    p = re.search("\"(.+?\..+?)\.",line)#finds the word and pos like "activate.v"
                    q = p.group(1)
                    r = re.search("\".+?\".+?\"(.+?)\"",line)#this finds the answer
                    writetog += str(q)+" "+str(n)+" "+str(r.group(1))
                else:
                    p = re.search("\"(.+?\..+?)\.",line)#finds the word and pos like "activate.v"
                    q = p.group(1)
                    r = re.search("\".+?\".+?\"(.+?)\"",line)#this finds the answer
                    writetog += " " + str(r.group(1))
                



if __name__ == "__main__":
    main()
