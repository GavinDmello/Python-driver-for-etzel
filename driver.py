import json
import asyncio
import websocket
import time
from websocket import create_connection

class Etzelclient:
	ws = websocket.WebSocket()

	def __init__(self,host):
		self.qbacks = {}
		self.ws = create_connection(host)
		self.opened = False
		self.queue = []

		# self.onopen = None


	def connect(self,host):
		pass

	def isleep(self,qname):
		content = {
			"qname": qname,
			"cmd": "ISLP"
		}
		data = json.JSONEncoder().encode(content)
		self.ws.send(data)



	
	def worker(self):

		evt = self.ws.recv()
		d = json.JSONDecoder().decode(evt)

		# if ("msg" in d):
			#the variable is not defined

		if (d["cmd"] == "awk"):
			self.fetch(d["qname"])
			#"self" is inside ws.worker scope. we need parent scope which is in the constructor :)
		elif (d["cmd"] == "nomsg"):
			self.isleep(d["qname"])
		elif (d["cmd"] == "msg"):
			self.qbacks[d["qname"]](d)
			self.fetch(d["qname"])



	def publish(self,queue, msg, options=None):
		
		content =dict({"qname" : queue,"msg" : msg,"cmd" : "PUB","delay" : 0,"expires" : 0})
		
		

		if((options != None) and ("delay" in options)):
			content["delay"] = options["delay"]
		

		if((options != None) and ("expires" in options)):
			content["expires"] = options["expires"]

		#print(content.dict());	
		data = json.JSONEncoder().encode(content)
		

		# data = json.JSONEncoder().encode(content)
		
		
		self.ws.send(data)
		

	def sendSubCmd(self,queue):
		content = {"qname" : queue,"cmd" : "SUB"}
		
		data = json.JSONEncoder().encode(content)
		self.ws.send(data)


	def acknowledge(self,queue,uid):
		content = {
			"qname" : queue,
			"cmd" : "ACK",
			"uid" : uid
		}
		
		data = json.JSONEncoder().encode(content)
		self.ws.send(data)

	def fetch(self,queue):
		#print(queue)
		content = {
			"qname" : queue,
			"cmd" : "FET"
		}

		data = json.JSONEncoder().encode(content)
		self.ws.send(data)
	
	def subscribe(self,queue, callback):
		self.sendSubCmd(queue) #we have to notify the server that we are subscribing
		self.qbacks[queue] = callback
		self.fetch(queue)

	def startwork(self):
		while True:
			self.worker()




# while True:
# 	time.sleep(10)