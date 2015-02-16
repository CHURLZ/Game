import pygame, math, Queue, time
from collision import *

class builder:
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
			if tile.walkable == True:
				openList.add(tile)

		while not frontier.empty():
			current = frontier.get()

			if current == goal:
				break
				
			for next in builder.getNeighbours(current, objList):
				if next not in visited and next in openList:
					visited[next] = current
					frontier.put(next)

		path = builder.reconstructPath(start, goal, visited)
		if path == None:
			return None
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
			return None
		return path

	@staticmethod
	def getNeighbours(obj, objList):

		left = builder.getAdjacent(obj, builder.LEFT, objList)
		right = builder.getAdjacent(obj, builder.RIGHT, objList)
		down = builder.getAdjacent(obj, builder.DOWN, objList)
		up = builder.getAdjacent(obj, builder.UP, objList)

		return {left, right, down, up}

	@staticmethod
	def getAdjacent(current, side, objList):
		if current == None:
			return None

		obj = None
		if side == builder.LEFT:
			obj = Collision.getObjectAt(objList, current.rect.x - 1, current.rect.y+1)
		elif side == builder.RIGHT:
			obj = Collision.getObjectAt(objList, current.rect.x + current.rect.width + 1, current.rect.y+1)	
		elif side == builder.UP:
			obj = Collision.getObjectAt(objList, current.rect.x + 1, current.rect.y - 1)	
		elif side == builder.DOWN:
			obj = Collision.getObjectAt(objList, current.rect.x + 1, current.rect.y + current.height + 1)	

		return obj