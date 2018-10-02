import re
import scorelib

def processPrintLines(printLinesArray):
	printNumber = None
	persons = []
	title = None
	genre = None
	printKey = None
	compositionYear = None
	editionTitle = None
	voices = []
	partiture = False
	incipit = None
	editors = []
	
	for line in printLinesArray:
		splitArray = line.split(":")
		if(len(splitArray) < 2):
			continue
		
		key = splitArray[0].strip()
		value = splitArray[1].strip()
		
		vc = re.compile( r"Voice.*")
		voiceMatch = vc.match(key)
		if(voiceMatch):
			voices.append(processVoiceLine(value))
		
		if(value == ""):
			continue
		if(key == "Print Number"):
			printNumber = int(value)
		if(key == "Composer"):
			persons = processComposerLine(value)
		if(key == "Title"):
			title = value
		if(key == "Genre"):
			genre = value
		if(key == "Key"):
			printKey = value
		if(key == "Composition Year"):
			compositionYear = processCompositionYear(value)
		if(key == "Edition"):
			editionTitle = value
		if(key == "Editor"):
			editors.append(value)
		if(key == "Partiture"):
			partiture = processPartiture(value)
		if(key == "Incipit"):
			incipit = value
		
	composition = scorelib.Composition(title, incipit, printKey, genre, compositionYear, voices, persons)
	edition = scorelib.Edition( composition, editors, editionTitle)
	printInstance = scorelib.Print(edition, printNumber, partiture)
	
	return printInstance

def processVoiceLine(voiceLine):
	rc = re.compile( r"(.+--.+?)[,;] (.*)")
	rangeMatch = rc.match(voiceLine)
	
	range = None
	name = None
	
	if(rangeMatch):
		range = rangeMatch.group(1)
		name = rangeMatch.group(2)
	elif(voiceLine != ""):
		name = voiceLine
	
	if(range == None and name == None):
		return None
	return scorelib.Voice(name, range)
	
def processComposerLine(composerLine):
	persons = []
	for composer in composerLine.split(';'):
		composerName = re.sub(r'\(.*\d.*\)', '', composer).strip()
		born = None
		died = None
		bc = re.compile( r".+ \((.+)\)")
		bracketsMatch = bc.match(composer)
		if bracketsMatch:
			bracketsContent = bracketsMatch.group(1)
			slashc = re.compile( r"(\d{4})-(\d{4})")
			slashMatch = slashc.match(bracketsContent)
			if(slashMatch):
				born = int(slashMatch.group(1))
				died = int(slashMatch.group(2))
				
			doubleShlashc = re.compile( r"(\d{4})--(\d{4})")
			doubleSlashMatch = doubleShlashc.match(bracketsContent)
			if(doubleSlashMatch):
				born = int(doubleSlashMatch.group(1))
				died = int(doubleSlashMatch.group(2))
			
			birthc = re.compile( r"(\d{4})--")
			birthMatch = birthc.match(bracketsContent)
			if(birthMatch):
				born = int(birthMatch.group(1))
			
			deadc = re.compile( r"\+(\d{4})")
			deadMatch = deadc.match(bracketsContent)
			if(deadMatch):
				died = int(deadMatch.group(1))
				
		persons.append(scorelib.Person(composerName, born, died))
	return persons

def processCompositionYear(compYearLine):
	number = re.findall(r'\d{4}', compYearLine)
	if number:
		return int(number[-1])
	return None

def processPartiture(part):
	yesc = re.compile( r".*yes.*")
	yesMatch = yesc.match(part)
	if(yesMatch):
		return True
	return False

