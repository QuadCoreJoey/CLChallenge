#! /usr/local/bin/python3

'''
Author: Joseph Caso
Date: 05/29/2019
Summary: Python script to server an HTTP server on 127.0.0.1 TCP/8000. 
The server accepts POST requests and wraps up everything into a
JSON Web Token according to the challenge specificiations and RFC 7519.
'''

from http.server import HTTPServer, BaseHTTPRequestHandler
import jwt, datetime, time, secrets, json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_POST(self):
		#self._set_headers()
		content_length = int(self.headers['Content-Length']) #get size of data
		data = self.rfile.read(content_length) #get POST data

		self.send_response(200)
		print(data) #TODO extract username from headers

		# JSON Web Token Secret Sauce
		payload = {
		'jti': secrets.token_hex(), #cryptographic nonce
		'iat': time.time(), #timestamp in UNIX
		'user':'username_here', #username, TODO
		'date': datetime.datetime.now().strftime('%Y-%m-%d') #todays date
		}

		#encode payload with JWT secret and HS512 alg
		signature = jwt.encode(payload, 'a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf', algorithm='HS512')

		self.send_header("x-my-jwt", signature) #return JSON Web Token
		self.end_headers()


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()