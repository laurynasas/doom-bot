from base import *
import time
import math
def moveToPoint(destX, destY, distance):
	"""Try to move in a straight line from where we are to a destination
	point in a finite amount of steps. Z axis is disregarded
	"""
	currentData = getAction('player')
	angle = currentData[u'angle'] 
	angle = angle / 360.0 * 106
	xdif = destX - currentData["position"]["x"]
	ydif = destY - currentData["position"]["y"]
	tan = math.atan2(ydif, xdif)
	tan = tan / 6.28 * 106
	spinPlayer(tan - angle)
	
	return False


