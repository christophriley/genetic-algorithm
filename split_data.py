import sys

numargs = len(sys.argv)
if numargs < 2:
    print "Syntax: split_data.py <input file> <test percentage>"
    sys.exit(1)

infilename = sys.argv[1]
testpercent = sys.argv[2]

infile = open(infilename, 'r')
lines = []
for line in infile:
    lines.append(line)

numlines = len(lines)
splitline = int(numlines * (float(testpercent) / 100))

testlines = lines[:splitline]
trainlines = lines[splitline:]

testfilename = infilename + ".test"
trainfilename = infilename + ".train"

testfile = open(testfilename, 'w')
trainfile = open(trainfilename, 'w')

for line in testlines:
    testfile.write(line)

for line in trainlines:
    trainfile.write(line)


trainfile.close()
testfile.close()
infile.close()
