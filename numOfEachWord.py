import sys, os, re
directory = "data_WSD/word files/"
for each in os.listdir(directory):
    f = open(directory+each)
    x = 0
    print each[:-4],
    for line in f:
        if line.startswith("<instance id=\""):
            x+=1
    print x
