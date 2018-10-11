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
	else:
		cur.execute('INSERT INTO person (born, died, name) VALUES (?, ?, ?)', (born, died, person.name))
	
	return cur.lastrowid

def addCompositionToDb(c):
	for row in cur.execute('SELECT * FROM score'):
		if(row[1] == c.name and row[2] == c.genre and row[3] == c.key and row[4] == c.incipit and row[5] == c.year):
			return row[0]
		
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
		if(row[1] == partiture and row[2] == editId):
			return
	cur.execute('INSERT INTO print (partiture, edition) VALUES (?, ?)',(partiture, editId))
