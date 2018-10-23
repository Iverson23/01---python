import scorelib
import sqlite3

def serialize(obj):
    return obj.__dict__

def getAllPrints():
	dbFilename = "scorelib.dat"

	conn = sqlite3.connect( dbFilename )
	cur = conn.cursor()
	
	persons = []
	compositions = []
	editions = []
	prints = []
	
	
	for row in cur.execute('SELECT * FROM score'):
		compositions.append(scorelib.Composition(row[1], row[4], row[3], row[2], row[5], [], []))
		
	for row in cur.execute('SELECT * FROM person'):
		persons.append(scorelib.Person(row[3], row[1], row[2]))
	
	for row in cur.execute('SELECT * FROM voice'):
		voice = scorelib.Voice(row[4],row[3])
		if(len(compositions[row[2] - 1].Voices) < row[1] - 1):
			compositions[row[2] - 1].Voices.append(None)
		if(len(compositions[row[2] - 1].Voices) < row[1] - 1):
			compositions[row[2] - 1].Voices.append(None)
		if(len(compositions[row[2] - 1].Voices) < row[1] - 1):
			compositions[row[2] - 1].Voices.append(None)
		if(len(compositions[row[2] - 1].Voices) < row[1] - 1):
			compositions[row[2] - 1].Voices.append(None)
		compositions[row[2] - 1].Voices.append(voice)
		
	for row in cur.execute('SELECT * FROM edition'):
		edition = scorelib.Edition(compositions[row[1] - 1], [], row[2])
		editions.append(edition)
		
	for row in cur.execute('SELECT * FROM score_author'):
		compositions[row[1] - 1].Composer.append(persons[row[2] - 1])
	
	for row in cur.execute('SELECT * FROM edition_author'):
		editions[row[1] - 1].Editor.append(persons[row[2] - 1])	
		
	for row in cur.execute('SELECT * FROM print'):
		part = True if row[1] == "Y" else False
		prints.append(scorelib.Print(editions[row[2] - 1], row[0], part)) 
		
	return prints
	