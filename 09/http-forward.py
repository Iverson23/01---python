import sys
import json
import socketserver
import socket
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from http.server import BaseHTTPRequestHandler, HTTPServer

def isInvalidJson(data):
	if data is None:
		return True
	if 'url' not in data:
		return True
	if 'type' in data and data['type'] == 'POST' and 'content' not in data:
		return True
	return False
		

class HandlerClass(BaseHTTPRequestHandler):
	def do_GET(self):
		headers = dict(self.headers)
		newRequest = urllib.request.Request(url = upstream, headers=headers)
		
		responseHeaders = None
		responseJson = None
		response = None
		code = None
		content = None
		newResponse = {}
		
		try:
			response = urllib.request.urlopen(newRequest, timeout = 1)
		except HTTPError as e:
			newResponse['code'] = e.code
			newResponse['headers'] = dict(e.headers.items())
		except socket.timeout:
			newResponse['code'] = 'timeout'
		else:
			newResponse['code'] = response.code
			newResponse['headers'] = dict(response.headers.items())
			content = bytes.decode(response.read(), 'utf-8')
			try:
				responseJson = json.loads(content)
			except ValueError:
				responseJson = None
		
			if responseJson is not None:
				newResponse["json"] = responseJson
			else:
				newResponse["content"] = content
	
		self.send_response(200)
		self.send_header( 'Connection', 'close')
		self.end_headers()
		self.wfile.write(bytes(json.dumps(newResponse, ensure_ascii=False), 'utf-8'))

	def do_POST(self):
		contentLen = self.headers['Content-length']
		length = 0
		if contentLen:
			length = int(contentLen)

		jsonData = None
		try:
			jsonData = json.loads(self.rfile.read(length))
		except ValueError:
			jsonData = None

		newResponse = {}
		if isInvalidJson(jsonData):
			newResponse['code'] = 'invalid json'
			self.send_response(200, 'OK')
			self.send_header('Connection', 'close')
			self.end_headers()
			self.wfile.write(bytes(json.dumps(newResponse, ensure_ascii=False), 'utf-8'))
			return			
		
		urlAddress = jsonData['url']
		
		newHeaders = dict(jsonData['headers']) if 'headers' in jsonData else {}
		newType = str(jsonData['type']) if 'type' in jsonData else 'GET'
		newData = str(jsonData['content']).encode('UTF-8') if 'content' in jsonData and newType == 'POST' else None
		newTimeout = int(jsonData['timeout']) if 'timeout' in jsonData else 1
		

		newRequest = urllib.request.Request(urlAddress, data = newData, method = newType)
		for header in newHeaders:
			newRequest.add_header(header, newHeaders[header])
		
		try:
			response = urllib.request.urlopen(newRequest, timeout = newTimeout)
		except HTTPError as e:
			newResponse['code'] = e.code
			newResponse['headers'] = dict(e.headers.items())
		except socket.timeout:
			newResponse['code'] = 'timeout'
		else:
			newResponse['code'] = response.code
			newResponse['headers'] = dict(response.headers.items())
			content = bytes.decode(response.read(), 'utf-8')
			try:
				responseJson = json.loads(content)
			except ValueError:
				responseJson = None
		
			if responseJson is not None:
				newResponse["json"] = responseJson
			else:
				newResponse["content"] = content

		self.send_response( 200, 'OK')
		self.send_header( 'Connection', 'close')
		self.end_headers()
		self.wfile.write(bytes(json.dumps(newResponse, ensure_ascii=False), 'utf-8'))

port = int(sys.argv[1])
upstream = sys.argv[2]

with HTTPServer(("", port), HandlerClass) as httpd:
	httpd.serve_forever()
