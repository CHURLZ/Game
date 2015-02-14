import pygame, math
from collision import *

class AI:
	NONE = "none"
	LEFT = "left"
	RIGHT = "right"
	UP = "up"
	DOWN = "down"

	@staticmethod
	def calculatePath(objA, goal, objList):
		openList = set()
		#closedList = set()
		visited = set()
		path = set()
		current = objA


		for tile in objList:
			openList.add(tile)

		path.add(current)

		while openList:

			if current == goal:
				break

			lowest = None
			lowestTile = None
			for next in AI.getNeighbours(current, openList, goal):
				if next == None:
					openList.discard(next)

				if(next not in visited and next != None):
					heuristic = AI.getHeuristic(goal, next)
					if heuristic < lowest or lowest == None:
						lowest = heuristic
						lowestTile = next
					visited.add(next)

					
					if next.walkable == False:
						next.image = pygame.image.load("img/Red.png")
					else:
						next.image = pygame.image.load("img/Green.png")
			current = lowestTile
			path.add(current)
		
		for p in path:
			p.image = pygame.image.load("img/Path.png")	

		print "JARRO!"
		return "lol" #restructurePath()

	@staticmethod
	def getNeighbours(obj, objList, goal):

		left = AI.getAdjacent(obj, AI.LEFT, objList)
		right = AI.getAdjacent(obj, AI.RIGHT, objList)
		down = AI.getAdjacent(obj, AI.DOWN, objList)
		up = AI.getAdjacent(obj, AI.UP, objList)

		return {left, right, down, up}

	@staticmethod
	def restructurePath():
		return path
	
	@staticmethod
	def getHeuristic(goal, tile):
		x = tile.rect.x - goal.rect.x
		y = tile.rect.y - goal.rect.y
		return (abs)(x+y)

	@staticmethod
	def getAdjacent(current, side, objList):
		if current == None:
			return None
		obj = None
		if side == AI.LEFT:
			obj = Collision.getTileAt(objList, current.rect.x - 1, current.rect.y)
		elif side == AI.RIGHT:
			obj = Collision.getTileAt(objList, current.rect.x + current.rect.width + 1, current.rect.y)	
		elif side == AI.UP:
			obj = Collision.getTileAt(objList, current.rect.x, current.rect.y - 2)	
		elif side == AI.DOWN:
			obj = Collision.getTileAt(objList, current.rect.x, current.rect.y + current.height + 2)	

		return obj