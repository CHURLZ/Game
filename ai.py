import pygame, math
from collision import *

class AI:
	LEFT = "left"
	RIGHT = "right"
	UP = "up"
	DOWN = "down"
	openList = []
	closedList = set()
	path = []

	@staticmethod
	def calculatePath(objA, goal, objList):
		openList = []
		closedList = set()
		path = []

		return r #restructurePath()

	@staticmethod
	def checkNeighbours(obj, objList, goal):
		if obj == None or obj.walkable == False:
			AI.closedList.add(obj)
			return 

		obj.image = pygame.image.load(green.png)
		left = AI.getAdjacent(obj, AI.LEFT, objList)
		right = AI.getAdjacent(obj, AI.RIGHT, objList)
		up = AI.getAdjacent(obj, AI.UP, objList)
		down = AI.getAdjacent(obj, AI.DOWN, objList)


		checkNeighbours(left, objList, goal)
		checkNeighbours(right, objList, goal)
		checkNeighbours(up, objList, goal)
		checkNeighbours(down, objList, goal)

		#hLeft = AI.getHeuristic(goal, left)
		#hRight = AI.getHeuristic(goal, right)
		#hUp = AI.getHeuristic(goal, up)
		#hDown = AI.getHeuristic(goal, down)

	@staticmethod
	def restructurePath():
		return path
	
	@staticmethod
	def getHeuristic(goal, tile):
		x = tile.rect.x - goal.rect.x
		y = tile.rect.y - goal.rect.y
		return (int)(math.sqrt((x * x) + (y * y)))

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