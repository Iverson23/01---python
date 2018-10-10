import sys
import parseHelper
import loadHelper

textFilename = sys.argv[1]
dbFilename = sys.argv[2]

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


loadHelper.createDb(dbFilename)

for Print in load(textFilename):
	compId = loadHelper.addCompositionToDb(Print.composition())
	editId = loadHelper.addEditionToDb(Print.edition, compId)
	
	for person in Print.composition().authors:
		authId = loadHelper.addPersonToDb(person)
		loadHelper.fillScoreAuthor(authId, compId)
		
	for person in Print.edition.authors:
		authId = loadHelper.addPersonToDb(person)
		loadHelper.fillEditionAuthor(authId, editId)
	
	if(compId > 0):
		counter = 1
		for voice in Print.composition().voices:
			if(voice != None):
				loadHelper.addVoiceToDb(voice, compId, counter)
			counter = counter + 1
	
	loadHelper.addPrintToDb(Print, editId)

loadHelper.commitDb()