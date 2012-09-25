import sys, os, re

numargs = len(sys.argv)
if numargs < 2:
    print "Syntax: word_separator.py <input file> <output folder>"
    sys.exit(1)

infilename = sys.argv[1]
outfolder = sys.argv[2]

def main():
    f = open(infilename)
    add_to_a_file = ""
    counter = 0
    nextmilestone = 10
    print
    for line in f:
        counter += 1
        if line.startswith("<instance id=\""):
            word = re.search("\"(.+?)\.",line).group(1)
        if len(line)>1:
            add_to_a_file+=line
        else:
            splitbydots = infilename.split(".")
            extension = splitbydots[len(splitbydots) - 1]
            try:
                g = open(outfolder + word + "." + extension , 'a')
            except:
                g = open(outfolder + word + "." + extension, 'w')
            #print add_to_a_file
            g.write(add_to_a_file+"\n")
            g.close()
            add_to_a_file = ""
            
        if counter == nextmilestone:
            nextmilestone *= 10
            print counter
            
    print counter #final line count
            


if __name__ == "__main__":
    main()
