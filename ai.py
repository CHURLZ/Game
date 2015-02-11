import pygame, math
from collision import *

class AI:
	LEFT = "left"
	RIGHT = "right"
	UP = "up"
	DOWN = "down"

	@staticmethod
	def calculatePath(objA, x, y, objList):
		openList = []
		closedList = set()
		path = []

		current = objA.currentTile
		r = AI.getHeuristic(Collision.getTileAt(objList, x,y), AI.getAdjacent(current, AI.LEFT, objList))
		#AI.getAdjacent(current, AI.RIGHT)
		#AI.getAdjacent(current, AI.UP)
		#AI.getAdjacent(current, AI.DOWN)

		return r #restructurePath()
	
	@staticmethod
	def restructurePath():
		return path
	
	@staticmethod
	def getHeuristic(goal, tile):
		x = tile.rect.x - goal.rect.x
		y = tile.rect.y - goal.rect.y
		return math.sqrt((x * x) + (y * y))

	@staticmethod
	def getAdjacent(current, side, objList):
		
		if side == AI.LEFT:
			return Collision.getTileAt(objList, current.rect.x - 2, current.rect.y)		
		elif side == AI.RIGHT:
			return Collision.getTileAt(objList, current.rect.x + current.rect.width + 2, current.rect.y)	
		elif side == AI.UP:
			return Collision.getTileAt(objList, current.rect.x, current.rect.y - 2)	
		elif side == AI.DOWN:
			return Collision.getTileAt(objList, current.rect.x, current.rect.y + current.height + 2)	
		else:
			return None