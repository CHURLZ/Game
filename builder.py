import pygame, math, Queue, time
from zone import *
from collision import *
from classes import Terrain
import images

class builder:
	LEFT = "left"
	RIGHT = "right"
	UP = "up"
	DOWN = "down"


	# States
	INACTIVE = 0
	WALL = 1
	ZONE = 2

	state = 0

	# BUILD
	initBuild = False
	buildFrom = None
	buildTo = None
	builtSinceLastLoop = True
	initRemove = False
	builtSinceLastLoop = True
	# BUILD

	@staticmethod
	def onMouseDown(x, y, event):
		if builder.state == builder.INACTIVE:
			return
		elif builder.state == builder.WALL:
			if event.button == 1:
				builder.initBuild = True
				builder.buildFrom = Collision.getObjectAt(Terrain.List, x, y)
			if event.button == 3:
				builder.initRemove = True
				builder.buildFrom = Collision.getObjectAt(Terrain.List, x, y)

		elif builder.state == builder.ZONE:
			Terrain.zones.append(Zone((x, y)))


	@staticmethod
	def onMouseRelease(x, y, event):
		if builder.state == builder.INACTIVE:
			return
		elif builder.state == builder.WALL:
			if event.button == 1:
				builder.buildWall(x, y)
					
			elif event.button == 3:
			  	builder.destroyWall(x, y)
		elif builder.state == builder.ZONE:
			for zone in Terrain.zones:
					if zone.inLimbo:
						zone.onMouseRelease(Terrain.List, (x, y))



	@staticmethod
	def buildWall(x, y):
		if not builder.initBuild:
			return

		builder.buildTo = Collision.getObjectAt(Terrain.List, x, y)
		builder.buildPlan = builder.calculatePath(builder.buildFrom, builder.buildTo, Terrain.List)
		if builder.buildTo == None:
			builder.buildPlan = None
		if builder.buildPlan != None:
			for tile in builder.buildPlan:
				if tile.buildable:
					tile.image = images.brickHori
					tile.default_image = tile.image
					tile.walkable = False
		builder.initBuild = False
		builder.builtSinceLastLoop = True


	@staticmethod
	def destroyWall(x, y):
		try:
			if builder.initRemove:
				builder.buildTo = Collision.getObjectAt(Terrain.List, x, y)
				builder.buildPlan = builder.calculatePath(builder.buildFrom, builder.buildTo, Terrain.List)
				if builder.buildTo == None:
					builder.buildPlan = None
				builder.initRemove = False
				if builder.buildPlan != None:
					for tile in builder.buildPlan:
						tile.image = images.grayScaleFloor
						tile.default_image = tile.image
						tile.walkable = True
		except AttributeError:
			print "~ error removing Wall"
		builder.initRemove = False
		builder.builtSinceLastLoop = True

	@staticmethod
	def drawBuildPath(x, y):
		if builder.initBuild and pygame.mouse.get_pressed():
			for tile in Terrain.List:
				if tile.image == images.buildPath:
					tile.image = tile.default_image
			builder.buildPlan = None
			obj = Collision.getObjectAt(Terrain.List, x, y)
			if obj != builder.buildFrom:
				builder.buildPlan = builder.calculatePath(builder.buildFrom, obj, Terrain.List)
			if builder.buildPlan != None:
				for tile in builder.buildPlan:
					tile.image = images.buildPath

	@staticmethod
	def drawRemovePath(x, y):
		if builder.initRemove and pygame.mouse.get_pressed():
			for tile in Terrain.List:
				if tile.image == images.removePath:
					tile.image = tile.default_image
			
			builder.buildPlan = None
			obj = Collision.getObjectAt(Terrain.List, x, y)
			if obj != builder.buildFrom:
				builder.buildPlan = builder.calculatePath(builder.buildFrom, obj, Terrain.List)
			if builder.buildPlan != None:
				for tile in builder.buildPlan:
					tile.image = images.removePath


	@staticmethod
	def calculatePath(start, goal, objList):
		startTime = time.clock()

		openList = set()

		frontier = Queue.Queue()
		frontier.put(start)
		visited = {}
		visited[start] = None

		for tile in objList:
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
	def floodRoom(start, objList):
		startTime = time.clock()

		openList = set()

		frontier = Queue.Queue()
		frontier.put(start)
		visited = {}
		visited[start] = None

		for tile in objList:
			if tile.walkable:
				openList.add(tile)

		while not frontier.empty():
			current = frontier.get()
				
			for next in builder.getNeighbours(current, objList):
				if next not in visited and next in openList:
					visited[next] = current
					frontier.put(next)

		return visited
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

		@staticmethod
		def getRoom(x, y):
			s = Collision.getObjectAt(Terrain.List, 50, 100)
			room = builder.floodRoom(s, Terrain.List)
			return room
			#for r in room:
			#	r.image = images.grayScaleFloor