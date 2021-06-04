import json

def getKey(name):
	with open("Secret.json") as f:
		keys=json.load(f)
	return keys[name]
