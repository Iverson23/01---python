import sys
import export
import json

printNumber = sys.argv[1]

def serialize(obj):
    return obj.__dict__
	
for p in export.getAllPrints():
	if(p.print_id == int(printNumber)):
		print(json.dumps(p.composition().Composer, default=serialize, indent=2, ensure_ascii=False))