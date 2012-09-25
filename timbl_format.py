import sys, os, re, relevant_functions

#Allow for running on arbitrary files -Chris
#First argument is input, second argument is output
#If second argument is missing, use first argument and add ".mbl" extension
numargs = len(sys.argv)
if numargs < 2:
    print "Syntax: timbl_format.py <input file>"
    sys.exit(1)
infilename = sys.argv[1]
dirname = ""

#print "Infile: " + infilename
#print "Outfile: " + outfilename

#check if we're doing an individual file or a whole directory
filelist = []
if os.path.isdir(infilename):
    dirname = infilename
    for file in os.listdir(infilename):
        filelist.append(dirname + "/" + file)
else:
    filelist.append(infilename)

for infile in filelist:
    outfile = infile + ".mbl"
    relevant_functions.get_features(infile, outfile, [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])


'''def main():
    f = open(infilename)
    g = open(outfilename,"w")
    areWeInContext = "no" #if we are in the <context> portion of a sentence
    answers = [] # in case there are multiple possible answers
    timblLine = "" #what we eventually write to the training file
    for line in f:
        line = line[:-1]
        if line.startswith("<answer"):
            a =  re.search("\".+?\".+(\".+?\")",line)
            answer =a.group(1)[1:-1]
            answers.append(answer)
            
        if line.startswith("<context>"):
            if areWeInContext == "yes":
                areWeInContext = "no"
                answer = "0"
                other_answers = [] #make sure to handle the other answers in below if statement
            else:
                areWeInContext = "yes"

        if (areWeInContext == "yes") and (line != "<context>"): #line now is the context
            line = line.split() # split at whitespace to get the positions of each word
            newline = []
            for x, each in enumerate(line):
                each = each.rsplit("/",1)#-Dan:only 1 split from the right to only grab what we need
                if each[0].startswith("<head>"):
                    CT0 = each[0][6:]
                    CP0 = each[1][:-1]
                    head_position = x 
                    each[0] = each[0][6:] 
                    each[1] = each[1][:-1]
                newline.append(each)

            #now we have the head word and the head word's position.

            try:
                CT1 = newline[head_position+1][0]
            except:
                CT1 = "-"
            try:
                CTneg1 =newline[head_position-1][0]
            except:
                CTneg1 = "-"
            try:
                CT2 = newline[head_position+2][0]
            except:
                CT2 ="-"

            try:
                CTneg2 =newline[head_position-2][0]
            except:
                CTneg2="-"
            
            try:
                CT3 = newline[head_position+3][0]
            except:
                CT3 ="-"
      
            try:
                CTneg3 =newline[head_position-3][0]
            except:
                CTneg3 ="-"
      
            try:
                CP1 = newline[head_position+1][1]
            except:
                CP1="-"
            
      
            try:
                CPneg1 =newline[head_position-1][1]
            except:
                CPneg1="-"
      
            try:
                CP2 = newline[head_position+2][1]
            except:
                CP2="-"
      
            try:
                CPneg2 =newline[head_position-2][1]
            except:
                CPneg2="-"
      
            try:
                CP3 = newline[head_position+3][1]
            except:
                CP3="-"
      
            try:
                CPneg3 =newline[head_position-3][1]
            except:
                CPneg3="-"
      
            ###### below are the noun, verb, and preposition BEFORE the target word
            haveNB = "no"
            NB = "-"
            haveVB = "no"
            VB = "-"
            havePB = "no"
            PB = "-"
            x = head_position-1
            while (x >=0):
                if (newline[x][1].startswith("NN")) and (haveNB == "no"): #any kind of noun
                    NB = newline[x][0]
                    haveNB = "yes"
                if (newline[x][1].startswith("VB")) and (haveVB == "no"): #any kind of verb
                    VB = newline[x][0]
                    haveVB = "yes"
                if (newline[x][1] == "IN") and (havePB == "no"): #any kind of preposition
                    PB = newline[x][0]
                    havePB = "yes"
                x-=1
            
            ###### below are the noun, verb, and preposition AFTER the target word
            haveNA = "no"
            NA = "derp"
            haveVA = "no"
            VA = "derp"
            havePA = "no"
            PA = "derp"
            x = head_position+1
            while (x <=len(newline)-1):
                #print newline[x]
                if (newline[x][1].startswith("NN")) and (haveNA == "no"): #any kind of noun
                    NA = newline[x][0]
                    haveNA = "yes"
                if (newline[x][1].startswith("VB")) and (haveVA == "no"): #any kind of verb
                    VA = newline[x][0]
                    haveVA = "yes"
                if (newline[x][1] == "IN") and (havePA == "no"): #any kind of preposition
                    PA = newline[x][0]
                    havePA = "yes"
                x+=1
            if NA == "derp":
                NA="-"
            if VA == "derp":
                VA="-"
            if PA == "derp":
                PA="-"

            
            for answer in answers:
                g.write(CTneg3+","+ CTneg2+","+CTneg1+","+CT0+","+CT1+","+CT2+","+CT3+","+CPneg3+","+CPneg2+","+CPneg1+","+CP0+","+CP1+","+CP2+","+CP3+","+NA+","+NB+","+VA+","+VB+","+PA+","+PB+","+answer+"\n")
            answers = []



            
      



    f.close()

if __name__ == "__main__":
    main()
   ''' 

