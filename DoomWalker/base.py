#!/usr/bin/python

import requests
import logging
import random
import time
import json
import math

RESTFUL_HOST="localhost"
RESTFUL_PORT=6001

def sendAction(objectName, payload):
	global RESTFUL_HOST
	global RESTFUL_PORT
	
	url = 'http://{}:{}/api/{}/actions'.format(RESTFUL_HOST, RESTFUL_PORT, objectName)
	logging.debug('Calling {} with payload {}'.format(url, payload))
	try:
		requests.post(url, json=payload)
		return True
	except:
		logging.error('POST API call failed')
		return False
		
def getAction(objectName):
	global RESTFUL_HOST
	global RESTFUL_PORT
	
	url = 'http://{}:{}/api/{}'.format(RESTFUL_HOST, RESTFUL_PORT, objectName)
	logging.debug('Calling {}'.format(url))
	try:
		req = requests.get(url)
		data = json.loads(req.text)
		return data
	except:
		logging.error('GET API call failed')
		return None

def spinPlayer(amount):
	if amount < 0:
		actionType = "turn-right"
		amount = abs(amount)
	else:
		actionType = "turn-left"
	
	sendAction('player', {'type': actionType, 'amount': amount})

def movePlayer(amount):
	if amount < 0:
		actionType = "backward"
		amount = abs(amount)
	else:
		actionType = "forward"
	
	sendAction('player', {'type': actionType, 'amount': amount})

def shoot():
	sendAction('player', {'type': 'shoot'})


def distanceBetweenPoints(x1, y1, x2, y2):  
	dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
	return dist

def simpleTrig(a, b):
	logging.debug('simpleTrig({}, {})'.format(a, b))
	return math.degrees(
		math.acos(float(a) / float(b))
	)

def turnToFacePoint(destX, destY):
	currentData = getAction('player')
	
	distance = distanceBetweenPoints(
		currentData["position"]["x"],
		currentData["position"]["y"],
		destX,
		destY
	)
	
	angle = int(simpleTrig(
		abs(currentData["position"]["x"] - destX),
		abs(distance)		
	))

	logging.debug('Uncorrected angle is {}'.format(angle))
	
	if currentData["position"]["x"] < destX and currentData["position"]["y"] < destY:
		angle = 90 - angle
	elif currentData["position"]["x"] < destX and currentData["position"]["y"] >= destY:
		angle += 90
	elif currentData["position"]["x"] >= destX and currentData["position"]["y"] >= destY:
		angle = 270 - angle
	elif currentData["position"]["x"] >= destX and currentData["position"]["y"] < destY:
		angle += 270
	
	logging.debug('Corrected angle is {}'.format(angle))
	
	reorientPlayer(angle)

def reorientPlayer(angle, attempts=10, pause=1, accuracy=10):
	"""Try and make the player point in a specific direction
	"""
	
	for i in range(attempts):
		currentData = getAction('player')
		
		diff = currentData["angle"] - angle
		
		"""If we would spin >180 degrees, go the other way"""
		if diff > 180:
			diff -= 360
		
		logging.debug('We are facing {} and want to be facing {}, difference of {}'.format(currentData["angle"], angle, diff))
		
		if abs(diff) < accuracy:
			logging.debug('Close enough - angle is {} vs {}'.format(currentData["angle"], angle))
			return True
		
		"""Game units are roughly 105 in a circle"""
		spinAmount = int(float(diff) * float(105.0 / 360.0))
			
		spinPlayer(spinAmount)
		
		time.sleep(pause)

	logging.debug('Gave up - angle is {} vs {}'.format(currentData["angle"], angle))
	
	return False
