e=etzelclient("ws://127.0.0.1:8080/connect");
e.connect("ws://127.0.0.1:8080/connect");

for x in range(1,10):
	e.publish("test1", "hi py %d" %x)
	
def hello(a):
	
	e.acknowledge(a["qname"],a["uid"])
e.subscribe("test1",hello)
e.startwork()