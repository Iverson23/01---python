import sqlite3

qry = open('scorelib.sql', 'r').read()
conn = None
cur = None

def createDb(dbFilename):
	global conn
	conn = sqlite3.connect( dbFilename )
	global cur
	cur = conn.cursor()
	cur.executescript(qry)

def commitDb():
	conn.commit()

def addPersonToDb(person):
	born = person.born
	died = person.died
	cur.execute('SELECT * FROM person WHERE name=?', (person.name,))
	row = cur.fetchone()
	if(row != None):
		if(row[1] != None):
			born = row[1]
		if(row[2] != None):
			died = row[2]		
		cur.execute('UPDATE person SET born=?, died=? WHERE name=?', (born, died, person.name))
		cur.execute('SELECT * FROM person WHERE name=?', (person.name,))
		row = cur.fetchone()
		return row[0]
	else:
		cur.execute('INSERT INTO person (born, died, name) VALUES (?, ?, ?)', (born, died, person.name))
	
	return cur.lastrowid

addedCompositions = []
def addCompositionToDb(c):
	scoreRowsEqual = False
	id = None
	for row in cur.execute('SELECT * FROM score'):
		if(row[1] == c.name and row[2] == c.genre and row[3] == c.key and row[4] == c.incipit and row[5] == c.year):
			scoreRowsEqual = True
			id = row[0]
	
		#check same authors
		if(scoreRowsEqual):
			if(len(c.authors) == len(addedCompositions[id - 1].authors)):
				newNames = []
				for composer in c.authors:
					newNames.append(composer.name)
				for composer in addedCompositions[id - 1].authors:
					if(composer.name in newNames):
						continue
					else:
						scoreRowsEqual = False
						break
			else:
				scoreRowsEqual = False
		
		#check same voices
		if(scoreRowsEqual):
			if(len(c.voices) == len(addedCompositions[id - 1].voices)):
				voices = []
				for voice in c.voices:
					voices.append(voice)
				counter = 0
				for voice in addedCompositions[id - 1].voices:
					if(voice != None):
						if(voice.name == voices[counter].name and voice.range == voices[counter].range):
							continue
							counter = counter + 1
						else:
							scoreRowsEqual = False
							break
					elif(voices[counter] != None):
						scoreRowsEqual = False
			else:
				scoreRowsEqual = False
		
		if(scoreRowsEqual):
			return id
		
	addedCompositions.append(c)
	cur.execute('INSERT INTO score (name, genre, key, incipit, year) VALUES (?, ?, ?, ?, ?)', (c.name, c.genre, c.key, c.incipit, c.year))
	return cur.lastrowid

def addVoiceToDb(v, compId, number):
	for row in cur.execute('SELECT * FROM voice'):
		if(row[1] == number and row[2] == compId and row[3] == v.range and row[4] == v.name):
			return
		
	cur.execute('INSERT INTO voice (number, score, range, name) VALUES (?, ?, ?, ?)',(number, compId, v.range, v.name))
	
def addEditionToDb(e, compId):
	for row in cur.execute('SELECT * FROM edition'):
		if(row[1] == compId and row[2] == e.name):
			return row[0]

	cur.execute('INSERT INTO edition (score, name, year) VALUES (?, ?, ?)',(compId, e.name, None))
	return cur.lastrowid

def fillScoreAuthor(authId, compId):
	for row in cur.execute('SELECT * FROM score_author'):
		if(row[1] == compId and row[2] == authId):
			return
	cur.execute('INSERT INTO score_author (score, composer) VALUES (?, ?)',(compId, authId))
	
def fillEditionAuthor(authId, editId):
	for row in cur.execute('SELECT * FROM edition_author'):
		if(row[1] == editId and row[2] == authId):
			return
	cur.execute('INSERT INTO edition_author (edition, editor) VALUES (?, ?)',(editId, authId))

def addPrintToDb(p, editId):
	partiture = "Y" if p.partiture else "N"
	for row in cur.execute('SELECT * FROM print'):
		if(row[0] == p.print_id and row[1] == partiture and row[2] == editId):
			return
	cur.execute('INSERT INTO print (id, partiture, edition) VALUES (?, ?, ?)',(p.print_id, partiture, editId))
