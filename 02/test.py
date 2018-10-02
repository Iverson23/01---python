import sys
import parseHelper

filename = sys.argv[1]

def load(filename):
	prints = []
	file = open(filename, 'r', encoding='utf-8')
	
	printLinesArray = []
	for line in file:
		if line in ['\n', '\r\n']:
			if(len(printLinesArray) > 0):
				prints.append(parseHelper.processPrintLines(printLinesArray))
				printLinesArray = []
		else:
			printLinesArray.append(line)
	prints.append(parseHelper.processPrintLines(printLinesArray))
	return prints



f1=open('./testfile.txt', 'w+', encoding='utf-8')
for p in load(filename):
	p.format()		
	f1.write(str(p))
	f1.write("\n")




