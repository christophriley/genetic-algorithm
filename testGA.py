import geneticframework

mypop = geneticframework.Population()
mypop.reacquireAllFitness()
mypop.display()



nextgen = mypop.generateNextPopulation()
for x in range(10):
    nextgen.display()
    nextgen = nextgen.generateNextPopulation()

nextgen.display()

#poptwo = mypop.generateNextPopulation()
#poptwo.display()
#popthree = poptwo.generateNextPopulation()
#popthree.display()
