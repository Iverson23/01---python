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

class Handler(http.server.CGIHTTPRequestHandler):
	dirPath = None
	args = None
	
	def do_POST(self):
		self.handleRequest()

	def do_GET(self):
		self.handleRequest()
		
	def handleRequest(self):
		self.path, _, self.args = self.path.partition("?")
		fullPath = os.path.normpath(self.dirPath + self.path)

		print(fullPath)
		if os.path.isfile(fullPath):
			if fullPath.endswith(".cgi"):
				relPath = os.path.relpath(fullPath)
				file = os.path.basename(relPath)
				if(self.args):
					file = file + '?' + self.args
				self.cgi_info = os.path.dirname(relPath), file 
				self.run_cgi()
			else:
				self.send_response(http.client.OK)
				self.send_header("Content-type", "text/plain")
				self.end_headers()
				with open(fullPath, 'rb') as f:
					while True:
						fileData = f.read(1024)
						if not fileData:
							break
						self.wfile.write(fileData)
		else:
			self.send_error(404, explain = "Wrong path")
			
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	pass

port = int(sys.argv[1])
dir = sys.argv[2]
handler = Handler
handler.dirPath = os.path.abspath(dir)
s = ThreadedHTTPServer(("localhost", port), handler)
s.serve_forever()