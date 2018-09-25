import sys
import re

filePath = sys.argv[1]
statOf = sys.argv[2]

file = open(filePath, 'r', encoding='utf-8')
comp = re.compile( r"Composer: (.+)" )
cent = re.compile(r"Composition Year: (.+)")

compDict = {}
centDict = {}

for line in file:
	compMatch = comp.match(line)
	centMatch = cent.match(line)
	if compMatch:
		for composer in compMatch.group(1).split(';'):	
			composer = re.sub(r'\(.*\d.*\)', '', composer)
			composer = composer.strip()
			if composer in compDict:
				compDict[composer] = compDict[composer] + 1
			else:
				compDict[composer] = 1
	elif centMatch:
		number = re.findall(r'\d+', centMatch.group(1))
		if not number:
			continue
		number = int(number[-1])
		if len((str(number))) == 2:				
			if number in centDict:
				centDict[number] = centDict[number] + 1
			else:
				centDict[number] = 1
		else:
			year = number % 100 # we need to check if the year is not round like 1800 for example, this still belongs to 18th century
			if(year > 0):
				number = int(str(number)[:2]) + 1
			else:
				number = int(str(number)[:2])
				
			if number in centDict:
				centDict[number] = centDict[number] + 1
			else:
				centDict[number] = 1
if statOf == 'composer':
	for key in compDict:
		print(key + ": " + str(compDict[key]))
elif statOf == 'century':
	for key in centDict:
		print(str(key) + "th century: " + str(centDict[key]))
		


	
	