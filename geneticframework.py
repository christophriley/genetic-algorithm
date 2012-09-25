import random, os

showdebug = True

def debug(msg):
    if showdebug:
       print msg

#TiMBL information
defaulttargetword = "note"
datadir = "data/by_word/"

#Genetic Algorithm Parameters
#take <mu> best individuals from <lam>bda total individuals in the population 
mu = 20
lam = 40

#chance to mutate, crossover
mutchance = .1
crosschance = .1
uniformcrossrate = .5
persistpercent = .50
mutpercent = .35

#number of features
numfeats = 20

#generate the list of parameters:
#f = feature (ignore, include)
#m = distance metric
#w = weighting parameter (1, 2, 3, 4, 5)
#d = neighbor weighting parameter (1, 2, 3, 4)
#k = number of neighbors (1,3,5,7,9,11,15,25,35,45)
paramlist = []
for x in range(numfeats):
    paramlist.append("f")
paramlist.append("m")
paramlist.append("w")
paramlist.append("d")
paramlist.append("k")

#dictionary for looking up possible parameter values:
paramvalues = {'f':[0,1], 'm':['O', 'M', 'J'], 'w':[0,1,2,3,4], 'd':['Z','ID','IL'], 'k':[1,3,5,7,9,11,15,25,35,45]}

def retrieve_fitness(self, individual):
    return int(float(individual.getfitness()) * 100)

class Population:
    Name = "Population"
    def __init__(self, number = 1, newindividuals = "none", targetword = defaulttargetword):
        self.mu = mu
        self.lam = lam
        self.mutchance = mutchance
        self.crosschance = crosschance
        self.number = number
        self.targetword = targetword

        if newindividuals is "none":
            self.individuals = []
            for x in range(self.mu):
                newname = "G" + str(number) + "-i"
                newname += str(x)
                newindividual = Individual(newname, targetword = self.targetword)
                self.individuals.append(newindividual)
        else:
            self.individuals = newindividuals

        self.numIndividuals = len(self.individuals)

    def reacquireAllFitness(self):
        for individual in self.individuals:
            individual.acquirefitness()

    def generateNextPopulation(self, newpopulationnumber = -1, targetword=defaulttargetword):
        newindividuals = []
        if newpopulationnumber is -1:
            newpopulationnumber = self.number + 1

        mutatepoint = int(round(self.lam * persistpercent))
        crossoverpoint = int(round(self.lam * (persistpercent + mutpercent)))

        #these individuals persist
        for x in range(0, mutatepoint):
            newchild = self.individuals[x].copy()
#            newchild = self.individuals[random.randrange(0, mu)].copy()
            newname = "G" + str(newpopulationnumber) + "-i" + str(x)
            newchild.setname(newname)
            newindividuals.append(newchild)

        #these individuals mutate
        for x in range(mutatepoint, crossoverpoint):
            mutator = self.individuals[random.randrange(0, mu)].copy()
            newname = "G" + str(newpopulationnumber) + "-i" + str(x)
            mutator.setname(newname)
            mutator.mutate(self.mutchance)
            mutator.setfitness(-1)
            newindividuals.append(mutator)

        #these individuals come from cross over
        for x in range(crossoverpoint, self.lam):
            parentone = self.individuals[random.randrange(0, mu)].copy()
            parenttwo = self.individuals[random.randrange(0, mu)].copy()
            childparams = []

            crosstypes = ["single", "double", "uniform"]
            crosstype = crosstypes[random.randrange(0, len(crosstypes))]
                
            debug("*****\n" + crosstype + " crossover:" + parentone.getname() + " with " + parenttwo.getname())
            debug(parentone.display())
            debug(parenttwo.display())

            childparams = parentone.crossover(parenttwo, crosstype=crosstype)
            debug(childparams)

            newchildname = "G" + str(newpopulationnumber) + "-i" + str(x)
            newchild = Individual(newchildname, childparams, targetword = self.targetword)
            newindividuals.append(newchild)

        #run the fitness function for each individual that does not already have a fitness score
        for individual in newindividuals:
            if individual.getfitness() < 0:
                individual.acquirefitness()

        #cull the population back down to size mu
        fitlist = []

        for x in range(0, len(newindividuals)):
            fitlist.append([newindividuals[x].getfitness(), x])
        fitlist = sorted(fitlist, key=lambda individual: individual[0], reverse=True)

        culledindividuals = []
        for x in range(0, mu):
            individualnumber = fitlist[x][1]
            culledindividuals.append(newindividuals[individualnumber])

        newpop = Population(newindividuals=culledindividuals, number=newpopulationnumber, targetword = targetword)

        return newpop
#        return newindividuals
        
    def getIndividuals(self):
        return self.individuals

    def display(self):
        displaytext = ""
        print "Population \"" + str(self.number) + "\" contains " + str(self.numIndividuals) + " individuals."
        for x in range(len(self.individuals)):
            displaytext += self.individuals[x].display() + "\n"
        print displaytext
           

class Individual:
    Name = "Individual"
    def __init__(self, name, parameters="none", fitness=-1, targetword = defaulttargetword):
        self.name = name
        self.fitness = fitness
        self.targetword = targetword
        
        if parameters is "none":
            self.parameters = []

            for param in paramlist:
                numvalues = len(paramvalues[param])
                thisvalue = random.randrange(0,numvalues)
                self.parameters.append(paramvalues[param][thisvalue])
        else:
            self.parameters = parameters

    def getname(self):
        return self.name

    def setname(self, name):
        self.name = name

    def getparam(self, index):
        return self.parameters[index]

    def getparams(self):
        return self.parameters

    def getfitness(self):
        return self.fitness

    def setfitness(self, fitness):
        self.fitness = fitness

    def acquirefitness(self):
        trainfile = datadir + self.targetword + ".train.mbl.train"
        testfile = datadir + self.targetword + ".train.mbl.test"

        #metric
        mindex = len(self.parameters) - 4
        mvalue = self.parameters[mindex]

        #uncomment this to force overlap only
        #mvalue = "O"

        params = "-m" + str(mvalue) + ":I21,"
        ignorelist = []
        for x in range(0,20):
            if int(self.parameters[x]) == 0:
                ignorelist.append(x + 1)
        debug(ignorelist)
        ignorestring = ",".join(map(str, ignorelist))
        params += ignorestring

        #k value
        kindex = len(self.parameters) - 1
        kvalue = self.parameters[kindex]
        params += " -k" + str(kvalue)

        
        #feature weighting
        windex = len(self.parameters) - 3
        wvalue = self.parameters[windex]
        params += " -w" + str(wvalue)

        #voting weights
        dindex = len(self.parameters) - 2
        dvalue = self.parameters[dindex]
        params += " -d" + str(dvalue)

        timblstring = "timbl -f " + trainfile + " -t " + testfile + " " + params + " &> timbl.output"
        debug(timblstring)
        os.system(timblstring)


        outfile = ""
        for file in os.listdir(datadir):
            components = file.split(".")
            if components[len(components) - 1] == "out":
                outfile = file
        outfile = datadir + outfile

        accuracy = -1
        output = open("timbl.output", "r")
        for line in output:
            tokens = line.split(" ")
            if tokens[0] == "overall":
                accuracy = tokens[9]

        output.close()
        
        os.system("rm -f " + outfile)
        self.fitness = accuracy
        debug(self.display())
        
    def copy(self):
        newindividual = Individual(self.name, self.parameters, fitness=self.fitness, targetword = self.targetword)
        return newindividual
            
    def mutate(self, mutchance):
        for index in range(0, len(paramlist)):
            mutateThisParameter = random.random()
            if mutateThisParameter <= mutchance:
                paramtype = paramlist[index]
                possiblevalues = paramvalues[paramtype]
                newvalue = possiblevalues[random.randrange(0, len(possiblevalues))]
                self.parameters[index] = str(newvalue)
                
    def crossover(self, parenttwo, crosstype="single"):
        childparams = []
        pointone = random.randrange(0, len(self.parameters) - 1)
        pointtwo = len(self.parameters)
        if crosstype is "double" and pointone < len(self.parameters):
            pointtwo = random.randrange(pointone + 1,len(self.parameters))
        print pointone, pointtwo
        if crosstype is "single" or crosstype is "double":
            for x in range(0, len(self.parameters)):
                if x < pointone or x > pointtwo:
                    childparams.append(self.parameters[x])
                else:
                    childparams.append(parenttwo.getparam(x))
        elif crosstype is "uniform":
            for x in range(0, len(self.parameters)):
                if random.random() < uniformcrossrate:
                    childparams.append(self.parameters[x])
                else:
                    childparams.append(str(parenttwo.getparam(x)))
                    
        return childparams
                
    def display(self):
        displaystring = "(" + self.name + ")"
        displaystring += "-["
        paramlist = []
        for param in self.parameters:
            paramlist.append(str(param))
        displaystring += " ".join(paramlist)
#        displaystring += " ".join(str(param) for param in self.parameters)
#        for param in self.parameters:
#            displaystring += " " + str(param)
        displaystring += "]"
        displaystring += "{" + str(self.fitness) + "}"
        return displaystring


