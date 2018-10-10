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
	cur.execute('SELECT * FROM score WHERE name=? AND genre=? AND key=? AND incipit=? AND year=?',(c.name, c.genre, c.key, c.incipit, c.year))
	row = cur.fetchone()
	if(row != None):
		return 0
		
	cur.execute('INSERT INTO score (name, genre, key, incipit, year) VALUES (?, ?, ?, ?, ?)', (c.name, c.genre, c.key, c.incipit, c.year))
	return cur.lastrowid

def addVoiceToDb(v, compId, number):
	cur.execute('SELECT * FROM voice WHERE number=? AND score=? AND range=? AND name=?',(number, compId, v.range, v.name))
	row = cur.fetchone()
	if(row != None):
		return
		
	cur.execute('INSERT INTO voice (number, score, range, name) VALUES (?, ?, ?, ?)',(number, compId, v.range, v.name))
	
def addEditionToDb(e, compId):
	cur.execute('SELECT * FROM edition WHERE score=? AND name=?',(compId, e.name))
	row = cur.fetchone()
	if(row != None):
		return 0
	else:
		cur.execute('INSERT INTO edition (score, name, year) VALUES (?, ?, ?)',(compId, e.name, None))
	return cur.lastrowid

def fillScoreAuthor(authId, compId):
	cur.execute('INSERT INTO score_author (score, composer) VALUES (?, ?)',(compId, authId))
	
def fillEditionAuthor(authId, editId):
	cur.execute('INSERT INTO edition_author (edition, editor) VALUES (?, ?)',(editId, authId))

def addPrintToDb(p, editId):
	partiture = "Y" if p.partiture else "N"
	cur.execute('INSERT INTO print (partiture, edition) VALUES (?, ?)',(partiture, editId))
