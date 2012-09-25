import re, os, sys, random, geneticframework
def timbl_testing_time(generation,settings,Kn1,Kn2,ind):#settings is a list of 100 lists, each of which is the settings for that individual
    directory = "Generations/"+str(generation)
    for word in ["note"]:#os.listdir(directory): #each word we're testing has its own folder in each generation
        training_file =directory+"/"+str(word)+"/TIMBL_train_"+str(Kn1)+"_without_"+str(Kn2)+".txt"
        testing_file = directory+"/"+str(word)+"/TIMBL_test_"+str(Kn1)+"_"+str(Kn2)+".txt"
        ignores = ""
        x = 0
        while x < 20: #20, aka 21st feature, is answer and always is on
            if settings[x] == 0:
                ignores+=str(x+1)+","#timbl counts form feature 1
            x+=1
        if ignores != "":
            ignores = ignores[:-1]#remove final comma
    print "ignores:",ignores
    print "settings:",settings
    os.system("./timbl -f /Users/danielbishop/School/L715_2/Final/"+str(training_file)+" -t /Users/danielbishop/School/L715_2/Final/"+str(testing_file)+" -d "+str(settings[-3])+" -k "+str(settings[-2])+" -w "+str(settings[-1])+" -mO:I"+str(ignores))
    os.system("mv  "+testing_file+".* .")#ought move it to this directory

    ###STARTING HERE IS THE SCORER STUFF
    
    #from here, grab the answer that timbl provided and make settings[-4] into that answer. After all of these are done the pop is ready for the scorer
    os.system("ls *.out > fname.txt")
    for line in open("fname.txt","r"):
        f_name = line[:-1] #to cut off the newline that otherwise is at the end
    f = open(f_name,"r")
    g = open(os.getcwd()+"/scorer.answers","w")#rewrite, only keep one at a time
    for line in f:#last thing is the instance id, second to last is the answer timbl gave
        #print line
        split_line = line.split(",")
        #print split_line
        instance_id_num = split_line[-3]
        instance_id = split_line[-3].split(".")
        instance_id_word =  instance_id[0]+"."+instance_id[1]

        instance_id_num = split_line[-3]
  
        answer = split_line[-1][:-1]#last thing timbl returns, is the answer given by timbl (and added into the individuals as the settings are altered and refolded in to the orgininal individual.getparams or whatever as timbl runs)
        g.write(str(instance_id_word)+" "+str(instance_id_num)+" "+str(answer)+"\n")#each answer line is the word, the id, and the answer all separated by spaces
    g.close()
    os.system("./scorer "+os.getcwd()+"/scorer.answers "+os.getcwd()+"/key_files/EnglishLS.train."+word+".key "+os.getcwd()+"/EnglishLS.sensemap > scoreroutput.txt")#Note: I don't yet know what the output of this looks like. So not sure what to do with it. Don't know if it makes a file or... or what.

    f.close()
    os.remove("fname.txt")
    os.remove(f_name)#remove the .out file
    raw_input()
    p = open("scoreroutput.txt","r")
    for line in p:
        if line.startswith(" precision"):
            pass
            #if better than best in output/word then alter that file to reflect the best set of outcomes and send along the settings (which is the features and timbl parameters)
        elif line.startswith(" recall"):
            pass
        elif line.startswith(" attempted"):
            pass
    p.close()

    #os.system("mv Generations/"+str(generation)+"/"+str(word)+"/*.out output/")



def timbl_files_maker(population, generation, Kn1, Kn2):#ONLY RUN ONCE OR MANUALLY REMOVE FOLDERS IN Generations
    print "Now making training and test files for TiMBL, for generation"+str(generation)
    #directory = "data_WSD/k-fold_CV/"+str(Kn1)
    directory = "data_WSD/k-fold_CV/dummy_10"#only has activate
    if not os.path.exists("Generations/"+str(generation)):#it shouldn't
        os.makedirs("Generations/"+str(generation))
    else:
        print "WEIRD: Generations/"+str(generation)+" folder already exists"
    for word in os.listdir(directory): #word is the word being tested as well as the name of the folder with the word's files
        #only one word for now
        if word != ".DS_Store": #rassa-frassin mumble mumble dern .DS_Store
            os.makedirs("Generations/"+str(generation)+"/"+word)#make a folder for each word's files since there's going to be a zillion files
            directory2 = directory+"/"+word
            x = 0
            #prunt "LENGTH OF POPULATION: "+str(len(population[0]))
            while x < len(population):#population is of Pop size, population[1] is the timbl settings
                fTrain =open("Generations/"+str(generation)+"/"+word+"/"+word+"_train_"+str(x+1)+".txt","w")#our training file for this word
                #fTest = open("Generations/"+str(generation)+"/"+word+"/"+word+"_test_"+str(x+1)+".txt","w")
                for files in os.listdir(directory2):#the individual files in the k-fold CV's folder for the specified word
                    if (files != ".DS_Store") and (files != str(Kn2)+".txt"):                        
                        fTrain.write(open(directory2+"/"+str(files)).read())
                    elif (files != ".DS_Store") and (files == str(Kn2)+".txt"):
                        #fTest.write(open(directory2+"/"+str(files)).read())
                        get_features(directory2+"/"+str(files), "Generations/"+str(generation)+"/"+word+"/"+word+"_TIMBL_test_"+str(x+1)+".txt", population[x][0])
                    #else: #ought not happen unless file is .DS_Store I think
                        #print files, "<- HAD BETTER BE .DS_STORE" #checked - it is only here, don't worry
                f1 ="Generations/"+str(generation)+"/"+word+"/"+word+"_train_"+str(x+1)+".txt"
                f2 = "Generations/"+str(generation)+"/"+word+"/"+word+"_TIMBL_train_"+str(x+1)+".txt"
                get_features(f1, f2, population[x][0])
                removepath = "Generations/"+str(generation)+"/"+word+"/"+word+"_train_"+str(x+1)+".txt"
                os.remove(removepath)
                x+=1


def get_features(filein,fileout,features_to_add):#the file that comes in and the file we write to, and a list of which features are 'turned on' (#21, the answer, always is turned on)
    f = open(filein)
    g = open(fileout,"w")
    areWeInContext = "no" #if we are in the <context> portion of a sentence
    answers = [] # in case there are multiple possible answers
    timblLine = "" #what we eventually write to the training file
    instance_id = ""#add to the end of the training file
    for line in f:
        line = line[:-1]
        if line.startswith("<instance id"):
            a = re.search("\"(.+?)\"",line)
            instance_id = a.group(1)#this is the instance id, e.g., activate.v.bnc.00024693
        
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
                re
                each = each.rsplit("/",1)#I need to separate at the *last* / to keep the extra slashes in some bullshit
                if each[0].startswith("<head>"):
                    CT0 = each[0][6:]
                    CT0 = CT0.split("/")[0]
                    CP0 = each[1][:-1]
                    head_position = x 
                    each[0] = each[0][6:] 
                    each[1] = each[1][:-1]
                newline.append(each)
            #now we have the head word and the head word's position.
            try:
                CT1 = newline[head_position+1][0]
                #if len(CT1) == 0:
                    #prunt newline
                    
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
            v = head_position-1
            try:
                while (v >=0):
                    #prunt "V",str(v)
                    #prunt "NEWLINE[v][1]:",str(newline[v][1])
                    if (newline[v][1].startswith("NN")) and (haveNB == "no"): #any kind of noun
                        NB = newline[v][0]
                        haveNB = "yes"
                    if (newline[v][1].startswith("VB")) and (haveVB == "no"): #any kind of verb
                        VB = newline[v][0]
                        haveVB = "yes"
                    if (newline[v][1] == "IN") and (havePB == "no"): #any kind of preposition
                        PB = newline[v][0]
                        havePB = "yes"
                    v-=1
            except:
                #prunt "MADNESS @ "+str(filein)+": "+str(line)
                pass
            ###### below are the noun, verb, and preposition AFTER the target word
            haveNA = "no"
            NA = "-"
            haveVA = "no"
            VA = "-"
            havePA = "no"
            PA = "-"
            v = head_position+1
            try:
                while (v <=len(newline)-1):
                    #prunt newline[x]
                    if (newline[v][1].startswith("NN")) and (haveNA == "no"): #any kind of noun
                        NA = newline[v][0]
                        haveNA = "yes"
                    if (newline[v][1].startswith("VB")) and (haveVA == "no"): #any kind of verb
                        VA = newline[v][0]
                        haveVA = "yes"
                    if (newline[v][1] == "IN") and (havePA == "no"): #any kind of preposition
                        PA = newline[v][0]
                        havePA = "yes"
                    v+=1
            except:
                #prunt "MADNESS @ "+str(filein)+": "+str(line)
                pass
            features = [CTneg3,CTneg2,CTneg1,CT0,CT1,CT2,CT3,CPneg3,CPneg2,CPneg1,CP0,CP1,CP2,CP3,NA,NB,VA,VB,PA,PB,instance_id,answer]#all of the features
            popped = 0
            for index, each in enumerate(features_to_add):
                if each == 0:
                    #prunt index
                    features.pop(index-popped)#to avoid out-of-bounds due to querying an index that no longer exists due to a shorter list
                    popped +=1
            features = re.sub(" ","",str(features))#make the features list into a string without spaces between the commas separating them
            features = features[1:-1]
            features = re.sub("'","",str(features))
            for index, answer in enumerate(answers):
                g.write(features+"\n")
            answers = []

    f.close()
    g.close()

def gen1(MuP, CrOP,Pop,G,Gn,A,F,K,Kn1,Kn2,I,SOTW):
    #ignore: MuP, CrOP, G, Gn, A, F, I, SOTW
    #use: Pop, K?, Kn1, Kn2
    directory = "data_WSD/k-fold_CV/"+str(Kn1)
    initial_population = [] #eventually of pop size Pop
    #features = [CTneg3,CTneg2,CTneg1,CT0,CT1,CT2,CT3,CPneg3,CPneg2,CPneg1,CP0,CP1,CP2,CP3,NA,NB,VA,VB,PA,PB,answer]
    #timbl will be running with default values for now
    print "WARNING! ACHTUNG! TiMBL is running under DEFAULT SETTINGS ONLY FOR NOW."
    timbl_settings_d = ["Z","ID","IL","ED:a","ED:a:b"]#not sure what numbers are valid for a and b
    timbl_settings_w = [0,1,2,3,4]#valid settings for -w
    #timbl_settings_a = [0,1,2,3,4]#valid settings for -a
    timbl_settings_k = [1,3,5,7,9,11,15,25,35,45]#(some of the) valid settings for -k
    #valid_param_values = {'f':['i','w','m'], 'w':[1,2,3,4,5], 'd':[1,2,3,4], 'k':[1,3,5,7,9,11,15,25,35,45]}#valid settings for TiMBL's various settings

    #assemble initial feature sets for the first generation and add them into the initial_population. First generation will have
    #the same feature sets across all words. Successive generations
    x = 0
    y = 0
    #specify as option? Ugh I don't wanna. Just do 40% uni-featured, 40% max-featured, 20% random
    while x < Pop*.4: #minimal examples, with one feature turned on only
        individual = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"Z",1,1]#the last 2 zeroes before the last 3 things (the timbl settings) are the instance id (already there) and the timbl answer (to be filled in later)
        if y == len(individual)-3:
            y = 0
        individual[y] = 1
        initial_population.append(individual)
        x+=1
        y+=1
    y = 0
    while x < Pop*.8:#maximal examples, with all but one features on (likely will beat the crap out of the minimal examples)
        individual = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,"Z",1,1]#-a 0 -d Z -k 1 -w 1 as timbl settings, all defaults#REMOVED A
        if y == len(individual)-3:#avoid going out of bounds and instead loop back to beginning
            #as above, the last 2 zeroes before the last 3 things (the timbl settings) are the instance id (already there) and the timbl answer (to be filled in later)
            y = 0
        individual[y] = 0
        initial_population.append(individual)
        y+=1
        x +=1

    while x < Pop:#the remaining 20% will be random
        individual = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,"Z",1,1]#the last 2 zeroes before the last 3 things (the timbl settings) are the instance id (already there) and the timbl answer (to be filled in later)
        y = 0
        while y<=19:
            individual[y] = random.randint(0,1)
            y+=1
        initial_population.append(individual)
        x += 1

    #prunt "INITIAL POPULATION'S FEATURES AND SETTINGS"

    #At this point we have knowledge of which features we want turned on for the individuals.

    #INCORPORATE WITH CHRIS' SHIT HERE
    PopofIndividuals = []
    for x,each in enumerate(initial_population):
        new=geneticframework.Individual("1:"+str(x),each)
        PopofIndividuals.append(new)
    mypop= geneticframework.Population(name="GENERATION1", newindividuals=PopofIndividuals)
    #mypop.display()
    settings = []
    for each in initial_population:
        settings.append(each[1])#this takes the settings part of each
    tests = 0
    #NEED FOR LOOP HERE: For each word in the Generations/1/ folder. NOT IN THE timbl_testing_time function!!!
    for ind, Individual in enumerate(PopofIndividuals):
         timbl_testing_time(1,Individual.getparams(),Kn1,Kn2,ind) #this needs to have returned the parameters for the individual to rewrite it
         
         tests +=1
         #print "NUMBER OF TIMBL TESTS WAS:",str(tests)
    #After all the TiBML tests are run, then send the whole population to the scorer
    scorer(PopofIndividuals)

def initialize(args):
    #args is a list of space-separated arguments from command line
    if "-MuP" in args:#mutation probability
        MuP = float(args[args.index("-MuP")+1])
    else:
        MuP = .05
        print "Mutation probability of genes not specified (-MuP): default setting is "+str(MuP)

    if "-CrOP" in args:#CrossOver probability
        CrOP = float(args[args.index("-CrOP")+1])
    else:
        CrOP = .05
        print "Crossover probability of genes not specified (-CrOP): default setting is "+str(CrOP)

    if "-Pop" in args:#population size per generation
        Pop = int(args[args.index("-Pop")+1])
    else:
        Pop = 100
        print "Population size per generation not specified (-Pop): default setting is "+str(Pop)

    if "-G" in args:#how many generations of no improvement over best F-score before quitting
        G = int(args[args.index("-G")+1])
        Gn = "NO"
    elif "-Gn" in args:#How many generations, period, before halting
        G = "NO"
        Gn = int(args[args.index("-Gn")+1])
    else:
        G = "NO"
        Gn = 100
        print "Number of generations not specified (-Gn) nor Generations without improvement (-G): "
        print "default setting is until "+str(Gn)+" generations total."

    if "-A" in args:#percentage of new generation formed from asexual reproduction
        A = int(args[args.index("-A")+1])
    else:
        A = 20
        print "Percentage of new population each round formed via asexual reproduction not specified (-A): default setting is "+str(A)+"%"

    if "-F" in args:#how many individuals per generation deemed fit
        F = int(args[args.index("-G")+1])
    else:
        F = 20
        print "Number of individuals per generation deemed fit for reproduction not specified (-F): default setting is "+str(F)
    if int(F)>=int(Pop):
        print "ALERT: Number of individuals per generation deemed fit is equal to or greater than all individuals per generation. Using default values of population 100 and fit number of 20."

    if "-K" in args:#k-fold cross validation done per generation
        K = int(args[args.index("-K")+1])
        Kn1="NO"
        Kn2="NO"
    elif "-Kn" in args:#use K from k-fold but only do one test, from section n of the k-fold
        K= "NO"
        Kn1 = int(args[args.index("-Kn")+1])#which k-fold cross validation to use (2-fold, 7-fold, etc)
        Kn2 = int(args[args.index("-Kn")+2])#which of the sections of the above k-fold you'll use as test data (use section X as dev set)
    else:
        K = "NO"
        Kn1 = 10#use ten-fold cross validation files
        Kn2 = 10#train on 1-9 and test (dev set) on 10
        print "K-fold cross validation not specified (-K or -Kn x y): default is -Kn "+str(Kn1),str(Kn2)
        print "Thus, only one test per individual per generation, from "+str(Kn1)+"-fold CV, using section "+str(Kn2)

    if "-I" in args:#import folder of a generation's individuals to continue testing with same/different parameters
        I = int(args[args.index("-I")+1])
    else:
        I = "NO"
        print "Import folder of a previous generation not specified (-I): default setting is none, to treat this as generation 1"

    if "-SOTW" in args:#survival of the worst - this is the number of those in F that are culled randomly from the *worst* performers for purposes of exploring wider swathes of the search space.
        SOTW = int(args[args.index("-SOTW")+1])
    else:
        SOTW = "NO"
        print "Use of n worst performers in reproduction not specified (-SOTW): default setting is not to do so."

    options = [MuP, CrOP,Pop,G,Gn,A,F,K,Kn1,Kn2,I,SOTW]
    return options


        

def main():
    options = initialize(sys.argv)
    MuP = options[0]
    CrOP =options[1]
    Pop =options[2]
    G =options[3]
    Gn =options[4]
    A =options[5]
    F =options[6]
    K =options[7]
    Kn1 = options[8]
    Kn2 =options[9]
    I =options[10]
    SOTW = options[11]
    print "OPTIONS: "+str(options)
    #If First Generation, then a special round is necessary to form the individuals. All other generations will use a group of size Pop already there to run with.
    #Special First Gen case - only form the initial Pop population. Then return here for testing, scoring, and reproduction.
    #All other cases: Reproduction will form the Pop-size population and thus can go straight to testing, scoring, and reproduction.
    
    if I == "NO":
        gen1(MuP, CrOP,Pop,G,Gn,A,F,K,Kn1,Kn2,I,SOTW)
    else:
        circleoflife(MuP, CrOP,Pop,G,Gn,A,F,K,Kn1,Kn2,I,SOTW) #entering the main loop with an existing folder. If I was NO, gen1() will form an equivalent folder

if __name__ == "__main__":
    main()
