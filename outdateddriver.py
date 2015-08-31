import json
import asyncio
import websockets
import time


class etzelclien:

	def __init__(self,host):
		self.qbacks = {}
		self.ws =  websockets.connect(host)
		self.opened = False
		self.queue = []

		# self.onopen = None


	def connect(self,host):
		pass

	def isleep(qname):
		content = {
			"qname": qname,
			"cmd": "ISLP"
		}
		data = json.JSONEncoder().encode(content)
		yield from self.ws.send(data)



	
	def worker(self):
		print("hello")

		evt =  yield from self.ws.recv()
		d = json.JSONDecoder(evt)

		# if ("msg" in d):
			#the variable is not defined

		if (d["cmd"] == "awk"):
			self.fetch(d["qname"])
			#"self" is inside ws.onmessage scope. we need parent scope which is in the constructor :)
		elif (d["cmd"] == "nomsg"):
			self.isleep(d["qname"])
		elif (d["cmd"] == "msg"):
			self.qbacks[d["qname"]](d)
			self.fetch(d["qname"])


	@asyncio.coroutine
	def publish(queue, msg, options=None):

		content = {
			"qname" : queue,
			"msg" : msg,
			"cmd" : "PUB",
			"delay" : 0,
			"expires" : 0
		}

		if((options != None) and ("delay" in options)):
			content["delay"] = options["delay"]
		

		if((options != None) and ("expires" in options)):
			content["expires"] = options["expires"]
		

		data = json.JSONEncoder().encode(content)
		print("hello from before")
		yield from self.ws.send(data)
		print("hello again")

	def sendSubCmd(self,queue):
		content = {"qname" : queue,"cmd" : "SUB"}
		
		data = json.JSONEncoder().encode(content)
		yield from self.ws.send(data)


	def acknowledge(queue,uid):
		content = {
			"qname" : queue,
			"cmd" : "ACK",
			"uid" : uid
		}
		
		data = json.JSONEncoder().encode(content)
		yield from self.ws.send(data)

	def fetch(self,queue):
		content = {
			"qname" : queue,
			"cmd" : "FET"
		}

		data = json.JSONEncoder().encode(content)
		yield from self.ws.send(data)
	
	def subscribe(self,queue, callback):
		self.sendSubCmd(queue) #we have to notify the server that we are subscribing
		self.qbacks[queue] = callback
		self.fetch(queue)
		print("done")

	def startwork(self):
		while True:
			self.worker()



e=etzelclient("ws://127.0.0.1:8080/connect");
e.connect("ws://127.0.0.1:8080/connect");
e.publish("test1","hi");
def hello(a):
	print(a["msg"])
e.subscribe("test1",hello)
e.worker()
# while True:
# 	time.sleep(10)