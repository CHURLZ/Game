import pygame, math, Queue, time
from collision import *

class AI:
	NONE = "none"
	LEFT = "left"
	RIGHT = "right"
	UP = "up"
	DOWN = "down"

	@staticmethod
	def calculatePath(start, goal, objList):
		startTime = time.clock()

		openList = set()

		frontier = Queue.Queue()
		frontier.put(start)
		visited = {}
		visited[start] = None

		for tile in objList:
			tile.image = pygame.image.load(tile.default_image)
			if tile.walkable == True:
				openList.add(tile)

		while not frontier.empty():
			current = frontier.get()

			if current == goal:
				break
				
			for next in AI.getNeighbours(current, objList):
				if next not in visited and next in openList:
					visited[next] = current
					frontier.put(next)
					next.image = pygame.image.load("img/BlueFloorGreenTint.png")

		path = AI.reconstructPath(start, goal, visited)
		if path == None:
			return None
		for p in path:
			p.image = pygame.image.load("img/BlueFloorPathTint.png")
		stopTime = time.clock()
		return path

	@staticmethod
	def reconstructPath(start, goal, visited):
		current = goal
		path = [current]
		try:
			path = [current]
			while current != start:
				current = visited[current]
				path.append(current)
		except KeyError:
			print "no path!"
			return None
		return path

	@staticmethod
	def getNeighbours(obj, objList):

		left = AI.getAdjacent(obj, AI.LEFT, objList)
		right = AI.getAdjacent(obj, AI.RIGHT, objList)
		down = AI.getAdjacent(obj, AI.DOWN, objList)
		up = AI.getAdjacent(obj, AI.UP, objList)

		return {left, right, down, up}
	
	@staticmethod
	def getHeuristic(current, goal):
		x = current.rect.x - goal.rect.x
		y = current.rect.y - goal.rect.y
		return (abs)(x+y)

	@staticmethod
	def getAdjacent(current, side, objList):
		if current == None:
			return None

		obj = None
		if side == AI.LEFT:
			obj = Collision.getObjectAt(objList, current.rect.x - 1, current.rect.y+1)
		elif side == AI.RIGHT:
			obj = Collision.getObjectAt(objList, current.rect.x + current.rect.width + 1, current.rect.y+1)	
		elif side == AI.UP:
			obj = Collision.getObjectAt(objList, current.rect.x + 1, current.rect.y - 1)	
		elif side == AI.DOWN:
			obj = Collision.getObjectAt(objList, current.rect.x + 1, current.rect.y + current.height + 1)	

		return obj
