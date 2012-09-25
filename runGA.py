import geneticframework, sys

targetwordthisrun = "note"

if len(sys.argv) < 2:
    print "Syntax: runGA.py <number of generations> [target word]"
    sys.exit(0)

if len(sys.argv) > 2:
    targetwordthisrun = sys.argv[2]

numgens = int(sys.argv[1])

mypop = geneticframework.Population(targetword=targetwordthisrun)
mypop.reacquireAllFitness()
mypop.display()


nextgen = mypop.generateNextPopulation(targetword=targetwordthisrun)
for x in range(numgens):
    nextgen.display()
    nextgen = nextgen.generateNextPopulation(targetword=targetwordthisrun)

nextgen.display()

#poptwo = mypop.generateNextPopulation()
#poptwo.display()
#popthree = poptwo.generateNextPopulation()
#popthree.display()
