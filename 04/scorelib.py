class Print:
	def __init__( self, edition, print_id, partiture ):
		self.Edition = edition
		self.print_id = print_id
		self.Partiture = partiture
	def format( self ):
		print(str(self))
	def composition( self ):
		return self.Edition.Composition
	def __str__(self):
		line = ""
		if(self.print_id != None):
			line = line + "Print Number: " + str(self.print_id) + "\n"
		if(self.edition != None):
			line = line + str(self.edition)
		if(self.partiture != None):
			if(self.partiture):
				line = line + "Partiture: yes" + "\n"
			else:
				line = line + "Partiture: no" + "\n"
		return line

class Edition:
	def __init__( self, composition, authors, name ):
		self.Edition = name
		self.Composition = composition
		self.Editor = authors
		
	def __str__(self):
		line = ""
		if(self.composition != None):
			line = line + str(self.composition)
		if(self.name != None):
			line = line + "Edition: " + self.name + "\n"
		if(len(self.authors) > 0):
			line = line + "Editor: " + str(self.authors[0]) + "\n"

		return line
	
class Composition:
	def __init__( self, name, incipit, key, genre, year, voices, authors ):
		self.Title = name
		self.Incipit = incipit
		self.Key = key
		self.Genre = genre
		self.year = year
		self.Voices = voices
		self.Composer = authors
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
		if(self.name != None):
			line = line + "Title: " + self.name + "\n"
		if(self.genre != None):
			line = line + "Genre: " + self.genre + "\n"
		if(self.key != None):
			line = line + "Key: " + self.key + "\n"
		if(self.year != None):
			line = line + "Composition Year: " + str(self.year) + "\n"
		if(self.incipit != None):
			line = line + "Incipit: " + self.incipit + "\n"
		counter = 1
		if(len(self.voices) > 0):
			for voice in self.voices:
				if(voice != None):
					line = line + "Voice " + str(counter) + ": " + str(voice)					
				counter = counter + 1

		return line
		
class Voice:
	def __init__( self, name, range ):
		self.Name = name
		self.Range = range
	def __str__(self):
		line = ""
		if(self.range != None):
			line = self.range + ", " + self.name + "\n"
		elif(self.name != None):
			line = self.name + "\n"
		return line
	
class Person:
	def __init__( self, name, born, died ):
		self.Name = name
		self.Born = born
		self.Died = died
	def __str__(self):
		compLine = ""
		b = ""
		d = ""
		
		if(self.born != None):
			b = str(self.born)
		if(self.died != None):
			d = str(self.died)
			
		if(self.name != None):
			compLine = compLine + self.name
		if(b != "" or d != ""):
			compLine = compLine + " (" + b + "--" + d + ")"
		
		return compLine