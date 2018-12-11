import sys
import http.server
import http.client
import os
import json
import pprint
import socketserver
import urllib.error
import urllib.parse
import urllib.request

class Game:
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
		self.next = 1
		self.winner = None

	def status(self):
		if self.winner != None:
			return {"winner": self.winner}
		return {"board": self.board, "next": self.next}
		
	def play(self, player, x, y):
		if self.winner != None:
			return {"status": "bad", "message": "Game is done"}
		if player != self.next:
			return {"status": "bad", "message": "Not your turn"}
		if x > 2 or x < 0 or y > 2 or y < 0:
			return {"status": "bad", "message": "Out of board"}
		if self.board[x][y] != 0:
			return {"status": "bad", "message": "Field is already filled"}
		
		self.board[x][y] = player
		if player == 1:
			self.next = 2
		else:
			self.next = 1

		
		win = self.checkBoard()
		if win >= 0:
			self.winner = win
		
		return {"status": "ok"}

	def checkBoard(self):
		# rows
		for x in range(0,3):
			row = set([self.board[x][0],self.board[x][1],self.board[x][2]])
			if len(row) == 1 and self.board[x][0] != 0:
				return self.board[x][0]
	
		# columns
		for x in range(0,3):
			column = set([self.board[0][x],self.board[1][x],self.board[2][x]])
			if len(column) == 1 and self.board[0][x] != 0:
				return self.board[0][x]
	
		# diagonals
		if self.board[0][0] == self.board[1][1] == self.board[2][2] or self.board[0][2] == self.board[1][1] == self.board[2][0]:
			if(self.board[1][1] != 0):
				return self.board[1][1]
	
		if 0 not in self.board[0] and 0 not in self.board[1] and 0 not in self.board[2]:
			return 0
		
		return -1
		
class Handler(http.server.BaseHTTPRequestHandler):
	currentGames = []
	
	def do_GET(self):
		url = urllib.parse.urlparse(self.path)
		params = urllib.parse.parse_qs(url.query)
		
		if url.path == "/start":
			
			if len(self.currentGames) < 1:
				id = 0
			else:
				id = self.currentGames[len(self.currentGames) - 1].id + 1
			
			name = params["name"][0] if "name" in params else ""
			newGame = Game(id, name)
			self.currentGames.append(newGame)

			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			self.wfile.write(bytes(json.dumps({"id": id}, indent = 2, ensure_ascii = False), "utf-8"))
			return
			
		elif url.path == "/play":
			try:
				id = int(params["game"][0])
				x = int(params["x"][0])
				y = int(params["y"][0])
				player = int(params["player"][0])
				currentGame = None
				for game in self.currentGames:
					if game.id == id:
						currentGame = game
						break

				status = currentGame.play(player, x, y)
				self.send_response(200)
				self.send_header('Content-Type', 'application/json')
				self.end_headers()
				self.wfile.write(bytes(json.dumps(status, indent = 2, ensure_ascii = False), "utf-8"))
				
			except:
				self.send_error(402, "wrong request from play")
				
		elif url.path == "/status":
			try:
				id = int(params["game"][0])
				currentGame = None
				for game in self.currentGames:
					if game.id == id:
						currentGame = game
						break
				
				status = currentGame.status()
				self.send_response(200)
				self.send_header('Content-Type', 'application/json')
				self.end_headers()
				self.wfile.write(bytes(json.dumps(status, indent = 2, ensure_ascii = False), "utf-8"))
				
			except:
				self.send_error(402, "Wrong request from status")
				
		else:
			self.send_error(402, "wrong request")

			
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	pass

port = int(sys.argv[1])
s = ThreadedHTTPServer(("localhost", port), Handler)
s.serve_forever()