#!/usr/bin/python

try:
	from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
except:
	from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
try:
	from urlparse import urlparse
	from urlparse import urlparse, parse_qs
except:
	from urllib.parse import urlparse, parse_qs

#Configurar puertos led
import os
#import RPi.GPIO as GPIO 
#import time
port = int(os.environ.get("PORT", 5000))	
PORT_NUMBER = port

#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)

#led = 11

#GPIO.setup(led,GPIO.OUT)

def ledOn():
    print('led on')
    #Encender led

def ledOff():
    print('led off')

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):

		path=self.path
		print(self.path.split('/')[-1])
		nombre=self.path.split('/')[-1]
		datos=''
		if(self.path=='ledOn'):
			ledOn();
			#GPIO.output(led,1)
			datos='ok'
		if(self.path=='ledOff'):
			ledOff();
			#GPIO.output(led,0)
			datos='ok'
		if self.path=="/":  #127.0.0.1:5000/
			nombre="index.html" #127.0.0.1:5000/index.html
		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"): #si el string termina con html eso significa endswith
				mimetype='text/html'
				f=open(nombre)#Si es verdadero va a leer el archivo, en modo read, por DEFECTO
				datos=f.read()#Lee todo el texto
				f.close()
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if self.path.endswith(".dat"):
				mimetype='text/html'
				datos='ok'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				#f = open(curdir + sep + self.path,'r') 
				self.send_response(200)#codigo 200 cuando la respuesta es positiva
				self.send_header('Content-type',mimetype)
				self.end_headers()
				
				try:
					self.wfile.write(datos)
				except:
					self.wfile.write(bytes(datos, 'UTF-8'))
				
			return


		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('0.0.0.0', PORT_NUMBER), myHandler)
	print ('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()
	