from base import *
from move import *
def findNearestEnemy():
	"""Gets all the world objects, finds the enemies, then
	figures out which one is closest to the player's current
	position. Dumb calculation, does not take map into account.
	"""
	
	playerData = getAction('player')
	distance = 500
	worldObjectData = getAction('world/objects?' + str(distance))
	
	enemies = []
	
	for worldObject in worldObjectData:
		flags = worldObject['flags']
		if u'MF_SPECIAL' in flags:
			if flags[u'MF_SPECIAL']:
 				enemies.append(worldObject)
					

	logging.debug('Found {} enemies'.format(len(enemies)))
	
	nearestEnemy = None
	nearestEnemyDistance = 999999.0
	
	for enemy in enemies:
			
		distance = enemy['distance']
		tid = str(enemy['id'])
		los = 'world/los/0/' + tid
		if getAction(los)['los']:
			if distance < nearestEnemyDistance:
				nearestEnemy = enemy
				nearestEnemyDistance = enemy["distance"]
	moveToPoint(nearestEnemy["position"]["x"], nearestEnemy["position"]["y"], nearestEnemyDistance)
	return False
