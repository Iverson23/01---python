class Print:
	def __init__( self, edition, print_id, partiture ):
		self.edition = edition
		self.print_id = print_id
		self.partiture = partiture
	def format( self ):
		return str(self)
	def composition( self ):
		return self.edition.composition
	def __str__(self):
		line = ""
		if(self.print_id):
			line = line + "Print Number: " + str(self.print_id) + "\n"
		if(self.edition):
			line = line + str(self.edition)
		if(self.partiture is not None):
			if(self.partiture):
				line = line + "Partiture: yes" + "\n"
			else:
				line = line + "Partiture: no" + "\n"
		return line

class Edition:
	def __init__( self, composition, authors, name ):
		self.composition = composition
		self.authors = authors
		self.name = name
	def __str__(self):
		line = ""
		if(self.composition):
			line = line + str(self.composition)
		if(self.name):
			line = line + "Edition: " + self.name + "\n"
		if(len(self.authors) > 0):
			line = line + "Editor: " + str(self.authors[0]) + "\n"

		return line
	
class Composition:
	def __init__( self, name, incipit, key, genre, year, voices, authors ):
		self.name = name
		self.incipit = incipit
		self.key = key
		self.genre = genre
		self.year = year
		self.voices = voices
		self.authors = authors
	def __str__(self):
		line = ""
		if(len(self.authors) > 0):
			line = line + "Composer: "
			index = 0
			for author in self.authors:
				if(index > 0):
					line = line + "; " + str(author)
				else:
					line = line + str(author)
				index = index + 1
			line = line + "\n"
		if(self.name):
			line = line + "Title: " + self.name + "\n"
		if(self.genre):
			line = line + "Genre: " + self.genre + "\n"
		if(self.key):
			line = line + "Key: " + self.key + "\n"
		if(self.year):
			line = line + "Composition Year: " + str(self.year) + "\n"
		if(self.incipit):
			line = line + "Incipit: " + self.incipit + "\n"
		counter = 1
		if(len(self.voices) > 0):
			for voice in self.voices:
				line = line + "Voice " + str(counter) + ": " + str(voice)
				counter = counter + 1

		return line
		
class Voice:
	def __init__( self, name, range ):
		self.name = name
		self.range = range
	def __str__(self):
		line = ""
		if(self.range):
			line = self.range + ", " + self.name + "\n"
		else:
			line = self.name + "\n"
		return line
	
class Person:
	def __init__( self, name, born, died ):
		self.name = name
		self.born = born
		self.died = died
	def __str__(self):
		compLine = ""
		if(self.name):
			compLine = compLine + self.name
		if(self.born != "" or self.died != ""):
			compLine = compLine + " (" + self.born + "--" + self.died + ")"
		
		return compLine