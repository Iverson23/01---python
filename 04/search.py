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
	for comp in p.composition().authors:
		if (re.search(composerNameSubs, comp.name, re.IGNORECASE) and not comp.name in composerNames):
			composerNames.append(comp.name)
			output.append(Comp(comp.name, []))
			
for p in export.getAllPrints():
	pComposers = []# vsechny jmena autoru v print
	for pc in p.composition().authors: 
		pComposers.append(pc.name)
	for c in composerNames: # pro vsechny hledadne autory checkni jestli tento print slozen
		if(c in pComposers):
			for o in output:
				if o.name == c:
					o.prints.append(p)

#f = open("output.txt", "w", encoding='utf-8')
for c in output:
	print(json.dumps(c, default=serialize, indent=2))
	#f.write(json.dumps(c, default=serialize, indent=2))
	