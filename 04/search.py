import sys
import export
import json
import re

composerNameSubs = sys.argv[1]

def serialize(obj):
    return obj.__dict__
	
class Comp:
	def __init__( self, name, prints ):
		self.name = name
		self.prints = prints

		
composerNames = []
output = []
for p in export.getAllPrints():
	for comp in p.composition().Composer:
		if (re.search(composerNameSubs, comp.Name, re.IGNORECASE) and not comp.Name in composerNames):
			composerNames.append(comp.Name)
			output.append(Comp(comp.Name, []))
			
for p in export.getAllPrints():
	pComposers = []# vsechny jmena autoru v print
	for pc in p.composition().Composer: 
		pComposers.append(pc.Name)
	for c in composerNames: # pro vsechny hledadne autory checkni jestli tento print slozen
		if(c in pComposers):
			for o in output:
				if o.name == c:
					o.prints.append(p)

outputDict = {}

for c in output:
	pr = []
	
	for p in c.prints:
		newPrintObject = {}
		newPrintObject["Print Number"] = p.print_id
		newPrintObject["Partiture"] = p.Partiture
		
		newCompObject = {}
		newCompObject["Title"] = p.composition().Title
		newCompObject["Incipit"] = p.composition().Incipit
		newCompObject["Key"] = p.composition().Key
		newCompObject["Genre"] = p.composition().Genre
		newCompObject["Composition Year"] = p.composition().year
		newCompObject["Voice"] = p.composition().Voices
		newCompObject["Composer"] = p.composition().Composer
		p.Edition.Composition = newCompObject
		newPrintObject["Edition"] = p.Edition
		pr.append(newPrintObject)
		
	outputDict[c.name] = pr
	
print(json.dumps(outputDict, default=serialize, indent=2, ensure_ascii=False))
#f = open("output.txt", "w", encoding='utf-8')
#f.write(json.dumps(outputDict, default=serialize, indent=2, ensure_ascii=False))
	